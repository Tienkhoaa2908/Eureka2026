from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class RevenueCorrection:
    province: str
    year: int
    expected_legacy_value: float
    verified_value: float
    source_table: str


VERIFIED_REVENUE_CORRECTIONS: tuple[RevenueCorrection, ...] = (
    RevenueCorrection("Hòa Bình", 2016, 23040.0, 33040.0, "144"),
    RevenueCorrection("Gia Lai", 2023, 133195.0, 131195.0, "151"),
    RevenueCorrection("An Giang", 2023, 212941.0, 212961.0, "151"),
)


def _as_float(value: object) -> float:
    if value is None or str(value).strip() == "":
        raise ValueError("blank numeric value")
    return float(str(value).replace(",", ""))


def apply_verified_revenue_corrections(
    rows: Iterable[Mapping[str, object]],
    *,
    require_all: bool = True,
) -> list[dict[str, object]]:
    """Apply only corrections with independently verified source evidence.

    The function refuses to overwrite an unexpected value. This makes stale or
    already-modified inputs fail loudly rather than silently changing data.
    Revenue growth is then recomputed from corrected annual revenue.
    """

    output = [dict(row) for row in rows]
    corrections = {(c.province, c.year): c for c in VERIFIED_REVENUE_CORRECTIONS}
    seen: set[tuple[str, int]] = set()

    for row in output:
        province = str(row.get("Tinh") or "").strip()
        try:
            year = int(float(str(row.get("Nam"))))
        except (TypeError, ValueError):
            continue

        key = (province, year)
        correction = corrections.get(key)
        if correction is None:
            continue

        current = _as_float(row.get("Doanh_thu_ty_dong"))
        allowed = {
            correction.expected_legacy_value,
            correction.verified_value,
        }
        if current not in allowed:
            raise ValueError(
                f"{province} {year}: expected legacy/verified revenue "
                f"{sorted(allowed)}, found {current}"
            )

        row["Doanh_thu_ty_dong"] = correction.verified_value
        seen.add(key)

    missing = set(corrections) - seen
    if require_all and missing:
        raise ValueError(f"required correction keys missing from panel: {sorted(missing)}")

    revenue_by_key: dict[tuple[str, int], float] = {}
    for row in output:
        province = str(row.get("Tinh") or "").strip()
        try:
            year = int(float(str(row.get("Nam"))))
            revenue = _as_float(row.get("Doanh_thu_ty_dong"))
        except (TypeError, ValueError):
            continue
        revenue_by_key[(province, year)] = revenue

    for row in output:
        province = str(row.get("Tinh") or "").strip()
        try:
            year = int(float(str(row.get("Nam"))))
            revenue = _as_float(row.get("Doanh_thu_ty_dong"))
        except (TypeError, ValueError):
            continue

        previous = revenue_by_key.get((province, year - 1))
        row["Tang_truong_Doanh_thu_pct"] = (
            None if previous is None else round((revenue / previous - 1.0) * 100.0, 2)
        )

    return output
