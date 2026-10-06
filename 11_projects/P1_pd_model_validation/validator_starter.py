"""
validator_starter.py — YOUR side of Project P1: independent validation of CC-PD-01.

Run AFTER developer_model.py, with the same --data argument:
    python validator_starter.py --data synthetic     # pipeline test only
    python validator_starter.py --data ucimlrepo     # real data → portfolio

It runs end-to-end, prints the evidence for each validation area and writes it to
outputs/validation_evidence.md (tables you can paste into your report). It reports facts, not
conclusions — the findings are yours to draw.

Six exercises are marked TODO(you). Until you complete them they print 'TODO' instead of a result.
They are the calculations an interviewer will ask you to explain, so write them yourself.

Work order: read outputs/MDD_developer_summary.md → run this script → complete the TODOs →
write the report from REPORT_TEMPLATE.md → only then open ANSWER_KEY.md.

Areas (SR 11-7 / SR 26-2: conceptual soundness, outcomes analysis, ongoing monitoring):
  §1 Data review               §6 Stability & segments
  §2 Replication               §7 Challengers (benchmarking) + DeLong
  §3 Conceptual soundness      §8 Sensitivity
  §4 Discrimination (holdout)  §9 Fairness
  §5 Calibration               §10 Implementation (parallel run)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

from common import COLUMNS, TARGET, add_toolkit_to_path, load_data

add_toolkit_to_path()
import developer_model as dm  # noqa: E402
import validation_toolkit as vt  # noqa: E402

OUT = dm.OUT

SEED = 2026
PAY = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
BILL = [f"BILL_AMT{i}" for i in range(1, 7)]
PAYAMT = [f"PAY_AMT{i}" for i in range(1, 7)]
PROTECTED = ["SEX", "MARRIAGE", "AGE"]
DOCUMENTED_CODES = {  # UCI data dictionary
    "SEX": {1, 2},
    "EDUCATION": {1, 2, 3, 4},
    "MARRIAGE": {1, 2, 3},
    **{c: {-1, *range(1, 10)} for c in PAY},
}
EXPECTED_SIGN = {"LIMIT_BAL": "-", **{c: "+" for c in PAY}, **{c: "-" for c in PAYAMT}}


# ---------------------------------------------------------------------------
# Evidence log: prints to screen and builds outputs/validation_evidence.md
# ---------------------------------------------------------------------------
def md_table(df: pd.DataFrame, digits: int = 4) -> str:
    def fmt(v):
        if isinstance(v, (float, np.floating)):
            return "" if np.isnan(v) else f"{v:.{digits}g}" if abs(v) < 1e-3 and v != 0 else f"{v:.{digits}f}"
        return str(v)

    d = df.reset_index()
    lines = ["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * d.shape[1]]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in d.itertuples(index=False)]
    return "\n".join(lines)


class Evidence:
    def __init__(self, label: str):
        self.parts = [f"# CC-PD-01 — validation evidence\n*Data: {label}*"]

    def section(self, title: str) -> None:
        print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")
        self.parts.append(f"\n## {title}")

    def note(self, text: str) -> None:
        print(text)
        self.parts.append(text)

    def table(self, df: pd.DataFrame, caption: str, digits: int = 4) -> None:
        print(f"\n{caption}\n{df.to_string()}")
        self.parts.append(f"\n**{caption}**\n\n{md_table(df, digits)}")

    def todo(self, name: str) -> None:
        self.note(f"> TODO(you): {name} — not implemented yet (see its docstring).")

    def save(self) -> Path:
        path = OUT / "validation_evidence.md"
        path.write_text("\n\n".join(self.parts) + "\n")
        return path


# ---------------------------------------------------------------------------
# TODO(you) exercises — replace each `raise NotImplementedError` with your code
# ---------------------------------------------------------------------------
def undocumented_codes(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(you) #1 — data review.

    For every variable in DOCUMENTED_CODES, find the values present in df that are NOT in the data
    dictionary. Return one row per (variable, code) with columns: n, share, bad_rate.
    Hint: loop over DOCUMENTED_CODES; df.loc[~df[col].isin(codes)]; groupby(col)[TARGET].agg(...).
    """
    raise NotImplementedError


