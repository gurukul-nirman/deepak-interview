"""
developer_model.py — the DEVELOPER's side of Project P1. You play the independent validator.

What it does (deliberately, like a first-line team under deadline pressure):
  1. Builds 'CC-PD-01', a logistic-regression PD model on the UCI Taiwan credit-card data.
  2. Writes the developer's evidence pack to outputs/:
       MDD_developer_summary.md   model documentation summary — the claims you must challenge
       dev_sample_ids.csv         accounts in the development sample
       model_coefficients.csv     full-precision coefficients (development code)
       implementation_spec.csv    coefficient table handed to IT for production
       development_scores.csv     developer's scores for every account
       production_scores.csv      parallel-run extract from the 'production' engine

The documentation contains claims that are wrong, unsupported or incomplete. Find them with
validator_starter.py, write your report from REPORT_TEMPLATE.md, and only then open ANSWER_KEY.md.

Do NOT fix anything here — this file is the 'model under review'.

Run:
  python developer_model.py --data synthetic        # test the pipeline (not for your portfolio)
  python developer_model.py --data ucimlrepo        # real data (pip install ucimlrepo)
  python developer_model.py --data "default of credit card clients.xls"   # pip install xlrd
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import COLUMNS, TARGET, add_toolkit_to_path, load_data

add_toolkit_to_path()
from validation_toolkit import gini_score, hosmer_lemeshow, ks_statistic, psi  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

MODEL_ID = "CC-PD-01"
FEATURES = list(COLUMNS)   # "all 23 variables, to maximise information"
SEED = 42
CUT_OFF = 0.50
SPEC_DECIMALS = 4          # the MDD coefficient table format, transcribed by IT


def build_dev_sample(df: pd.DataFrame, seed: int = SEED) -> pd.DataFrame:
    """'Balanced' development sample: every bad plus an equal number of randomly drawn goods."""
    bads = df[df[TARGET] == 1]
    goods = df[df[TARGET] == 0].sample(n=len(bads), random_state=seed)
    return pd.concat([bads, goods]).sort_index()


def fit(dev: pd.DataFrame):
    X = sm.add_constant(dev[FEATURES].astype(float))
    return sm.Logit(dev[TARGET].astype(int), X).fit(disp=False, maxiter=500)


def score(coefs: pd.Series, df: pd.DataFrame) -> np.ndarray:
    z = coefs["const"] + df[FEATURES].astype(float).to_numpy() @ coefs[FEATURES].to_numpy()
    return 1 / (1 + np.exp(-z))


def _fmt_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def write_mdd(df: pd.DataFrame, dev: pd.DataFrame, res, pd_dev: np.ndarray, label: str) -> str:
    coefs = res.params
    y_dev = dev[TARGET].to_numpy()
    gini, ks = gini_score(y_dev, pd_dev), ks_statistic(y_dev, pd_dev)
    flagged = pd_dev >= CUT_OFF
    accuracy = float((flagged == (y_dev == 1)).mean())
    hl_stat, hl_p, _ = hosmer_lemeshow(y_dev, pd_dev)
    stab = psi(df["PAY_6"], df["PAY_0"])
    n_sig = int((res.pvalues.drop("const") < 0.05).sum())
    hl_text = (f"The Hosmer–Lemeshow test is passed (statistic {hl_stat:.1f}, p = {hl_p:.3f})." if hl_p >= 0.05 else
               f"The Hosmer–Lemeshow statistic is {hl_stat:.1f} (p = {hl_p:.3f}); HL is known to over-reject in large "
               "samples, so this result was disregarded.")
    stab_text = ("below the 0.10 stability threshold" if stab < 0.10 else
                 "below the 0.25 action threshold" if stab < 0.25 else "attributable to seasonality")

    coef_tbl = pd.DataFrame({
        "Variable": coefs.index,
        "Coefficient": [f"{v:.{SPEC_DECIMALS}f}" for v in coefs],
        "Std. error": [f"{v:.{SPEC_DECIMALS}f}" for v in res.bse],
        "p-value": [f"{v:.3f}" for v in res.pvalues],
    })

    return f"""# {MODEL_ID} — Model Development Document (summary)
*Prepared by: Retail Analytics (first line) · Submitted to Model Risk Management for initial validation*
*Data: {label}*

