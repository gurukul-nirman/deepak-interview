# 01.3 · Machine Learning for Credit Risk — what a validator must know

> **Why this matters for your target band:** new validation JDs (Wells Fargo LQAS, SocGen, Citi) ask for ML model validation exposure. You don't need to be an ML engineer; you need to **explain, challenge and validate** ML models credibly — and know when *not* to use them.

---

## §1. When ML helps (and when it doesn't)
| ML adds value | LR scorecard is better |
|---|---|
| Non-linear effects & interactions (e.g., young business × high utilisation) | Regulatory capital/IFRS 9 models where transparency and stability dominate |
| Large, rich data (transactions, cash-flow, device data) | Small samples / low-default portfolios |
| Fraud, collections prioritisation, early-warning | Need for simple reason codes and stable points |
| Challenger/benchmark for a scorecard | When the uplift isn't statistically or economically meaningful |

**Typical uplift** of GBMs over a well-built WoE scorecard on traditional bureau data is modest (a few Gini points); larger with alternative data. **[Assumption — varies widely]**

---

## §2. Trees, forests, boosting — in plain words
- **Decision tree:** repeatedly splits data on the variable/threshold that best separates goods and bads (Gini impurity or entropy). Easy to read; overfits when deep.
- **Random forest (bagging):** many deep trees on bootstrap samples with random feature subsets; average them → lower variance.
- **Gradient boosting (GBM, XGBoost, LightGBM, sklearn HistGradientBoosting):** builds shallow trees **sequentially**, each fitting the errors (gradients) of the current ensemble; learning rate shrinks each step.

**Key hyperparameters and what they control:**
| Parameter | Effect | Overfitting lever |
|---|---|---|
| `n_estimators` / iterations | Number of trees | More trees + early stopping |
| `learning_rate` (eta) | Step size | Lower = more robust, needs more trees |
| `max_depth` | Interaction order | Shallow (2–4) for credit = more stable, explainable |
| `min_child_weight` / min samples per leaf | Smallest allowed leaf | Higher = smoother |
| `subsample`, `colsample_bytree` | Row/feature sampling | Adds randomness, reduces variance |
| `reg_lambda` (L2), `reg_alpha` (L1), `gamma` | Penalties | Regularisation |
| `monotone_constraints` / `monotonic_cst` | Forces direction (e.g., higher score → lower risk) | Intuitive, defensible behaviour |
| `scale_pos_weight` / class weights | Rebalance rare bads | **Distorts calibration** → recalibrate |

---

