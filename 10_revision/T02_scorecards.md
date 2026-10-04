# T02 · Logistic regression & scorecards — quick refresher
**Study:** `01_foundations/02_logistic_regression_and_scorecards.md` · **Test:** `START TOPIC T02`

## 60-second summary
- LR models **log-odds** linearly → bounded PD, interpretable, stable, regulator-friendly.
- Build script: objective → sample design (observation point, **performance window from vintages**, **bad definition from roll rates**, indeterminates, exclusions) → samples (dev/holdout/OOT) → fine→coarse classing → **WoE/IV** → correlation/VIF + selection + business review → **reject inference** → LR → **PDO scaling** → validation → cut-off/swap sets → MRM.
- WoE = ln(%G/%B) (Siddiqi): single-variable WoE LR coefficient is **exactly −1**; positive sign in a multivariate model = multicollinearity.

## Quick Q → short answer
| Q | A |
|---|---|
| Why not linear regression? | Predictions outside [0,1]; heteroskedastic non-normal errors |
| LR assumptions? | Binary y, independence, linear logit, no severe multicollinearity, enough events; NOT normal errors/homoskedasticity |
| Interpret β = 0.18? | Odds × e^0.18 ≈ 1.20 per unit |
| IV thresholds? | <0.02 useless · 0.02–0.1 weak · 0.1–0.3 medium · 0.3–0.5 strong · >0.5 check leakage |
| Why WoE? | Linearises, handles missing/outliers as bins, common scale, monotonic explainable points |
| What does WoE lose? | Within-bin information; depends on binning; overfits small bins |
| Missing values? | Own bin with its own WoE — never default to 0 points |
| Bin rules? | 4–8 coarse bins, monotonic where logical, ≥5% population, enough bads |
| Indeterminates? | Neither good nor bad (e.g., max 30–59 DPD); excluded to sharpen separation |
| Reject inference methods? | Hard cut-off, parcelling, fuzzy augmentation, re-weighting, bureau data, test approvals |
| PDO meaning? | Points to double the odds |
| 600 @ 50:1, PDO 20? | Factor 28.85, Offset 487.12; PD 2%≈599, 5%≈572, 10%≈551 |
| Points per attribute? | −(β·WoE + β0/n)·Factor + Offset/n (model predicts bad) |
| Oversampling fix? | β0 + ln(π1/π0) − ln(ρ1/ρ0) or weights |
| Swap set? | Who new vs old card approves at equal approval rate; compare bad rates |
| Separation? | A bin with zero bads → MLE doesn't converge → merge bins / Firth |
| How many variables? | Typically 8–15, stable and explainable |

## Traps
- Choosing performance window without vintage evidence ✗
- Keeping a wrong-sign variable "because significant" ✗
- Stepwise as the only selection method ✗

## From my mock interviews (auto-updated)
_No entries yet._
