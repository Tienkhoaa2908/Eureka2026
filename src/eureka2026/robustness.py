from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Sequence

import numpy as np
import statsmodels.api as sm
from scipy.stats import norm

CANONICAL_PANEL_SHA256 = "a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd"
LAG10 = tuple(f"cstp{i}_lag1" for i in range(1, 11))
CUR10 = tuple(f"cstp{i}" for i in range(1, 11))
LAG9 = tuple(f"cstp{i}_lag1" for i in (1, 2, 3, 4, 5, 7, 8, 9, 10))


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_panel(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 945:
        raise ValueError(f"expected 945 rows, found {len(rows)}")
    return rows


def bh(pvals: Sequence[float]) -> list[float]:
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    q = np.ones(n)
    running = 1.0
    for pos in range(n - 1, -1, -1):
        idx = order[pos]
        running = min(running, p[idx] * n / (pos + 1))
        q[idx] = running
    return q.tolist()


def add_history(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by = {(r["Tinh"], int(r["Nam"])): r for r in rows}
    out = []
    for r in rows:
        p = r["Tinh"]
        y = int(r["Nam"])
        rev = float(r["Doanh_thu_ty_dong"])
        prev = by.get((p, y - 1))
        prev2 = by.get((p, y - 2))
        nxt = by.get((p, y + 1))
        x: dict[str, object] = dict(r)
        x["Nam"] = y
        x["revenue"] = rev
        x["log_revenue"] = math.log(rev)
        x["log_revenue_change"] = (
            None if prev is None
            else math.log(rev) - math.log(float(prev["Doanh_thu_ty_dong"]))
        )
        x["cstp5_lag2"] = (
            None if prev2 is None or prev2["cstp5"] == ""
            else float(prev2["cstp5"])
        )
        x["cstp5_lead1"] = (
            None if nxt is None or nxt["cstp5"] == ""
            else float(nxt["cstp5"])
        )
        out.append(x)
    return out


def sample(
    rows: Sequence[dict[str, object]],
    years: set[int],
    predictors: Sequence[str],
) -> list[dict[str, object]]:
    output = []
    for r in rows:
        if int(r["Nam"]) not in years or r["log_revenue_change"] is None:
            continue
        if any(r.get(c) in (None, "") for c in predictors):
            continue
        output.append(r)
    return output


def design(
    rows: Sequence[dict[str, object]],
    predictors: Sequence[str],
    scaling: tuple[np.ndarray, np.ndarray] | None = None,
):
    raw = np.asarray([[float(r[c]) for c in predictors] for r in rows], float)
    if scaling is None:
        means = raw.mean(0)
        sds = raw.std(0, ddof=1)
    else:
        means, sds = scaling
    z = (raw - means) / sds
    provinces = sorted({str(r["Tinh"]) for r in rows})
    years = sorted({int(r["Nam"]) for r in rows})
    cols = [np.ones(len(rows)), z]
    names = ["const", *predictors]
    for province in provinces[1:]:
        cols.append(np.asarray([r["Tinh"] == province for r in rows], float))
        names.append("province:" + province)
    for year in years[1:]:
        cols.append(np.asarray([int(r["Nam"]) == year for r in rows], float))
        names.append("year:" + str(year))
    X = np.column_stack(cols)
    groups = np.asarray(
        [provinces.index(str(r["Tinh"])) for r in rows], int
    )
    return X, groups, names, (means, sds), provinces, years


def fit(
    rows: Sequence[dict[str, object]],
    predictors: Sequence[str],
    outcome: str = "log_revenue_change",
    scaling=None,
    winsor=None,
):
    X, groups, names, sc, provinces, years = design(
        rows, predictors, scaling
    )
    y = np.asarray([float(r[outcome]) for r in rows], float)
    if winsor is not None:
        lo, hi = np.quantile(y, [winsor, 1 - winsor])
        y = np.clip(y, lo, hi)
    result = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": groups,
            "use_correction": True,
            "df_correction": True,
        },
        use_t=True,
    )
    return result, X, y, groups, names, sc, provinces, years


