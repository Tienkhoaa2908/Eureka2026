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
Next: re-run only after DATA-INTEGRITY-01 and commit the exact script/output artifact.
