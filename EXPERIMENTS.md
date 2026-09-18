# EXPERIMENTS

All experiments must be reproducible from a committed script/notebook plus immutable input artifact or checksum. Do not record model metrics from memory.

## E-000 — Legacy EDA audit
Date: 2026-09-18
Status: AUDITED, NOT A FINAL RESULT
Inputs: uploaded Panel_10_CSTP_2010_2024.xlsx and legacy EDA code.
Findings:
- 945 province-year rows.
- CSTP6 missing exactly 189 rows = 63 provinces × 2010–2012.
- Full 10-subindex VIF diagnostic uses 756 rows from 2013–2024.
- Current VIFs are all < 5; largest observed values are around 3.5.
- The legacy .ipynb has syntax errors in 8 code cells.
Interpretation: collinearity is not the primary blocker; reproducibility and identification are.

## E-001 — Preliminary two-way FE smoke test
Date: 2026-09-18
Status: SUPERSEDED BY E-004
Purpose: verify technical estimability before canonical pipeline completion.

## E-002 — DATA-INTEGRITY-01
Date: 2026-09-18
Status: **PASS**
Key result:
- corrected Hòa Bình 2016, Gia Lai 2023, and An Giang 2023 revenue transcription errors;
- after correction all 90 regional-subtotal QA residuals have absolute value ≤ 3.

Evidence:
- `artifacts/qa/DATA-INTEGRITY-01.md`.

## E-003 — REPRO-PIPELINE-01
Date: 2026-09-18
Status: **PASS**
Result:
- 945-row deterministic canonical panel;
- full contemporaneous 10-CSTP N=756;
- full lagged 10-CSTP N=693;
- output SHA-256 `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`;
- repeat builds byte-identical.

Evidence:
- `artifacts/qa/REPRO-PIPELINE-01.md`.

## E-004 — STAT-BASELINE-01
Date: 2026-09-18
Status: **PASS**

Input:
- canonical panel SHA-256 `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`.

Design:
- 2014–2024;
- N=693, 63 province clusters;
- ten standardized one-year-lagged PCI components;
- province FE + year FE;
- province-clustered SE with cluster-t inference;
- BH FDR across 10 component coefficients per model/outcome;
- outcomes: log revenue and log revenue change;
- sensitivity excludes 2020–2021 outcome years;
- leave-one-province-out coefficient sensitivity.

Results:
- log revenue: no component has BH q<0.05;
- log revenue change: CSTP5 beta=0.03628, 95% CI [0.01852, 0.05404], p=0.000129, q=0.001289;
- no-2020/2021 outcome sensitivity: CSTP5 beta=0.03840, q=0.01290;
- CSTP5 log-change leave-one-province-out beta range [0.03403, 0.03947], zero sign flips across 63 omissions;
- CSTP6 raw p≈0.054 in the full change model but q≈0.270, therefore not multiplicity-adjusted evidence.

Interpretation:
CSTP5 is the only component with a multiplicity-adjusted association in the prespecified growth specification under these checks. This is not a causal estimate and not a cross-outcome “winner”.

Result artifact SHA-256:
- coefficients `7062c90249e350c43fc99147f3dded50a864383ab51e47306cdd14f88ae32495`;
- influence `077c03fa5be000bcbb4879d5e6ddc3cf2a37bc39b08b031bebc9ab91e1ced1bb`;
- scaling `960a0b6df763da43676217d739d2c8b940322aa50bbf1857a4f6fe7dbf1c456d`.

QA:
- `artifacts/qa/STAT-BASELINE-01.md`.

Next:
G4 PRED-BENCHMARK-01.
