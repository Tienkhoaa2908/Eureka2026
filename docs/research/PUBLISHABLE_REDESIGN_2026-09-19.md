# Publishable scientific redesign — 2026-09-19

Status: **active redesign; G7 submission packaging is paused until this redesign is evaluated.**

## 1. Why the current paper is not yet strong enough

The existing G3–G5 evidence is internally honest but scientifically narrow:

- one aggregate outcome (provincial enterprise revenue) mixes several mechanisms;
- aggregate revenue rises when there are more firms, when firms are larger, when labor productivity rises, or simply when nominal prices/sector composition change;
- the main CSTP5 association is positive in the prespecified lagged FE model but weakens/disappears in several alternative periods/specifications;
- lagged PCI does not add stable future-year predictive value beyond a strong non-PCI Elastic Net.

Therefore the publishable question should no longer be “which PCI component predicts revenue?” The next paper must explain **where institutional quality enters the enterprise-development process and which margin it changes**.

## 2. Proposed scientific question

### Working title

**Where Do Local Institutions Matter? Decomposing Enterprise Development into Entry, Scale, Productivity and Profitability Margins across Vietnamese Provinces**

Vietnamese working title:

**Cơ chế thể chế địa phương có bền vững theo thời gian? Phân rã tăng trưởng doanh nghiệp và kiểm chứng chéo quản trị cấp tỉnh tại Việt Nam giai đoạn 2015–2023**

Use “association / relationship / institutional channel” until a causal design is validated.

### Core research question

> Do improvements in business-facing local governance primarily appear on the **extensive margin** (more firms / firm entry) or the **intensive margin** (larger firms, higher revenue per worker, profitability and wages), and are these relationships corroborated by an independent citizen-facing governance measure?

This is materially more informative than ranking PCI components because different policy mechanisms imply different observable margins.

## 3. Scientific mechanism

A province’s aggregate enterprise revenue can be decomposed conceptually as:

`aggregate revenue = number of operating firms × revenue per operating firm`

and:

`revenue per operating firm = workers per firm × revenue per worker`

Thus log aggregate revenue can be interpreted through:

1. **Extensive margin / enterprise dynamism** — active firms, active firms per 1,000 population, entry rate, active-firm growth.
2. **Firm scale** — workers per firm, capital per firm, fixed assets per worker.
3. **Productivity / operating performance** — revenue per worker, revenue per firm, profit per firm, profit margin.
4. **Labor-value channel** — average monthly employee income.

This allows the project to answer *how* governance is related to business development, not merely whether aggregate revenue moves.

## 4. Theory-guided institutional channels

To avoid a 10 × many-outcome fishing exercise, primary hypotheses should be grouped ex ante.

### H1 — Market-entry / extensive-margin channel
Primary governance dimensions: CSTP1 Entry Costs, CSTP3 Transparency, CSTP10 Legal Institutions & Security.
Primary outcomes: new registrations relative to lagged active firms; active firms per 1,000 population.

### H2 — Transaction-cost / intensive-margin channel
Primary governance dimensions: CSTP4 Time Costs, CSTP5 Informal Charges.
Primary outcomes: revenue per worker, profit margin, revenue per firm.

### H3 — Capability-building channel
Primary governance dimensions: CSTP8 Business Support, CSTP9 Labor Training.
Primary outcomes: revenue per worker, employee income, capital/fixed assets per worker.

### H4 — Governance-validation / triangulation channel
Add PAPI dimensions: Control of Corruption in the Public Sector; Transparency in Local Decision-making; Public Administrative Procedures.
PCI is business-facing; PAPI is citizen-facing. Agreement across both is stronger construct-validity evidence than repeated PCI-only specifications.

## 5. New official data to acquire

The NSO PX-Web enterprise database contains province-year tables directly suitable for the mechanism decomposition.

