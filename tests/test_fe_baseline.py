import unittest

import numpy as np

from src.eureka2026.fe_baseline import benjamini_hochberg, standardization_stats


class FEBaselineTests(unittest.TestCase):
    def test_bh_known_values(self):
        p = [0.001, 0.01, 0.04, 0.20]
        q = benjamini_hochberg(p)
        self.assertAlmostEqual(q[0], 0.004)
        self.assertAlmostEqual(q[1], 0.02)
        self.assertAlmostEqual(q[2], 0.05333333333333334)
        self.assertAlmostEqual(q[3], 0.20)

    def test_bh_preserves_input_order_and_bounds(self):
        p = [0.5, 0.001, 0.2, 0.04]
        q = benjamini_hochberg(p)
        self.assertEqual(len(q), len(p))
        self.assertTrue(all(0.0 <= x <= 1.0 for x in q))
        self.assertLess(q[1], q[3])

    def test_standardization_uses_sample_sd(self):
        rows = []
        for value in (1.0, 2.0, 3.0):
            row = {f"cstp{i}_lag1": str(value + i) for i in range(1, 11)}
            rows.append(row)
        means, sds = standardization_stats(rows)
        self.assertTrue(np.allclose(means, np.arange(1, 11, dtype=float) + 2.0))
        self.assertTrue(np.allclose(sds, np.ones(10)))

    def test_standardization_rejects_zero_variance(self):
        rows = [{f"cstp{i}_lag1": "5" for i in range(1, 11)} for _ in range(3)]
        with self.assertRaisesRegex(ValueError, "invalid standardization"):
            standardization_stats(rows)


if __name__ == "__main__":
    unittest.main()
