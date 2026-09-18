from __future__ import annotations

import csv
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

from src.eureka2026.pipeline import build_panel
from src.eureka2026.province_names import CANONICAL_PROVINCES


def _cell_ref(col: int, row: int) -> str:
    name = ""
    n = col + 1
    while n:
        n, rem = divmod(n - 1, 26)
        name = chr(65 + rem) + name
    return f"{name}{row}"


def _write_xlsx(path: Path, sheet_name: str, rows: list[list[object]]) -> None:
    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row):
            if value is None or value == "":
                continue
            ref = _cell_ref(c_idx, r_idx)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                cells.append(f'<c r="{ref}"><v>{value}</v></c>')
            else:
                cells.append(
                    f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'
                )
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets><sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/></Relationships>'
    )
    worksheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/></Relationships>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '</Types>'
    )
    with ZipFile(path, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", rels)
        zf.writestr("xl/worksheets/sheet1.xml", worksheet)


def _revenue_rows() -> list[list[object]]:
    rows: list[list[object]] = [[
        "Tinh", "Vung", "Nam", "PCI", "PCI_lag1",
        "Doanh_thu_ty_dong", "Tang_truong_doanh_thu_pct",
    ]]
    overrides = {
        ("Hòa Bình", 2015): 25819,
        ("Hòa Bình", 2016): 23040,
        ("Hòa Bình", 2017): 36346,
        ("Gia Lai", 2022): 117148,
        ("Gia Lai", 2023): 133195,
        ("Gia Lai", 2024): 168328,
        ("An Giang", 2022): 196282,
        ("An Giang", 2023): 212941,
        ("An Giang", 2024): 234032,
    }
    for p_idx, province in enumerate(CANONICAL_PROVINCES):
        for year in range(2010, 2025):
            revenue = overrides.get(
                (province, year),
                100000 + p_idx * 1000 + (year - 2010) * 100,
            )
            pci = 50 + p_idx / 100 + (year - 2010) / 10
            rows.append([province, "Region", year, pci, None, revenue, None])
    return rows


def _cstp_rows() -> list[list[object]]:
    headers = [
        "Tinh", "Nam", "1. Gia nhập TT", "2. Tiếp cận ĐĐ", "3. Minh bạch",
        "4. CP thời gian", "5. CP KCT", "6. CT bình đẳng", "7. Năng động",
        "8. HT doanh nghiệp", "9. Đào tạo LĐ", "10. TCPL & ANTT",
    ]
    rows: list[list[object]] = [headers]
    for p_idx, province in enumerate(CANONICAL_PROVINCES):
        for year in range(2010, 2025):
            vals = []
            for idx in range(1, 11):
                if idx == 6 and year <= 2012:
                    vals.append(None)
                else:
                    vals.append(4.0 + idx / 10 + p_idx / 1000 + (year - 2010) / 100)
            rows.append([province, year, *vals])
    return rows


class PipelineTests(unittest.TestCase):
    def test_deterministic_full_build_and_verified_corrections(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            revenue = root / "revenue.xlsx"
            cstp = root / "cstp.xlsx"
            _write_xlsx(revenue, "Panel", _revenue_rows())
            _write_xlsx(cstp, "Panel_CSTP", _cstp_rows())

            out1, qa1 = root / "panel1.csv", root / "qa1.json"
            out2, qa2 = root / "panel2.csv", root / "qa2.json"
            s1 = build_panel(revenue, cstp, out1, qa1)
            s2 = build_panel(revenue, cstp, out2, qa2)

            self.assertEqual(s1["output_csv_sha256"], s2["output_csv_sha256"])
            self.assertEqual(s1["rows"], 945)
            self.assertEqual(s1["full_10_cstp_rows"], 756)
            self.assertEqual(s1["lagged_full_10_cstp_rows"], 693)

            with out1.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            by_key = {(r["Tinh"], int(r["Nam"])): r for r in rows}
            self.assertEqual(by_key[("Hòa Bình", 2016)]["Doanh_thu_ty_dong"], "33040")
            self.assertEqual(by_key[("Hòa Bình", 2016)]["Tang_truong_Doanh_thu_pct"], "27.97")
            self.assertEqual(by_key[("Gia Lai", 2023)]["Doanh_thu_ty_dong"], "131195")
            self.assertEqual(by_key[("An Giang", 2023)]["Doanh_thu_ty_dong"], "212961")
            self.assertEqual(by_key[("An Giang", 2013)]["cstp6_lag1"], "")
            self.assertNotEqual(by_key[("An Giang", 2014)]["cstp6_lag1"], "")


if __name__ == "__main__":
    unittest.main()