### Enterprise stock / entry
- V05.04 — active enterprises at 31/12 by locality (2017–2024).
- V05.08 — active enterprises with production/business results by locality (2010, 2015–2023).
- V05.02 — newly registered enterprises by locality (2016–2024).

### Labor / scale
- V05.11 — total workers in active enterprises with business results by locality (2010, 2015–2023).
- V05.17 — annual average business capital by locality (2010, 2015–2023).
- V05.44 — fixed assets per worker by locality.

### Revenue / profit / labor value
- V05.23 — net business revenue by locality.
- V05.38 — pre-tax enterprise profit by locality.
- V05.41 — enterprise profitability ratio by locality (2010, 2015–2023).
- V05.35 — average monthly employee income by locality.

### Population denominator
Use NSO average population by province to construct firm density if the precomputed density series is not definition-compatible.

## 6. Proposed analysis window

Main mechanism panel: **2015–2023**, subject to 63-province completeness checks for every selected table.
Entry extension: **2017–2024** (or 2016–2024 where the denominator is available).

## 7. Statistical architecture

### 7.1 Outcome construction
- `log_firms = log(active firms with results)`
- `log_revenue_per_firm = log(revenue / active firms with results)`
- `log_workers_per_firm = log(workers / active firms with results)`
- `log_revenue_per_worker = log(revenue / workers)`
- `asinh_profit_per_firm = asinh(profit / active firms)`
- `profit_margin = profit / revenue`
- `log_capital_per_firm = log(capital / active firms)`
- `log_capital_per_worker = log(capital / workers)`
- `log_monthly_income = log(monthly income)`
- `entry_rate = new registrations / lagged active firms`

### 7.2 Primary estimator
`y_it = province_FE + year_FE + beta * governance_i,t-1 + error_it`

- lag governance one year;
- province-clustered uncertainty;
- no causal wording.

### 7.3 Within-year standardization
Construct year-specific z-scores/ranks for governance because PCI score dispersion and measurement can drift over time. Raw-score specifications remain robustness checks.

### 7.4 Within–between decomposition
For each key institutional channel, decompose governance into province mean + within-province deviation. This separates structural cross-province differences from a province’s own institutional improvement.

### 7.5 Distributed lags
Use lag 1 and lag 2 only for prespecified primary channels. Do not scan arbitrary lags.

### 7.6 Multiple testing
Apply BH FDR within prespecified hypothesis families rather than across an indiscriminate 10 × outcome grid.

### 7.7 Specification curves
For each primary hypothesis, predefine a specification multiverse: raw score vs within-year z-score; lag1 vs lag1+lag2; full period vs excluding 2020–2022; ratio level vs log/growth where meaningful; limited control variants.

### 7.8 Negative controls / falsification
Use future-governance leads, province-trajectory permutations preserving year structure, and theoretically defensible negative-control exposures.

### 7.9 Spatial sensitivity
Prior Vietnam evidence documents spatial spillovers, so test residual spatial/cross-sectional dependence and add spatial sensitivity only when diagnostics warrant it.

## 8. Preliminary diagnostics from the current 2014–2024 panel

These are exploratory diagnostics, not final paper results.

### CSTP5 within vs between
Single-component year-effects Mundlak-style decomposition on lagged CSTP5 and log-revenue change:
- standardized within-province coefficient ≈ **0.0151**, p≈**0.035**;
- between-province coefficient ≈ **-0.0021**, p≈**0.755**;
- approximately 73% of observed CSTP5 variance in the current lagged sample is within-province.

This is more consistent with a within-province movement signal than a simple cross-sectional “better provinces are richer” story, but it is not causal.

### Nonlinearity / pandemic interaction
Exploratory tests find no clear quadratic CSTP5 term (p≈0.216) and no clear CSTP5 × 2020–2022 interaction (p≈0.890). Do not manufacture a threshold or pandemic-resilience story from the current revenue-only panel.

