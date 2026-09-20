"""Source-level QA only: never fits models or declares the scientific gate passed."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path


def audit(root: Path) -> dict:
    tables = []
    values = {}
    for meta_path in sorted((root / 'raw/nso/metadata').glob('*.json')):
        meta = json.loads(meta_path.read_text())
        code = meta.get('table_code', meta_path.stem)
        source = root / 'raw/nso/source' / (code + '.csv')
        normalized = list((root / 'raw/nso/normalized').glob(code + '_*.csv'))
        row = {'table': code, 'source_url': meta.get('source_url'),
               'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None,
               'normalized': bool(normalized)}
        if row['source_sha256'] != meta.get('raw_export_sha256'):
            raise ValueError(f'{code}: source hash mismatch')
        if normalized:
            p = normalized[0]
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            if digest != meta.get('normalized_sha256'):
                raise ValueError(f'{code}: normalized hash mismatch')
            with p.open() as f:
                records = list(csv.DictReader(f))
            series = {(r['province'], int(r['year'])): None if not r['value'] else float(r['value']) for r in records}
            if len(series) != len(records):
                raise ValueError(f'{code}: duplicate keys')
            vals = [v for v in series.values() if v is not None]
            values[code] = series
            row.update(rows=len(records), provinces=len({k[0] for k in series}),
                       years=sorted({k[1] for k in series}), missing=len(records)-len(vals),
                       negative=sum(v < 0 for v in vals), minimum=min(vals), maximum=max(vals),
                       normalized_sha256=digest, declared_unit=meta.get('declared_unit'))
        tables.append(row)
    result = {'status': 'SOURCE_QA_ONLY_NOT_ANALYSIS_LOCK', 'tables': tables}
    if all(c in values for c in ('E05.23', 'E05.38', 'E05.41')):
        revenue, profit, official = [values[c] for c in ('E05.23', 'E05.38', 'E05.41')]
        differences = []
        for (province, year), r in revenue.items():
            p, o = profit.get((province, year)), official.get((province, year))
            if r is None or r <= 0 or p is None or o is None:
                continue
            calculated = 100*p/r
            differences.append({'province': province, 'year': year, 'constructed': calculated,
                                'official': o, 'difference_percentage_points': calculated-o})
        result['profitability_comparison'] = {
            'n': len(differences), 'tolerance_percentage_points': .01,
            'within_tolerance': sum(abs(d['difference_percentage_points']) <= .01 for d in differences),
            'largest_discrepancies': sorted(differences, key=lambda d: abs(d['difference_percentage_points']), reverse=True)[:10],
            'interpretation': 'Check definition and denominator; do not overwrite official values.'}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.input_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'tables': len(result['tables']), 'status': result['status']}))


if __name__ == '__main__':
    main()
