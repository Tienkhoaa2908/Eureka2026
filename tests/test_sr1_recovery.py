"""Dữ liệu trong kiểm thử là giả lập, không phải bằng chứng nghiên cứu."""
import csv
import tempfile
import unittest
from pathlib import Path

import numpy as np
from bs4 import BeautifulSoup

from src.eureka2026.province_names import CANONICAL_PROVINCES
from src.eureka2026.sr1_build import _read_pci, build_entry_panel, SERIES_TO_FILE
from src.eureka2026.sr1_fetch import _choose_scalar_option, normalize_province_loose, _parse_wide_pxweb_csv
from src.eureka2026.sr1_models import mechanism_decomposition, run


class RecoveryTests(unittest.TestCase):
    def test_hue_alias_is_explicitly_historical(self):
        self.assertIsNone(normalize_province_loose("Hue"))
        self.assertEqual(normalize_province_loose("Hue", historical_63=True), "Thừa Thiên Huế")
        body = b'"Province","2023","2024"\n"Hue",10,12\n'
        rows = _parse_wide_pxweb_csv(body, (2023, 2024), "fixture", "fixture", "persons")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["province"], "Thừa Thiên Huế")
        self.assertEqual(_parse_wide_pxweb_csv(b'"Province","2025"\n"Hue",10\n', (2025,), "fixture", "fixture", "persons"), [])

    def test_total_year_header_and_ambiguous_duplicate(self):
        rows = _parse_wide_pxweb_csv(b'"Province","Total 2022","Total Prel. 2023"\n"Ha Noi",12,14\n', (2022, 2023), "fixture", "population", "thousand_persons")
        self.assertEqual([r["value"] for r in rows], [12, 14])
        with self.assertRaisesRegex(ValueError, 'ambiguous repeated'):
            _parse_wide_pxweb_csv(b'"Province","2022","Total 2022","2023"\n"Ha Noi",12,13,14\n', (2022, 2023), "fixture", "population", "thousand_persons")

    def test_auxiliary_selection_must_be_unambiguous(self):
        box = BeautifulSoup('<select><option value="m">Male</option><option value="f">Female</option></select>', 'html.parser').select_one('select')
        with self.assertRaisesRegex(ValueError, 'chưa xác minh'):
            _choose_scalar_option(box)

    def test_duplicate_pci_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'pci.csv'
            path.write_text('province,year,component,value\nAn Giang,2020,cstp1,5\nAn Giang,2020,cstp1,6\n')
            with self.assertRaisesRegex(ValueError, 'duplicate PCI'):
                _read_pci(path)

    def test_missing_analysis_lock_blocks_before_reading_data(self):
        with self.assertRaisesRegex(ValueError, 'Chưa khóa'):
            run('file_does_not_exist', 'file_does_not_exist', 'unused')

    def test_entry_reads_normalized_layout_and_calendar_lag(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / 'raw'
            nso = raw / 'nso' / 'normalized'
            nso.mkdir(parents=True)
            for name, value in [('new_registrations', 20), ('active_all', 100),
                                ('active_per_1000', 2), ('average_population', 50)]:
                with (nso / SERIES_TO_FILE[name]).open('w', newline='') as f:
                    w = csv.writer(f); w.writerow(['province', 'year', 'value'])
                    for p in CANONICAL_PROVINCES:
                        for y in range(2017, 2025): w.writerow([p, y, value])
            (raw / 'pci').mkdir()
            with (raw / 'pci' / 'pci_components_2013_2024.csv').open('w', newline='') as f:
                w = csv.writer(f); w.writerow(['province', 'year', 'component', 'value'])
                for i, p in enumerate(CANONICAL_PROVINCES):
                    for y in range(2016, 2025):
                        for c in range(1, 11): w.writerow([p, y, f'cstp{c}', 3 + i / 100 + c / 100])
            out, qa = build_entry_panel(raw, Path(tmp) / 'processed')
            with out.open() as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(qa['rows'], 441)
            self.assertEqual(qa['missing_entry_rate'], 0)
            self.assertTrue(all(float(r['entry_rate']) == 0.2 for r in rows))
            self.assertEqual(qa['density_crosscheck_max_abs_difference'], 0)

    def test_decomposition_uses_common_sample_with_missing_outcomes(self):
        rng = np.random.default_rng(391)
        rows = []
        for i in range(32):
            for y in range(2016, 2022):
                x, x5, f, scale, worker = rng.normal(size=5)
                rows.append({'province': str(i), 'year': y, 'cstp4_lag1_z': x,
                             'cstp5_lag1_z': x5, 'dlog_revenue': f + scale + worker,
                             'dlog_active_firms': f, 'dlog_revenue_per_firm': scale + worker,
                             'dlog_workers_per_firm': scale, 'dlog_revenue_per_worker': worker})
        rows[0]['dlog_active_firms'] = None
        records, qa = mechanism_decomposition(rows)
        self.assertEqual({r['n'] for r in records}, {191})
        for values in qa.values():
            self.assertLess(abs(values['top_identity_residual']), 1e-9)
            self.assertLess(abs(values['intensive_identity_residual']), 1e-9)


if __name__ == '__main__':
    unittest.main()
