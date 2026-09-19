from __future__ import annotations

import unittest

import numpy as np

from src.eureka2026.sr1_fetch import decode_jsonstat2, normalize_province_loose
from src.eureka2026.sr1_models import _fe_beta_matrix, bh_adjust


class SR1AcquisitionTests(unittest.TestCase):
    def test_loose_province_normalization(self):
        self.assertEqual(normalize_province_loose("TP Hồ Chí Minh"), "TP. Hồ Chí Minh")
        self.assertEqual(normalize_province_loose("Ba Ria - Vung Tau"), "Bà Rịa - Vũng Tàu")
        self.assertEqual(normalize_province_loose("Thừa Thiên Huế*"), "Thừa Thiên Huế")
        self.assertIsNone(normalize_province_loose("TOTAL"))

    def test_jsonstat2_decoder(self):
        dataset = {
            "id": ["province", "year"],
            "size": [2, 2],
            "dimension": {
                "province": {
                    "category": {
                        "index": {"p1": 0, "p2": 1},
                        "label": {"p1": "An Giang", "p2": "Bắc Ninh"},
                    }
                },
                "year": {
                    "category": {
                        "index": {"y1": 0, "y2": 1},
                        "label": {"y1": "2022", "y2": "2023"},
                    }
                },
            },
            "value": [1.0, 2.0, 3.0, 4.0],
        }
        rows = decode_jsonstat2(dataset)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], {"province": "An Giang", "year": "2022", "value": 1.0})
        self.assertEqual(rows[-1], {"province": "Bắc Ninh", "year": "2023", "value": 4.0})


class SR1InferenceTests(unittest.TestCase):
    def test_bh_adjust_known(self):
        q = bh_adjust([0.001, 0.01, 0.04, 0.2])
        self.assertAlmostEqual(q[0], 0.004)
        self.assertAlmostEqual(q[1], 0.02)
        self.assertAlmostEqual(q[2], 0.05333333333333334)
        self.assertAlmostEqual(q[3], 0.2)

    def test_fe_coefficient_additivity_for_exact_decomposition(self):
        rng = np.random.default_rng(17)
        x = rng.normal(size=(35, 6))
        firms = 0.4 * x + rng.normal(scale=0.5, size=x.shape)
        workers_per_firm = -0.1 * x + rng.normal(scale=0.3, size=x.shape)
        revenue_per_worker = 0.25 * x + rng.normal(scale=0.4, size=x.shape)
        revenue_per_firm = workers_per_firm + revenue_per_worker
        revenue = firms + revenue_per_firm

        b_total = _fe_beta_matrix(revenue, x)
        b_extensive = _fe_beta_matrix(firms, x)
        b_intensive = _fe_beta_matrix(revenue_per_firm, x)
        b_scale = _fe_beta_matrix(workers_per_firm, x)
        b_productivity = _fe_beta_matrix(revenue_per_worker, x)

        self.assertAlmostEqual(b_total, b_extensive + b_intensive, places=12)
        self.assertAlmostEqual(b_intensive, b_scale + b_productivity, places=12)


if __name__ == "__main__":
    unittest.main()