### Component-ranking instability
CSTP5 has a single-component FE coefficient ≈0.0151 and a joint 10-component FE coefficient ≈0.0363. The joint coefficient remains ≈0.0319–0.0363 when other PCI components are removed one at a time. This reinforces moving from post-hoc component ranking to theory-guided mechanisms.

## 9. Novelty boundary after deeper literature review

Bach Ngoc Thang (2017) already studies how subnational governance relates to private-manufacturing **entry, firm size and labor-productivity growth** in Vietnam over 2006–2014. Thoa & Hung (2026) also study provincial market entry over 2017–2024.

Therefore this project must **not** claim that decomposing governance into entry/size/productivity channels is new by itself.

H1 entry becomes a replication/temporal-external-validity benchmark. The genuinely differentiated contribution, if supported by data, is:
- post-2015 temporal transportability of earlier institutional mechanisms;
- exact accounting decomposition of aggregate revenue growth into extensive and intensive margins using one matched province-year system;
- further decomposition of the intensive margin into workers-per-firm and revenue-per-worker;
- profitability, wage and capital-intensity extensions;
- within-versus-between institutional change;
- independent citizen-facing PAPI triangulation;
- prespecified falsification and multiplicity-aware evidence.

A stronger paper question is therefore: **which previously proposed institutional mechanisms persist in a later institutional/economic regime, and on which exact accounting margin do they appear?**

## 9B. What would make this publishable

A publishable result should be able to state something like:

> Provincial governance is not uniformly related to enterprise performance. Business-facing institutions appear on distinct margins: entry-oriented governance is associated with enterprise formation/density, while transaction-cost governance is more closely related to intensive operational outcomes. These relationships can be triangulated against citizen-facing governance measures, and aggregate revenue obscures this mechanism heterogeneity.

That is more scientifically meaningful than “CSTP5 is significant” or “XGBoost does not beat Elastic Net.”

## 10. Practical meaning

If governance improvement is associated mainly with:
- **entry / density:** focus on registration, licensing, transparency, legal predictability;
- **revenue per worker / profit:** focus on time costs, inspections, informal charges;
- **capital/labor intensity:** focus on training and business support;
- **citizen/business governance divergence:** diagnose implementation gaps experienced differently by firms and residents.

This creates a policy diagnostic matrix rather than the generic recommendation to “raise PCI”.

## 11. What not to do
- Do not add more ML algorithms for novelty.
- Do not run all ten PCI components against every new outcome and cherry-pick significant cells.
- Do not use aggregate PCI as the main exposure; composite PCI weights have historically been calibrated using economic-performance variables.
- Do not call PAPI/PCI coefficients causal effects.
- Do not package the current manuscript as final until the mechanism redesign is tested.

## 12. Current research decision

**Pause G7 packaging. Open SCIENCE-REDESIGN-01.**

The next large research run must acquire/validate the NSO mechanism datasets and PAPI data, build the mechanism panel, freeze hypothesis families before final coefficients are read, run the mechanism/triangulation models and specification curves, then decide whether the evidence supports a publication-quality paper.

## 13. Public sources verified for this redesign

- NSO enterprise table index: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/
- NSO V05.02: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.02.px/
- NSO V05.08: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.08.px/
- NSO V05.11: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.11.px/
- NSO V05.17: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.17.px/
- NSO V05.23: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.23.px/
- NSO V05.35: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.35.px/
- NSO V05.38: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.38.px/
- NSO V05.41: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.41.px/
- NSO V05.44: https://pxweb.nso.gov.vn/pxweb/vi/Doanh%20nghi%E1%BB%87p/Doanh%20nghi%E1%BB%87p/V05.44.px/
- PCI annual data: https://pcivietnam.vn/en/pci-data
- PCI methodology: https://www.pcivietnam.vn/en/about/pci-methodology.html
- PAPI annual Excel data: https://papi.org.vn/eng/papi-data/
- PAPI vs PCI comparison: https://papi.org.vn/eng/hoi-dap/giua-papi-va-pci-co-nhung-gi-tuong-dong-va-khac-biet/