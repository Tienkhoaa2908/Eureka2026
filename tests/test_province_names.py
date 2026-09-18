import unittest

from src.eureka2026.province_names import CANONICAL_PROVINCES, normalize_province_name


class ProvinceNameTests(unittest.TestCase):
    def test_has_exactly_63_canonical_provinces(self):
        self.assertEqual(len(CANONICAL_PROVINCES), 63)
        self.assertEqual(len(set(CANONICAL_PROVINCES)), 63)

    def test_explicit_aliases(self):
        self.assertEqual(normalize_province_name("TP.HCM"), "TP. Hồ Chí Minh")
        self.assertEqual(normalize_province_name("Bà Rịa-Vũng Tàu"), "Bà Rịa - Vũng Tàu")

    def test_unknown_name_fails_loudly(self):
        with self.assertRaisesRegex(ValueError, "unknown province"):
            normalize_province_name("Province 64")


if __name__ == "__main__":
    unittest.main()
