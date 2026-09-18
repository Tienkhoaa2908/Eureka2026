# Literature matrix — institutions, PCI and enterprise outcomes

Updated: 2026-09-18

This matrix is used to position the Euréka contribution. It is deliberately outcome- and method-specific; it does not imply that prior studies estimate the same estimand.

| Study | Data / unit | Method | Outcome / focus | Result relevant to this project |
|---|---|---|---|---|
| Nguyen, Le & Bryant (2013), Journal of World Business, DOI 10.1016/j.jwb.2012.06.008 | private manufacturing firms in Vietnam; multilevel firm/subnational setting | multilevel analysis | export strategy and firm performance | subnational institutional conditions moderate firm-strategy/performance relationships; supports separating province context from firm outcomes |
| Huynh (2022), Asian-Pacific Economic Literature, DOI 10.1111/apel.12362 | enterprise survey data, provinces, 2011–2018 | Spatial Durbin Model | firm performance, profit, TFP | reports direct/spatial institutional effects; control of corruption is positively related to profits and informal charges negatively to TFP; motivates spatial-dependence caution |
| “Total factor productivity and institutional quality in Vietnam: which institutions matter most?” (2024), Asia-Pacific Journal of Regional Science, DOI 10.1007/s41685-024-00343-9 | Vietnamese firms | panel/GMM design | TFP | component patterns differ; time costs and labor policy are prominent in reported specifications; supports outcome-specific rather than universal ranking |
| Kokko, Nguyen & Nilsson Hakkala (ADB, 2026), DOI 10.22617/WPS260325-2 | 63 provinces | difference-GMM / provincial manufacturing analysis | complexity, revenue, employment, productivity | reports limited effects of PCI changes on several provincial manufacturing outcomes in many specifications; directly supports testing weak/null institutional signals rather than assuming positive effects |
| Thoa & Hung (2026), Hue University Journal of Science, DOI 10.26459/hueunijed.v135i5C.8471 | provinces, 2017–2024 | FE + clustered robust SE; lagged model | firm market entry | component significance changes across contemporaneous/lagged models; informal charges is significant in lagged model while legal institutions/security is described as most stable across models |
| PCI/VCCI methodology | provincial business survey + published data | ten standardized sub-indices + weighted composite | economic governance | confirms the ten dimensions and that high CSTP5 corresponds to minimal informal charges |

## Method references used by the design

- Zou, H. & Hastie, T. (2005). “Regularization and variable selection via the elastic net.” JRSS B 67(2): 301–320. DOI: 10.1111/j.1467-9868.2005.00503.x.
- Breiman, L. (2001). “Random Forests.” Machine Learning 45: 5–32. DOI: 10.1023/A:1010933404324.
- Chen, T. & Guestrin, C. (2016). “XGBoost: A Scalable Tree Boosting System.” KDD 2016: 785–794. DOI: 10.1145/2939672.2939785.
- Tashman, L.J. (2000). “Out-of-sample tests of forecasting accuracy: an analysis and review.” International Journal of Forecasting 16(4): 437–450. DOI: 10.1016/S0169-2070(00)00065-0.

## Verified public source links

- PCI methodology: https://pcivietnam.vn/en/about/pci-methodology.html
- PCI FAQ / interpretation: https://pcivietnam.vn/en/faqs.html
- Nguyen et al. 2013: https://doi.org/10.1016/j.jwb.2012.06.008
- Huynh 2022: https://doi.org/10.1111/apel.12362
- TFP/institutions 2024: https://doi.org/10.1007/s41685-024-00343-9
- ADB 2026: https://www.adb.org/publications/business-climate-economic-complexity-performance-provincial-viet-nam
- Thoa & Hung 2026: https://doi.org/10.26459/hueunijed.v135i5C.8471

## Gap supported by the matrix

The defensible gap is **not** “PCI and firm performance have never been studied.” Prior evidence is substantial and mixed.

The project’s contribution is narrower: on a long province panel, use the same audited institutional data to separate (1) within-province association, (2) future-year generalization, and (3) robustness/falsification. The resulting evidence can show that a statistically detectable institutional relationship need not deliver incremental forecasting value.

This distinction is both methodologically useful and directly relevant to avoiding causal overinterpretation of machine-learning feature importance.
