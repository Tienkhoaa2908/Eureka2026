# PUBLICATION PIVOT — institutions and the margins of enterprise development

Updated: 2026-09-19  
Status: ACTIVE scientific redesign before final submission freeze

## 1. Why the current paper is not yet publication-strong

The existing project is methodologically careful, but its main outcome—aggregate nominal enterprise revenue by province—bundles together several economically different mechanisms:

```
total enterprise revenue
= number of operating/reporting firms
× workers per firm
× revenue per worker
```

Therefore a coefficient on aggregate revenue cannot tell whether better local governance is associated with:

1. more firms entering/formalizing/remaining active (**extensive margin**);
2. firms becoming larger in employment (**scale margin**); or
3. higher revenue generated per worker (**intensive/performance margin**).

This ambiguity is now the central scientific weakness. Running more ML on the same aggregate outcome does not solve it.

## 2. Publication-grade research question

> **At which margin of enterprise development does provincial economic governance show up in Vietnam: entry/formalization, operating-firm scale, or revenue generated per worker; and are these relationships stable across institutional dimensions, periods and regional shocks?**

This question is scientifically different from “which PCI component predicts revenue most?”

## 3. Theoretical mechanism

Entry-regulation theory predicts that regulatory frictions can change the creation/formalization of firms and the competitive pressure faced by incumbents. Djankov et al. (2002) document that heavier entry regulation is associated with corruption and larger unofficial economies. Klapper, Laeven & Rajan (2006) show that costly entry regulation suppresses new firm creation and can also reduce incumbent dynamism.

That creates a natural distinction:

### Extensive margin
Governance may reduce the fixed/administrative cost of becoming or remaining a formal operating enterprise.

Observable outcomes:
- new enterprise registrations;
- active firms per 1,000 residents;
- growth in operating firms with business results.

### Scale margin
Governance may affect firms' ability to expand employment.

Observable outcome:
- workers per operating/reporting firm.

### Intensive margin
Governance may affect efficiency, market access, transaction costs or resource allocation among firms already operating.

Observable outcomes:
- revenue per worker;
- revenue per operating/reporting firm;
- profit rate / pretax profit as supplementary outcomes.

## 4. Exact accounting decomposition

Using a common NSO enterprise universe:

- F_it = operating enterprises with business results;
- L_it = workers in those enterprises;
- R_it = net business revenue of those enterprises.

Then:

```
R_it = F_it × (L_it / F_it) × (R_it / L_it)
```

Taking log differences:

```
Δlog R_it
= Δlog F_it
+ Δlog(L_it/F_it)
+ Δlog(R_it/L_it)
```

If the same sample and the same linear FE design matrix are used for all four outcomes, the estimated PCI coefficient obeys the same additive decomposition (up to numerical precision):

```
β_total = β_firm_count + β_workers_per_firm + β_revenue_per_worker
```

This converts the current aggregate-revenue association into a mechanism decomposition rather than a feature ranking.

## 5. How this reconciles the Vietnam literature

The recent evidence is not actually asking one common question:

- Thoa & Hung (2026) report PCI-component relationships with **firm market entry**.
- Huynh (2022) reports direct and spatial relationships with **profits/TFP**.
- the 2024 TFP study finds Time Costs and Labor Policy prominent for **firm productivity**.
- Kokko, Nguyen & Nilsson Hakkala (ADB, 2026) report limited PCI effects on several provincial manufacturing **revenue/employment/productivity** outcomes.

A plausible scientific synthesis is that institutions can operate differently on the extensive and intensive margins. The new design tests that proposition directly rather than treating mixed prior findings as noise.

## 6. New hypotheses — fixed before inspecting the new outcomes

### H1 — extensive-margin channel
Lagged improvements in business-governance quality are more likely to be reflected in entry/formalization outcomes than in aggregate revenue alone.

Theory-facing dimensions:
- CSTP1 Entry Costs;
- CSTP5 Informal Charges;
- CSTP10 Legal Institutions/Security.

### H2 — intensive-margin channel
Conditional relationships with revenue per worker/profitability may differ from relationships with firm entry/density.

Literature-facing dimensions:
- CSTP4 Time Costs;
- CSTP5 Informal Charges;
- CSTP9 Labor Policy;
- CSTP10 Legal Institutions/Security.

### H3 — channel decomposition
Any aggregate-revenue association should be decomposable into operating-firm count, workers-per-firm and revenue-per-worker components. A large extensive-margin contribution would imply a different policy mechanism from a large revenue-per-worker contribution.

### H4 — regional-shock robustness
A publishable institutional signal should not be wholly explained by region-specific year shocks or smooth province-specific trends.

## 7. Confirmatory hierarchy

To avoid turning the enlarged dataset into a specification search:

1. run joint PCI-block tests for each prespecified outcome;
2. component-level inference only follows the prespecified hierarchy and uses BH FDR;
3. report failures as prominently as successes;
4. main FE uses province + year effects;
5. region×year FE and province-specific trends are robustness designs;
6. first-difference institutional-change specifications are secondary;
7. ML remains a prediction appendix unless it answers a distinct prospective question.

## 8. What the current CSTP5 result becomes

The existing CSTP5 result is no longer the paper's “answer.”

It becomes a **discovery fact**:

> Lagged CSTP5 is positively associated with aggregate revenue growth in the primary 2014–2024 FE specification, but the signal is period/specification bounded and does not add stable future-year forecast value.

The new multi-margin data will test where that aggregate association comes from. If it is mostly firm-count growth, the mechanism is extensive. If mostly revenue per worker, it is intensive. If neither replicates, the aggregate result is likely too unstable for a strong publication claim.

## 9. Practical meaning

The policy implication depends on the channel:

- **entry/formalization channel:** simplify procedures, reduce informal payments, strengthen predictable/legal administration;
- **scale channel:** governance may help firms expand employment but does not by itself identify the complementary constraint;
- **revenue-per-worker channel:** stronger evidence for an intensive business-performance mechanism;
- **entry-only with weak intensive response:** institutional reform may expand the formal business base without automatically raising incumbent productivity; complementary finance, skills, technology or market-linkage policies would then remain necessary.

These are hypotheses/interpretations until the new outcome analysis is completed.

## 10. Publication criterion

The upgraded paper is worth submitting to a journal only if it can make a bounded claim such as:

> “Subnational governance is associated with a specific margin of enterprise development, and an accounting/econometric decomposition explains why aggregate revenue results differ from entry/productivity evidence.”

If the new outcomes show no stable channel, the honest scientific contribution becomes a carefully documented null/instability result rather than an artificial PCI ranking.
