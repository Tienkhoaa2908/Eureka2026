from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import statsmodels.api as sm
import statsmodels

CANONICAL_PANEL_SHA256 = "a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd"
COMPONENTS = tuple(f"cstp{i}_lag1" for i in range(1, 11))
COMPONENT_LABELS = {
    "cstp1_lag1": "Chi phí gia nhập thị trường",
    "cstp2_lag1": "Tiếp cận đất đai",
    "cstp3_lag1": "Tính minh bạch",
    "cstp4_lag1": "Chi phí thời gian",
    "cstp5_lag1": "Chi phí không chính thức",
    "cstp6_lag1": "Cạnh tranh bình đẳng",
    "cstp7_lag1": "Tính năng động",
    "cstp8_lag1": "Dịch vụ hỗ trợ doanh nghiệp",
    "cstp9_lag1": "Đào tạo lao động",
    "cstp10_lag1": "Thiết chế pháp lý & ANTT",
}


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def benjamini_hochberg(pvalues: Sequence[float]) -> list[float]:
    p = np.asarray(pvalues, dtype=float)
    if p.ndim != 1 or len(p) == 0:
        raise ValueError("pvalues must be a non-empty 1D sequence")
    if np.any((p < 0) | (p > 1) | ~np.isfinite(p)):
        raise ValueError("pvalues must be finite and in [0, 1]")
    n = len(p)
    order = np.argsort(p)
    q = np.ones(n, dtype=float)
    running = 1.0
    for pos in range(n - 1, -1, -1):
        idx = order[pos]
        rank = pos + 1
        running = min(running, p[idx] * n / rank)
        q[idx] = running
    return q.tolist()


def _read_panel(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("canonical panel is empty")
    required = {"Tinh", "Nam", "Doanh_thu_ty_dong", *COMPONENTS}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"canonical panel missing columns: {sorted(missing)}")
    return rows


def _analysis_rows(rows: Iterable[dict[str, str]], *, exclude_covid: bool = False) -> list[dict[str, str]]:
    sample = []
    for row in rows:
        year = int(row["Nam"])
        if year < 2014 or year > 2024:
            continue
        if exclude_covid and year in {2020, 2021}:
            continue
        if any(row[c] == "" for c in COMPONENTS):
            continue
        sample.append(row)
    expected_n = 567 if exclude_covid else 693
    expected_years = 9 if exclude_covid else 11
    provinces = {r["Tinh"] for r in sample}
    years = {int(r["Nam"]) for r in sample}
    if len(sample) != expected_n or len(provinces) != 63 or len(years) != expected_years:
        raise ValueError(
            f"analysis sample mismatch: n={len(sample)}, provinces={len(provinces)}, years={len(years)}"
        )
    return sample


def standardization_stats(rows: Sequence[dict[str, str]]) -> tuple[np.ndarray, np.ndarray]:
    raw = np.asarray([[float(r[c]) for c in COMPONENTS] for r in rows], dtype=float)
    means = raw.mean(axis=0)
    sds = raw.std(axis=0, ddof=1)
    if np.any(~np.isfinite(means)) or np.any(~np.isfinite(sds)) or np.any(sds <= 0):
        raise ValueError("invalid standardization statistics")
    return means, sds


def _outcome(rows: Sequence[dict[str, str]], all_rows: Sequence[dict[str, str]], name: str) -> np.ndarray:
    if name == "log_revenue":
        return np.log(np.asarray([float(r["Doanh_thu_ty_dong"]) for r in rows], dtype=float))
    if name != "log_revenue_change":
        raise ValueError(f"unknown outcome: {name}")
    revenue = {(r["Tinh"], int(r["Nam"])): float(r["Doanh_thu_ty_dong"]) for r in all_rows}
    values = []
    for r in rows:
        key_prev = (r["Tinh"], int(r["Nam"]) - 1)
        if key_prev not in revenue:
            raise ValueError(f"missing previous revenue for {r['Tinh']} {r['Nam']}")
        values.append(math.log(float(r["Doanh_thu_ty_dong"])) - math.log(revenue[key_prev]))
    return np.asarray(values, dtype=float)


