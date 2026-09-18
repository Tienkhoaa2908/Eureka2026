# EXPERIMENTS

All experiments must be reproducible from a committed script/notebook plus immutable input artifact or checksum. Do not record model metrics from memory.

## E-000 — Legacy EDA audit
Date: 2026-09-18
Status: AUDITED, NOT A FINAL RESULT
Inputs: uploaded Panel_10_CSTP_2010_2024.xlsx and legacy EDA code.
Findings:
- 945 province-year rows.
- Sub-index 6 missing exactly 189 rows = 63 provinces × 2010–2012.
- Full 10-subindex VIF diagnostic uses 756 rows from 2013–2024.
- Current VIFs are all < 5; largest observed values are around 3.5.
- The legacy .ipynb has syntax errors in 8 code cells caused by uncommented separator text.
Interpretation: collinearity is not the primary blocker; reproducibility and identification are.

## E-001 — Preliminary two-way FE smoke test
Date: 2026-09-18
Status: PRELIMINARY / DO NOT CITE AS FINAL
Design: 2014–2024, one-year-lagged 10 PCI sub-indices, province FE, year FE, province-clustered SE; outcomes log revenue and log revenue change.
Purpose: verify that the proposed inferential pipeline is technically estimable on 693 province-year rows.
Result: model estimation succeeds. Coefficient patterns differ materially by outcome, reinforcing the need for prespecified outcomes and robustness checks rather than a single 'winner' sub-index.
Next: re-run only after G2 reproducible pipeline passes and commit the exact script/output artifact.

## E-002 — DATA-INTEGRITY-01
Date: 2026-09-18
Status: **PASS**
Inputs:
- legacy `panel_PCI_doanhthu_2010_2024.xlsx`;
- six archived GSO/NSO table screenshots;
- official NSO Statistical Yearbook / indicator cross-checks.

Legacy workbook SHA-256:
`bbd5a7277b2473da49d7831fd1530a52a5563025f1d8aceadc3869cd0c40d345`

Findings:
- Three large region-subtotal discrepancies trace to three province-level transcription errors:
  - Hòa Bình 2016: 23,040 → 33,040;
  - Gia Lai 2023: 133,195 → 131,195;
  - An Giang 2023: 212,941 → 212,961.
- After correction, all 90 region-year subtotal checks have absolute residual ≤ 3; 47 are exact.
- Correcting revenue materially changes affected annual growth values, so growth must always be regenerated downstream.
- Source blocks are documented in `data/metadata/data_lineage.csv`; individual corrections in `data/metadata/revenue_corrections.csv`.
- The exact publication/page behind the archived 2020–2024 Table 151 screenshot is not retained; official NSO PX-Web and the 2024 yearbook provide cross-checkable lineage.

Correction implementation:
`src/eureka2026/revenue_corrections.py`

QA artifact:
`artifacts/qa/DATA-INTEGRITY-01.md`

Next:
G2 REPRO-PIPELINE-01.