def component_table(spec: str, rows, predictors, result, names):
    indices = [names.index(c) for c in predictors]
    pvals = [float(result.pvalues[i]) for i in indices]
    qvals = bh(pvals)
    ci = result.conf_int()
    out = []
    for c, idx, q in zip(predictors, indices, qvals):
        out.append({
            "spec": spec,
            "component": c,
            "beta_std": float(result.params[idx]),
            "se_cluster": float(result.bse[idx]),
            "p_value": float(result.pvalues[idx]),
            "q_bh": float(q),
            "ci95_low": float(ci[idx, 0]),
            "ci95_high": float(ci[idx, 1]),
            "n": len(rows),
            "clusters": len({str(r["Tinh"]) for r in rows}),
            "r_squared": float(result.rsquared),
        })
    return out


def pesaran_cd(rows, residuals):
    provinces = sorted({str(r["Tinh"]) for r in rows})
    years = sorted({int(r["Nam"]) for r in rows})
    by = {
        (str(r["Tinh"]), int(r["Nam"])): float(e)
        for r, e in zip(rows, residuals)
    }
    matrix = np.asarray(
        [[by[(province, year)] for year in years] for province in provinces],
        float,
    )
    corr = np.corrcoef(matrix)
    vals = corr[np.triu_indices(len(provinces), 1)]
    n = len(provinces)
    t = len(years)
    cd = math.sqrt(2 * t / (n * (n - 1))) * float(vals.sum())
    p = 2 * (1 - norm.cdf(abs(cd)))
    return {
        "n_entities": n,
        "t_periods": t,
        "mean_pairwise_residual_corr": float(vals.mean()),
        "pesaran_cd": cd,
        "asymptotic_p_value": float(p),
    }


