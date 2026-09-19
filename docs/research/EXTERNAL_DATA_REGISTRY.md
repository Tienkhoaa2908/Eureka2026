# EXTERNAL DATA REGISTRY — publication extension

Updated: 2026-09-19

Primary source family: Vietnam NSO/GSO PX-Web enterprise database.

A third-party Hugging Face mirror may be used only as an ingestion convenience. Final lineage and spot checks must resolve to the official NSO matrix IDs/pages. The mirror is not a substitute for official-source verification.

## Priority A — exact multi-margin decomposition

| ID | Official variable | Unit | Scientific role | Planned transformation |
|---|---|---|---|---|
| V05.08 | Operating enterprises with business results at 31/12 by province | enterprises | extensive operating-firm stock F | log F, Δlog F |
| V05.11 | Workers in operating enterprises with business results by province | persons | labor scale L | log L; workers/firm = L/F |
| V05.23 | Net business revenue of operating enterprises with business results by province | billion VND | aggregate business outcome R | log R; revenue/worker = R/L; revenue/firm = R/F |

Official PX-Web shows V05.11 and V05.23 with years 2010 and 2015–2023. V05.08 reports 10 years and must be checked at ingestion for the exact identical year list before deriving ratios.

Primary continuous target window if all three align: **2015–2023**.

Exact identity:

`log R = log F + log(L/F) + log(R/L)`.

## Priority A — entry/formalization

| ID | Official variable | Unit | Role |
|---|---|---|---|
| V05.02 | Newly registered enterprises by province | enterprises | gross entry flow |
| V05.04 | Active enterprises at 31/12 by province | enterprises | active-enterprise stock |
| V05.05 | Active enterprises per 1,000 residents by province | enterprises / 1,000 residents | scale-normalized business density |

V05.05 officially lists 2017–2024. V05.02 contains nine years and V05.04 eight years; exact year lists must be captured in the ingestion metadata before model specification.

Derived candidate:
`entry_rate_t = new_registrations_t / active_enterprises_{t-1}`.

Do not call this a survival-adjusted entry rate; it is a registration flow normalized by the prior active stock.

## Priority B — profitability/capital validation

| ID | Official variable | Unit | Role |
|---|---|---|---|
| V05.38 | Pretax profit by province | published unit to verify | intensive profitability |
| V05.41 | Profit rate by province | % | scale-free profitability |
| V05.17 | Average annual business capital by province | billion VND | capital intensity |
| V05.20 | Fixed assets + long-term financial investment by province | billion VND | asset intensity |
| V05.35 | Average monthly employee income by province | published unit to verify | labor-income outcome |

V05.17 officially lists 2010 and 2015–2023. V05.20/V05.38/V05.41/V05.35 are listed by NSO as province-year enterprise matrices; exact year lists and units must be captured before use.

Derived candidates:
- capital per reporting firm = V05.17 / V05.08;
- fixed assets per worker = V05.20 / V05.11;
- pretax profit per reporting firm = V05.38 / V05.08.

## Priority B — macro controls

| ID | Variable | Role |
|---|---|---|
| V03.10 | GRDP growth index at constant 2010 prices by province | local demand/business-cycle control |
| V03.12 | GRDP per capita by province | development-level robustness |
| V02.03-07 / related population tables | average population by province | denominator/source cross-check |

Do not mechanically control for variables that could themselves be mediators. Each control must have a causal role stated before inclusion.

## Priority C — structure/heterogeneity

| ID | Variable | Coverage caveat |
|---|---|---|
| V05.26 | Firms by employment-size class and province | official page currently shows 2021–2023 only |
| V05.29 | Firms by capital-size class and province | verify exact year coverage |

These are useful for recent descriptive heterogeneity, not for the main long-panel identification unless coverage improves.

## Source pages verified in the research scan

- V05.02: official NSO PX-Web, new registrations by province.
- V05.05: official NSO PX-Web, active firms per 1,000 residents; 2017–2024 displayed.
- V05.08: official NSO PX-Web, operating firms with business results by province.
- V05.11: official NSO PX-Web, workers by province; 2010, 2015–2023 displayed.
- V05.17: official NSO PX-Web, average business capital; 2010, 2015–2023 displayed.
- V05.20: official NSO PX-Web, fixed assets/long-term investment by province.
- V05.23: official NSO PX-Web, net business revenue; 2010, 2015–2023 displayed.
- V05.26: official NSO PX-Web, employment-size distribution; 2021–2023 displayed.
- V05.41: official NSO PX-Web, profit rate by province.
- V03.10: official NSO PX-Web, constant-price GRDP growth by province.
- V03.12: official NSO PX-Web, GRDP per capita by province.

## Ingestion contract

Every imported matrix must store:

- matrix ID;
- official title;
- official source URL;
- retrieval date;
- published unit;
- exact year list;
- raw province labels;
- raw-file SHA-256;
- parser version;
- canonical province match coverage;
- missingness summary;
- spot checks against official PX-Web values.

No derived outcome enters a regression before these checks pass.

## Critical consistency rule

The decomposition R = F × (L/F) × (R/L) is valid only if V05.08, V05.11 and V05.23 refer to the same enterprise universe and year definition. Their titles all refer to enterprises operating with business results, but this must be verified in metadata/notes before the identity is treated as publication evidence.