def prior_correct(pd_sample: np.ndarray, sample_bad_rate: float, population_bad_rate: float) -> np.ndarray:
    """TODO(you) #2 — calibration.

    The model was fitted on a 50/50 sample, so its intercept reflects a 50% default rate.
    Shift the log-odds back to the population rate (King & Zeng prior correction):
        logit(p_pop) = logit(p_sample) − ln[ (ȳ/(1−ȳ)) · ((1−τ)/τ) ]
    where ȳ = sample bad rate, τ = population bad rate. Return corrected PDs.
    """
    raise NotImplementedError


def sensitivity_scenarios(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """TODO(you) #3 — sensitivity analysis.

    Return {scenario_name: shocked copy of df}. Build at least:
      'PAY_0 +1 month'  : PAY_0 + 1 for accounts with PAY_0 >= 0 (cap at 8)
      'BILL_AMT +10%'   : all six bill amounts × 1.10
      'PAY_AMT −50%'    : all six payment amounts × 0.50
    Never modify df in place (use df.copy()). One example is already provided in run().
    """
    raise NotImplementedError


def adverse_impact_ratio(favourable: np.ndarray, group: pd.Series, protected, reference) -> float:
    """TODO(you) #4 — fairness.

    AIR = favourable-outcome rate of the protected group / favourable-outcome rate of the reference group.
    Here 'favourable' = NOT flagged for a credit-line reduction. Four-fifths rule: AIR < 0.80 → review.
    """
    raise NotImplementedError


def parallel_run_summary(y: np.ndarray, dev_pd: np.ndarray, prod_pd: np.ndarray,
                         tol: float = 1e-6, cut_off: float = dm.CUT_OFF) -> pd.Series:
    """TODO(you) #5 — implementation testing.

    Compare development vs production PDs for the same accounts. Return a Series with:
      n, pct_mismatch (|Δ| > tol), max_abs_diff, mean_pd_dev, mean_pd_prod,
      gini_dev, gini_prod, flag_rate_dev, flag_rate_prod (PD >= cut_off), pct_flag_changed.
    """
    raise NotImplementedError


def write_monitoring_plan() -> pd.DataFrame:
    """TODO(you) #6 — ongoing monitoring (the MDD only says 'annual review').

    Return a table with columns: metric, frequency, green, amber, red, action_if_red, owner.
    Cover at least: score PSI, CSI of key characteristics, Gini (with CI), calibration (A/E and
    per-grade Jeffreys), cut-off flag rate, overrides, data-quality checks, fairness (AIR).
    Justify each threshold in your report (why that number?).
    """
    raise NotImplementedError


def _attempt(ev: Evidence, name: str, fn, *args):
    try:
        return fn(*args)
    except NotImplementedError:
        ev.todo(name)
        return None


# ---------------------------------------------------------------------------
# Helpers (provided)
# ---------------------------------------------------------------------------
def balanced(train: pd.DataFrame, seed: int = SEED) -> pd.DataFrame:
    """The developer's sampling method, re-applied to a training split."""
    bads = train[train[TARGET] == 1]
    goods = train[train[TARGET] == 0].sample(n=len(bads), random_state=seed)
    return pd.concat([bads, goods])


def fit_logit(train: pd.DataFrame, features: list[str]):
    X = sm.add_constant(train[features].astype(float))
    return sm.Logit(train[TARGET].astype(int), X).fit(disp=False, maxiter=500)


def predict(res, df: pd.DataFrame, features: list[str]) -> np.ndarray:
    return np.asarray(res.predict(sm.add_constant(df[features].astype(float), has_constant="add")))


def engineer(df: pd.DataFrame) -> pd.DataFrame:
    """Features a validator would expect to see instead of 23 raw columns."""
    d = df.copy()
    lim = d["LIMIT_BAL"].clip(lower=1)
    d["util_1m"] = (d["BILL_AMT1"] / lim).clip(-0.5, 2)
    d["util_avg_6m"] = (d[BILL].mean(axis=1) / lim).clip(-0.5, 2)
    d["pay_ratio_1m"] = np.where(d["BILL_AMT2"] > 0, (d["PAY_AMT1"] / d["BILL_AMT2"].where(d["BILL_AMT2"] > 0)).clip(0, 1), 1.0)
    d["months_late_6m"] = (d[PAY] >= 1).sum(axis=1)
    d["max_late_6m"] = d[PAY].max(axis=1).clip(lower=0)
    d["log_limit"] = np.log(lim)
    return d


def woe_challenger(train: pd.DataFrame, test: pd.DataFrame):
    """C1: WoE logistic regression on engineered, non-protected features (natural default rate)."""
    tr, te = engineer(train), engineer(test)
    cats = {"PAY_0": lambda s: s.clip(-2, 3).astype(int).astype(str), "PAY_2": lambda s: s.clip(-2, 3).astype(int).astype(str),
            "months_late_6m": lambda s: s.clip(0, 4).astype(str), "max_late_6m": lambda s: s.clip(0, 3).astype(str)}
    numeric = ["log_limit", "util_1m", "util_avg_6m", "pay_ratio_1m"]
    feats, iv = [], {}
    for col in list(cats) + numeric:
        if col in cats:
            b_tr, b_te = cats[col](tr[col]), cats[col](te[col])
        else:
            edges = vt.quantile_bins(tr[col], 5)
            b_tr, b_te = vt.apply_bins(tr[col], edges), vt.apply_bins(te[col], edges)
        table, iv[col] = vt.woe_iv(b_tr, tr[TARGET])
        woe = table["woe"]
        tr[f"w_{col}"] = b_tr.map(woe).astype(float)
        te[f"w_{col}"] = b_te.map(woe).fillna(0.0).astype(float)  # unseen bin → neutral WoE
        feats.append(f"w_{col}")
    res = fit_logit(tr, feats)
    return predict(res, te, feats), res, pd.Series(iv, name="IV").sort_values(ascending=False)


def gbm_challenger(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
    """C2: gradient boosting with monotonic constraints, no protected attributes."""
    tr, te = engineer(train), engineer(test)
    feats = ["LIMIT_BAL", *PAY, *BILL, *PAYAMT, "util_1m", "util_avg_6m", "pay_ratio_1m", "months_late_6m"]
    sign = {**{c: 1 for c in PAY}, "LIMIT_BAL": -1, **{c: -1 for c in PAYAMT}, "months_late_6m": 1, "pay_ratio_1m": -1}
    model = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=15, random_state=SEED,
                                           monotonic_cst=[sign.get(f, 0) for f in feats])
    model.fit(tr[feats], tr[TARGET])
    return model.predict_proba(te[feats])[:, 1]


# ---------------------------------------------------------------------------
# Main validation run
# ---------------------------------------------------------------------------
def run(source: str) -> None:
    df, label = load_data(source)
    df = df.reset_index(drop=True)
    df.insert(0, "acct_id", np.arange(1, len(df) + 1))
    if not (OUT / "model_coefficients.csv").exists():
        sys.exit("Run developer_model.py first (same --data).")
    ev = Evidence(label)
    feats = dm.FEATURES
    tau = df[TARGET].mean()

    # §1 ---------------------------------------------------------------
    ev.section("§1 Data review")
    ev.note(f"Accounts: {len(df):,} · default rate: {tau:.2%} · duplicate rows (excl. ID): "
            f"{int(df.drop(columns='acct_id').duplicated().sum())} · negative BILL_AMT1: {int((df['BILL_AMT1'] < 0).sum())}")
    ev.table(df[COLUMNS].describe().T[["min", "50%", "max"]], "Ranges")
    codes = _attempt(ev, "#1 undocumented_codes", undocumented_codes, df)
    if codes is not None:
        ev.table(codes, "Codes outside the data dictionary")
    pay_codes = pd.DataFrame({c: df[c].value_counts() for c in PAY}).fillna(0).astype(int)
    ev.table(pay_codes, "Repayment-status code counts by month (PAY_0 = Sept … PAY_6 = Apr)")
    ev.table(df.groupby("PAY_0")[TARGET].agg(n="size", bad_rate="mean"), "Bad rate by PAY_0 code")
    ev.note("Target: `default payment next month` — 6-month observation window (Apr–Sep 2005), "
            "outcome observed in Oct 2005 only.")

    # §2 ---------------------------------------------------------------
    ev.section("§2 Replication")
    ids = pd.read_csv(OUT / "dev_sample_ids.csv")["acct_id"]
    dev = df[df["acct_id"].isin(ids)]
    rep = fit_logit(dev, feats).params
    doc = pd.read_csv(OUT / "model_coefficients.csv", index_col="variable")["coefficient"]
    rel = ((rep - doc).abs() / doc.abs().clip(lower=1e-12)).max()
    ev.note(f"Re-fitted on the documented sample ({len(dev):,} accounts). "
            f"Max relative coefficient difference vs model_coefficients.csv: {rel:.2e} "
            f"→ {'REPLICATED' if rel < 1e-4 else 'NOT replicated — investigate'}")

    # §3 ---------------------------------------------------------------
    ev.section("§3 Conceptual soundness")
    res_dev = fit_logit(dev, feats)
    sd = dev[feats].std()
    coef = pd.DataFrame({"coef": res_dev.params[feats], "p_value": res_dev.pvalues[feats],
                         "effect_per_1sd": res_dev.params[feats] * sd,
                         "expected_sign": [EXPECTED_SIGN.get(f, "n/a") for f in feats]})
    coef["sign_ok"] = np.where(coef["expected_sign"] == "n/a", "",
                               np.where(np.sign(coef["coef"]).map({1.0: "+", -1.0: "-", 0.0: "0"}) == coef["expected_sign"],
                                        "yes", "NO"))
    ev.table(coef, "Coefficients, significance, standardised effect and sign check")
    ev.table(vt.vif(dev[feats]).to_frame().sort_values("VIF", ascending=False), "VIF (development sample)", 1)
    ev.table(df[BILL].corr().round(3), "Correlation of BILL_AMT1–6", 3)

    # §4 ---------------------------------------------------------------
    ev.section("§4 Discrimination — out-of-sample")
    ev.note("The developer used every defaulter in estimation, so no independent test set exists. The developer's "
            "method is re-applied to a stratified 70/30 split; the holdout keeps the natural default rate.")
    train, test = train_test_split(df, test_size=0.3, stratify=df[TARGET], random_state=SEED)
    bal = balanced(train)
    champ = fit_logit(bal, feats)
    pd_test = predict(champ, test, feats)
    pd_bal_in = predict(champ, bal, feats)
    y = test[TARGET].to_numpy()
    lo, hi = vt.bootstrap_gini_ci(y, pd_test)
    perf = pd.DataFrame({
        "Gini": [vt.gini_score(bal[TARGET], pd_bal_in), vt.gini_score(y, pd_test)],
        "KS": [vt.ks_statistic(bal[TARGET], pd_bal_in), vt.ks_statistic(y, pd_test)],
    }, index=["in-sample (balanced train)", "holdout (natural rate)"])
    ev.table(perf, "Champion (developer method) — in-sample vs holdout")
    ev.note(f"Holdout Gini 95% bootstrap CI: [{lo:.3f}, {hi:.3f}]")
    gains = vt.gains_table(y, pd_test)
    ev.table(gains[["n", "bad_rate", "cum_bad_pct", "ks", "lift"]], "Holdout gains table (decile 1 = riskiest)")
    ev.note(f"Rank-order breaks: {vt.rank_order_breaks(gains)}")

    # §5 ---------------------------------------------------------------
    ev.section("§5 Calibration")
    hl, hl_p, cal = vt.hosmer_lemeshow(y, pd_test, dof_adjust=0)
    ev.note(f"Holdout: mean predicted PD {pd_test.mean():.2%} vs observed default rate {y.mean():.2%} "
            f"(A/E = {y.mean() / pd_test.mean():.2f}); HL = {hl:.1f}, p = {hl_p:.3g}")
    ev.table(cal[["n", "avg_pd", "observed_dr"]], "Calibration by PD decile (holdout, uncorrected)")
    grades = test.assign(pd=pd_test, grade=pd.qcut(pd_test, 7, labels=[f"G{i}" for i in range(1, 8)]))
    ev.table(vt.grade_calibration_tests(grades, "grade", "pd", TARGET)[["N", "D", "PD", "DR", "jeffreys_p", "result"]],
             "One-sided per-grade tests (uncorrected PD) — what do these tests NOT detect?")
    pd_corr = _attempt(ev, "#2 prior_correct", prior_correct, pd_test, bal[TARGET].mean(), train[TARGET].mean())
    if pd_corr is not None:
        hl_c, hl_pc, cal_c = vt.hosmer_lemeshow(y, pd_corr, dof_adjust=0)
        ev.note(f"After prior correction: mean PD {pd_corr.mean():.2%} vs DR {y.mean():.2%}; HL = {hl_c:.1f}, p = {hl_pc:.3g}")
        ev.table(cal_c[["n", "avg_pd", "observed_dr"]], "Calibration by PD decile (holdout, prior-corrected)")

    # §6 ---------------------------------------------------------------
    ev.section("§6 Stability & segment performance")
    ev.note(f"Score PSI, train vs holdout: {vt.psi(predict(champ, train, feats), pd_test):.4f} "
            "(a sanity check of the split — not evidence of stability over time)")
    stab, stab_tbl = vt.psi(df["PAY_6"], df["PAY_0"], return_table=True)
    ev.table(stab_tbl, f"The developer's 'stability' test re-performed: PSI(PAY_6 → PAY_0) = {stab:.4f}")
    seg = test.assign(pd=pd_test, limit_band=pd.qcut(test["LIMIT_BAL"].rank(method="first"), 5, labels=[f"L{i}" for i in range(1, 6)]),
                      age_band=pd.cut(test["AGE"], [0, 25, 40, 61, 200], labels=["≤25", "26–40", "41–61", "62+"]),
                      edu=test["EDUCATION"].map({1: "grad school", 2: "university", 3: "high school"}).fillna("other/undoc."))
    rows = []
    for col in ["limit_band", "age_band", "edu"]:
        for k, g in seg.groupby(col, observed=True):
            if g[TARGET].nunique() == 2 and len(g) >= 100:
                rows.append({"segment": f"{col}={k}", "n": len(g), "bad_rate": g[TARGET].mean(),
                             "gini": vt.gini_score(g[TARGET], g["pd"])})
    ev.table(pd.DataFrame(rows).set_index("segment"), "Holdout Gini by segment")

    # §7 ---------------------------------------------------------------
    ev.section("§7 Challengers & benchmarking")
    pd_c1, res_c1, iv = woe_challenger(train, test)
    pd_c2 = gbm_challenger(train, test)
    no_prot = [f for f in feats if f not in PROTECTED]
    pd_np = predict(fit_logit(bal, no_prot), test, no_prot)
    ev.table(iv.to_frame(), "C1 information values (train)")
    rows = []
    for name, p in [("Champion without SEX/MARRIAGE/AGE", pd_np), ("C1 WoE logistic", pd_c1), ("C2 monotonic GBM", pd_c2)]:
        a_ch, a_c, z, pval = vt.delong_test(y, pd_test, p)
        rows.append({"model": name, "gini": 2 * a_c - 1, "gini_champion": 2 * a_ch - 1, "delong_z": z, "p_value": pval})
    ev.table(pd.DataFrame(rows).set_index("model"), "Holdout Gini vs champion (DeLong test on the same accounts)")

    # §8 ---------------------------------------------------------------
    ev.section("§8 Sensitivity")
    base = predict(champ, test, feats).mean()
    rows = [{"scenario": "LIMIT_BAL −20% (example)",
             "mean_pd": predict(champ, test.assign(LIMIT_BAL=test["LIMIT_BAL"] * 0.8), feats).mean()}]
    shocks = _attempt(ev, "#3 sensitivity_scenarios", sensitivity_scenarios, test)
    for name, shocked in (shocks or {}).items():
        rows.append({"scenario": name, "mean_pd": predict(champ, shocked, feats).mean()})
    sens = pd.DataFrame(rows).set_index("scenario")
    sens["change_vs_base"] = sens["mean_pd"] - base
    ev.note(f"Base mean PD (holdout, uncorrected): {base:.4f}")
    ev.table(sens, "Champion sensitivity — is each direction economically sensible?")

    # §9 ---------------------------------------------------------------
    ev.section("§9 Fairness")
    fair = test.assign(flagged=pd_test >= dm.CUT_OFF,
                       age_band=pd.cut(test["AGE"], [0, 25, 40, 61, 200], labels=["≤25", "26–40", "41–61", "62+"]))
    ev.note(f"Champion flags {fair['flagged'].mean():.1%} of the holdout at cut-off {dm.CUT_OFF} "
            f"(MDD reports the rate on the balanced sample).")
    for col in ["SEX", "MARRIAGE", "age_band"]:
        ev.table(fair.groupby(col, observed=True).agg(n=("flagged", "size"), flag_rate=("flagged", "mean"),
                                                      bad_rate=(TARGET, "mean")), f"Flag rate by {col}")
    air = _attempt(ev, "#4 adverse_impact_ratio", adverse_impact_ratio, ~fair["flagged"].to_numpy(), fair["SEX"], 1, 2)
    if air is not None:
        ev.note(f"AIR (SEX: 1 = male vs 2 = female reference): {air:.3f}")
    ev.table(coef.loc[PROTECTED + ["EDUCATION"], ["coef", "p_value", "effect_per_1sd"]],
             "Demographic coefficients in the developer's model")

    # §10 --------------------------------------------------------------
    ev.section("§10 Implementation — parallel run")
    spec = pd.read_csv(OUT / "implementation_spec.csv", index_col="variable")["coefficient"]
    diff = pd.DataFrame({"development": doc, "implemented": spec})
    diff["rel_diff"] = (diff["development"] - diff["implemented"]).abs() / diff["development"].abs().clip(lower=1e-12)
    ev.table(diff[diff["rel_diff"] > 0.01].sort_values("rel_diff", ascending=False),
             "Coefficients whose implemented value differs from development by more than 1%", 6)
    scores = (pd.read_csv(OUT / "development_scores.csv")
              .merge(pd.read_csv(OUT / "production_scores.csv"), on="acct_id", suffixes=("_dev", "_prod"))
              .merge(df[["acct_id", TARGET]], on="acct_id"))
    summ = _attempt(ev, "#5 parallel_run_summary", parallel_run_summary,
                    scores[TARGET].to_numpy(), scores["pd_dev"].to_numpy(), scores["pd_prod"].to_numpy())
    if summ is not None:
        ev.table(summ.to_frame("value"), "Parallel run: development vs production")

    # §11 --------------------------------------------------------------
    ev.section("§11 Monitoring plan (your proposal)")
    plan = _attempt(ev, "#6 write_monitoring_plan", write_monitoring_plan)
    if plan is not None:
        ev.table(plan.set_index("metric"), "Proposed monitoring plan")

    path = ev.save()
    print(f"\nEvidence written to {path}\nNext: write your report from REPORT_TEMPLATE.md. "
          "Open ANSWER_KEY.md only after your findings list is final.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default="synthetic", help="synthetic | ucimlrepo | path to .xls/.xlsx/.csv")
    run(ap.parse_args().data)
