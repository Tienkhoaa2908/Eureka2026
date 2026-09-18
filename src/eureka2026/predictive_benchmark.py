from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import xgboost as xgb
from xgboost import XGBRegressor

CANONICAL_PANEL_SHA256 = "a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd"
RANDOM_SEED = 20260918
OUTER_TEST_YEARS = (2019, 2020, 2021, 2022, 2023, 2024)
START_YEAR = 2014
PCI_FEATURES = tuple(f"cstp{i}_lag1" for i in range(1, 11))
PCI_LABELS = {
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
OUTCOMES = ("log_revenue_change", "log_revenue")


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_panel(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    required = {"Tinh", "Nam", "Doanh_thu_ty_dong", *PCI_FEATURES}
    if not rows:
        raise ValueError("canonical panel is empty")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"canonical panel missing columns: {sorted(missing)}")
    return rows


def _model_rows(rows: Sequence[dict[str, str]]) -> list[dict[str, object]]:
    revenue = {(r["Tinh"], int(r["Nam"])): float(r["Doanh_thu_ty_dong"]) for r in rows}
    output: list[dict[str, object]] = []
    for r in rows:
        year = int(r["Nam"])
        if year < START_YEAR or year > max(OUTER_TEST_YEARS):
            continue
        if any(r[c] == "" for c in PCI_FEATURES):
            continue
        province = r["Tinh"]
        rev_t = float(r["Doanh_thu_ty_dong"])
        rev_t1 = revenue.get((province, year - 1))
        rev_t2 = revenue.get((province, year - 2))
        if rev_t1 is None or rev_t2 is None:
            raise ValueError(f"missing revenue history for {province} {year}")
        row: dict[str, object] = {
            "province": province,
            "year": year,
            "trend": float(year - START_YEAR),
            "lag_log_revenue": math.log(rev_t1),
            "lag_log_revenue_change": math.log(rev_t1) - math.log(rev_t2),
            "log_revenue": math.log(rev_t),
            "log_revenue_change": math.log(rev_t) - math.log(rev_t1),
        }
        for c in PCI_FEATURES:
            row[c] = float(r[c])
        output.append(row)

    provinces = {str(r["province"]) for r in output}
    years = {int(r["year"]) for r in output}
    if len(output) != 693 or len(provinces) != 63 or years != set(range(2014, 2025)):
        raise ValueError(
            f"predictive sample mismatch: n={len(output)}, provinces={len(provinces)}, years={sorted(years)}"
        )
    return output


def outer_folds(rows: Sequence[Mapping[str, object]]) -> list[tuple[list[int], list[int], int]]:
    folds = []
    for test_year in OUTER_TEST_YEARS:
        train = [i for i, r in enumerate(rows) if START_YEAR <= int(r["year"]) < test_year]
        test = [i for i, r in enumerate(rows) if int(r["year"]) == test_year]
        if len(test) != 63:
            raise ValueError(f"outer test year {test_year}: expected 63 rows, found {len(test)}")
        expected_train = 63 * (test_year - START_YEAR)
        if len(train) != expected_train:
            raise ValueError(
                f"outer train ending {test_year-1}: expected {expected_train}, found {len(train)}"
            )
        if max(int(rows[i]["year"]) for i in train) >= test_year:
            raise ValueError("temporal leakage in outer fold")
        folds.append((train, test, test_year))
    return folds


def inner_folds(rows: Sequence[Mapping[str, object]], outer_train_indices: Sequence[int]) -> list[tuple[list[int], list[int], int]]:
    train_years = sorted({int(rows[i]["year"]) for i in outer_train_indices})
    if len(train_years) < 4:
        raise ValueError("need at least four outer-training years for inner temporal tuning")
    validation_years = train_years[3:]
    validation_years = validation_years[-2:]
    folds = []
    outer_set = set(outer_train_indices)
    for val_year in validation_years:
        train = [i for i in outer_train_indices if int(rows[i]["year"]) < val_year]
        val = [i for i in outer_train_indices if int(rows[i]["year"]) == val_year]
        if len(val) != 63 or not set(train).issubset(outer_set) or not set(val).issubset(outer_set):
            raise ValueError("invalid inner fold membership")
        if max(int(rows[i]["year"]) for i in train) >= val_year:
            raise ValueError("temporal leakage in inner fold")
        folds.append((train, val, val_year))
    return folds


def _raw_x(rows: Sequence[Mapping[str, object]], indices: Sequence[int], include_pci: bool) -> np.ndarray:
    data = []
    for i in indices:
        r = rows[i]
        values: list[object] = [
            str(r["province"]),
            float(r["lag_log_revenue"]),
            float(r["lag_log_revenue_change"]),
            float(r["trend"]),
        ]
        if include_pci:
            values.extend(float(r[c]) for c in PCI_FEATURES)
        data.append(values)
    return np.asarray(data, dtype=object)


def _y(rows: Sequence[Mapping[str, object]], indices: Sequence[int], outcome: str) -> np.ndarray:
    if outcome not in OUTCOMES:
        raise ValueError(f"unknown outcome: {outcome}")
    return np.asarray([float(rows[i][outcome]) for i in indices], dtype=float)


def _preprocessor(include_pci: bool) -> ColumnTransformer:
    numeric_cols = list(range(1, 14 if include_pci else 4))
    return ColumnTransformer(
        transformers=[
            ("province", OneHotEncoder(handle_unknown="ignore", sparse_output=False), [0]),
            ("numeric", StandardScaler(), numeric_cols),
        ],
        remainder="drop",
        sparse_threshold=0.0,
    )


def _pipeline(model_name: str, include_pci: bool, params: Mapping[str, object]) -> Pipeline:
    if model_name == "elastic_net":
        model = ElasticNet(
            alpha=float(params["alpha"]),
            l1_ratio=float(params["l1_ratio"]),
            fit_intercept=True,
            max_iter=10000,
            tol=1e-6,
            selection="cyclic",
            random_state=RANDOM_SEED,
        )
    elif model_name == "random_forest":
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=params["max_depth"],
            min_samples_leaf=int(params["min_samples_leaf"]),
            max_features=params["max_features"],
            bootstrap=True,
            random_state=RANDOM_SEED,
            n_jobs=1,
        )
    elif model_name == "xgboost":
        model = XGBRegressor(
            objective="reg:squarederror",
            n_estimators=120,
            max_depth=int(params["max_depth"]),
            learning_rate=float(params["learning_rate"]),
            min_child_weight=float(params["min_child_weight"]),
            subsample=0.9,
            colsample_bytree=0.9,
            reg_alpha=0.0,
            reg_lambda=5.0,
            gamma=0.0,
            random_state=RANDOM_SEED,
            n_jobs=1,
            tree_method="hist",
            verbosity=0,
        )
    else:
        raise ValueError(model_name)
    return Pipeline([("prep", _preprocessor(include_pci)), ("model", model)])


