"""Kiểm toán gói bàn giao, không dùng siêu dữ liệu như số liệu quan sát."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

from .province_names import CANONICAL_PROVINCES, normalize_province_name
from .revenue_corrections import VERIFIED_REVENUE_CORRECTIONS


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv(data: bytes) -> tuple[list[str], list[dict]]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError("CSV chứa hàng có số ô vượt số cột")
    return list(reader.fieldnames or []), rows


def inspect_panel(rows: list[dict]) -> dict:
    keys = [(normalize_province_name(r["Tinh"]), int(r["Nam"])) for r in rows]
    counted = Counter(keys)
    expected = {(p, y) for p in CANONICAL_PROVINCES for y in range(2010, 2025)}
    by_key = dict(zip(keys, rows))
    lag_errors, growth_errors, range_errors = [], [], []
    for (p, year), row in zip(keys, rows):
        revenue, pci = float(row["Doanh_thu_ty_dong"]), float(row["PCI"])
        if not math.isfinite(revenue) or revenue <= 0 or not 0 <= pci <= 100:
            range_errors.append([p, year])
        prev = by_key.get((p, year - 1))
        lag = row["PCI_lag1"]
        growth = row["Tang_truong_doanh_thu_pct"]
        if prev is None:
            if lag != "": lag_errors.append([p, year])
            if growth != "": growth_errors.append([p, year])
        else:
            if lag == "" or abs(float(lag) - float(prev["PCI"])) > 1e-9:
                lag_errors.append([p, year])
            correct = 100 * (revenue / float(prev["Doanh_thu_ty_dong"]) - 1)
            if growth == "" or abs(float(growth) - correct) > 0.00500001:
                growth_errors.append([p, year])
    corrections = []
    for correction in VERIFIED_REVENUE_CORRECTIONS:
        value = float(by_key[(correction.province, correction.year)]["Doanh_thu_ty_dong"])
        corrections.append({"province": correction.province, "year": correction.year,
                            "value": value, "matches_registry": value == correction.verified_value})
    return {
        "grain": "tỉnh-năm", "rows": len(rows), "provinces": len({p for p, _ in keys}),
        "years": sorted({y for _, y in keys}),
        "rows_by_year": dict(sorted(Counter(y for _, y in keys).items())),
        "duplicate_keys": [[*k, n] for k, n in counted.items() if n > 1],
        "missing_keys": sorted(expected - set(keys)), "extra_keys": sorted(set(keys) - expected),
        "pci_lag_errors": lag_errors, "revenue_growth_errors": growth_errors,
        "range_errors": range_errors, "verified_corrections": corrections,
        "pci_components_present": [f"cstp{i}" for i in range(1, 11) if f"cstp{i}" in rows[0]],
        "research_use": "Chỉ đối chiếu lịch sử; thiếu số doanh nghiệp, lao động, vốn, lợi nhuận và thành phần PCI cho SR1.",
    }


def run(bundle: Path, output: Path) -> dict:
    repo = Path(__file__).resolve().parents[2]
    roles = {
        "Eureka2026_panel_corrected_2010_2024.csv": "Bảng quan sát dẫn xuất của hướng cũ",
        "Eureka2026_panel_QA_DATA_INTEGRITY_01.csv": "Nhật ký kiểm toán; không phải bảng quan sát",
        "SR1_DATA_CATALOG.csv": "Danh mục nguồn; không phải dữ liệu đã thu thập",
        "DATA_DICTIONARY_SR1.csv": "Từ điển biến; không phải bảng quan sát",
        "scientific_extension_sources.csv": "Danh mục nguồn bổ sung; không phải bảng quan sát",
    }
    inventory, metadata_comparisons = [], []
    with zipfile.ZipFile(bundle) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Gói ZIP có tên tệp trùng")
        for name in names:
            data = archive.read(name)
            columns, rows = read_csv(data)
            entry = {
                "filename": name, "bytes": len(data), "sha256": digest(data),
                "rows": len(rows), "columns": columns, "role": roles.get(name, "[CHƯA XÁC MINH]"),
                "nulls": {c: sum(r.get(c) in (None, "") for r in rows) for c in columns},
            }
            inventory.append(entry)
            if "Tinh" in columns and "Nam" in columns:
                entry["panel_checks"] = inspect_panel(rows)
            reference = repo / "data/metadata" / name
            if reference.is_file():
                repo_cols, repo_rows = read_csv(reference.read_bytes())
                key = "variable" if "variable" in columns else "source_id"
                old = {r[key]: r for r in rows}
                new = {r[key]: r for r in repo_rows}
                if len(old) != len(rows) or len(new) != len(repo_rows):
                    raise ValueError(f"Trùng khóa siêu dữ liệu: {name}")
                metadata_comparisons.append({
                    "filename": name, "repo_sha256": digest(reference.read_bytes()),
                    "byte_identical": data == reference.read_bytes(),
                    "same_schema": columns == repo_cols, "uploaded_rows": len(rows),
                    "repo_rows": len(repo_rows), "only_in_repo": sorted(set(new) - set(old)),
                    "only_in_upload": sorted(set(old) - set(new)),
                    "changed_rows": [{"key": k, "changes": {c: {"upload": old[k].get(c), "repo": new[k].get(c)}
                                    for c in set(columns) | set(repo_cols) if old[k].get(c) != new[k].get(c)}}
                                     for k in sorted(set(old) & set(new)) if old[k] != new[k]],
                    "resolution": "Giữ cả hai phiên bản; catalog main là trạng thái vận hành, không chứng minh đã có quan sát.",
                })
    result = {
        "bundle_filename": bundle.name, "bundle_sha256": digest(bundle.read_bytes()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
        "files": inventory, "metadata_comparisons": metadata_comparisons,
        "status": "KIỂM TOÁN BÀN GIAO; KHÔNG PHẢI ĐẠT CỔNG DỮ LIỆU SR1",
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "handoff_inventory.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    with (output / "handoff_inventory.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "rows", "bytes", "sha256", "role"], lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: e[k] for k in writer.fieldnames} for e in inventory)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/qa/handoff"))
    args = parser.parse_args()
    result = run(args.bundle, args.output)
    print(json.dumps({"files": len(result["files"]), "status": result["status"]}, ensure_ascii=False))