## §3. Overfitting control & honest evaluation
- Train / validation (for tuning, early stopping) / **test** / **out-of-time** — never tune on the test set.
- k-fold CV for tuning; **time-based splits** for temporal data.
- Compare train vs OOT Gini; check stability across seeds and resamples.
- **Leakage** (the #1 ML validation finding): post-observation variables (e.g., collections flags, later balances), IDs/timestamps correlated with the target, the same customer in train and test, future macro data.

---

## §4. Imbalanced data & calibration
- Use AUC/Gini/KS/PR-AUC, not accuracy (97% accuracy is trivial at a 3% bad rate).
- Oversampling (SMOTE) or class weights change the base rate → **probabilities are no longer calibrated**. Fix with **Platt scaling** (logistic on the score) or **isotonic regression** on a clean holdout, then test calibration as in `03_monitoring_validation/01_performance_monitoring_metrics.md` §2.

---

## §5. Explainability toolkit
| Tool | Scope | What it shows | Caveat |
|---|---|---|---|
| Gain/split importance | Global | How much each feature is used | Biased to high-cardinality features |
| Permutation importance | Global | Performance drop when a feature is shuffled | Misleading with correlated features |
| **SHAP** | Global + local | Each feature's additive contribution to a prediction | Correlated features share credit; explains the model, not causality |
| PDP / ICE | Global / per-record | Average / individual effect of one feature | PDP assumes independence |
| ALE | Global | Effect accounting for correlation | Less familiar to stakeholders |
| LIME | Local | Local linear surrogate | Unstable across runs |

**SHAP in one breath:** "Shapley values come from cooperative game theory: each feature's SHAP value is its average marginal contribution across all orderings of features. They're additive — base value + sum of SHAP values = the model output (log-odds for a boosted classifier) — so they give per-customer reason codes. TreeSHAP computes them exactly and fast for tree models."

**Reason codes / adverse action:** in the US, ECOA/Regulation B requires specific principal reasons for adverse action; the CFPB (Circular 2022-03) said complex algorithms don't excuse vague reasons. → Top negative SHAP contributors, mapped to stable, plain-language reason codes, validated for consistency. **[Certain on the rule; Likely on industry practice]**

---

## §6. Fairness (what validators test)
- **Concepts:** disparate treatment (using a protected attribute) vs disparate impact (neutral variable with discriminatory effect); **proxies** (ZIP code, some alternative data).
- **Metrics:** Adverse Impact Ratio (approval-rate ratio; < 0.8 flags review), standardised mean difference of scores, equal opportunity (TPR parity), calibration within groups. When base rates differ, you **can't satisfy all fairness metrics at once** — choose and justify.
- **Data:** US lenders typically can't collect race for non-mortgage credit → proxy methods (e.g., BISG) for testing. **[Likely]**
- **Rules:** US ECOA/fair lending · **EU AI Act** — credit scoring of natural persons is *high-risk*; obligations for stand-alone high-risk systems deferred to **2 Dec 2027** (AI Omnibus, Reg. (EU) 2026/1744, in force 27 Jul 2026) · India — RBI Fair Practices Code (non-discrimination) and RBI's FREE-AI framework (Aug 2025), built on by the **draft MRM guidance (24 Jun 2026)** which expects explainability and human oversight for AI-driven decisions. **[Certain on dates; Likely on details]**

---

## §7. Validating an ML credit model — checklist
1. **Purpose & justification:** why ML? Evidence of uplift vs an LR benchmark (DeLong p-value, OOT, segments) and its business value.
2. **Data:** lineage, leakage tests, feature definitions stable in production, alternative-data permissions.
3. **Conceptual soundness:** feature engineering logic; monotonic/interaction constraints; hyperparameter search documented (space, method, seeds); no tuning on test.
4. **Performance:** discrimination, calibration (post-calibration), stability across time/segments; sensitivity to seeds/resampling.
5. **Explainability:** global (SHAP summary) and local (reason codes) — consistent with business intuition; reason-code stability.
6. **Fairness:** metrics by protected-class proxies where lawful; mitigation documented.
7. **Robustness:** perturbation tests, missing-feature behaviour, extreme values.
8. **Implementation:** feature parity dev vs prod (training–serving skew), model artefact versioning, reproducibility (library versions).
9. **Monitoring:** feature PSI, prediction drift, SHAP-importance drift, performance on matured outcomes, fairness drift.
10. **Change governance:** is retraining a *model change*? Define thresholds (e.g., new features = material; periodic refit with same spec = non-material with monitoring).

---

## §8. "LR or XGBoost?" — your 60-second answer
> "It depends on materiality, use and evidence. For capital, provisioning or adverse-action-heavy decisions I default to a WoE logistic scorecard — transparent, stable, easy to monitor. I'd bring in gradient boosting where there's real non-linearity or rich data — fraud, early-warning, alternative data — and only if the uplift is statistically significant out-of-time and economically meaningful. If we do use it, I'd constrain it — shallow trees, monotonic constraints — calibrate it, explain it with SHAP-based reason codes, test fairness, and monitor drift. A common middle path is using the GBM as a challenger or to discover interactions that we then engineer into the scorecard."

---

## §8b. Fraud models (Wells Fargo's Lead QAS JD asks for fraud ML validation exposure)
- **Different from credit PD:** extreme imbalance (often ≪ 1% fraud), **label delay** (chargebacks/confirmations arrive weeks later), **adversarial drift** (fraudsters adapt), real-time latency constraints, and decisions at **alert thresholds** set by investigator capacity.
- **Metrics:** detection rate (recall) and **value detection rate** (% of fraud $ caught), **false-positive ratio** (false alerts per true fraud), alert rate, precision at the operating threshold, PR-AUC (more informative than ROC-AUC under extreme imbalance).
- **Validation focus:** label quality and delay handling, threshold setting vs capacity, drift monitoring (weekly), challenger rules vs model, explainability for investigators, feedback-loop bias (only alerted cases get investigated → labels are selective), and — under the EU AI Act — fraud detection is **excluded** from the credit-scoring high-risk category. **[Certain on the AI Act carve-out; Likely on practice]**

## §9. India-specific context worth knowing (for Indian lenders/fintech interviews)
- Small-business lending uses **GST returns, bank statements via the Account Aggregator framework, and bureau MSME ranks (e.g., TransUnion CIBIL's CMR)** — conceptually similar to the SBSS blend of business + principal credit data. **[Likely]**
- RBI ECL (effective 1 Apr 2027) and the draft MRM guidance (2026) will push banks/NBFCs to formalise ML model validation. **[Certain on issuance; Likely on impact]**

---

## §10. Rapid-fire
1. *Bagging vs boosting?* Parallel deep trees to cut variance vs sequential shallow trees to cut bias.
2. *Why shallow trees in credit?* Lower-order interactions → more stable and explainable.
3. *Your GBM's train Gini 0.80, OOT 0.55?* Overfitting or leakage — check features, regularise, early stopping.
4. *Are SHAP values causal?* No — they explain the model's use of features.
5. *SMOTE for PD?* Distorts calibration; recalibrate or avoid.
6. *How do you give reason codes from a GBM?* Top adverse SHAP contributions mapped to plain-language codes.
7. *Retraining monthly — model change?* Depends on policy; spec changes are material; same-spec refits need monitoring and thresholds.
8. *How do you test for proxy discrimination?* Correlate features with protected-class proxies; test outcome disparities; ablation (remove the feature, measure impact).