def parameter_grid(model_name: str) -> list[dict[str, object]]:
    if model_name == "elastic_net":
        return [
            {"alpha": a, "l1_ratio": l}
            for a, l in itertools.product((0.001, 0.01, 0.1), (0.1, 0.9))
        ]
    if model_name == "random_forest":
        return [
            {"max_depth": 3, "min_samples_leaf": 10, "max_features": 0.7},
            {"max_depth": 6, "min_samples_leaf": 5, "max_features": 0.7},
            {"max_depth": None, "min_samples_leaf": 5, "max_features": "sqrt"},
        ]
    if model_name == "xgboost":
        return [
            {"max_depth": d, "learning_rate": lr, "min_child_weight": mcw}
            for d, lr, mcw in itertools.product((2, 3), (0.03, 0.08), (5.0,))
        ]
    raise ValueError(model_name)


def _stable_param_key(params: Mapping[str, object]) -> str:
    return json.dumps(params, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class TuneResult:
    best_params: dict[str, object]
    mean_inner_mae: float
    inner_fold_mae: tuple[float, ...]


def tune_model(
    rows: Sequence[Mapping[str, object]],
    outer_train_indices: Sequence[int],
    outcome: str,
    model_name: str,
    include_pci: bool,
) -> TuneResult:
    folds = inner_folds(rows, outer_train_indices)
    scored: list[tuple[float, str, dict[str, object], tuple[float, ...]]] = []
    for params in parameter_grid(model_name):
        fold_mae = []
        for train_idx, val_idx, _ in folds:
            pipe = _pipeline(model_name, include_pci, params)
            pipe.fit(_raw_x(rows, train_idx, include_pci), _y(rows, train_idx, outcome))
            pred = pipe.predict(_raw_x(rows, val_idx, include_pci))
            fold_mae.append(float(mean_absolute_error(_y(rows, val_idx, outcome), pred)))
        mean_mae = float(np.mean(fold_mae))
        scored.append((mean_mae, _stable_param_key(params), dict(params), tuple(fold_mae)))
    scored.sort(key=lambda x: (x[0], x[1]))
    best = scored[0]
    return TuneResult(best_params=best[2], mean_inner_mae=best[0], inner_fold_mae=best[3])


def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    return float(mean_absolute_error(y_true, y_pred)), float(math.sqrt(mean_squared_error(y_true, y_pred)))


def _naive_prediction(rows: Sequence[Mapping[str, object]], test_idx: Sequence[int], outcome: str) -> np.ndarray:
    if outcome == "log_revenue_change":
        return np.zeros(len(test_idx), dtype=float)
    if outcome == "log_revenue":
        return np.asarray([float(rows[i]["lag_log_revenue"]) for i in test_idx], dtype=float)
    raise ValueError(outcome)


def _write_csv(path: Path, records: list[dict[str, object]], fieldnames: Sequence[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        raise ValueError(f"no records: {path}")
    fields = list(fieldnames or records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(records)


def _aggregate(metrics: list[dict[str, object]]) -> list[dict[str, object]]:
    by: dict[tuple[str, str, bool], list[dict[str, object]]] = defaultdict(list)
    for r in metrics:
        by[(str(r["outcome"]), str(r["model"]), bool(r["include_pci"]))].append(r)
    naive_by_outcome = {
        outcome: sorted(
            [r for r in metrics if r["outcome"] == outcome and r["model"] == "naive"],
            key=lambda r: int(r["test_year"]),
        )
        for outcome in OUTCOMES
    }
    en_base_by_outcome = {
        outcome: sorted(
            [
                r for r in metrics
                if r["outcome"] == outcome
                and r["model"] == "elastic_net"
                and not r["include_pci"]
            ],
            key=lambda r: int(r["test_year"]),
        )
        for outcome in OUTCOMES
    }
    out = []
    for (outcome, model, include_pci), records in sorted(by.items()):
        records = sorted(records, key=lambda r: int(r["test_year"]))
        maes = np.asarray([float(r["mae"]) for r in records])
        rmses = np.asarray([float(r["rmse"]) for r in records])
        naive_mae = np.asarray([float(r["mae"]) for r in naive_by_outcome[outcome]])
        enbase_mae = np.asarray([float(r["mae"]) for r in en_base_by_outcome[outcome]])
        if model == "naive":
            imp_naive = np.zeros_like(maes)
            wins_naive = 0
        else:
            imp_naive = naive_mae - maes
            wins_naive = int(np.sum(maes < naive_mae))
        imp_en = enbase_mae - maes
        wins_en = int(np.sum(maes < enbase_mae))
        out.append({
            "outcome": outcome, "model": model, "include_pci": include_pci,
            "mean_mae": float(maes.mean()), "median_mae": float(np.median(maes)),
            "mean_rmse": float(rmses.mean()), "median_rmse": float(np.median(rmses)),
            "mean_mae_improvement_vs_naive": float(imp_naive.mean()),
            "pct_mean_mae_improvement_vs_naive": float(
                (naive_mae.mean() - maes.mean()) / naive_mae.mean() * 100.0
            ),
            "wins_vs_naive": wins_naive, "folds": len(records),
            "mean_mae_improvement_vs_elastic_nonpci": float(imp_en.mean()),
            "pct_mean_mae_improvement_vs_elastic_nonpci": float(
                (enbase_mae.mean() - maes.mean()) / enbase_mae.mean() * 100.0
            ),
            "wins_vs_elastic_nonpci": wins_en,
        })
    return out


def _family_increment(metrics: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for outcome in OUTCOMES:
        for model in ("elastic_net", "random_forest", "xgboost"):
            base = sorted(
                [r for r in metrics if r["outcome"] == outcome and r["model"] == model and not r["include_pci"]],
                key=lambda r: int(r["test_year"]),
            )
            pci = sorted(
                [r for r in metrics if r["outcome"] == outcome and r["model"] == model and r["include_pci"]],
                key=lambda r: int(r["test_year"]),
            )
            if len(base) != 6 or len(pci) != 6:
                raise ValueError("missing family metrics")
            b = np.asarray([float(r["mae"]) for r in base])
            p = np.asarray([float(r["mae"]) for r in pci])
            delta = b - p
            out.append({
                "outcome": outcome, "model": model,
                "mean_mae_nonpci": float(b.mean()), "mean_mae_pci": float(p.mean()),
                "mean_mae_improvement_pci": float(delta.mean()),
                "pct_mean_mae_improvement_pci": float(delta.mean() / b.mean() * 100.0),
                "wins_pci_vs_same_family": int(np.sum(p < b)), "folds": 6,
                "pci_incremental_gate": bool(p.mean() < b.mean() and int(np.sum(p < b)) >= 4),
            })
    return out


def _importance_gate(
    aggregate: list[dict[str, object]],
    family: list[dict[str, object]],
) -> dict[tuple[str, str], bool]:
    agg = {(r["outcome"], r["model"], bool(r["include_pci"])): r for r in aggregate}
    fam = {(r["outcome"], r["model"]): r for r in family}
    result = {}
    for outcome in OUTCOMES:
        enbase = float(agg[(outcome, "elastic_net", False)]["mean_mae"])
        for model in ("elastic_net", "random_forest", "xgboost"):
            pcir = agg[(outcome, model, True)]
            primary = bool(
                float(pcir["mean_mae"]) < enbase
                and int(pcir["wins_vs_elastic_nonpci"]) >= 4
            )
            strict = bool(fam[(outcome, model)]["pci_incremental_gate"])
            result[(outcome, model)] = bool(primary and strict)
    return result


def run_benchmark(
    input_csv: str | Path,
    output_dir: str | Path,
    expected_sha256: str = CANONICAL_PANEL_SHA256,
) -> dict[str, object]:
    input_csv = Path(input_csv)
    output_dir = Path(output_dir)
    actual = sha256_file(input_csv)
    if expected_sha256 and actual != expected_sha256:
        raise ValueError(
            f"canonical panel checksum mismatch: expected {expected_sha256}, found {actual}"
        )
    rows = _model_rows(_read_panel(input_csv))
    folds = outer_folds(rows)
    metric_rows = []
    prediction_rows = []
    tuning_rows = []
    fitted_for_importance = {}

    for outcome in OUTCOMES:
        for train_idx, test_idx, test_year in folds:
            ytest = _y(rows, test_idx, outcome)
            naive = _naive_prediction(rows, test_idx, outcome)
            mae, rmse = _metrics(ytest, naive)
            metric_rows.append({
                "outcome": outcome, "model": "naive", "include_pci": False,
                "test_year": test_year, "train_start": START_YEAR,
                "train_end": test_year - 1, "n_train": len(train_idx),
                "n_test": len(test_idx), "mae": mae, "rmse": rmse,
                "best_params_json": "{}", "mean_inner_mae": "",
            })
            for j, i in enumerate(test_idx):
                prediction_rows.append({
                    "outcome": outcome, "model": "naive", "include_pci": False,
                    "test_year": test_year, "province": rows[i]["province"],
                    "y_true": round(float(ytest[j]), 10),
                    "y_pred": round(float(naive[j]), 10),
                    "abs_error": round(float(abs(ytest[j] - naive[j])), 10),
                })

            for model_name in ("elastic_net", "random_forest", "xgboost"):
                for include_pci in (False, True):
                    tuned = tune_model(
                        rows, train_idx, outcome, model_name, include_pci
                    )
                    pipe = _pipeline(model_name, include_pci, tuned.best_params)
                    pipe.fit(
                        _raw_x(rows, train_idx, include_pci),
                        _y(rows, train_idx, outcome),
                    )
                    pred = pipe.predict(_raw_x(rows, test_idx, include_pci))
                    mae, rmse = _metrics(ytest, pred)
                    metric_rows.append({
                        "outcome": outcome, "model": model_name,
                        "include_pci": include_pci, "test_year": test_year,
                        "train_start": START_YEAR, "train_end": test_year - 1,
                        "n_train": len(train_idx), "n_test": len(test_idx),
                        "mae": mae, "rmse": rmse,
                        "best_params_json": _stable_param_key(tuned.best_params),
                        "mean_inner_mae": tuned.mean_inner_mae,
                    })
                    tuning_rows.append({
                        "outcome": outcome, "model": model_name,
                        "include_pci": include_pci,
                        "outer_test_year": test_year,
                        "best_params_json": _stable_param_key(tuned.best_params),
                        "mean_inner_mae": tuned.mean_inner_mae,
                        "inner_validation_years": "|".join(
                            str(v) for _, _, v in inner_folds(rows, train_idx)
                        ),
                        "inner_fold_mae": "|".join(
                            format(x, ".12g") for x in tuned.inner_fold_mae
                        ),
                    })
                    for j, i in enumerate(test_idx):
                        prediction_rows.append({
                            "outcome": outcome, "model": model_name,
                            "include_pci": include_pci, "test_year": test_year,
                            "province": rows[i]["province"],
                            "y_true": round(float(ytest[j]), 10),
                            "y_pred": round(float(pred[j]), 10),
                            "abs_error": round(float(abs(ytest[j] - pred[j])), 10),
                        })
                    if include_pci:
                        fitted_for_importance[(outcome, model_name, test_year)] = (
                            pipe, list(test_idx)
                        )

    aggregate = _aggregate(metric_rows)
    family = _family_increment(metric_rows)
    gate = _importance_gate(aggregate, family)
    importance_rows = []
    for (outcome, model_name), passed in sorted(gate.items()):
        if not passed:
            continue
        for _, test_idx, test_year in folds:
            pipe, _ = fitted_for_importance[(outcome, model_name, test_year)]
            Xtest = _raw_x(rows, test_idx, True)
            ytest = _y(rows, test_idx, outcome)
            pi = permutation_importance(
                pipe, Xtest, ytest, scoring="neg_mean_absolute_error",
                n_repeats=30, random_state=RANDOM_SEED + test_year, n_jobs=1,
            )
            for pos, c in enumerate(PCI_FEATURES, start=4):
                importance_rows.append({
                    "outcome": outcome, "model": model_name,
                    "test_year": test_year, "feature": c,
                    "feature_label": PCI_LABELS[c],
                    "mae_increase_mean": float(pi.importances_mean[pos]),
                    "mae_increase_sd": float(pi.importances_std[pos]),
                })

    metrics_path = output_dir / "PRED-BENCHMARK-01_metrics.csv"
    pred_path = output_dir / "PRED-BENCHMARK-01_predictions.csv"
    tuning_path = output_dir / "PRED-BENCHMARK-01_tuning.csv"
    agg_path = output_dir / "PRED-BENCHMARK-01_aggregate.csv"
    family_path = output_dir / "PRED-BENCHMARK-01_pci_increment.csv"
    _write_csv(metrics_path, metric_rows)
    _write_csv(pred_path, prediction_rows)
    _write_csv(tuning_path, tuning_rows)
    _write_csv(agg_path, aggregate)
    _write_csv(family_path, family)

    fingerprint_rows = []
    grouped = defaultdict(list)
    for r in prediction_rows:
        grouped[(
            str(r["outcome"]), str(r["model"]),
            bool(r["include_pci"]), int(r["test_year"]),
        )].append(r)
    for (outcome, model, include_pci, test_year), records in sorted(grouped.items()):
        records = sorted(records, key=lambda r: str(r["province"]))
        payload = "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            for r in records
        ).encode("utf-8")
        fingerprint_rows.append({
            "outcome": outcome, "model": model, "include_pci": include_pci,
            "test_year": test_year, "n_predictions": len(records),
            "prediction_group_sha256": hashlib.sha256(payload).hexdigest(),
        })
    fingerprint_path = output_dir / "PRED-BENCHMARK-01_prediction_fingerprints.csv"
    _write_csv(fingerprint_path, fingerprint_rows)

    importance_path = None
    if importance_rows:
        importance_path = output_dir / "PRED-BENCHMARK-01_permutation_importance.csv"
        _write_csv(importance_path, importance_rows)

    metadata = {
        "status": "PASS",
        "input_csv_sha256": actual,
        "random_seed": RANDOM_SEED,
        "outer_test_years": list(OUTER_TEST_YEARS),
        "outer_fold_rule": "expanding: train 2014..t-1, test t",
        "inner_fold_rule": (
            "expanding within each outer train; use up to the two most recent "
            "validation years, each preceded by at least three training years"
        ),
        "models": [
            "naive", "elastic_net_nonpci", "elastic_net_pci",
            "random_forest_nonpci", "random_forest_pci",
            "xgboost_nonpci", "xgboost_pci",
        ],
        "outcomes": list(OUTCOMES),
        "feature_information_cutoff": (
            "target-year t features use revenue and PCI information no later "
            "than t-1; calendar trend t is deterministic"
        ),
        "primary_metric": "MAE",
        "secondary_metric": "RMSE",
        "feature_importance_gate": {
            f"{o}:{m}": v for (o, m), v in sorted(gate.items())
        },
        "feature_importance_generated": bool(importance_rows),
        "sklearn_version": sklearn.__version__,
        "xgboost_version": xgb.__version__,
        "numpy_version": np.__version__,
        "output_sha256": {},
    }
    for p in (
        metrics_path, pred_path, tuning_path, agg_path, family_path,
        fingerprint_path, importance_path,
    ):
        if p is not None:
            metadata["output_sha256"][p.name] = sha256_file(p)
    meta_path = output_dir / "PRED-BENCHMARK-01_metadata.json"
    meta_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    metadata["output_sha256"][meta_path.name] = sha256_file(meta_path)
    return metadata


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run time-respecting predictive benchmark for Euréka 2026."
    )
    p.add_argument("--input", default="data/processed/panel.csv")
    p.add_argument("--output-dir", default="artifacts/results")
    p.add_argument("--expected-sha256", default=CANONICAL_PANEL_SHA256)
    return p


def main() -> int:
    args = _parser().parse_args()
    metadata = run_benchmark(
        args.input, args.output_dir, args.expected_sha256
    )
    print(json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
