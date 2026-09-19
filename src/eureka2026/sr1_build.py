from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any

from .province_names import CANONICAL_PROVINCES

CORE_YEARS = tuple(range(2015, 2024))
ENTRY_TARGET_YEARS = tuple(range(2018, 2025))
COMPONENTS = tuple(f"cstp{i}" for i in range(1, 11))

SERIES_TO_FILE = {
    "active_results": "V05.08_active_results.csv",
    "workers": "V05.11_workers.csv",
    "capital": "V05.17_capital.csv",
    "revenue": "V05.23_revenue.csv",
    "monthly_income": "V05.35_monthly_income.csv",
    "profit": "V05.38_profit.csv",
    "profitability_ratio": "V05.41_profitability_ratio.csv",
    "fixed_assets_per_worker": "V05.44_fixed_assets_per_worker.csv",
    "new_registrations": "V05.02_new_registrations.csv",
    "active_all": "V05.04_active_all.csv",
    "active_per_1000": "V05.05_active_per_1000.csv",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_series(path: Path) -> dict[tuple[str, int], float | None]:
    out: dict[tuple[str, int], float | None] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (row["province"], int(row["year"]))
            raw = row["value"]
            value = None if raw in ("", "None", "null") else float(raw)
            if key in out:
                raise ValueError(f"duplicate series key {key} in {path}")
            out[key] = value
    return out


def _read_pci(path: Path) -> dict[tuple[str, int, str], float | None]:
    out: dict[tuple[str, int, str], float | None] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = (row["province"], int(row["year"]), row["component"])
            raw = row["value"]
            out[key] = None if raw in ("", "None", "null") else float(raw)
    return out


def _year_zscores(
    pci: dict[tuple[str, int, str], float | None],
    year: int,
    component: str,
) -> dict[str, float | None]:
    vals = [
        pci.get((province, year, component))
        for province in CANONICAL_PROVINCES
    ]
    observed = [float(v) for v in vals if v is not None]
    if len(observed) < 50:
        raise ValueError(
            f"too few PCI values for within-year standardization: {component} {year} n={len(observed)}"
        )
    mu = mean(observed)
    sd = stdev(observed)
    if sd <= 0:
        raise ValueError(f"zero PCI SD for {component} {year}")
    return {
        province: (
            None
            if pci.get((province, year, component)) is None
            else (float(pci[(province, year, component)]) - mu) / sd
        )
        for province in CANONICAL_PROVINCES
    }


def _safe_log(value: float | None, name: str, key: tuple[str, int]) -> float | None:
    if value is None:
        return None
    if value <= 0:
        raise ValueError(f"{name} must be positive at {key}, got {value}")
    return math.log(value)


def _write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError(f"no records for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def build_core_panel(raw_root: Path, output_root: Path) -> tuple[Path, dict[str, Any]]:
    nso_root = raw_root / "nso"
    pci_path = raw_root / "pci" / "pci_components_2014_2024.csv"
    series = {
        name: _read_series(nso_root / filename)
        for name, filename in SERIES_TO_FILE.items()
        if name not in {"new_registrations", "active_all", "active_per_1000"}
    }
    pci = _read_pci(pci_path)

    zcache: dict[tuple[int, str], dict[str, float | None]] = {}
    for exposure_year in range(2014, 2023):
        for component in COMPONENTS:
            zcache[(exposure_year, component)] = _year_zscores(
                pci, exposure_year, component
            )

    records: list[dict[str, Any]] = []
    identity_residuals = []
    missing_by_series = {name: 0 for name in series}
    for province in CANONICAL_PROVINCES:
        for year in CORE_YEARS:
            key = (province, year)
            vals = {name: data.get(key) for name, data in series.items()}
            for name, value in vals.items():
                if value is None:
                    missing_by_series[name] += 1

            firms = vals["active_results"]
            workers = vals["workers"]
            capital = vals["capital"]
            revenue = vals["revenue"]
            profit = vals["profit"]
            wage = vals["monthly_income"]
            profitability = vals["profitability_ratio"]
            fixed_worker = vals["fixed_assets_per_worker"]

            row: dict[str, Any] = {
                "province": province,
                "year": year,
                "active_firms": firms,
                "workers": workers,
                "capital_billion_vnd": capital,
                "revenue_billion_vnd": revenue,
                "profit_billion_vnd": profit,
                "monthly_income_thousand_vnd": wage,
                "profitability_ratio_pct_nso": profitability,
                "fixed_assets_per_worker_million_vnd_nso": fixed_worker,
            }

            if firms is not None and workers is not None and revenue is not None and capital is not None:
                if firms <= 0 or workers <= 0 or revenue <= 0 or capital <= 0:
                    raise ValueError(f"nonpositive core denominator at {key}")
                revenue_per_firm_million = revenue * 1000.0 / firms
                workers_per_firm = workers / firms
                revenue_per_worker_million = revenue * 1000.0 / workers
                capital_per_firm_million = capital * 1000.0 / firms
                capital_per_worker_million = capital * 1000.0 / workers

                row.update({
                    "log_active_firms": math.log(firms),
                    "revenue_per_firm_million_vnd": revenue_per_firm_million,
                    "log_revenue_per_firm": math.log(revenue_per_firm_million),
                    "workers_per_firm": workers_per_firm,
                    "log_workers_per_firm": math.log(workers_per_firm),
                    "revenue_per_worker_million_vnd": revenue_per_worker_million,
                    "log_revenue_per_worker": math.log(revenue_per_worker_million),
                    "capital_per_firm_million_vnd": capital_per_firm_million,
                    "log_capital_per_firm": math.log(capital_per_firm_million),
                    "capital_per_worker_million_vnd": capital_per_worker_million,
                    "log_capital_per_worker": math.log(capital_per_worker_million),
                    "log_revenue_billion": math.log(revenue),
                })
                residual1 = (
                    row["log_revenue_billion"]
                    - row["log_active_firms"]
                    - row["log_revenue_per_firm"]
                    + math.log(1000.0)
                )
                residual2 = (
                    row["log_revenue_per_firm"]
                    - row["log_workers_per_firm"]
                    - row["log_revenue_per_worker"]
                )
                identity_residuals.extend([abs(residual1), abs(residual2)])
            else:
                row.update({
                    "log_active_firms": None,
                    "revenue_per_firm_million_vnd": None,
                    "log_revenue_per_firm": None,
                    "workers_per_firm": None,
                    "log_workers_per_firm": None,
                    "revenue_per_worker_million_vnd": None,
                    "log_revenue_per_worker": None,
                    "capital_per_firm_million_vnd": None,
                    "log_capital_per_firm": None,
                    "capital_per_worker_million_vnd": None,
                    "log_capital_per_worker": None,
                    "log_revenue_billion": None,
                })

            if profit is not None and firms is not None and firms > 0:
                profit_per_firm_million = profit * 1000.0 / firms
                row["profit_per_firm_million_vnd"] = profit_per_firm_million
                row["asinh_profit_per_firm"] = math.asinh(profit_per_firm_million)
            else:
                row["profit_per_firm_million_vnd"] = None
                row["asinh_profit_per_firm"] = None

            if profit is not None and revenue is not None and revenue > 0:
                row["profit_margin_pct_constructed"] = profit / revenue * 100.0
            else:
                row["profit_margin_pct_constructed"] = None

            row["log_monthly_income"] = _safe_log(
                wage, "monthly_income", key
            )
            row["log_fixed_assets_per_worker"] = _safe_log(
                fixed_worker, "fixed_assets_per_worker", key
            )

            exposure_year = year - 1
            for component in COMPONENTS:
                raw = pci.get((province, exposure_year, component))
                row[f"{component}_lag1_raw"] = raw
                row[f"{component}_lag1_z"] = zcache[(exposure_year, component)][province]
            records.append(row)

    expected = len(CANONICAL_PROVINCES) * len(CORE_YEARS)
    if len(records) != expected:
        raise ValueError(f"core panel expected {expected}, got {len(records)}")
    max_identity = max(identity_residuals) if identity_residuals else math.inf
    if max_identity > 1e-10:
        raise ValueError(f"accounting log identity residual too large: {max_identity}")

    output_path = output_root / "mechanism_panel_2015_2023.csv"
    _write_csv(output_path, records)
    qa = {
        "rows": len(records),
        "provinces": len({r["province"] for r in records}),
        "years": sorted({r["year"] for r in records}),
        "missing_by_source_series": missing_by_series,
        "max_accounting_log_identity_abs_residual": max_identity,
        "sha256": sha256_file(output_path),
    }
    return output_path, qa


def build_entry_panel(raw_root: Path, output_root: Path) -> tuple[Path, dict[str, Any]]:
    nso_root = raw_root / "nso"
    new_regs = _read_series(nso_root / SERIES_TO_FILE["new_registrations"])
    active_all = _read_series(nso_root / SERIES_TO_FILE["active_all"])
    density = _read_series(nso_root / SERIES_TO_FILE["active_per_1000"])
    pci = _read_pci(raw_root / "pci" / "pci_components_2014_2024.csv")

    zcache: dict[tuple[int, str], dict[str, float | None]] = {}
    for exposure_year in range(2017, 2024):
        for component in COMPONENTS:
            zcache[(exposure_year, component)] = _year_zscores(
                pci, exposure_year, component
            )

    records = []
    for province in CANONICAL_PROVINCES:
        for year in ENTRY_TARGET_YEARS:
            regs = new_regs.get((province, year))
            lag_stock = active_all.get((province, year - 1))
            current_stock = active_all.get((province, year))
            firm_density = density.get((province, year))
            entry_rate = (
                None
                if regs is None or lag_stock is None or lag_stock <= 0
                else regs / lag_stock
            )
            row: dict[str, Any] = {
                "province": province,
                "year": year,
                "new_registrations": regs,
                "active_firms_all": current_stock,
                "lag_active_firms_all": lag_stock,
                "entry_rate": entry_rate,
                "active_firms_per_1000_people": firm_density,
                "log_active_firms_all": (
                    None if current_stock is None or current_stock <= 0
                    else math.log(current_stock)
                ),
            }
            exposure_year = year - 1
            for component in COMPONENTS:
                row[f"{component}_lag1_raw"] = pci.get(
                    (province, exposure_year, component)
                )
                row[f"{component}_lag1_z"] = zcache[(exposure_year, component)][province]
            records.append(row)

    expected = len(CANONICAL_PROVINCES) * len(ENTRY_TARGET_YEARS)
    if len(records) != expected:
        raise ValueError(f"entry panel expected {expected}, got {len(records)}")
    output_path = output_root / "entry_panel_2018_2024.csv"
    _write_csv(output_path, records)
    qa = {
        "rows": len(records),
        "provinces": len({r["province"] for r in records}),
        "years": sorted({r["year"] for r in records}),
        "missing_entry_rate": sum(r["entry_rate"] is None for r in records),
        "missing_density": sum(
            r["active_firms_per_1000_people"] is None for r in records
        ),
        "sha256": sha256_file(output_path),
    }
    return output_path, qa


def run(input_root: str | Path, output_root: str | Path) -> dict[str, Any]:
    input_root = Path(input_root)
    output_root = Path(output_root)
    core_path, core_qa = build_core_panel(input_root / "raw", output_root)
    entry_path, entry_qa = build_entry_panel(input_root / "raw", output_root)
    result = {
        "core": core_qa,
        "entry": entry_qa,
        "files": {
            "core": str(core_path),
            "entry": str(entry_path),
        },
    }
    qa_path = output_root / "mechanism_panel_qa.json"
    qa_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--input-root", default="artifacts/sr1")
    p.add_argument("--output-root", default="artifacts/sr1/processed")
    return p


def main() -> int:
    args = parser().parse_args()
    result = run(args.input_root, args.output_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
