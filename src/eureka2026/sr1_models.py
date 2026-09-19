from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import statsmodels.api as sm

RANDOM_SEED = 20260919
N_PERMUTATIONS = 199

PRIMARY_HYPOTHESES = {
    "H1_entry": {
        "panel": "entry",
        "pairs": [
            ("cstp1", "entry_rate"),
            ("cstp3", "entry_rate"),
            ("cstp10", "entry_rate"),
            ("cstp1", "log_active_firms_per_1000_people"),
            ("cstp3", "log_active_firms_per_1000_people"),
            ("cstp10", "log_active_firms_per_1000_people"),
        ],
    },
    "H2_transaction_cost": {
        "panel": "core",
        "pairs": [
            ("cstp4", "log_revenue_per_worker"),
            ("cstp5", "log_revenue_per_worker"),
            ("cstp4", "profit_margin_pct_constructed"),
            ("cstp5", "profit_margin_pct_constructed"),
            ("cstp4", "log_revenue_per_firm"),
            ("cstp5", "log_revenue_per_firm"),
        ],
    },
    "H3_capability": {
        "panel": "core",
        "pairs": [
            ("cstp8", "log_revenue_per_worker"),
            ("cstp9", "log_revenue_per_worker"),
            ("cstp8", "log_monthly_income"),
            ("cstp9", "log_monthly_income"),
            ("cstp8", "log_capital_per_worker"),
            ("cstp9", "log_capital_per_worker"),
        ],
    },
}


def _to_number(value: str) -> Any:
    if value in ("", "None", "null", "NA", "N/A"):
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def read_panel(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return [
            {k: _to_number(v) for k, v in row.items()}
            for row in csv.DictReader(f)
        ]


def bh_adjust(pvalues: Sequence[float]) -> list[float]:
    p = np.asarray(pvalues, dtype=float)
    n = len(p)
    order = np.argsort(p)
    out = np.ones(n, dtype=float)
    running = 1.0
    for pos in range(n - 1, -1, -1):
        idx = order[pos]
        running = min(running, float(p[idx]) * n / (pos + 1))
        out[idx] = running
    return out.tolist()


def _filter_rows(
    rows: Sequence[dict[str, Any]],
    outcome: str,
    exposures: Sequence[str],
    exclude_years: set[int] | None = None,
) -> list[dict[str, Any]]:
    exclude_years = exclude_years or set()
    out = []
    for row in rows:
        year = int(row["year"])
        if year in exclude_years:
            continue
        if row.get(outcome) is None:
            continue
        if any(row.get(x) is None for x in exposures):
            continue
        out.append(row)
    return out


def fit_fe(
    rows: Sequence[dict[str, Any]],
    outcome: str,
    exposures: Sequence[str],
    exclude_years: set[int] | None = None,
):
    sample = _filter_rows(rows, outcome, exposures, exclude_years)
    provinces = sorted({str(r["province"]) for r in sample})
    years = sorted({int(r["year"]) for r in sample})
    if len(provinces) < 30 or len(years) < 4:
        raise ValueError(
            f"insufficient FE sample for {outcome} {exposures}: "
            f"n={len(sample)} provinces={len(provinces)} years={len(years)}"
        )

    y = np.asarray([float(r[outcome]) for r in sample], dtype=float)
    cols = [np.ones(len(sample), dtype=float)]
    names = ["const"]
    for exposure in exposures:
        cols.append(np.asarray([float(r[exposure]) for r in sample], dtype=float))
        names.append(exposure)
    for province in provinces[1:]:
        cols.append(np.asarray([r["province"] == province for r in sample], dtype=float))
        names.append("province:" + province)
    for year in years[1:]:
        cols.append(np.asarray([int(r["year"]) == year for r in sample], dtype=float))
        names.append("year:" + str(year))
    X = np.column_stack(cols)
    groups = np.asarray([provinces.index(str(r["province"])) for r in sample], dtype=int)
    result = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": groups,
            "use_correction": True,
            "df_correction": True,
        },
        use_t=True,
    )
    return result, sample, names, provinces, years


def coefficient_record(
    family: str,
    component: str,
    outcome: str,
    specification: str,
    result,
    sample,
    names,
    exposure_name: str,
) -> dict[str, Any]:
    idx = names.index(exposure_name)
    ci = result.conf_int()[idx]
    return {
        "family": family,
        "component": component,
        "outcome": outcome,
        "specification": specification,
        "beta": float(result.params[idx]),
        "se_cluster": float(result.bse[idx]),
        "p_value": float(result.pvalues[idx]),
        "ci95_low": float(ci[0]),
        "ci95_high": float(ci[1]),
        "n": len(sample),
        "clusters": len({str(r["province"]) for r in sample}),
        "years": "|".join(str(y) for y in sorted({int(r["year"]) for r in sample})),
        "r_squared": float(result.rsquared),
    }


