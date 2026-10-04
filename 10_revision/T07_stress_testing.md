# T07 · Stress testing & econometrics — quick refresher
**Study:** `02_credit_risk/04_stress_testing_ccar.md` · run `05_coding/code/stress_test_diagnostics.py` · **Test:** `START TOPIC T07`

## 60-second summary
- CCAR/DFAST: baseline + severely adverse, **9 quarters**; **SCB** = max(2.5%, peak-to-trough CET1 decline + 4 quarters of dividends).
- **Fed final rules (30 Sep 2026):** annual public comment on scenarios & material model changes; two global market shocks; **SCB averaging of last two tests from 2028**; ~50% less volatility.
- Model hygiene: MEVs with economic rationale and **expected signs upfront** → stationarity/cointegration → HAC SEs → Breusch–Godfrey → **dynamic** out-of-time back-test → sensitivity → overlay governance.

## Quick Q → short answer
| Q | A |
|---|---|
| Top-down vs bottom-up? | Portfolio loss-rate regressions vs loan-level PD/LGD/EAD conditioned on macro |
| Choose MEVs? | Rationale & sign → lags/correlation → stationarity → parsimony → OOT |
| Target non-stationary? | Difference/transform, AR term, or cointegration + ECM |
| Why HAC SEs? | Autocorrelation/heteroskedasticity understate OLS SEs |
| DW with lagged dependent variable? | Biased → Breusch–Godfrey or Durbin's h |
| Long-run effect of a shock? | β/(1−ρ) |
| Back-test a stress model? | Dynamic OOT, realised-macro back-test, GFC episode, benchmarks; flag under-prediction |
| COVID data? | Dummy vs exclusion vs robust — show both, document |
| Non-monotonic severe losses? | Finding: sign/multicollinearity/lag issue |
| Practice-script numbers? | ΔUR +0.50, GDP −0.04, lag 0.77; BG p 0.16; OOT MAPE 10.9%, cum error +8.4% |

## From my mock interviews (auto-updated)
_No entries yet._
