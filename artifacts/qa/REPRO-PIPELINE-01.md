# REPRO-PIPELINE-01 — deterministic canonical panel build

Date: 2026-09-18  
Gate: G2 Reproducible pipeline  
Verdict: **PASS**

## Build contract

With the two identified migration inputs placed at:

- `data/raw/migration/panel_PCI_doanhthu_2010_2024.xlsx`
- `data/raw/migration/Panel_10_CSTP_2010_2024.xlsx`

run:

```bash
python -m src.eureka2026.pipeline
```

The command reads XLSX using a small standard-library reader, normalizes the 63-province universe through an explicit mapping, applies only the three G1-verified revenue corrections, rebuilds revenue growth and lagged fields, joins PCI/revenue/CSTP one-to-one, validates the panel, writes `data/processed/panel.csv`, and writes a machine-readable QA JSON locally.

No third-party Python runtime dependency is required for the canonical build.

## Input fingerprints

| Input | SHA-256 |
|---|---|
| legacy PCI/revenue panel | `bbd5a7277b2473da49d7831fd1530a52a5563025f1d8aceadc3869cd0c40d345` |
| 10-CSTP panel | `b777da5cc8364a5c315a05f8a4bb976501fddfa86a426e8e21a0f13b6b7ea32d` |

## Canonical output

`data/processed/panel.csv`

SHA-256:

`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

Verified dimensions:

- 945 province-year rows;
- 63 provinces/cities;
- 2010–2024 inclusive;
- 756 rows with all 10 contemporaneous CSTP values (2013–2024);
- 693 rows with all 10 one-year-lagged CSTP values (2014–2024).

The canonical CSV has 27 fields:

- identifiers/geography: `Tinh`, `Vung`, `Nam`;
- PCI: `PCI`, `PCI_lag1`;
- outcome: `Doanh_thu_ty_dong`, `Tang_truong_Doanh_thu_pct`;
- `cstp1..cstp10`;
- `cstp1_lag1..cstp10_lag1`.

## Determinism

Two consecutive builds from unchanged input bytes produced byte-identical CSV files with the same SHA-256 above.

The canonical first seven fields were additionally compared by province-year key against the corrected G1 audit workbook: **0 mismatches across 945 rows**.

## Invariants enforced in code

The build fails on:

- unknown province names;
- duplicate province-year keys;
- incomplete 63 × 15 universe;
- non-positive revenue;
- incomplete one-to-one join coverage;
- region changes within a province;
- non-structural CSTP missingness;
- non-missing CSTP6 in 2010–2012;
- incorrect lag missingness;
- missing or altered verified correction targets.

Legacy `PCI_lag1` and revenue-growth columns are not trusted. They are regenerated from canonical current-year values.

## Validation

Local validation before PR:

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

All 11 unit tests passed locally, including an end-to-end synthetic XLSX → canonical CSV test that builds twice and asserts identical output hashes.

CI runs the same compile/unit-test suite on push and pull request.

## Gate decision

G2 passes. The project now has a deterministic, repository-relative source-to-analysis build with recorded input/output fingerprints and no `/mnt/user-data` dependency in active source.

This unlocks G3: the prespecified two-way fixed-effects baseline on the 2014–2024 lagged 10-CSTP sample.
