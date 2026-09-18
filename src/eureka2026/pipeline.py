from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping

from .province_names import CANONICAL_PROVINCES, normalize_province_name
from .revenue_corrections import VERIFIED_REVENUE_CORRECTIONS, apply_verified_revenue_corrections
from .xlsx_reader import read_sheet_records

YEARS = tuple(range(2010, 2025))
CSTP_SOURCE_COLUMNS = (
    "1. Gia nhập TT", "2. Tiếp cận ĐĐ", "3. Minh bạch", "4. CP thời gian",
    "5. CP KCT", "6. CT bình đẳng", "7. Năng động", "8. HT doanh nghiệp",
    "9. Đào tạo LĐ", "10. TCPL & ANTT",
)
CSTP_COLUMNS = tuple(f"cstp{i}" for i in range(1, 11))
CSTP_LAG_COLUMNS = tuple(f"cstp{i}_lag1" for i in range(1, 11))
OUTPUT_COLUMNS = (
    "Tinh", "Vung", "Nam", "PCI", "PCI_lag1", "Doanh_thu_ty_dong",
    "Tang_truong_Doanh_thu_pct", *CSTP_COLUMNS, *CSTP_LAG_COLUMNS,
)


def _blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def _float(value: object, field: str) -> float:
    if _blank(value):
        raise ValueError(f"blank numeric field: {field}")
    try:
        return float(str(value).replace(",", ""))
    except ValueError as exc:
        raise ValueError(f"invalid numeric field {field}={value!r}") from exc


def _int(value: object, field: str) -> int:
    num = _float(value, field)
    if not num.is_integer():
        raise ValueError(f"non-integer {field}={value!r}")
    return int(num)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _keyed(rows: Iterable[Mapping[str, object]], label: str) -> dict[tuple[str, int], dict[str, object]]:
    out: dict[tuple[str, int], dict[str, object]] = {}
    for raw in rows:
        row = dict(raw)
        province = normalize_province_name(row.get("Tinh"))
        year = _int(row.get("Nam"), "Nam")
        key = (province, year)
        if key in out:
            raise ValueError(f"{label}: duplicate province-year key {key}")
        row["Tinh"] = province
        row["Nam"] = year
        out[key] = row
    return out


def _normalize_revenue_rows(rows: list[dict[str, object | None]]) -> list[dict[str, object]]:
    required = {"Tinh", "Vung", "Nam", "PCI", "Doanh_thu_ty_dong"}
    if not rows:
        raise ValueError("revenue/PCI input is empty")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"revenue/PCI input missing columns: {sorted(missing)}")
    normalized = []
    for raw in rows:
        normalized.append({
            "Tinh": normalize_province_name(raw.get("Tinh")),
            "Vung": str(raw.get("Vung") or "").strip(),
            "Nam": _int(raw.get("Nam"), "Nam"),
            "PCI": _float(raw.get("PCI"), "PCI"),
            "Doanh_thu_ty_dong": _float(raw.get("Doanh_thu_ty_dong"), "Doanh_thu_ty_dong"),
        })
    corrected = apply_verified_revenue_corrections(normalized, require_all=True)
    keyed = _keyed(corrected, "revenue/PCI")

    # Lag is always rebuilt from canonical current-year PCI, never trusted from legacy input.
    for key, row in keyed.items():
        province, year = key
        prev = keyed.get((province, year - 1))
        row["PCI_lag1"] = None if prev is None else prev["PCI"]
    return list(keyed.values())


def _normalize_cstp_rows(rows: list[dict[str, object | None]]) -> list[dict[str, object]]:
    if not rows:
        raise ValueError("CSTP input is empty")
    required = {"Tinh", "Nam", *CSTP_SOURCE_COLUMNS}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"CSTP input missing columns: {sorted(missing)}")
    normalized: list[dict[str, object]] = []
    for raw in rows:
        province = normalize_province_name(raw.get("Tinh"))
        year = _int(raw.get("Nam"), "Nam")
        out: dict[str, object] = {"Tinh": province, "Nam": year}
        for idx, source_col in enumerate(CSTP_SOURCE_COLUMNS, start=1):
            value = raw.get(source_col)
            name = f"cstp{idx}"
            if idx == 6 and year <= 2012:
                if not _blank(value):
                    raise ValueError(f"{province} {year}: cstp6 must be structurally missing")
                out[name] = None
            else:
                out[name] = _float(value, source_col)
        normalized.append(out)
    return normalized


