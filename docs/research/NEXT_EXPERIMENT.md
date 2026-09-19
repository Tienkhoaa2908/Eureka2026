# NEXT EXPERIMENT — SCIENCE-REDESIGN-01

Priority: P0  
Gate: SR1 Scientific redesign / mechanism validity

## Question

Where does provincial governance appear in the enterprise-development process: firm entry/density, firm scale, productivity, profitability, or labor value?

The existing aggregate-revenue paper is not accepted as the final scientific contribution until this question is tested.

## New official inputs

NSO PX-Web:
- V05.02 newly registered enterprises;
- V05.08 active enterprises with business results;
- V05.11 enterprise workers;
- V05.17 business capital;
- V05.23 net revenue;
- V05.35 average monthly employee income;
- V05.38 pre-tax profit;
- V05.41 profitability ratio;
- V05.44 fixed assets per worker;
- provincial population for density normalization.

Governance:
- annual PCI component data;
- annual PAPI Excel data, with explicit time-comparability restrictions.

Source manifest:
`data/metadata/scientific_extension_sources.csv`.

## Phase A — acquisition/integrity

1. Download official source exports without manual transcription.
2. Save source metadata, table code, unit, update date, URL and SHA-256.
3. Normalize province names using the existing historical 63-province contract.
4. Verify 63-province coverage for each intended year.
5. Check table-definition compatibility before forming ratios.
6. Do not interpolate missing official years.

## Phase B — construct mechanism outcomes

Primary matched panel target: 2015–2023.

Construct:
- active firms;
- revenue per firm;
- workers per firm;
- revenue per worker;
- profit per firm (asinh);
- profit margin;
- capital per firm;
- capital per worker;
- employee income;
- firm density;
- entry rate in the separate 2017/2016–2024 extension where feasible.

Verify accounting identities and denominator consistency.

## Phase C — freeze hypotheses before final estimation

H1 Entry: CSTP1, CSTP3, CSTP10 → entry rate / firm density.
H2 Transaction costs: CSTP4, CSTP5 → revenue per worker / profit margin / revenue per firm.
H3 Capabilities: CSTP8, CSTP9 → productivity / wage / capital intensity.
H4 Triangulation: matched PAPI dimensions → selected mechanism outcomes.

No 10×outcome significance mining.

## Phase D — estimation

For each prespecified family:
- province FE + year FE;
- lagged governance;
- within-year governance z-score primary, raw score robustness;
- province-clustered inference;
- BH FDR within hypothesis family;
- within/between decomposition;
- lag1+lag2 sensitivity;
- strict pandemic exclusion;
- future-lead placebo;
- trajectory permutation;
- specification curve;
- residual cross-sectional/spatial diagnostic.

## Pass criteria

SR1 passes only if at least one scientifically interpretable mechanism is:
- directionally coherent with theory;
- supported by more than one outcome/specification or independent governance measure;
- not driven by one period/region/province;
- not contradicted by falsification tests;
- transparently bounded where evidence is weak.

A null mechanism result is acceptable; in that case the paper must be reframed around measurement limits / aggregate-outcome masking rather than force a policy claim.

## Expected artifacts

- raw-source manifest with hashes;
- canonical mechanism panel;
- data dictionary;
- hypothesis preregistration file;
- mechanism coefficient family tables;
- within/between results;
- specification curves;
- PAPI triangulation results;
- QA report `artifacts/qa/SCIENCE-REDESIGN-01.md`;
- revised integrated contribution;
- decision on whether G7 packaging resumes.

## Scientific stop rule

Do not resume final manuscript/poster formatting until SR1 is evaluated.
