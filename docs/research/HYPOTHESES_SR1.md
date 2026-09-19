# SR1 hypothesis freeze — enterprise-development mechanisms

Frozen before the SR1 online workflow is run against final acquired outcome data.

Date: 2026-09-19  
Status: **FROZEN FOR PRIMARY SR1 TESTS**

## Scientific target

Test where business-facing provincial governance is associated with enterprise development rather than asking which of ten PCI components is globally “best”.

Primary exposure convention:
- one-year-lagged PCI sub-index;
- standardized within calendar year across provinces;
- higher score is interpreted according to PCI’s favorable orientation for that sub-index.

Primary estimator:
- province fixed effects;
- year fixed effects;
- province-clustered inference;
- family-wise Benjamini–Hochberg FDR.

No causal claim is authorized by this design.

## H1 — Market-entry / extensive-margin family

Theory: lower administrative/information/legal frictions should first appear in the creation and density of enterprises.

Prespecified tests (6):
- CSTP1 Entry Costs → entry rate;
- CSTP3 Transparency → entry rate;
- CSTP10 Legal Institutions & Security → entry rate;
- CSTP1 Entry Costs → log active enterprises per 1,000 people;
- CSTP3 Transparency → log active enterprises per 1,000 people;
- CSTP10 Legal Institutions & Security → log active enterprises per 1,000 people.

Panel: entry extension, target years 2018–2024.

## H2 — Transaction-cost / intensive-margin family

Theory: time burdens and informal charges should be more directly visible in the operating intensity and profitability of incumbent firms than in aggregate provincial scale.

Prespecified tests (6):
- CSTP4 Time Costs → log revenue per worker;
- CSTP5 Informal Charges → log revenue per worker;
- CSTP4 Time Costs → constructed profit margin;
- CSTP5 Informal Charges → constructed profit margin;
- CSTP4 Time Costs → log revenue per firm;
- CSTP5 Informal Charges → log revenue per firm.

Panel: matched enterprise-results panel, target years 2015–2023.

## H3 — Capability-building family

Theory: business-support and labor-policy institutions should be reflected in productivity, labor value and capital intensity.

Prespecified tests (6):
- CSTP8 Business Support → log revenue per worker;
- CSTP9 Labor Policy → log revenue per worker;
- CSTP8 Business Support → log average monthly employee income;
- CSTP9 Labor Policy → log average monthly employee income;
- CSTP8 Business Support → log capital per worker;
- CSTP9 Labor Policy → log capital per worker.

Panel: matched enterprise-results panel, target years 2015–2023.

## Exact accounting decomposition — prespecified mechanism anatomy

This analysis is not a search across outcomes; it exploits an exact accounting identity:

[
Deltalog Revenue =
Deltalog Firms +
Deltalog RevenuePerFirm
]

and

[
Deltalog RevenuePerFirm =
Deltalog WorkersPerFirm +
Deltalog RevenuePerWorker.
]

For CSTP4 and CSTP5, estimate the same two-way-FE design on all five terms using the identical balanced sample. By OLS linearity, coefficient additivity is required up to numerical tolerance.

Purpose:
- determine whether any transaction-cost association with aggregate revenue growth appears primarily through the extensive margin, firm scale, or revenue-per-worker margin;
- avoid attributing an aggregate revenue coefficient to “productivity” without decomposition.

The decomposition is descriptive/mechanistic association, not mediation causality.

## Robustness frozen before primary results

For each H1–H3 pair:
1. raw PCI score instead of within-year z-score;
2. contemporaneous year-z exposure;
3. exclude outcome years 2020–2022;
4. distributed lag with t-1 and t-2 governance;
5. future t+1 governance lead placebo;
6. within-versus-between decomposition;
7. leave-one-province and leave-one-year coefficient ranges;
8. 199 province-trajectory permutations preserving the time structure;
9. joint exposure specification within the same theory family/outcome.

## Evidence rule

A cell is **not** promoted to a scientific finding merely because p<0.05.

A mechanism may enter the main paper only when:
- family BH q<0.05 in the prespecified primary test;
- direction is coherent with the stated mechanism;
- the sign is not driven by one province or one year;
- future-lead placebo does not show a comparably strong contradictory signal;
- trajectory-permutation evidence is not inconsistent with the claimed signal;
- important failures in raw/current/strict-period/distributed-lag specifications are explicitly reported.

Multiple coherent outcomes in the same theory family strengthen the mechanism interpretation. Isolated significance weakens it.

## H4 — PAPI triangulation

PAPI remains a **secondary validation layer**, not part of the 18 PCI primary tests above.

It will be frozen separately only after:
- exact PAPI series/definitions are retrieved;
- temporal comparability is established for the selected dimensions;
- no SR1 outcome coefficients are used to choose which PAPI dimensions to test.

Candidate constructs, subject to definition stability:
- Control of Corruption in the Public Sector;
- Transparency in Local Decision-making;
- Public Administrative Procedures.

This separation prevents the PAPI stage from becoming post-hoc confirmation mining.

## Stop rule

If H1–H3 do not yield coherent, robustness-supported mechanisms, the paper must not invent one. The scientific contribution will instead be reframed around the limits of aggregate institutional indicators and the failure of institutional scores to map robustly onto decomposed enterprise margins.
