# PROGRESS

## 2026-09-18

Completed:
- Recovered and audited the uploaded project bundle and project description.
- Reframed the research question from unsupported causal ranking to panel inference + out-of-sample prediction.
- Reviewed official Euréka 2026 requirements and recent competition/literature context.
- Bootstrapped GitHub research-OS structure.
- Completed **G1 DATA-INTEGRITY-01**:
  - documented revenue source blocks;
  - corrected three source-backed transcription errors;
  - added machine-readable lineage/correction registries.
- Completed **G2 REPRO-PIPELINE-01**:
  - built one-command repository-relative canonical pipeline;
  - generated stable 945-row output;
  - added explicit province/merge/missingness tests.
- Completed **G3 STAT-BASELINE-01**:
  - implemented two-way FE with province-clustered cluster-t inference;
  - standardized all 10 lagged PCI components reproducibly;
  - added BH FDR multiplicity adjustment;
  - generated full and no-2020/2021 outcome specifications;
  - generated leave-one-province-out sensitivity;
  - found no multiplicity-adjusted component in the log-level outcome;
  - found CSTP5 as the only BH-adjusted association in the log-change outcome, stable in the recorded COVID and province-omission sensitivities;
  - expanded local suite to 15 passing tests before PR.
- Completed **G4 PRED-BENCHMARK-01**:
  - six fixed expanding test years 2019–2024;
  - nested temporal tuning and leakage tests;
  - Elastic Net, RF and XGBoost with/without PCI;
  - negative incremental-PCI result beyond the strongest non-PCI baseline;
  - feature-importance gate failed, so no ranking was produced.
- Completed **G5 ROBUSTNESS-01**:
  - strict pandemic exclusion;
  - contemporaneous and longer-period specifications;
  - winsorization;
  - distributed lag and future-lead placebo;
  - leave-one-year and leave-one-region checks;
  - residual dependence diagnostic.
- Completed **G6 scientific contribution synthesis**:
  - verified literature matrix;
  - integrated G3–G5 narrative;
  - full research-content manuscript draft;
  - number-to-artifact and anonymity checklists.

In progress:
- G7 final Euréka submission package: figures/tables, formatted anonymous manuscript, poster and final audits.

Blocked:
- Causal language remains blocked.
- Feature-importance ranking remains blocked by the negative G4 incremental-value gate.
- Scale-normalized outcome robustness requires new verified denominator/price data and is not required for the current canonical result.

Current next action:
Execute `docs/research/NEXT_EXPERIMENT.md` (SUBMISSION-PACKAGE-01).

## 2026-09-19 — publication-quality redesign

Completed:
- re-evaluated whether the existing G3–G6 story is strong enough for publication;
- concluded that aggregate revenue obscures economically distinct enterprise-development margins;
- verified additional official NSO PX-Web tables for enterprise entry, active firms, labor, capital, revenue, wages, profit, profitability and fixed assets per worker;
- verified annual PAPI Excel availability for 2011–2024 and its independent citizen-facing governance role;
- reviewed recent Vietnam literature on spatial institutional effects, market entry, TFP, PCI/PAPI alignment and provincial manufacturing outcomes;
- ran exploratory current-panel diagnostics: within/between CSTP5, quadratic nonlinearity, pandemic interaction and component-control stability;
- created docs/research/PUBLISHABLE_REDESIGN_2026-09-19.md;
- created data/metadata/scientific_extension_sources.csv;
- paused G7 packaging and activated SR1 SCIENCE-REDESIGN-01.

Current action:
Acquire and validate the official NSO/PAPI extension data, freeze mechanism hypotheses, then run the full mechanism/triangulation design in one research cycle.


## 2026-09-20 — đóng hướng cũ, chuyển hoàn toàn sang nghiên cứu cơ chế

Đã hoàn thành:
- đóng vĩnh viễn câu hỏi xếp hạng thành phần PCI theo doanh thu và hướng học máy (machine learning — học máy) làm đóng góp trung tâm;
- khóa câu hỏi nghiên cứu mới về tính bền vững theo thời gian của các cơ chế thể chế sau năm 2015;
- xác định các biên kết quả chính: gia nhập, mật độ, quy mô, doanh thu trên lao động, lợi nhuận, thu nhập lao động và cường độ vốn;
- đưa phân rã kế toán doanh thu vào lõi phương pháp;
- chuyển các kết quả G3–G6 cũ sang trạng thái tư liệu kiểm toán;
- đặt hiệu ứng cố định hai chiều, hiệu chỉnh đa kiểm định, phân rã trong/giữa tỉnh, độ trễ và phản chứng làm khung ước lượng chính;
- yêu cầu chẩn đoán trước khi mở mô hình không gian, bảng động hoặc phương pháp phức tạp hơn.

Việc tiếp theo duy nhất:
- hoàn tất SR1: khóa dữ liệu chính thức NSO/PCI/PAPI và dựng bảng cơ chế có thể tái tạo trước khi đọc kết quả cuối.