def fit_within_between(
    rows: Sequence[dict[str, Any]],
    outcome: str,
    exposure: str,
) -> dict[str, Any]:
    sample = _filter_rows(rows, outcome, [exposure])
    by_province: dict[str, list[float]] = defaultdict(list)
    for r in sample:
        by_province[str(r["province"])].append(float(r[exposure]))
    pmean = {p: float(np.mean(v)) for p, v in by_province.items()}
    within = np.asarray(
        [float(r[exposure]) - pmean[str(r["province"])] for r in sample],
        dtype=float,
    )
    between = np.asarray([pmean[str(r["province"])] for r in sample], dtype=float)
    y = np.asarray([float(r[outcome]) for r in sample], dtype=float)
    years = sorted({int(r["year"]) for r in sample})
    provinces = sorted(by_province)
    cols = [np.ones(len(sample)), within, between]
    names = ["const", "within", "between"]
    for year in years[1:]:
        cols.append(np.asarray([int(r["year"]) == year for r in sample], dtype=float))
        names.append("year:" + str(year))
    X = np.column_stack(cols)
    groups = np.asarray([provinces.index(str(r["province"])) for r in sample], dtype=int)
    result = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups, "use_correction": True, "df_correction": True},
        use_t=True,
    )
    ci = result.conf_int()
    iw = names.index("within")
    ib = names.index("between")
    return {
        "within_beta": float(result.params[iw]),
        "within_se": float(result.bse[iw]),
        "within_p": float(result.pvalues[iw]),
        "within_ci_low": float(ci[iw, 0]),
        "within_ci_high": float(ci[iw, 1]),
        "between_beta": float(result.params[ib]),
        "between_se": float(result.bse[ib]),
        "between_p": float(result.pvalues[ib]),
        "between_ci_low": float(ci[ib, 0]),
        "between_ci_high": float(ci[ib, 1]),
        "n": len(sample),
        "clusters": len(provinces),
    }


def _balanced_matrix(
    rows: Sequence[dict[str, Any]], outcome: str, exposure: str
) -> tuple[list[str], list[int], np.ndarray, np.ndarray]:
    sample = _filter_rows(rows, outcome, [exposure])
    provinces = sorted({str(r["province"]) for r in sample})
    years = sorted({int(r["year"]) for r in sample})
    by = {(str(r["province"]), int(r["year"])): r for r in sample}
    if len(by) != len(provinces) * len(years):
        raise ValueError(f"sample not balanced for permutation/influence: {outcome} {exposure}")
    y = np.asarray(
        [[float(by[(p, y_)][outcome]) for y_ in years] for p in provinces],
        dtype=float,
    )
    x = np.asarray(
        [[float(by[(p, y_)][exposure]) for y_ in years] for p in provinces],
        dtype=float,
    )
    return provinces, years, y, x


def _twoway_demean(a: np.ndarray) -> np.ndarray:
    return a - a.mean(axis=1, keepdims=True) - a.mean(axis=0, keepdims=True) + a.mean()


def _fe_beta_matrix(y: np.ndarray, x: np.ndarray) -> float:
    yt = _twoway_demean(y)
    xt = _twoway_demean(x)
    denom = float(np.sum(xt * xt))
    if denom <= 0:
        raise ValueError("zero FE exposure variation")
    return float(np.sum(xt * yt) / denom)


def permutation_pvalue(
    rows: Sequence[dict[str, Any]],
    outcome: str,
    exposure: str,
    rng: np.random.Generator,
    n_perm: int = N_PERMUTATIONS,
) -> tuple[float, float]:
    _, _, y, x = _balanced_matrix(rows, outcome, exposure)
    observed = _fe_beta_matrix(y, x)
    exceed = 0
    for _ in range(n_perm):
        perm = rng.permutation(x.shape[0])
        beta = _fe_beta_matrix(y, x[perm, :])
        if abs(beta) >= abs(observed):
            exceed += 1
    p = (exceed + 1) / (n_perm + 1)
    return observed, float(p)


