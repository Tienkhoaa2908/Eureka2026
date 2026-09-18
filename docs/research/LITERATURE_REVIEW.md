# Literature review map — PCI, institutions, and enterprise outcomes

Updated: 2026-09-18

The detailed structured evidence table now lives in `docs/research/LITERATURE_MATRIX.md`.

## Core measurement

PCI/VCCI constructs PCI from business survey data and published sources, standardizes ten sub-indices to a 10-point scale, and calibrates the composite PCI from those dimensions.

Sources:
- https://pcivietnam.vn/en/about/pci-methodology.html
- https://pcivietnam.vn/en/faqs.html

For CSTP5, stronger performance corresponds to **minimal informal charges**, so coefficient signs must be interpreted using that orientation.

## Closest empirical evidence

### Nguyen, Le & Bryant (2013)
Journal of World Business, DOI 10.1016/j.jwb.2012.06.008.  
Multilevel private-manufacturing evidence shows subnational institutional conditions matter for firm strategy/performance relationships.

### Huynh (2022)
Asian-Pacific Economic Literature, DOI 10.1111/apel.12362.  
Spatial Durbin analysis, 2011–2018. Reports direct/spatial institutional relationships; control of corruption is positively related to profits and informal charges negatively to TFP. Motivates spatial caution.

### Asia-Pacific Journal of Regional Science (2024)
“Total factor productivity and institutional quality in Vietnam: which institutions matter most?” DOI 10.1007/s41685-024-00343-9.  
Component patterns are outcome/specification-specific; time costs and labor policy are prominent in important TFP specifications.

### Kokko, Nguyen & Nilsson Hakkala (ADB, 2026)
DOI 10.22617/WPS260325-2.  
63-province evidence reports that PCI changes have limited effects on several manufacturing outcomes in many specifications. This makes weak/null results scientifically plausible rather than anomalous.

### Thoa & Hung (2026)
Hue University Journal of Science, DOI 10.26459/hueunijed.v135i5C.8471.  
FE + clustered SE on 2017–2024 market entry. Component significance differs between current and lagged models; informal charges is significant in the lagged model while legal institutions/security is described as the most stable dimension.

## Method references

- Zou & Hastie (2005), Elastic Net, DOI 10.1111/j.1467-9868.2005.00503.x.
- Breiman (2001), Random Forests, DOI 10.1023/A:1010933404324.
- Chen & Guestrin (2016), XGBoost, DOI 10.1145/2939672.2939785.
- Tashman (2000), out-of-sample forecasting tests, DOI 10.1016/S0169-2070(00)00065-0.

## Gap the project can defend

Do not claim that PCI and firm performance have not been studied.

The defensible gap is methodological and evidential:
- prior Vietnam studies use different units, outcomes and estimators and produce mixed component patterns;
- strict future-year out-of-sample validation is usually not the same exercise as FE inference;
- the project compares the two on one audited long panel and adds falsification/robustness to define the boundary of any apparent signal.

## Integrated position

G3–G5 support a bounded conclusion: CSTP5 has a lagged association in the primary growth specification, but the signal is period/specification-sensitive and does not add stable forecast value beyond the best non-PCI baseline.

That distinction, not a model/feature ranking, is the central contribution.
