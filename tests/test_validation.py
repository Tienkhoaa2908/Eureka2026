import unittest

from src.eureka2026.validation import CSTP_COLUMNS, validate_panel_rows


class ValidationTests(unittest.TestCase):
    def make_rows(self, kind: str):
        rows = []
        for p in range(63):
            for year in range(2010, 2025):
                row = {"Tinh": f"P{p:02d}", "Nam": str(year)}
                if kind == "revenue":
                    row["Doanh_thu_ty_dong"] = "100"
                else:
                    for c in CSTP_COLUMNS:
                        row[c] = "" if c == "cstp6" and year <= 2012 else "6.0"
                rows.append(row)
        return rows

    def test_valid_revenue_panel(self):
        result = validate_panel_rows(self.make_rows("revenue"), "revenue")
        self.assertTrue(result.ok, result.errors)

    def test_valid_structural_missingness(self):
        result = validate_panel_rows(self.make_rows("cstp"), "cstp")
        self.assertTrue(result.ok, result.errors)

    def test_rejects_imputed_pre2013_cstp6(self):
        rows = self.make_rows("cstp")
        rows[0]["cstp6"] = "6.0"
        result = validate_panel_rows(rows, "cstp")
        self.assertFalse(result.ok)
        self.assertTrue(any("structurally missing" in e for e in result.errors))

    def test_rejects_duplicate_key(self):
        rows = self.make_rows("revenue")
        rows.append(dict(rows[0]))
        result = validate_panel_rows(rows, "revenue")
        self.assertFalse(result.ok)
        self.assertTrue(any("duplicate" in e for e in result.errors))


if __name__ == "__main__":
    unittest.main()