def influence_summary(
    rows: Sequence[dict[str, Any]],
    outcome: str,
    exposure: str,
) -> dict[str, Any]:
    provinces, years, y, x = _balanced_matrix(rows, outcome, exposure)
    full = _fe_beta_matrix(y, x)
    province_betas = []
    for i in range(len(provinces)):
        keep = np.ones(len(provinces), dtype=bool)
        keep[i] = False
        province_betas.append(_fe_beta_matrix(y[keep, :], x[keep, :]))
    year_betas = []
    for j in range(len(years)):
        keep = np.ones(len(years), dtype=bool)
        keep[j] = False
        year_betas.append(_fe_beta_matrix(y[:, keep], x[:, keep]))
    return {
        "full_beta_demeaned": full,
        "leave_province_min": min(province_betas),
        "leave_province_max": max(province_betas),
        "leave_province_sign_flips": int(sum(np.sign(b) != np.sign(full) for b in province_betas)),
        "leave_year_min": min(year_betas),
        "leave_year_max": max(year_betas),
        "leave_year_sign_flips": int(sum(np.sign(b) != np.sign(full) for b in year_betas)),
    }


def mechanism_decomposition(
    rows: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Decompose governance association with revenue growth into exact margins.

    Because the outcomes obey accounting identities and every regression uses the
    same sample/design matrix, OLS linearity implies the corresponding
    coefficients must add exactly (up to floating-point tolerance).
    """
    outcomes = [
        ("aggregate_revenue", "dlog_revenue"),
        ("extensive_firm_stock", "dlog_active_firms"),
        ("intensive_revenue_per_firm", "dlog_revenue_per_firm"),
        ("firm_scale_workers_per_firm", "dlog_workers_per_firm"),
        ("labor_productivity_revenue_per_worker", "dlog_revenue_per_worker"),
    ]
    records: list[dict[str, Any]] = []
    qa: dict[str, Any] = {}
    for component in ("cstp4", "cstp5"):
        exposure = f"{component}_lag1_z"
        component_rows: list[dict[str, Any]] = []
        beta_by_outcome: dict[str, float] = {}
        for margin, outcome in outcomes:
            fitted = fit_fe(rows, outcome, [exposure])
            rec = coefficient_record(
                "DECOMP_transaction_cost",
                component,
                outcome,
                f"exact_growth_decomposition:{margin}",
                *fitted[:3],
                exposure,
            )
            rec["margin"] = margin
            component_rows.append(rec)
            beta_by_outcome[outcome] = float(rec["beta"])

        qvals = bh_adjust([float(r["p_value"]) for r in component_rows])
        for row, q in zip(component_rows, qvals):
            row["q_bh_decomposition"] = q

        total = beta_by_outcome["dlog_revenue"]
        extensive = beta_by_outcome["dlog_active_firms"]
        intensive = beta_by_outcome["dlog_revenue_per_firm"]
        scale = beta_by_outcome["dlog_workers_per_firm"]
        productivity = beta_by_outcome["dlog_revenue_per_worker"]
        residual_top = total - extensive - intensive
        residual_bottom = intensive - scale - productivity
        if max(abs(residual_top), abs(residual_bottom)) > 1e-9:
            raise ValueError(
                f"{component}: regression decomposition identity failed "
                f"top={residual_top} bottom={residual_bottom}"
            )
        for row in component_rows:
            row["aggregate_beta"] = total
            row["share_of_aggregate_beta"] = (
                None if abs(total) < 1e-12 else float(row["beta"]) / total
            )
            row["top_identity_residual"] = residual_top
            row["intensive_identity_residual"] = residual_bottom
        qa[component] = {
            "aggregate_beta": total,
            "extensive_beta": extensive,
            "intensive_beta": intensive,
            "scale_beta": scale,
            "productivity_beta": productivity,
            "top_identity_residual": residual_top,
            "intensive_identity_residual": residual_bottom,
        }
        records.extend(component_rows)
    return records, qa


def _write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError(f"no records for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for record in records:
        for key in record:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def run(core_csv: str | Path, entry_csv: str | Path, output_dir: str | Path) -> dict[str, Any]:
    panels = {
        "core": read_panel(core_csv),
        "entry": read_panel(entry_csv),
    }
    output_dir = Path(output_dir)
    rng = np.random.default_rng(RANDOM_SEED)

    primary_rows: list[dict[str, Any]] = []
    within_between_rows: list[dict[str, Any]] = []
    robustness_rows: list[dict[str, Any]] = []
    influence_rows: list[dict[str, Any]] = []
    permutation_rows: list[dict[str, Any]] = []
    decomposition_rows, decomposition_qa = mechanism_decomposition(panels["core"])

    for family, config in PRIMARY_HYPOTHESES.items():
        panel = panels[str(config["panel"])]
        family_primary = []
        for component, outcome in config["pairs"]:
            z = f"{component}_lag1_z"
            raw = f"{component}_lag1_raw"

            primary_fit = fit_fe(panel, outcome, [z])
            rec = coefficient_record(
                family, component, outcome, "primary_lag1_year_z",
                *primary_fit[:3], z
            )
            family_primary.append(rec)

            wb = fit_within_between(panel, outcome, z)
            wb.update({"family": family, "component": component, "outcome": outcome})
            within_between_rows.append(wb)

            raw_fit = fit_fe(panel, outcome, [raw])
            robustness_rows.append(coefficient_record(
                family, component, outcome, "lag1_raw_score",
                *raw_fit[:3], raw
            ))

            current = f"{component}_current_z"
            current_fit = fit_fe(panel, outcome, [current])
            robustness_rows.append(coefficient_record(
                family, component, outcome, "contemporaneous_year_z",
                *current_fit[:3], current
            ))

            strict_fit = fit_fe(panel, outcome, [z], exclude_years={2020, 2021, 2022})
            robustness_rows.append(coefficient_record(
                family, component, outcome, "strict_no_2020_2022",
                *strict_fit[:3], z
            ))

            lag2 = f"{component}_lag2_z"
            distributed = fit_fe(panel, outcome, [z, lag2])
            robustness_rows.append(coefficient_record(
                family, component, outcome, "distributed_lag1",
                *distributed[:3], z
            ))
            robustness_rows.append(coefficient_record(
                family, component, outcome, "distributed_lag2",
                *distributed[:3], lag2
            ))

            lead = f"{component}_lead1_z"
            lead_fit = fit_fe(panel, outcome, [lead])
            robustness_rows.append(coefficient_record(
                family, component, outcome, "future_lead_placebo",
                *lead_fit[:3], lead
            ))

            influence = influence_summary(panel, outcome, z)
            influence.update({"family": family, "component": component, "outcome": outcome})
            influence_rows.append(influence)

            observed, perm_p = permutation_pvalue(panel, outcome, z, rng)
            permutation_rows.append({
                "family": family,
                "component": component,
                "outcome": outcome,
                "observed_beta": observed,
                "permutation_p_two_sided": perm_p,
                "n_permutations": N_PERMUTATIONS,
            })

        qvals = bh_adjust([float(r["p_value"]) for r in family_primary])
        for row, q in zip(family_primary, qvals):
            row["q_bh_family"] = q
            primary_rows.append(row)

        by_outcome: dict[str, list[str]] = defaultdict(list)
        for component, outcome in config["pairs"]:
            if component not in by_outcome[outcome]:
                by_outcome[outcome].append(component)
        for outcome, components in by_outcome.items():
            exposures = [f"{component}_lag1_z" for component in components]
            joint = fit_fe(panel, outcome, exposures)
            for component, exposure in zip(components, exposures):
                robustness_rows.append(coefficient_record(
                    family, component, outcome, "joint_family_lag1_year_z",
                    *joint[:3], exposure
                ))

    primary_path = output_dir / "SR1_primary_hypotheses.csv"
    wb_path = output_dir / "SR1_within_between.csv"
    robust_path = output_dir / "SR1_robustness.csv"
    influence_path = output_dir / "SR1_influence.csv"
    perm_path = output_dir / "SR1_permutation.csv"
    decomp_path = output_dir / "SR1_exact_growth_decomposition.csv"
    _write_csv(primary_path, primary_rows)
    _write_csv(wb_path, within_between_rows)
    _write_csv(robust_path, robustness_rows)
    _write_csv(influence_path, influence_rows)
    _write_csv(perm_path, permutation_rows)
    _write_csv(decomp_path, decomposition_rows)

    significant = [
        r for r in primary_rows if float(r["q_bh_family"]) < 0.05
    ]
    metadata = {
        "status": "COMPLETED",
        "random_seed": RANDOM_SEED,
        "n_permutations": N_PERMUTATIONS,
        "primary_test_count": len(primary_rows),
        "primary_family_counts": {
            family: len(config["pairs"])
            for family, config in PRIMARY_HYPOTHESES.items()
        },
        "primary_q_lt_0_05_count": len(significant),
        "exact_growth_decomposition": decomposition_qa,
        "primary_q_lt_0_05": [
            {
                "family": r["family"],
                "component": r["component"],
                "outcome": r["outcome"],
                "beta": r["beta"],
                "q": r["q_bh_family"],
            }
            for r in significant
        ],
        "interpretation_rule": (
            "Primary evidence requires family-BH q<0.05 plus coherent robustness; "
            "isolated nominal p-values are not publication claims."
        ),
    }
    meta_path = output_dir / "SR1_metadata.json"
    meta_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--core", default="artifacts/sr1/processed/mechanism_panel_2015_2023.csv")
    p.add_argument("--entry", default="artifacts/sr1/processed/entry_panel_2018_2024.csv")
    p.add_argument("--output-dir", default="artifacts/sr1/results")
    return p


def main() -> int:
    args = parser().parse_args()
    result = run(args.core, args.entry, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
