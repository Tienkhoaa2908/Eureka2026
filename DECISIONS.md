# DECISIONS

Decision log. New decisions append below; superseded decisions remain with status marked SUPERSEDED.

## D-001 — Separate inference from prediction
Date: 2026-09-18
Status: ACTIVE
Decision: Maintain two linked tracks: (A) interpretable panel-econometric inference and (B) out-of-sample ML prediction.
Reason: feature importance from Random Forest/XGBoost is not a causal-effect estimator; combining the tracks prevents predictive performance from being misreported as institutional impact.

## D-002 — Use lagged PCI sub-indices in the primary model
Date: 2026-09-18
Status: ACTIVE
Decision: Primary predictors are t-1 PCI sub-indices; contemporaneous specifications are robustness checks.
Reason: temporal ordering is clearer and reduces, but does not eliminate, simultaneity concerns.

## D-003 — Main 10-subindex window starts in 2013
Date: 2026-09-18
Status: ACTIVE
Decision: Never impute sub-index 6 for 2010–2012 as ordinary missing data. Use 2013–2024 for contemporaneous 10-index models and 2014–2024 for one-year-lagged 10-index models.
Reason: the variable was not available in the earlier period; this is structural missingness.

## D-004 — Two-way fixed effects are the minimum inferential baseline
Date: 2026-09-18
Status: ACTIVE
Decision: Province FE + year FE, with province-clustered standard errors, must be reported before advanced ML results.
Reason: pooled correlations mix stable province differences with within-province change and common national shocks.

## D-005 — No random row train/test split
Date: 2026-09-18
Status: ACTIVE
Decision: Prediction evaluation must respect time ordering using expanding or rolling splits.
Reason: random splitting leaks future regime information and repeated province characteristics into training.

## D-006 — Do not rank a PCI component as 'most impactful' from one feature-importance plot
Date: 2026-09-18
Status: ACTIVE
Decision: A component may be called robust only if its signal is directionally/stably supported across prespecified econometric and predictive robustness checks.
Reason: correlated predictors make impurity-based importance unstable and causal wording unjustified.

## D-007 — Revenue outcome needs scale/price robustness
Date: 2026-09-18
Status: ACTIVE
Decision: Main outcome candidates are log nominal revenue and log growth; add real/deflated revenue and scale-normalized outcomes if source data can support them.
Reason: raw provincial revenue is dominated by province size and price-level trends.

## D-008 — Correct three verified revenue transcription errors only in derived data
Date: 2026-09-18
Status: ACTIVE
Decision:
- Hòa Bình 2016 revenue: 23,040 → 33,040.
- Gia Lai 2023 revenue: 133,195 → 131,195.
- An Giang 2023 revenue: 212,941 → 212,961.
- Recompute any growth or lagged outcome derived from revenue after applying corrections.
- Preserve the raw/legacy artifact unchanged and apply corrections through committed code.
Reason: archived source tables and official NSO cross-checks independently identify the three legacy values as transcription errors. Encoding the correction rather than editing raw evidence preserves provenance.

## D-009 — Treat tiny regional subtotal residuals as QA metadata, not province data
Date: 2026-09-18
Status: ACTIVE
Decision: After the verified corrections, remaining region-year subtotal residuals (maximum absolute value 3) are documented but not redistributed across provinces.
Reason: the model unit is province-year, and inventing province-level adjustments to force regional arithmetic equality would alter published province observations without evidence.
