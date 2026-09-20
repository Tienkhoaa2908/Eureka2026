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


## E-005 — PRED-BENCHMARK-01
Date: 2026-09-18
Status: **PASS — negative incremental-PCI result**

Input:
- canonical panel SHA-256 `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`.

Design:
- outer test years 2019–2024;
- expanding training window from 2014;
- nested expanding temporal tuning;
- naive, Elastic Net, Random Forest, XGBoost;
- non-PCI and PCI-added variants;
- outcomes: log revenue change (primary), log revenue (secondary);
- MAE primary, RMSE secondary.

Primary change result:
- non-PCI Elastic Net mean MAE = **0.08819** (best);
- PCI Elastic Net = 0.08890;
- PCI Random Forest = 0.09523;
- non-PCI XGBoost = 0.10172;
- PCI XGBoost = 0.10321;
- non-PCI Random Forest = 0.10365;
- naive = 0.11484.

RF gains ~8.12% versus RF without PCI and wins 5/6 same-family folds, but remains ~7.98% worse than non-PCI Elastic Net and beats that stronger baseline only 1/6 folds.

Secondary level result:
- non-PCI Elastic Net mean MAE = **0.08859** (best);
- adding PCI worsens mean MAE in Elastic Net, RF and XGBoost.

No PCI-added model passes the feature-importance gate. No feature ranking is generated.

Evidence:
- `artifacts/qa/PRED-BENCHMARK-01.md`
- `artifacts/results/PRED-BENCHMARK-01_*.csv/json`.

## E-006 — ROBUSTNESS-01
Date: 2026-09-18
Status: **PASS with outcome-data caveat**

Target: primary G3 CSTP5 log-change association.

Key checks:
- strict no-2020–2022: beta=0.03316, p=0.00672, q=0.06720;
- contemporaneous 10 components: CSTP5 p=0.99419;
- long 2011–2024 lagged 9 components: CSTP5 beta=0.01170, q=0.31121;
- winsorized outcome: beta=0.03416, q=0.001491;
- single-component lag1: beta=0.01507, p=0.04358;
- distributed lag: lag1 beta=0.02514, p=0.00824; lag2 null;
- future-lead placebo: p=0.47656;
- leave-one-year beta [0.03191, 0.04924], 0 sign flips;
- leave-one-region beta [0.02907, 0.03990], 0 sign flips;
- Pesaran CD p=0.166 with short-T caveat.

Interpretation:
CSTP5 is not a universal winner. The signal is lagged and robust to some influence/outlier checks but period/specification-sensitive and not forecast-incremental.

Evidence:
- `artifacts/qa/ROBUSTNESS-01.md`
- `artifacts/results/ROBUSTNESS-01_*.csv/json`.

## E-007 — Integrated literature/contribution synthesis
Date: 2026-09-18
Status: **PASS**

Outputs:
- `docs/research/LITERATURE_MATRIX.md`
- `docs/research/INTEGRATED_RESULTS_AND_CONTRIBUTION.md`
- `docs/submission/MANUSCRIPT_DRAFT.md`

Result:
The literature is mixed across outcomes/units/methods. The defensible contribution is the auditable separation of association, future-year prediction and falsification, including retention of negative predictive evidence.


## E-008 — Đặt lại thiết kế khoa học sang cơ chế hậu 2015
Date: 2026-09-20
Status: **ĐANG HOẠT ĐỘNG — KHÔNG PHẢI KẾT QUẢ ĐỊNH LƯỢNG**

Mục tiêu:
- đóng hướng doanh thu tổng hợp + dự báo;
- đặt tính bền vững theo thời gian và phân rã cơ chế làm câu hỏi trung tâm;
- khóa các họ giả thuyết trước khi đọc hệ số cuối;
- mở rộng dữ liệu NSO/PAPI theo các biên gia nhập, quy mô, hiệu quả, lợi nhuận, lao động và vốn.

Lưu ý:
- E-004 đến E-007 được giữ nguyên làm lịch sử kiểm toán;
- kết quả cũ không được mang sang như bằng chứng xác nhận giả thuyết mới;
- không có hệ số hoặc chỉ số mới nào được khai báo trong E-008.


## 2026-09-20 — phục hồi SR1 và kiểm toán trước mô hình

Đã hợp nhất lịch sử main/PR13 trong PR16 nháp, kiểm toán ZIP và sửa lỗi thu thập NSO. Run 35482892847 thu được toàn bộ nguồn trừ bước chuẩn hóa dân số; giữ CSV gốc để sửa parser tiêu đề Total/năm sơ bộ. Không mở khóa mô hình: cần xác minh tính nhất quán PCI, quần thể H4 và mẫu số tỷ suất lợi nhuận. Bằng chứng và giới hạn: `docs/research/RECOVERY_AUDIT_2026-09-20.md`.
