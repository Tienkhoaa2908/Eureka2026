# Euréka 2026 submission synthesis plan

Updated: 2026-09-18  
Current gate: G7 Submission package  
Registration deadline: 2026-09-25

## Working title

**Chất lượng điều hành kinh tế cấp tỉnh và kết quả doanh nghiệp tại Việt Nam: Bằng chứng từ dữ liệu bảng và dự báo ngoài mẫu giai đoạn 2010–2024**

The title deliberately avoids causal wording.

## Central research question

Which dimensions of provincial economic governance show stable lagged associations with enterprise outcomes after province/year heterogeneity is controlled, and do those PCI dimensions add genuine future-year predictive value beyond strong non-PCI baselines?

## Contribution to foreground

- audited 63-province × 15-year data pipeline with explicit source-backed corrections;
- inference and prediction are separated rather than conflated;
- two-way FE with clustered inference and multiple-testing control;
- fixed expanding-window future-year evaluation with nested temporal tuning;
- negative ML/PCI evidence is retained rather than converted into a feature-importance story;
- robustness/falsification explicitly identifies where CSTP5 holds and where it fails.

## Statements approved

1. No lagged PCI component survives BH correction in the log-revenue-level FE model.
2. CSTP5 is the only BH-adjusted lagged component in the primary 2014–2024 log-revenue-change FE specification; beta≈0.0363 per one SD, but this is a conditional association.
3. CSTP5 survives winsorization and province/year/region omission, but weakens under stricter pandemic exclusion and is null in longer-period/contemporaneous variants.
4. Lagged PCI does not improve mean out-of-sample prediction beyond the best non-PCI Elastic Net over the six fixed test years 2019–2024.
5. No feature-importance ranking is reported because no PCI-added model passes the generalization gate.

## Statements prohibited

- “CSTP5 is the most impactful PCI component.”
- “Increasing CSTP5 by one SD causes revenue growth to rise 3.69%.”
- “XGBoost proves which institution matters most.”
- “PCI has no effect.”
- “There is no spatial dependence.”

## Final package

- anonymous manuscript;
- abstract consistent with bounded claims;
- final tables/figures generated from committed artifacts;
- required portrait poster;
- checked references using primary/official sources;
- reproducibility/code statement if allowed;
- anonymity audit;
- number-to-artifact audit for every quantitative statement.

## Figure/table shortlist

1. Pipeline/sample construction: 945 → 756 → 693.
2. G3 coefficient plot for log revenue change, with 95% CI and BH status.
3. G4 test-year MAE comparison: non-PCI Elastic Net vs PCI-added models.
4. G5 CSTP5 robustness plot: primary, strict-COVID, longer period, contemporaneous, winsorized, distributed lag/placebo.
5. Literature matrix demonstrating outcome/method heterogeneity.

## Format reminder from official 2026 rules

- A4;
- Times New Roman 13;
- line spacing 1.3–1.5;
- left margin 3 cm; top/bottom/right 2 cm;
- no author, institution, supervisor, logo, acknowledgements or identifying marks in research content/appendices;
- Vietnamese or English;
- poster portrait 0.8 m × 1.3 m.

## Submission gate

G7 passes only after manuscript/poster are consistent with repository state, anonymous, format-compliant, source-cited and every number is reproducible.
