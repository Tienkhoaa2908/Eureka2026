# NEXT EXPERIMENT — SUBMISSION-PACKAGE-01

Priority: P0  
Gate: G7 Euréka submission

## Objective

Turn the validated G1–G6 evidence into an anonymous, internally consistent Euréka 2026 submission package without changing the scientific claims to make the story look stronger.

## Inputs

- `docs/submission/MANUSCRIPT_DRAFT.md`
- `docs/submission/SUBMISSION_PLAN.md`
- `docs/submission/NUMBER_TO_ARTIFACT_MAP.md`
- `docs/submission/ANONYMITY_CHECKLIST.md`
- G1–G5 QA and result artifacts
- official 2026 competition requirements in `docs/competition/EUREKA_2026.md`

## Procedure

1. Generate publication-ready figures/tables from committed result artifacts:
   - sample/data flow;
   - G3 coefficient plot;
   - G4 outer-year MAE comparison;
   - G5 CSTP5 robustness plot;
   - literature comparison table.
2. Freeze the manuscript result wording against `NUMBER_TO_ARTIFACT_MAP.md`.
3. Complete reference verification against primary/official source pages/DOIs.
4. Produce the anonymous formatted manuscript using official margins/font/spacing.
5. Produce the required portrait poster using the same bounded claims.
6. Run anonymity audit and metadata audit.
7. Run number-to-artifact audit: every quantitative statement must point to committed evidence.
8. Re-run code/static tests and confirm the current Git commit/CI.
9. Do not add SHAP/feature-importance figures; G4 gate failed.
10. Do not change “association” to “impact/effect” without a new identification design.

## Pass criteria

- manuscript has no unsupported causal/ranking language;
- all reported numeric claims match committed artifacts;
- all references resolve to intended sources;
- anonymous content has no author/institution/supervisor/logo/acknowledgement identifiers;
- format complies with official Euréka 2026 requirements;
- poster and manuscript tell the same scientific story;
- final code/tests/CI pass;
- current-state docs point to the exact final files.

## Output artifacts

- final anonymous manuscript source and PDF/DOCX as appropriate;
- final figures/tables;
- poster;
- final references;
- signed-off anonymity and number audits;
- `artifacts/qa/SUBMISSION-PACKAGE-01.md`.

## Current scientific story to preserve

A lagged CSTP5 association appears in the primary FE growth specification but is bounded by period/specification robustness and does not create stable incremental future-year predictive value beyond the best non-PCI baseline. This is the result, not a failure to obtain a desired ML ranking.
