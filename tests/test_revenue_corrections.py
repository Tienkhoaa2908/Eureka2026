import unittest

from src.eureka2026.revenue_corrections import apply_verified_revenue_corrections


class RevenueCorrectionTests(unittest.TestCase):
    def legacy_rows(self):
        return [
            {"Tinh": "Hòa Bình", "Nam": 2015, "Doanh_thu_ty_dong": 25819},
            {"Tinh": "Hòa Bình", "Nam": 2016, "Doanh_thu_ty_dong": 23040},
            {"Tinh": "Hòa Bình", "Nam": 2017, "Doanh_thu_ty_dong": 36346},
            {"Tinh": "Gia Lai", "Nam": 2022, "Doanh_thu_ty_dong": 117148},
            {"Tinh": "Gia Lai", "Nam": 2023, "Doanh_thu_ty_dong": 133195},
            {"Tinh": "Gia Lai", "Nam": 2024, "Doanh_thu_ty_dong": 168328},
            {"Tinh": "An Giang", "Nam": 2022, "Doanh_thu_ty_dong": 196282},
            {"Tinh": "An Giang", "Nam": 2023, "Doanh_thu_ty_dong": 212941},
            {"Tinh": "An Giang", "Nam": 2024, "Doanh_thu_ty_dong": 234032},
        ]

    def test_applies_all_verified_values_and_recomputes_growth(self):
        rows = apply_verified_revenue_corrections(self.legacy_rows())
        by_key = {(r["Tinh"], r["Nam"]): r for r in rows}

        self.assertEqual(by_key[("Hòa Bình", 2016)]["Doanh_thu_ty_dong"], 33040.0)
        self.assertEqual(by_key[("Gia Lai", 2023)]["Doanh_thu_ty_dong"], 131195.0)
        self.assertEqual(by_key[("An Giang", 2023)]["Doanh_thu_ty_dong"], 212961.0)

        self.assertEqual(by_key[("Hòa Bình", 2016)]["Tang_truong_Doanh_thu_pct"], 27.97)
        self.assertEqual(by_key[("Hòa Bình", 2017)]["Tang_truong_Doanh_thu_pct"], 10.01)
        self.assertEqual(by_key[("Gia Lai", 2023)]["Tang_truong_Doanh_thu_pct"], 11.99)
        self.assertEqual(by_key[("Gia Lai", 2024)]["Tang_truong_Doanh_thu_pct"], 28.30)
        self.assertEqual(by_key[("An Giang", 2023)]["Tang_truong_Doanh_thu_pct"], 8.50)
        self.assertEqual(by_key[("An Giang", 2024)]["Tang_truong_Doanh_thu_pct"], 9.89)

    def test_rejects_unexpected_source_value(self):
        rows = self.legacy_rows()
        rows[1]["Doanh_thu_ty_dong"] = 99999
        with self.assertRaisesRegex(ValueError, "expected legacy/verified revenue"):
            apply_verified_revenue_corrections(rows)


if __name__ == "__main__":
    unittest.main()
