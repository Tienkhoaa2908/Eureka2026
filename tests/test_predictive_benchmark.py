from __future__ import annotations

import math
import unittest

from src.eureka2026.predictive_benchmark import (
    OUTER_TEST_YEARS,
    PCI_FEATURES,
    _model_rows,
    inner_folds,
    outer_folds,
    parameter_grid,
)


def synthetic_canonical_rows():
    rows = []
    for p in range(63):
        province = f"P{p:02d}"
        for year in range(2010, 2025):
            revenue = (
                100000 + 1000 * p + 750 * (year - 2010)
                + 5 * (year - 2010) ** 2
            )
            row = {
                "Tinh": province,
                "Nam": str(year),
                "Doanh_thu_ty_dong": str(revenue),
            }
            for i, c in enumerate(PCI_FEATURES, start=1):
                row[c] = (
                    "" if (i == 6 and year <= 2013)
                    else str(4 + i / 10 + p / 1000 + (year - 2010) / 100)
                )
            rows.append(row)
    return rows


class PredictiveBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = _model_rows(synthetic_canonical_rows())

    def test_sample_contract(self):
        self.assertEqual(len(self.rows), 693)
        self.assertEqual(len({r["province"] for r in self.rows}), 63)
        self.assertEqual(
            {r["year"] for r in self.rows}, set(range(2014, 2025))
        )

    def test_outer_folds_are_fixed_and_leak_free(self):
        folds = outer_folds(self.rows)
        self.assertEqual(
            [y for _, _, y in folds], list(OUTER_TEST_YEARS)
        )
        for train, test, year in folds:
            self.assertEqual(len(test), 63)
            self.assertEqual(len(train), 63 * (year - 2014))
            self.assertLess(
                max(self.rows[i]["year"] for i in train), year
            )
            self.assertEqual(
                {self.rows[i]["year"] for i in test}, {year}
            )
            self.assertTrue(set(train).isdisjoint(test))

    def test_inner_folds_never_touch_outer_test(self):
        for outer_train, outer_test, outer_year in outer_folds(self.rows):
            for train, val, val_year in inner_folds(
                self.rows, outer_train
            ):
                self.assertTrue(set(train).isdisjoint(outer_test))
                self.assertTrue(set(val).isdisjoint(outer_test))
                self.assertLess(
                    max(self.rows[i]["year"] for i in train), val_year
                )
                self.assertLess(val_year, outer_year)

    def test_small_prespecified_grids(self):
        self.assertEqual(len(parameter_grid("elastic_net")), 6)
        self.assertEqual(len(parameter_grid("random_forest")), 3)
        self.assertEqual(len(parameter_grid("xgboost")), 4)

    def test_lagged_revenue_features_are_pre_target(self):
        raw = synthetic_canonical_rows()
        revenue = {
            (r["Tinh"], int(r["Nam"])): float(r["Doanh_thu_ty_dong"])
            for r in raw
        }
        for r in self.rows:
            p, y = r["province"], r["year"]
            self.assertAlmostEqual(
                r["lag_log_revenue"],
                math.log(revenue[(p, y - 1)]),
                places=12,
            )
            self.assertAlmostEqual(
                r["lag_log_revenue_change"],
                math.log(revenue[(p, y - 1)])
                - math.log(revenue[(p, y - 2)]),
                places=12,
            )


if __name__ == "__main__":
    unittest.main()
