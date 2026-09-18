from pathlib import Path
import unittest


class LegacyPathTests(unittest.TestCase):
    def test_active_source_has_no_mnt_user_data_paths(self):
        offenders = []
        for root_name in ("src", "scripts"):
            root = Path(root_name)
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file() and path.suffix in {".py", ".sh", ".toml", ".yml", ".yaml"}:
                    text = path.read_text(encoding="utf-8")
                    if "/mnt/user-data" in text:
                        offenders.append(str(path))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
