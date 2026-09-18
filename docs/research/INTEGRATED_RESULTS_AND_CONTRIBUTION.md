# Integrated results and scientific contribution

Updated: 2026-09-18

## Central result

The project does **not** support a universal ranking of PCI components.

Instead, three evidence layers lead to a bounded conclusion:

1. **Inference (G3):** CSTP5 is the only lagged component passing BH correction in the prespecified 2014–2024 log-revenue-change FE model; no component passes for log-revenue level.
2. **Prediction (G4):** the ten lagged PCI components do not improve future-year prediction beyond the best non-PCI Elastic Net over fixed 2019–2024 test years; nonlinear models do not dominate the simpler regularized baseline.
3. **Robustness/falsification (G5):** the CSTP5 lagged association survives several influence/outlier checks but weakens under a stricter pandemic window and disappears in longer-period and contemporaneous specifications.

## Interpretation of CSTP5

PCI/VCCI defines the Informal Charges dimension so that a well-performing province is characterized by **minimal informal charges**. Therefore the positive lagged coefficient is directionally consistent with the interpretation that a better informal-charge environment is associated with higher subsequent revenue change in the primary specification.

It is not a causal estimate. Do not rewrite beta≈0.0363 as “reducing informal charges causes revenue growth to increase 3.69%.”

## Why G3 and G4 are not contradictory

The FE model asks whether within-province variation in lagged governance has a conditional association after province/year effects and other PCI dimensions are partialled out.

The forecasting benchmark asks whether PCI materially lowers prediction error in **unseen future years** after lagged revenue, recent change, province identity, trend, regularization, model selection and regime shifts are considered.

A coefficient can be statistically detectable without adding forecast value because:
- effect size may be small relative to shocks and outcome volatility;
- lagged revenue/history can absorb much predictable variation;
- PCI dimensions overlap/correlate;
- relationships can drift by period/regime;
- parameter/model-selection uncertainty is substantial with 63 provinces and short T.

That distinction is a core scientific contribution, not an inconsistency.

## Relation to Vietnam literature

Prior results are mixed:
- Nguyen, Le & Bryant (2013) show subnational institutions matter through interactions with firm strategy/performance.
- Huynh (2022) reports direct and spatial effects and a negative relationship between informal charges and TFP.
- The 2024 TFP study finds other dimensions such as time costs/labor policy more prominent in important specifications.
- ADB (Kokko, Nguyen & Nilsson Hakkala, 2026) reports limited effects of PCI changes on several provincial manufacturing outcomes in many models.
- Thoa & Hung (2026) find PCI-component patterns vary across contemporaneous and lagged market-entry models.

Therefore the present outcome-specific, specification-bounded result is more credible than a universal “best PCI component” claim.

## Defensible novelty claim for Euréka

> The study builds an auditable 2010–2024 province-year PCI–enterprise-revenue panel and evaluates institutional signals through three deliberately separated layers: two-way fixed-effects inference with multiplicity control, strict future-year out-of-sample prediction with nested temporal tuning, and robustness/falsification checks. The design shows that a statistically detectable lagged association need not translate into incremental forecast value, preventing feature importance from being misrepresented as institutional impact.

Novelty is not “we used XGBoost.”

## Policy boundary

The evidence is consistent with the practical importance of reducing informal-charge burdens, but it does not establish that changing CSTP5 alone will causally raise provincial enterprise revenue by a fixed percentage.

Policy prioritization should combine:
- the broader institutional literature;
- mechanism-specific evidence;
- local business diagnostics;
- and causal/quasi-experimental designs where available.

A machine-learning feature ranking is not used as a policy ranking.

## Main limitations

1. Outcome is aggregate nominal provincial enterprise revenue, not firm-level productivity/profit.
2. Province size, firm count and sector composition evolve over time and are not fully removed by FE.
3. A common national deflator is absorbed by year FE in log-level two-way-FE models; genuinely new scale robustness requires verified province-specific prices or per-firm/per-worker outcomes.
4. Two-way FE does not remove time-varying confounding or reverse causality.
5. Pesaran CD does not reject residual dependence, but short T limits power and does not rule out spatial mechanisms.
6. PCI measurement and component construction can drift over a long panel.
7. The exact publication/page behind the archived 2020–2024 Table 151 screenshot remains a documented lineage caveat.

## Result hierarchy for the manuscript

1. data provenance and correction audit;
2. sample construction / structural missingness;
3. FE baseline and multiplicity-aware uncertainty;
4. future-year prediction and the negative incremental-PCI result;
5. robustness/falsification boundary;
6. comparison with mixed Vietnam evidence;
7. cautious policy implications.

Do not lead the paper with XGBoost, SHAP or feature ranking.
