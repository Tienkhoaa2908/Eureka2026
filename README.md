# Eureka 2026 — PCI, thể chế địa phương và kết quả doanh nghiệp Việt Nam

Kho lưu trữ nghiên cứu cho đề tài dự thi **Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026**.

## Research question

> Những chiều cạnh nào của chất lượng điều hành kinh tế cấp tỉnh (10 chỉ số thành phần PCI) có quan hệ dự báo ổn định với kết quả doanh nghiệp ở cấp tỉnh, sau khi kiểm soát khác biệt cố hữu giữa tỉnh và cú sốc chung theo năm; và machine learning có cải thiện dự báo ngoài mẫu so với các baseline kinh tế lượng hay không?

Cho tới khi có chiến lược nhận dạng nhân quả đủ mạnh, dự án dùng ngôn ngữ **association / relationship / predictive signal**, không suy diễn feature importance thành “tác động nhân quả”.

## Canonical data

- 63 tỉnh/thành × 15 năm (2010–2024) = 945 province-year observations.
- 10 PCI components; CSTP6 structurally unavailable in 2010–2012.
- Complete contemporaneous 10-CSTP sample: 756 rows.
- Complete lagged 10-CSTP sample: 693 rows.
- Canonical SHA-256: `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`.

Build:

```bash
python -m src.eureka2026.pipeline
```

Run the statistical baseline after building:

```bash
python -m src.eureka2026.fe_baseline
```

## Current evidence

G1 data integrity, G2 reproducibility, and G3 statistical baseline have passed.

G3 uses 2014–2024, province FE + year FE, province-clustered cluster-t inference, and BH FDR across the ten lagged PCI components.

- Log revenue level: no component has BH q<0.05.
- Log revenue change: CSTP5 (Chi phí không chính thức) has beta=0.03628, p=0.000129, q=0.001289, 95% CI [0.01852, 0.05404].
- Excluding 2020–2021 outcome years: CSTP5 remains BH-adjusted (beta=0.03840, q=0.01290).
- Leave-one-province-out for the full change model: CSTP5 keeps the same sign in all 63 omissions.

This is an association result, not a causal effect and not a basis for calling CSTP5 the “most impactful” PCI component.

See `artifacts/qa/STAT-BASELINE-01.md`.

## Start here

1. `PROJECT_STATE.md`
2. `docs/research/NEXT_EXPERIMENT.md`
3. `docs/research/QUALITY_GATES.md`
4. `DECISIONS.md`
5. `EXPERIMENTS.md`
6. `docs/research/METHODOLOGY_V1.md`
7. `docs/research/LITERATURE_REVIEW.md`
8. `docs/competition/EUREKA_2026.md`
9. `docs/handover/RECOVERY_PROMPT.md`
10. `docs/handover/SYNC_PROMPT.md`

## Current gate

**G4 — Predictive benchmark: CURRENT.**

The next task is a fixed six-fold expanding-window benchmark (test years 2019–2024) comparing naive, non-PCI Elastic Net, PCI-added Elastic Net, Random Forest, and XGBoost. No random row split is permitted. Feature importance is allowed only if a PCI-added model demonstrates out-of-sample incremental value.

## Local validation

```bash
python -m pip install -r requirements.txt
python -m compileall -q src tests
python -m unittest discover -s tests -v
```