def write_csv(path, records):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(records[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(records)


def run(
    input_csv: str | Path,
    output_dir: str | Path,
    expected_sha256=CANONICAL_PANEL_SHA256,
):
    input_csv = Path(input_csv)
    output_dir = Path(output_dir)
    actual = sha256_file(input_csv)
    if expected_sha256 and actual != expected_sha256:
        raise ValueError("canonical checksum mismatch")
    rows = add_history(read_panel(input_csv))

    full = sample(rows, set(range(2014, 2025)), LAG10)
    if len(full) != 693:
        raise ValueError(len(full))
    full_raw = np.asarray(
        [[float(r[c]) for c in LAG10] for r in full]
    )
    full_scaling = (full_raw.mean(0), full_raw.std(0, ddof=1))
    base, _, _, _, _, _, _, _ = fit(
        full, LAG10, scaling=full_scaling
    )

    coeff = []
    targeted = []
    year_loo = []
    region_loo = []

    strict = sample(
        rows, set(range(2014, 2020)) | {2023, 2024}, LAG10
    )
    strict_res = fit(strict, LAG10, scaling=full_scaling)
    coeff += component_table(
        "strict_no_covid_2020_2022",
        strict, LAG10, strict_res[0], strict_res[4],
    )

    cont = sample(rows, set(range(2013, 2025)), CUR10)
    cont_res = fit(cont, CUR10)
    coeff += component_table(
        "contemporaneous_10", cont, CUR10, cont_res[0], cont_res[4]
    )

    long9 = sample(rows, set(range(2011, 2025)), LAG9)
    long_res = fit(long9, LAG9)
    coeff += component_table(
        "long_2011_2024_lag9", long9, LAG9, long_res[0], long_res[4]
    )

    winsor_res = fit(
        full, LAG10, scaling=full_scaling, winsor=0.01
    )
    coeff += component_table(
        "winsorized_outcome_1pct",
        full, LAG10, winsor_res[0], winsor_res[4],
    )

    single = fit(
        full,
        ("cstp5_lag1",),
        scaling=(
            np.asarray([full_scaling[0][4]]),
            np.asarray([full_scaling[1][4]]),
        ),
    )
    idx = single[4].index("cstp5_lag1")
    ci = single[0].conf_int()[idx]
    targeted.append({
        "check": "single_component_lag1",
        "term": "cstp5_lag1",
        "beta_std": float(single[0].params[idx]),
        "se_cluster": float(single[0].bse[idx]),
        "p_value": float(single[0].pvalues[idx]),
        "ci95_low": float(ci[0]),
        "ci95_high": float(ci[1]),
        "n": len(full),
    })

    dlag = sample(
        rows, set(range(2015, 2025)),
        ("cstp5_lag1", "cstp5_lag2"),
    )
    dres = fit(dlag, ("cstp5_lag1", "cstp5_lag2"))
    for term in ("cstp5_lag1", "cstp5_lag2"):
        idx = dres[4].index(term)
        ci = dres[0].conf_int()[idx]
        targeted.append({
            "check": "distributed_lag",
            "term": term,
            "beta_std": float(dres[0].params[idx]),
            "se_cluster": float(dres[0].bse[idx]),
            "p_value": float(dres[0].pvalues[idx]),
            "ci95_low": float(ci[0]),
            "ci95_high": float(ci[1]),
            "n": len(dlag),
        })

    lead = sample(
        rows, set(range(2014, 2024)), ("cstp5_lead1",)
    )
    lead_res = fit(lead, ("cstp5_lead1",))
    idx = lead_res[4].index("cstp5_lead1")
    ci = lead_res[0].conf_int()[idx]
    targeted.append({
        "check": "future_lead_placebo",
        "term": "cstp5_lead1",
        "beta_std": float(lead_res[0].params[idx]),
        "se_cluster": float(lead_res[0].bse[idx]),
        "p_value": float(lead_res[0].pvalues[idx]),
        "ci95_low": float(ci[0]),
        "ci95_high": float(ci[1]),
        "n": len(lead),
    })

    for year in range(2014, 2025):
        sub = [r for r in full if int(r["Nam"]) != year]
        result = fit(sub, LAG10, scaling=full_scaling)
        idx = result[4].index("cstp5_lag1")
        year_loo.append({
            "dropped_year": year,
            "beta_std": float(result[0].params[idx]),
            "se_cluster": float(result[0].bse[idx]),
            "p_value": float(result[0].pvalues[idx]),
            "n": len(sub),
        })

    for region in sorted({str(r["Vung"]) for r in full}):
        sub = [r for r in full if str(r["Vung"]) != region]
        result = fit(sub, LAG10, scaling=full_scaling)
        idx = result[4].index("cstp5_lag1")
        region_loo.append({
            "dropped_region": region,
            "beta_std": float(result[0].params[idx]),
            "se_cluster": float(result[0].bse[idx]),
            "p_value": float(result[0].pvalues[idx]),
            "n": len(sub),
            "clusters": len({str(r["Tinh"]) for r in sub}),
        })

    cd = pesaran_cd(full, base.resid)

    coeff_path = output_dir / "ROBUSTNESS-01_coefficients.csv"
    target_path = output_dir / "ROBUSTNESS-01_cstp5_targeted.csv"
    loo_path = output_dir / "ROBUSTNESS-01_year_loo.csv"
    region_path = output_dir / "ROBUSTNESS-01_region_loo.csv"
    write_csv(coeff_path, coeff)
    write_csv(target_path, targeted)
    write_csv(loo_path, year_loo)
    write_csv(region_path, region_loo)

    meta = {
        "status": "PASS",
        "input_sha256": actual,
        "specifications": {
            "strict_no_covid_2020_2022": {
                "years": "2014-2019,2023-2024", "n": len(strict)
            },
            "contemporaneous_10": {
                "years": "2013-2024", "n": len(cont)
            },
            "long_2011_2024_lag9": {
                "years": "2011-2024", "n": len(long9)
            },
            "winsorized_outcome_1pct": {
                "years": "2014-2024", "n": len(full)
            },
            "distributed_lag": {
                "years": "2015-2024", "n": len(dlag)
            },
            "future_lead_placebo": {
                "years": "2014-2023", "n": len(lead)
            },
        },
        "pesaran_cd_full_change": cd,
        "output_sha256": {},
    }
    for path in (coeff_path, target_path, loo_path, region_path):
        meta["output_sha256"][path.name] = sha256_file(path)

    meta_path = output_dir / "ROBUSTNESS-01_metadata.json"
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    meta["output_sha256"][meta_path.name] = sha256_file(meta_path)
    return meta


def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/processed/panel.csv")
    p.add_argument("--output-dir", default="artifacts/results")
    return p


def main():
    args = parser().parse_args()
    print(json.dumps(
        run(args.input, args.output_dir),
        ensure_ascii=False, sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