def _design(
    rows: Sequence[dict[str, str]],
    means: np.ndarray,
    sds: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, list[str], list[int]]:
    provinces = sorted({r["Tinh"] for r in rows})
    years = sorted({int(r["Nam"]) for r in rows})
    raw = np.asarray([[float(r[c]) for c in COMPONENTS] for r in rows], dtype=float)
    z = (raw - means) / sds
    columns = [np.ones(len(rows), dtype=float), z]
    names = ["const", *COMPONENTS]
    for province in provinces[1:]:
        columns.append(np.asarray([r["Tinh"] == province for r in rows], dtype=float))
        names.append(f"province:{province}")
    for year in years[1:]:
        columns.append(np.asarray([int(r["Nam"]) == year for r in rows], dtype=float))
        names.append(f"year:{year}")
    X = np.column_stack(columns)
    groups = np.asarray([provinces.index(r["Tinh"]) for r in rows], dtype=int)
    return X, groups, names, years


def _fit(
    rows: Sequence[dict[str, str]],
    all_rows: Sequence[dict[str, str]],
    outcome_name: str,
    means: np.ndarray,
    sds: np.ndarray,
):
    X, groups, names, years = _design(rows, means, sds)
    y = _outcome(rows, all_rows, outcome_name)
    rank = int(np.linalg.matrix_rank(X))
    if rank != X.shape[1]:
        raise ValueError(f"design matrix is rank-deficient: rank={rank}, columns={X.shape[1]}")
    result = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups, "use_correction": True, "df_correction": True},
        use_t=True,
    )
    return result, X, y, groups, names, years


def _coefficient_rows(
    spec: str,
    rows: Sequence[dict[str, str]],
    result,
    X: np.ndarray,
    groups: np.ndarray,
    outcome_name: str,
) -> list[dict[str, object]]:
    p = result.pvalues[1:11]
    q = benjamini_hochberg(p)
    ci = result.conf_int()[1:11]
    out = []
    for i, component in enumerate(COMPONENTS):
        beta = float(result.params[i + 1])
        out.append({
            "spec": spec,
            "outcome": outcome_name,
            "component": component,
            "component_label": COMPONENT_LABELS[component],
            "beta_std": beta,
            "pct_equivalent": 100.0 * (math.exp(beta) - 1.0),
            "se_cluster": float(result.bse[i + 1]),
            "t_stat": float(result.tvalues[i + 1]),
            "p_value": float(result.pvalues[i + 1]),
            "q_bh": float(q[i]),
            "ci95_low": float(ci[i, 0]),
            "ci95_high": float(ci[i, 1]),
            "n": len(rows),
            "clusters": len(set(groups.tolist())),
            "df_inference": int(getattr(result, "df_resid_inference", len(set(groups.tolist())) - 1)),
            "r_squared": float(result.rsquared),
            "condition_number": float(np.linalg.cond(X)),
        })
    return out


