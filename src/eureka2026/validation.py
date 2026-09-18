from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

EXPECTED_YEARS = tuple(range(2010, 2025))
EXPECTED_PROVINCES = 63
CSTP_COLUMNS = tuple(f"cstp{i}" for i in range(1, 11))


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def _is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def validate_panel_rows(rows: Iterable[dict[str, str]], kind: str) -> ValidationResult:
    rows = list(rows)
    errors: list[str] = []
    warnings: list[str] = []

    if kind not in {"revenue", "cstp"}:
        return ValidationResult((f"unknown kind: {kind}",), ())

    if not rows:
        return ValidationResult(("panel is empty",), ())

    keys: list[tuple[str, int]] = []
    by_year: Counter[int] = Counter()
    years_by_province: dict[str, set[int]] = defaultdict(set)

    for idx, row in enumerate(rows, start=2):
        province = (row.get("Tinh") or "").strip()
        raw_year = row.get("Nam")
        if not province:
            errors.append(f"row {idx}: missing Tinh")
            continue
        try:
            year = int(float(str(raw_year)))
        except (TypeError, ValueError):
            errors.append(f"row {idx}: invalid Nam={raw_year!r}")
            continue

        keys.append((province, year))
        by_year[year] += 1
        years_by_province[province].add(year)

        if year not in EXPECTED_YEARS:
            errors.append(f"row {idx}: year outside 2010-2024: {year}")

        if kind == "revenue":
            value = row.get("Doanh_thu_ty_dong")
            if _is_blank(value):
                errors.append(f"row {idx}: missing Doanh_thu_ty_dong")
            else:
                try:
                    if float(str(value).replace(",", "")) <= 0:
                        errors.append(f"row {idx}: non-positive revenue={value!r}")
                except ValueError:
                    errors.append(f"row {idx}: invalid revenue={value!r}")
        else:
            for c in CSTP_COLUMNS:
                value = row.get(c)
                if c == "cstp6" and year <= 2012:
                    if not _is_blank(value):
                        errors.append(
                            f"row {idx}: cstp6 must be structurally missing before 2013"
                        )
                elif _is_blank(value):
                    errors.append(f"row {idx}: unexpected missing {c} in {year}")

    duplicate_keys = [key for key, n in Counter(keys).items() if n > 1]
    if duplicate_keys:
        errors.append(f"duplicate province-year keys: {duplicate_keys[:10]}")

    if len(keys) != EXPECTED_PROVINCES * len(EXPECTED_YEARS):
        errors.append(f"expected 945 valid rows, found {len(keys)}")

    for year in EXPECTED_YEARS:
        n = by_year[year]
        if n != EXPECTED_PROVINCES:
            errors.append(f"year {year}: expected 63 provinces, found {n}")

    if len(years_by_province) != EXPECTED_PROVINCES:
        errors.append(f"expected 63 unique provinces, found {len(years_by_province)}")

    expected_year_set = set(EXPECTED_YEARS)
    for province, years in years_by_province.items():
        if years != expected_year_set:
            missing = sorted(expected_year_set - years)
            extra = sorted(years - expected_year_set)
            errors.append(f"{province}: missing years={missing}, extra years={extra}")

    return ValidationResult(tuple(errors), tuple(warnings))


def validate_csv(path: str | Path, kind: str) -> ValidationResult:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return validate_panel_rows(csv.DictReader(handle), kind=kind)
