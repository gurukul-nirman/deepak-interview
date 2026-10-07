"""
stress_test_diagnostics.py — the standard diagnostic battery a validator runs on a
macro-driven loss model (CCAR/DFAST/ICAAP/IFRS 9 satellite model), on synthetic quarterly data.

Model: quarterly net charge-off (NCO) rate ~ unemployment change + GDP growth + lagged NCO
Run:  python stress_test_diagnostics.py
Needs: numpy, pandas, statsmodels
"""
from __future__ import annotations

import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.tsa.stattools import adfuller, kpss

for _stream in (sys.stdout, sys.stderr):  # Windows consoles/pipes default to cp1252 and crash on → ≈ −
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
warnings.filterwarnings("ignore")
rng = np.random.default_rng(5)

# ---------------------------------------------------------------- synthetic macro history (2005Q1–2025Q4)
q = pd.period_range("2005Q1", "2025Q4", freq="Q")
n = len(q)
unemp = np.empty(n)
unemp[0] = 5.0
for t in range(1, n):
    shock = 0.9 if q[t].year in (2008, 2009) else (3.5 if (q[t].year == 2020 and q[t].quarter == 2) else 0.0)
    unemp[t] = max(3.0, unemp[t - 1] + 0.05 * (5 - unemp[t - 1]) + shock + rng.normal(0, 0.15))
gdp_yoy = 2.2 - 1.1 * (unemp - 5) + rng.normal(0, 0.6, n)  # % YoY
d_unemp = np.r_[np.nan, np.diff(unemp)]  # quarterly change (stationary transform)
nco = np.empty(n)
nco[0] = 1.0
for t in range(1, n):
    covid_support = -1.0 if q[t].year in (2020, 2021) else 0.0  # stimulus suppressed losses
    nco[t] = 0.25 + 0.75 * nco[t - 1] + 0.55 * np.nan_to_num(d_unemp[t]) - 0.04 * gdp_yoy[t] \
        + 0.4 * covid_support * (d_unemp[t] > 0.5) + rng.normal(0, 0.08)

df = pd.DataFrame({"nco": nco, "unemp": unemp, "d_unemp": d_unemp, "gdp_yoy": gdp_yoy}, index=q)
df["nco_lag1"] = df["nco"].shift(1)
df["covid_dummy"] = ((df.index.year == 2020) | (df.index.year == 2021)).astype(int)
df = df.dropna()

print("=" * 90)
print("1) STATIONARITY — ADF (H0: unit root) and KPSS (H0: stationary). Use BOTH; they can disagree.")
for col in ["nco", "unemp", "d_unemp", "gdp_yoy"]:
    adf_p = adfuller(df[col], autolag="AIC")[1]
    kpss_p = kpss(df[col], regression="c", nlags="auto")[1]
    verdict = "stationary" if (adf_p < 0.05 and kpss_p > 0.05) else "non-stationary/unclear"
    print(f"  {col:<8} ADF p={adf_p:.3f}  KPSS p={kpss_p:.3f}  → {verdict}")

print("\n2) MODEL — OLS with Newey–West (HAC) standard errors; check SIGNS against economic intuition")
X = sm.add_constant(df[["nco_lag1", "d_unemp", "gdp_yoy", "covid_dummy"]])
ols = sm.OLS(df["nco"], X).fit()
hac = ols.get_robustcov_results(cov_type="HAC", maxlags=4)
print(pd.DataFrame({"coef": hac.params, "HAC_se": hac.bse, "p": hac.pvalues}, index=X.columns).round(4))
print(f"  Adj R² = {ols.rsquared_adj:.3f}   expected signs: d_unemp (+), gdp_yoy (−), nco_lag1 (+, <1)")

print("\n3) RESIDUAL DIAGNOSTICS")
dw = durbin_watson(ols.resid)
bg_p = acorr_breusch_godfrey(ols, nlags=4)[1]
bp_p = het_breuschpagan(ols.resid, X)[1]
jb_p = jarque_bera(ols.resid)[1]
print(f"  Durbin–Watson = {dw:.2f} (≈2 good; NB biased with a lagged dependent variable → prefer BG)")
print(f"  Breusch–Godfrey(4) p = {bg_p:.3f} (H0: no autocorrelation)")
print(f"  Breusch–Pagan p = {bp_p:.3f} (H0: homoskedastic)")
print(f"  Jarque–Bera p = {jb_p:.3f} (H0: normal residuals)")

print("\n4) MULTICOLLINEARITY — VIF")
for i, col in enumerate(X.columns):
    if col != "const":
        print(f"  {col:<12} VIF = {variance_inflation_factor(X.values, i):.2f}")

print("\n5) OUT-OF-TIME BACKTEST — fit to 2005–2019, dynamic forecast 2022–2025 (skip COVID years)")
train = df[df.index.year <= 2019]
test = df[df.index.year >= 2022]
m = sm.OLS(train["nco"], sm.add_constant(train[["nco_lag1", "d_unemp", "gdp_yoy"]])).fit()
pred, prev = [], test["nco_lag1"].iloc[0]
for _, r in test.iterrows():  # dynamic: feed back own prediction, like a 9-quarter stress projection
    yhat = m.params["const"] + m.params["nco_lag1"] * prev + m.params["d_unemp"] * r["d_unemp"] + m.params["gdp_yoy"] * r["gdp_yoy"]
    pred.append(yhat)
    prev = yhat
pred = np.array(pred)
mape = np.mean(np.abs((test["nco"] - pred) / test["nco"])) * 100
cum_err = (pred.sum() - test["nco"].sum()) / test["nco"].sum() * 100
print(f"  MAPE = {mape:.1f}%   cumulative error = {cum_err:+.1f}% (negative = model under-predicts losses)")

print("\n6) SENSITIVITY — +1pp shock to the quarterly unemployment change, 1 quarter")
print(f"  Immediate NCO impact = {m.params['d_unemp']:+.3f} pp; long-run multiplier = "
      f"{m.params['d_unemp'] / (1 - m.params['nco_lag1']):+.3f} pp")

print("\n7) STABILITY — coefficient on d_unemp across rolling 40-quarter windows")
coefs = []
for end in range(40, len(train) + 1, 4):
    w = train.iloc[end - 40:end]
    coefs.append(sm.OLS(w["nco"], sm.add_constant(w[["nco_lag1", "d_unemp", "gdp_yoy"]])).fit().params["d_unemp"])
print("  " + "  ".join(f"{c:.2f}" for c in coefs) + "   ← sign flips or big swings = finding")
print("=" * 90)