def _validate_universe(rows: list[dict[str, object]], label: str) -> None:
    if len(rows) != 945:
        raise ValueError(f"{label}: expected 945 rows, found {len(rows)}")
    keys = [(str(r["Tinh"]), int(r["Nam"])) for r in rows]
    counts = Counter(keys)
    dup = [k for k, n in counts.items() if n > 1]
    if dup:
        raise ValueError(f"{label}: duplicate keys {dup[:10]}")
    provinces = {p for p, _ in keys}
    if provinces != set(CANONICAL_PROVINCES):
        raise ValueError(
            f"{label}: province universe mismatch; missing={sorted(set(CANONICAL_PROVINCES)-provinces)}, "
            f"extra={sorted(provinces-set(CANONICAL_PROVINCES))}"
        )
    by_province: dict[str, set[int]] = defaultdict(set)
    by_year: Counter[int] = Counter()
    for p, y in keys:
        by_province[p].add(y)
        by_year[y] += 1
    expected_years = set(YEARS)
    for p in CANONICAL_PROVINCES:
        if by_province[p] != expected_years:
            raise ValueError(f"{label}: incomplete years for {p}")
    for y in YEARS:
        if by_year[y] != 63:
            raise ValueError(f"{label}: year {y} expected 63 rows, found {by_year[y]}")


