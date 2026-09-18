# DATA-INTEGRITY-01 — Revenue lineage and correction audit

Date: 2026-09-18  
Gate: G1 Data integrity  
Verdict: **PASS with documented lineage caveat**

## Scope

Audit the 2010–2024 province-year enterprise net-revenue series before any final econometric or ML result is accepted.

Legacy workbook SHA-256:

`bbd5a7277b2473da49d7831fd1530a52a5563025f1d8aceadc3869cd0c40d345`

Locally corrected audit workbook SHA-256:

`959160fcaf1bccc3657c6f30032026bd2e31ab90a75540161376a67ca1a5180a`

The corrected binary workbook is a local audit artifact, not the canonical public data file. Corrections are encoded reproducibly in `src/eureka2026/revenue_corrections.py` and `data/metadata/revenue_corrections.csv`.

## Source blocks

| Years | Official/archived source | Table | Unit | Status |
|---|---|---:|---|---|
| 2010–2014 | NSO Statistical Yearbook 2015 + archived screenshots | 126 | Tỷ đồng | verified source block |
| 2015–2019 | NSO Statistical Yearbook 2020 + archived screenshots | 144 | Tỷ đồng | verified source block |
| 2020–2024 | archived GSO/NSO Table 151 screenshots + official NSO PX-Web series | 151 | Tỷ đồng | verified with lineage caveat |

The exact publication/page that produced the archived 2020–2024 Table 151 screenshot was not retained in the source bundle. The screenshot bytes are fingerprinted, the indicator/unit are traceable to the official NSO series, and 2020–2023 values were additionally cross-checked against NSO Statistical Yearbook 2024 Table 168. This caveat is documented rather than silently inferred.

Machine-readable lineage: `data/metadata/data_lineage.csv`.

## Three gross discrepancies resolved

The legacy notebook treated three large province-sum versus published-region-subtotal mismatches as possible source discrepancies. Direct re-reading of the archived tables and official NSO cross-checks showed that all three were province-level transcription errors in the derived panel:

| Province | Year | Legacy | Verified | Correction |
|---|---:|---:|---:|---:|
| Hòa Bình | 2016 | 23,040 | **33,040** | +10,000 |
| Gia Lai | 2023 | 133,195 | **131,195** | -2,000 |
| An Giang | 2023 | 212,941 | **212,961** | +20 |

The first correction resolves the previous -10,000 northern-region mismatch. The Gia Lai correction reduces the Tây Nguyên 2023 mismatch from +2,001 to +1. The An Giang correction reduces the Mekong 2023 mismatch from -21 to -1.

Across all 90 region-year subtotal checks after the three corrections:
- 47 are exact matches;
- 43 have small non-zero residuals;
- maximum absolute residual = 3;
- no residual exceeds 3.

Regional subtotals are QA checks only; the analysis unit remains province-year.

## Derived-variable impact

Because annual revenue growth is derived from revenue, it must be recomputed after corrections. The corrected values include:

| Province | Growth year | Corrected growth |
|---|---:|---:|
| Hòa Bình | 2016 | 27.97% |
| Hòa Bình | 2017 | 10.01% |
| Gia Lai | 2023 | 11.99% |
| Gia Lai | 2024 | 28.30% |
| An Giang | 2023 | 8.50% |
| An Giang | 2024 | 9.89% |

The correction module recomputes growth from corrected revenue rather than patching growth values independently.

## Structural checks carried forward

Previously verified panel invariants:
- 945 province-year rows = 63 provinces/cities × 15 years;
- province-year keys are complete for 2010–2024;
- full 10-subindex sample contains 756 rows for 2013–2024;
- lagged full-10-index sample contains 693 rows for 2014–2024;
- CSTP6 is structurally unavailable in 2010–2012 and must remain missing.

Automated source-independent invariant tests remain in `tests/test_validation.py`. Correction-specific tests are in `tests/test_revenue_corrections.py`.

## Evidence fingerprints

Revenue screenshot SHA-256:

- Table 151, screenshot 111051: `aa5a82cb6665ef5e89544e5e3af8404a96c200d267e3cb1a3b22f01ec3a0a2c7`
- Table 151, screenshot 111059: `809f364155d2a73f9e604df447c97a4c091bcba50b12f1e8794157c2e634de0f`
- Table 144, screenshot 112820: `d07f1a8c6a2aa904dc1656e7269961940218653cb6c3f1043f64f0b00b795a7f`
- Table 144, screenshot 112830: `341c27af9b6746484f64e22f1d58c360d773bd59285717e4dfbb1be2aec5b681`
- Table 126, screenshot 113159: `e2d46dd2c825e7f73e78d005d0c12bf4988b89f9496cae01bb4457c254619900`
- Table 126, screenshot 113212: `fa15736dcb1e61497852a9b382adda3edc4e03b826911ee1a6cd29c9698748e8`

## Gate decision

G1 passes because the gross discrepancies are resolved, correction logic is explicit and testable, source blocks are documented, structural missingness is preserved, and no unexplained large subtotal inconsistency remains.

The 2020–2024 Table 151 publication/page metadata gap remains a documentation caveat. G2 must now build a deterministic raw → corrected clean → model pipeline and eliminate legacy absolute paths before final model estimation.
