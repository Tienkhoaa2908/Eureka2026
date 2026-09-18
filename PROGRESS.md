# PROGRESS

## 2026-09-18

Completed:
- Recovered and audited the uploaded project bundle and project description.
- Verified the 63 × 15 panel shape and full 10-subindex panel shape.
- Identified notebook syntax defects and non-portable hardcoded paths.
- Reframed the research question from unsupported causal ranking to panel inference + out-of-sample prediction.
- Reviewed official Euréka 2026 timeline, scoring criteria, report structure, formatting, and anonymization constraints.
- Reviewed recent Euréka economics themes and relevant Vietnam PCI/institution literature.
- Bootstrapped GitHub research-OS structure.
- Completed **DATA-INTEGRITY-01**:
  - traced 2010–2014 revenue to Table 126;
  - traced 2015–2019 revenue to Table 144;
  - documented archived 2020–2024 Table 151 evidence and official NSO series;
  - identified and encoded three source-backed transcription corrections;
  - recomputed affected revenue-growth values in the audit workbook;
  - added machine-readable lineage/correction registries;
  - reduced all 90 regional subtotal QA residuals to absolute value ≤ 3.
- Added correction code and correction-specific tests.

In progress:
- G2 reproducible raw → clean → model pipeline.
- Literature matrix and final method specification.

Blocked:
- Final FE/model results remain blocked until G2 passes.
- Causal language remains blocked until a defensible identification strategy exists.

Current next action:
Execute `docs/research/NEXT_EXPERIMENT.md` (REPRO-PIPELINE-01).