def _build_rows(revenue_rows: list[dict[str, object]], cstp_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    _validate_universe(revenue_rows, "revenue/PCI")
    _validate_universe(cstp_rows, "CSTP")
    rev = _keyed(revenue_rows, "revenue/PCI")
    cstp = _keyed(cstp_rows, "CSTP")
    if set(rev) != set(cstp):
        raise ValueError("merge coverage is not 100% one-to-one")

    region_by_province: dict[str, set[str]] = defaultdict(set)
    for (province, _), r in rev.items():
        region = str(r.get("Vung") or "").strip()
        if not region:
            raise ValueError(f"blank region for {province}")
        region_by_province[province].add(region)
    inconsistent = {p: sorted(v) for p, v in region_by_province.items() if len(v) != 1}
    if inconsistent:
        raise ValueError(f"region changes within province: {inconsistent}")

    order = {p: i for i, p in enumerate(CANONICAL_PROVINCES)}
    rows: list[dict[str, object]] = []
    for province, year in sorted(rev, key=lambda k: (order[k[0]], k[1])):
        r = rev[(province, year)]
        c = cstp[(province, year)]
        out = {
            "Tinh": province,
            "Vung": r["Vung"],
            "Nam": year,
            "PCI": r["PCI"],
            "PCI_lag1": r["PCI_lag1"],
            "Doanh_thu_ty_dong": r["Doanh_thu_ty_dong"],
            "Tang_truong_Doanh_thu_pct": r["Tang_truong_Doanh_thu_pct"],
        }
        for col in CSTP_COLUMNS:
            out[col] = c[col]
        for idx, col in enumerate(CSTP_COLUMNS, start=1):
            prev = cstp.get((province, year - 1))
            out[f"cstp{idx}_lag1"] = None if prev is None else prev[col]
        rows.append(out)
    return rows


def _validate_canonical(rows: list[dict[str, object]]) -> None:
    _validate_universe(rows, "canonical panel")
    for row in rows:
        p, y = str(row["Tinh"]), int(row["Nam"])
        revenue = _float(row["Doanh_thu_ty_dong"], "Doanh_thu_ty_dong")
        if revenue <= 0:
            raise ValueError(f"{p} {y}: non-positive revenue")
        if y == 2010:
            if row["PCI_lag1"] is not None or row["Tang_truong_Doanh_thu_pct"] is not None:
                raise ValueError(f"{p} 2010: lag/growth must be missing")
        else:
            if row["PCI_lag1"] is None or row["Tang_truong_Doanh_thu_pct"] is None:
                raise ValueError(f"{p} {y}: missing PCI lag or revenue growth")
        for idx in range(1, 11):
            current = row[f"cstp{idx}"]
            lag = row[f"cstp{idx}_lag1"]
            if idx == 6 and y <= 2012:
                if current is not None:
                    raise ValueError(f"{p} {y}: cstp6 structural missingness violated")
            elif current is None:
                raise ValueError(f"{p} {y}: unexpected missing cstp{idx}")
            expected_lag_missing = y == 2010 or (idx == 6 and y <= 2013)
            if expected_lag_missing and lag is not None:
                raise ValueError(f"{p} {y}: cstp{idx}_lag1 should be missing")
            if not expected_lag_missing and lag is None:
                raise ValueError(f"{p} {y}: unexpected missing cstp{idx}_lag1")

    by_key = {(str(r["Tinh"]), int(r["Nam"])): r for r in rows}
    expected = {
        ("Hòa Bình", 2016): (33040.0, 27.97),
        ("Gia Lai", 2023): (131195.0, 11.99),
        ("An Giang", 2023): (212961.0, 8.50),
    }
    for key, (revenue, growth) in expected.items():
        r = by_key[key]
        if float(r["Doanh_thu_ty_dong"]) != revenue or float(r["Tang_truong_Doanh_thu_pct"]) != growth:
            raise ValueError(f"verified correction/derived growth mismatch at {key}")


def _format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return format(value, ".15g")
    return str(value)


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(OUTPUT_COLUMNS)
        for row in rows:
            writer.writerow([_format_value(row[col]) for col in OUTPUT_COLUMNS])


def build_panel(
    revenue_xlsx: str | Path,
    cstp_xlsx: str | Path,
    output_csv: str | Path,
    qa_json: str | Path,
) -> dict[str, object]:
    revenue_xlsx = Path(revenue_xlsx)
    cstp_xlsx = Path(cstp_xlsx)
    output_csv = Path(output_csv)
    qa_json = Path(qa_json)

    revenue_source = read_sheet_records(revenue_xlsx, "Panel")
    cstp_source = read_sheet_records(cstp_xlsx, "Panel_CSTP")
    revenue_rows = _normalize_revenue_rows(revenue_source)
    cstp_rows = _normalize_cstp_rows(cstp_source)
    rows = _build_rows(revenue_rows, cstp_rows)
    _validate_canonical(rows)
    _write_csv(output_csv, rows)

    summary: dict[str, object] = {
        "status": "PASS",
        "revenue_xlsx": str(revenue_xlsx),
        "revenue_xlsx_sha256": _sha256(revenue_xlsx),
        "cstp_xlsx": str(cstp_xlsx),
        "cstp_xlsx_sha256": _sha256(cstp_xlsx),
        "output_csv": str(output_csv),
        "output_csv_sha256": _sha256(output_csv),
        "rows": len(rows),
        "provinces": len({r["Tinh"] for r in rows}),
        "years": [min(YEARS), max(YEARS)],
        "full_10_cstp_rows": sum(1 for r in rows if all(r[c] is not None for c in CSTP_COLUMNS)),
        "lagged_full_10_cstp_rows": sum(1 for r in rows if all(r[c] is not None for c in CSTP_LAG_COLUMNS)),
        "verified_revenue_corrections": [
            {"province": c.province, "year": c.year, "verified_value": c.verified_value}
            for c in VERIFIED_REVENUE_CORRECTIONS
        ],
    }
    qa_json.parent.mkdir(parents=True, exist_ok=True)
    qa_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Build the canonical Euréka 2026 province-year panel.")
    p.add_argument("--revenue-xlsx", default="data/raw/migration/panel_PCI_doanhthu_2010_2024.xlsx")
    p.add_argument("--cstp-xlsx", default="data/raw/migration/Panel_10_CSTP_2010_2024.xlsx")
    p.add_argument("--output", default="data/processed/panel.csv")
    p.add_argument("--qa", default="artifacts/qa/repro_pipeline_run.json")
    return p


def main() -> int:
    args = _parser().parse_args()
    summary = build_panel(args.revenue_xlsx, args.cstp_xlsx, args.output, args.qa)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
