# Eureka 2026 — PCI, thể chế địa phương và kết quả doanh nghiệp Việt Nam

Research repository for a 2010–2024 province-panel study prepared for **Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026**.

## Research question

> Những chiều cạnh nào của chất lượng điều hành kinh tế cấp tỉnh có liên hệ ổn định với kết quả doanh nghiệp sau khi kiểm soát dị biệt tỉnh/năm; và các chiều PCI đó có tạo thêm giá trị dự báo cho những năm tương lai ngoài các baseline không dùng PCI hay không?

The project separates **inference, prediction and robustness**. Feature importance is never treated as causal impact.

## Canonical data

- 63 provinces/cities × 15 years = 945 rows.
- Full contemporaneous 10-CSTP N=756.
- Full lagged 10-CSTP N=693.
- Canonical SHA-256: `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`.

Build:
```bash
python -m src.eureka2026.pipeline
```

## Current evidence

**G1–G6 have passed. G7 submission package is current.**

### G3 — inference
- log revenue level: no lagged PCI component has BH q<0.05;
- log revenue change: CSTP5 has beta=0.03628, p=0.000129, q=0.001289 in the primary FE model;
- this is association, not causality.

### G4 — future-year prediction
- six fixed expanding outer folds, test 2019–2024;
- non-PCI Elastic Net is best on mean MAE for both log change (0.08819) and log level (0.08859);
- adding PCI does not produce stable incremental value beyond that strong baseline;
- no PCI-added model passes the feature-importance gate, so no SHAP/permutation ranking is generated.

### G5 — robustness
CSTP5 remains positive under outlier/year/region checks, but:
- strict COVID exclusion weakens BH q to 0.06720;
- contemporaneous specification is null;
- longer 2011–2024 nine-component specification is null;
- future-lead placebo is null.

The project therefore rejects a universal “most impactful PCI component” narrative.

## Start here

1. `PROJECT_STATE.md`
2. `docs/research/INTEGRATED_RESULTS_AND_CONTRIBUTION.md`
3. `docs/research/LITERATURE_MATRIX.md`
4. `artifacts/qa/STAT-BASELINE-01.md`
5. `artifacts/qa/PRED-BENCHMARK-01.md`
6. `artifacts/qa/ROBUSTNESS-01.md`
7. `docs/submission/MANUSCRIPT_DRAFT.md`
8. `docs/research/NEXT_EXPERIMENT.md`
9. `docs/handover/RECOVERY_PROMPT.md`

## Main commands

```bash
python -m pip install -r requirements.txt
python -m src.eureka2026.pipeline
python -m src.eureka2026.fe_baseline
python -m src.eureka2026.predictive_benchmark
python -m src.eureka2026.robustness
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

## Current gate

**G7 — SUBMISSION-PACKAGE-01.**

Research-content draft: `docs/submission/MANUSCRIPT_DRAFT.md`.

Registration deadline: **2026-09-25**.
