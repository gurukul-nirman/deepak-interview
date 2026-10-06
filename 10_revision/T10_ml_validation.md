# T10 · ML model validation — quick refresher
**Study:** `01_foundations/03_ml_for_credit_risk.md` · **Test:** `START TOPIC T10`

## 60-second summary
- Use ML only for **significant, stable, material** OOT uplift (DeLong + $ impact) that's worth the governance cost.
- Validate: leakage · tuning governance · monotonic constraints · **calibration after resampling** · SHAP global/local + reason codes · fairness · robustness/seeds · training–serving parity · drift monitoring · retraining = model change?

## Quick Q → short answer
| Q | A |
|---|---|
| Bagging vs boosting? | Parallel deep trees (variance↓) vs sequential shallow trees (bias↓) |
| Overfitting controls? | Shallow depth, learning rate + early stopping, min child weight, subsampling, L1/L2, OOT |
| SHAP? | Additive Shapley contributions: base + Σ SHAP = output (log-odds); not causal; correlated features share credit |
| Reason codes from GBM? | Top adverse SHAP contributors → mapped plain-language codes (ECOA/Reg B) |
| SMOTE for PD? | Distorts calibration → recalibrate (Platt/isotonic) or avoid |
| Fairness tests? | Adverse impact ratio, score distribution gaps, error-rate parity on lawful proxies; trade-offs documented |
| Leakage examples? | Post-observation variables, target-derived fields, same customer in train & test |
| Monotonic constraints? | Force intuitive directions → explainable, regulator-friendly |
| GBM +0.04 Gini OOT, p = 0.006? | Significant — still check materiality, stability, explainability, fairness, cost |
| Fraud model metrics? | Detection & value detection rate, false-positive ratio, precision at threshold, PR-AUC |

## From my mock interviews (auto-updated)
_No entries yet._
