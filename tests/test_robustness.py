from __future__ import annotations

import unittest

import numpy as np

from src.eureka2026.robustness import bh, pesaran_cd


class RobustnessTests(unittest.TestCase):
    def test_bh_known_values(self):
        q = bh([0.001, 0.01, 0.04, 0.20])
        self.assertAlmostEqual(q[0], 0.004)
        self.assertAlmostEqual(q[1], 0.02)
        self.assertAlmostEqual(q[2], 0.05333333333333334)
        self.assertAlmostEqual(q[3], 0.20)

    def test_pesaran_cd_balanced_shape(self):
        rows = []
        residuals = []
        values = {
            "A": [1, -1, 1, -1, 0],
            "B": [-1, 1, -1, 1, 0],
            "C": [1, 0, -1, 0, 1],
            "D": [0, 1, 0, -1, 1],
        }
        for province, seq in values.items():
            for year, residual in zip(range(2018, 2023), seq):
                rows.append({"Tinh": province, "Nam": year})
                residuals.append(residual)
        result = pesaran_cd(rows, np.asarray(residuals, float))
        self.assertEqual(result["n_entities"], 4)
        self.assertEqual(result["t_periods"], 5)
        self.assertTrue(np.isfinite(result["pesaran_cd"]))
        self.assertGreaterEqual(result["asymptotic_p_value"], 0.0)
        self.assertLessEqual(result["asymptotic_p_value"], 1.0)


if __name__ == "__main__":
    unittest.main()
