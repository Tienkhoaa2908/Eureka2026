# CHANGELOG

## 2026-09-18

### Added
- Research operating model, quality gates, handover prompts.
- Competition/literature/audit documentation.
- Revenue lineage and correction registry.
- Deterministic canonical panel builder and tests.
- `src/eureka2026/fe_baseline.py`.
- FE utility tests for standardization and BH correction.
- NumPy/statsmodels dependency contract.
- G3 coefficient, influence, scaling, metadata, and QA artifacts.

### Changed
- Research framing separates association/inference from prediction.
- G1 Data integrity: PASS.
- G2 Reproducible pipeline: PASS.
- G3 Statistical baseline: PASS.
- Current gate advanced to G4 PRED-BENCHMARK-01.
- CI now installs declared statistical dependencies before compile/unit tests.

### G3 recorded finding
- No lagged PCI component survives BH FDR in the log-revenue-level FE model.
- CSTP5 is the only BH-adjusted association in the log-revenue-change FE model and remains positive/BH-adjusted after excluding 2020–2021 outcome years.
- The result is explicitly associational and is not labeled causal or “most impactful”.

### Known limitations / open work
- Aggregate nominal revenue has inflation/scale/sector-composition limitations.
- Two-way FE does not eliminate time-varying confounding or reverse causality.
- A stricter COVID-window robustness design remains for G5.
- Spatial dependence remains untested.
- Exact publication/page for the archived 2020–2024 Table 151 extract remains a documented lineage caveat.


### Added — G4/G5/G6 deep validation
- `src/eureka2026/predictive_benchmark.py` and temporal leakage tests.
- `src/eureka2026/robustness.py` and robustness utility tests.
- scikit-learn, XGBoost and SciPy dependency contract.
- fold-level predictive metrics, nested tuning audit, PCI-increment comparison, prediction fingerprints and metadata.
- robustness coefficient, CSTP5 targeted, year-LOO, region-LOO and metadata artifacts.
- `artifacts/qa/PRED-BENCHMARK-01.md`.
- `artifacts/qa/ROBUSTNESS-01.md`.
- `docs/research/LITERATURE_MATRIX.md`.
- `docs/research/INTEGRATED_RESULTS_AND_CONTRIBUTION.md`.
- `docs/submission/MANUSCRIPT_DRAFT.md`.
- `docs/submission/NUMBER_TO_ARTIFACT_MAP.md`.
- `docs/submission/ANONYMITY_CHECKLIST.md`.
- `docs/submission/SUBMISSION_PLAN.md`.

### Changed — evidence state
- G4 Predictive benchmark: PASS with negative incremental-PCI conclusion.
- G5 Robustness: PASS with outcome-data caveat.
- G6 Scientific contribution: PASS.
- Current gate advanced to G7 submission package.
- Working manuscript no longer frames CSTP5 as a universal “most impactful” component.
- XGBoost/Random Forest are retained as benchmark models, not as the source of the paper’s novelty.

### G4/G5 recorded finding
- non-PCI Elastic Net is best on mean MAE for both outcomes;
- no PCI-added model passes the feature-importance gate;
- CSTP5 primary FE signal survives some robustness checks but weakens or disappears in strict-period/alternative-period specifications;
- final interpretation is bounded association + negative predictive increment, not causal ranking.

## 2026-09-19 — scientific redesign

### Changed
- G7 final packaging paused.
- Added SR1 Scientific redesign / mechanism validity gate.
- Reframed the target paper from PCI-component vs aggregate revenue to a decomposition of entry, scale, productivity, profitability and labor-value margins.

### Added
- docs/research/PUBLISHABLE_REDESIGN_2026-09-19.md.
- data/metadata/scientific_extension_sources.csv.
- new SR1 experiment protocol in docs/research/NEXT_EXPERIMENT.md.

### Evidence added
- verified NSO PX-Web source tables for enterprise-stock, entry, labor, capital, revenue, wages, profit and profitability outcomes;
- verified PAPI annual Excel data availability;
- exploratory current-panel diagnostics arguing against a threshold/COVID-resilience narrative and for a within-province mechanism redesign.


## 2026-09-20 — chuyển hướng nghiên cứu hoàn toàn

### Thay đổi
- hướng cũ về doanh thu tổng hợp, xếp hạng thành phần PCI và dự báo bằng học máy (machine learning — học máy) được đóng như một hướng nghiên cứu;
- README, PROJECT_STATE, NEXT_EXPERIMENT, QUALITY_GATES và RECOVERY_PROMPT được viết lại theo hướng cơ chế;
- câu hỏi trung tâm chuyển sang tính bền vững theo thời gian của các cơ chế thể chế sau năm 2015;
- phân rã gia nhập/quy mô/doanh thu trên lao động/lợi nhuận/lao động/vốn trở thành kiến trúc chính;
- học máy không còn là nguồn đóng góp khoa học của bản thảo mới.

### Thêm
- `docs/research/HYPOTHESES_SR1.md` với H1–H5;
- quyết định D-026 đến D-030;
- thí nghiệm thiết kế E-008.

### Giữ lại có chủ đích
- dữ liệu, mã nguồn, kết quả và hiện vật G1–G6 cũ không bị xóa để bảo toàn lịch sử và khả năng kiểm toán.


## 2026-09-20 — phục hồi SR1 và kiểm toán trước mô hình

Đã hợp nhất lịch sử main/PR13 trong PR16 nháp, kiểm toán ZIP và sửa lỗi thu thập NSO. Run 35482892847 thu được toàn bộ nguồn trừ bước chuẩn hóa dân số; giữ CSV gốc để sửa parser tiêu đề Total/năm sơ bộ. Không mở khóa mô hình: cần xác minh tính nhất quán PCI, quần thể H4 và mẫu số tỷ suất lợi nhuận. Bằng chứng và giới hạn: `docs/research/RECOVERY_AUDIT_2026-09-20.md`.