## 1. Purpose and intended use
{MODEL_ID} estimates the **probability of default (PD)** of credit-card accounts. Intended uses:
1. **12-month PD** for IFRS 9 Stage 1 expected credit loss.
2. Risk-based pricing of credit-line increases.
3. Credit-line reduction for high-risk accounts (PD ≥ {CUT_OFF:.2f}).

Proposed model risk tier: **Tier 3 (low)** — the model is a standard logistic regression.

## 2. Data
- Source: credit-card accounts of a Taiwanese bank; repayment history April–September 2005.
- Population: {len(df):,} accounts. Target: `default payment next month` (October 2005).
  Observed default rate: {df[TARGET].mean():.2%}.
- No missing values were found, so no data treatment was required.

## 3. Development sample
To address class imbalance, the development sample was **balanced to 50/50**: all {int(df[TARGET].sum()):,}
defaulters plus {int(len(dev) - dev[TARGET].sum()):,} randomly selected non-defaulters (seed {SEED}),
giving {len(dev):,} accounts. All accounts in the sample were used for estimation to maximise the
information available. Account IDs: `outputs/dev_sample_ids.csv`.

## 4. Methodology and variables
Logistic regression (maximum likelihood, statsmodels) on **all 23 variables** in their raw form,
to maximise information: credit limit, sex, education, marital status, age, six months of repayment
status (PAY_0 … PAY_6), six months of bill amounts and six months of payment amounts.
{n_sig} of 23 variables are significant at the 5% level; the remaining variables were retained to
preserve information.

**Appendix A — coefficients (MDD format, {SPEC_DECIMALS} d.p.)**

{_fmt_table(coef_tbl)}

## 5. Performance (development sample)
| Metric | Value |
|---|---|
| Gini | {gini:.3f} |
| KS | {ks:.3f} |
| Accuracy at cut-off {CUT_OFF:.2f} | {accuracy:.1%} |
| Accounts flagged at cut-off | {flagged.mean():.1%} |

The Gini of {gini:.2f} demonstrates strong discriminatory power.

## 6. Calibration
Mean predicted PD on the development sample is **{pd_dev.mean():.1%}** against an observed default rate of
**{y_dev.mean():.1%}**. {hl_text}
The model is therefore **well calibrated** and suitable for IFRS 9 and pricing.

## 7. Stability
The PSI between the April (PAY_6) and September (PAY_0) repayment-status distributions is **{stab:.3f}**
({stab_text}), demonstrating that the portfolio — and therefore the model — is **stable over time**.

## 8. Fairness
Demographic variables (sex, marital status, age, education) improve model fit and were retained.
Because the model is fully data-driven, it is objective and **free from bias**.

## 9. Implementation
The Appendix A coefficient table was provided to IT and implemented in the production scoring engine.
A parallel-run extract is available in `outputs/production_scores.csv`.

## 10. Ongoing monitoring
The model will be reviewed **annually** by the development team.

## 11. Limitations
None identified.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default="synthetic", help="synthetic | ucimlrepo | path to .xls/.xlsx/.csv")
    args = ap.parse_args()

    df, label = load_data(args.data)
    df = df.reset_index(drop=True)
    df.insert(0, "acct_id", np.arange(1, len(df) + 1))

    dev = build_dev_sample(df)
    res = fit(dev)
    if not res.mle_retvals.get("converged", True):
        print("WARNING: optimiser did not converge (the developer shipped it anyway).")
    coefs = res.params
    spec = coefs.round(SPEC_DECIMALS)          # what IT received

    OUT.mkdir(exist_ok=True)
    dev[["acct_id"]].to_csv(OUT / "dev_sample_ids.csv", index=False)
    coefs.rename("coefficient").to_csv(OUT / "model_coefficients.csv", index_label="variable")
    spec.rename("coefficient").to_csv(OUT / "implementation_spec.csv", index_label="variable")
    pd.DataFrame({"acct_id": df["acct_id"], "pd": score(coefs, df)}).to_csv(
        OUT / "development_scores.csv", index=False)
    pd.DataFrame({"acct_id": df["acct_id"], "pd": score(spec, df)}).to_csv(
        OUT / "production_scores.csv", index=False)
    (OUT / "MDD_developer_summary.md").write_text(write_mdd(df, dev, res, score(coefs, dev), label), encoding="utf-8")

    print(f"[{label}] {MODEL_ID} built on {len(dev):,} accounts; evidence pack written to {OUT}")
    print("Next: read outputs/MDD_developer_summary.md, then run validator_starter.py with the same --data.")


if __name__ == "__main__":
    main()
