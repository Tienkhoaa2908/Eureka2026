# Number-to-artifact audit

Updated: 2026-09-18

Every quantitative claim intended for the manuscript must map to a committed reproducibility artifact.

| Claim | Value | Artifact |
|---|---|---|
| Canonical panel rows | 945 | `data/metadata/canonical_build_manifest.json` |
| Province count | 63 | `data/metadata/canonical_build_manifest.json` |
| Full 10-CSTP contemporaneous N | 756 | `data/metadata/canonical_build_manifest.json` |
| Full lagged 10-CSTP N | 693 | `data/metadata/canonical_build_manifest.json` |
| Canonical SHA-256 | a5b76b...211dd | `data/metadata/canonical_build_manifest.json` |
| Hòa Bình 2016 correction | 23,040 → 33,040 | `data/metadata/revenue_corrections.csv` |
| Gia Lai 2023 correction | 133,195 → 131,195 | `data/metadata/revenue_corrections.csv` |
| An Giang 2023 correction | 212,941 → 212,961 | `data/metadata/revenue_corrections.csv` |
| G3 CSTP5 beta | 0.03628 | `artifacts/results/STAT-BASELINE-01_coefficients.csv` |
| G3 CSTP5 95% CI | [0.01852, 0.05404] | same |
| G3 CSTP5 p / q | 0.000129 / 0.001289 | same |
| G3 implied exp(beta)-1 | 3.69% | same |
| G4 best change MAE | 0.08819, Elastic Net non-PCI | `artifacts/results/PRED-BENCHMARK-01_aggregate.csv` |
| RF PCI same-family improvement | 8.12%; 5/6 folds | `artifacts/results/PRED-BENCHMARK-01_pci_increment.csv` |
| RF+PCI gap vs non-PCI Elastic Net | ~7.98% worse | `artifacts/results/PRED-BENCHMARK-01_aggregate.csv` |
| G4 best level MAE | 0.08859, Elastic Net non-PCI | same |
| Strict-COVID CSTP5 beta/q | 0.03316 / 0.06720 | `artifacts/results/ROBUSTNESS-01_coefficients.csv` |
| Longer-period CSTP5 beta/q | 0.01170 / 0.31121 | same |
| Contemporaneous CSTP5 p | 0.99419 | same |
| Winsorized CSTP5 beta/q | 0.03416 / 0.001491 | same |
| CSTP5 lag1 / lag2 | 0.02514 / -0.00480 | `artifacts/results/ROBUSTNESS-01_cstp5_targeted.csv` |
| Future-lead placebo p | 0.47656 | same |
| Leave-one-year beta range | [0.03191, 0.04924] | `artifacts/results/ROBUSTNESS-01_year_loo.csv` |
| Leave-one-region beta range | [0.02907, 0.03990] | `artifacts/results/ROBUSTNESS-01_region_loo.csv` |
| Pesaran CD / p | -1.3853 / 0.1660 | `artifacts/results/ROBUSTNESS-01_metadata.json` |

Rules:
1. Never copy a number into the final manuscript from chat memory.
2. Prefer the committed artifact as source of truth.
3. If a number changes after rerun, update the manuscript and this audit together.
4. Rounded manuscript values must retain enough precision to reproduce the interpretation.