def _leave_one_province_out(
    rows: Sequence[dict[str, str]],
    all_rows: Sequence[dict[str, str]],
    outcome_name: str,
    means: np.ndarray,
    sds: np.ndarray,
    full_beta: np.ndarray,
) -> list[dict[str, object]]:
    provinces = sorted({r["Tinh"] for r in rows})
    coefs = []
    for province in provinces:
        reduced = [r for r in rows if r["Tinh"] != province]
        result, _, _, _, _, _ = _fit(reduced, all_rows, outcome_name, means, sds)
        coefs.append(result.params[1:11])
    matrix = np.vstack(coefs)
    output = []
    for i, component in enumerate(COMPONENTS):
        vals = matrix[:, i]
        output.append({
            "outcome": outcome_name,
            "component": component,
            "component_label": COMPONENT_LABELS[component],
            "full_beta": float(full_beta[i]),
            "loo_min_beta": float(vals.min()),
            "loo_max_beta": float(vals.max()),
            "max_abs_delta": float(np.max(np.abs(vals - full_beta[i]))),
            "sign_flip_count": int(np.sum(np.sign(vals) != np.sign(full_beta[i]))),
            "provinces_dropped": len(provinces),
        })
    return output


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_baseline(
    input_csv: str | Path,
    output_dir: str | Path,
    expected_sha256: str = CANONICAL_PANEL_SHA256,
) -> dict[str, object]:
    input_csv = Path(input_csv)
    output_dir = Path(output_dir)
    actual_sha = sha256_file(input_csv)
    if expected_sha256 and actual_sha != expected_sha256:
        raise ValueError(
            f"canonical panel checksum mismatch: expected {expected_sha256}, found {actual_sha}"
        )

    all_rows = _read_panel(input_csv)
    full = _analysis_rows(all_rows, exclude_covid=False)
    no_covid = _analysis_rows(all_rows, exclude_covid=True)
    full_means, full_sds = standardization_stats(full)
    nc_means, nc_sds = standardization_stats(no_covid)

    coefficient_rows: list[dict[str, object]] = []
    influence_rows: list[dict[str, object]] = []
    model_meta: dict[str, object] = {}

    for spec, sample, means, sds in (
        ("full", full, full_means, full_sds),
        ("no_covid_2020_2021", no_covid, nc_means, nc_sds),
    ):
        for outcome_name in ("log_revenue", "log_revenue_change"):
            result, X, y, groups, names, years = _fit(
                sample, all_rows, outcome_name, means, sds
            )
            coefficient_rows.extend(
                _coefficient_rows(spec, sample, result, X, groups, outcome_name)
            )
            residuals = np.asarray(result.resid, dtype=float)
            key = f"{spec}:{outcome_name}"
            model_meta[key] = {
                "n": len(sample),
                "clusters": len(set(groups.tolist())),
                "years": years,
                "design_columns": X.shape[1],
                "design_rank": int(np.linalg.matrix_rank(X)),
                "r_squared": float(result.rsquared),
                "adjusted_r_squared": float(result.rsquared_adj),
                "condition_number": float(np.linalg.cond(X)),
                "max_abs_residual": float(np.max(np.abs(residuals))),
                "rmse_residual": float(np.sqrt(np.mean(residuals ** 2))),
                "cluster_df_inference": int(
                    getattr(result, "df_resid_inference", 62)
                ),
            }
            if spec == "full":
                influence_rows.extend(
                    _leave_one_province_out(
                        sample,
                        all_rows,
                        outcome_name,
                        full_means,
                        full_sds,
                        np.asarray(result.params[1:11], dtype=float),
                    )
                )

    scaling_rows = []
    for spec, means, sds, sample in (
        ("full", full_means, full_sds, full),
        ("no_covid_2020_2021", nc_means, nc_sds, no_covid),
    ):
        for i, component in enumerate(COMPONENTS):
            scaling_rows.append({
                "spec": spec,
                "component": component,
                "component_label": COMPONENT_LABELS[component],
                "mean": float(means[i]),
                "sd_sample": float(sds[i]),
                "n": len(sample),
            })

    coeff_path = output_dir / "STAT-BASELINE-01_coefficients.csv"
    influence_path = output_dir / "STAT-BASELINE-01_influence.csv"
    scaling_path = output_dir / "STAT-BASELINE-01_scaling.csv"
    metadata_path = output_dir / "STAT-BASELINE-01_metadata.json"
    _write_csv(coeff_path, coefficient_rows)
    _write_csv(influence_path, influence_rows)
    _write_csv(scaling_path, scaling_rows)

    metadata: dict[str, object] = {
        "status": "PASS",
        "input_csv_sha256": actual_sha,
        "numpy_version": np.__version__,
        "statsmodels_version": statsmodels.__version__,
        "standardization": (
            "sample mean and sample SD (ddof=1), separately for full and no-COVID samples"
        ),
        "covariance": (
            "province-clustered, small-sample correction, t inference with cluster df correction"
        ),
        "fdr": (
            "Benjamini-Hochberg within the 10 component tests for each model specification/outcome"
        ),
        "models": model_meta,
        "outputs": {
            "coefficients": coeff_path.name,
            "influence": influence_path.name,
            "scaling": scaling_path.name,
        },
    }
    metadata["output_sha256"] = {
        coeff_path.name: sha256_file(coeff_path),
        influence_path.name: sha256_file(influence_path),
        scaling_path.name: sha256_file(scaling_path),
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run the prespecified Euréka 2026 two-way FE baseline."
    )
    p.add_argument("--input", default="data/processed/panel.csv")
    p.add_argument("--output-dir", default="artifacts/results")
    p.add_argument("--expected-sha256", default=CANONICAL_PANEL_SHA256)
    return p


def main() -> int:
    args = _parser().parse_args()
    metadata = run_baseline(args.input, args.output_dir, args.expected_sha256)
    print(json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
