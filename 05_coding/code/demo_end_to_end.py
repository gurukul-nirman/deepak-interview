"""
demo_end_to_end.py — build → monitor → validate a small-business credit-card scorecard (synthetic data).

The story deliberately mirrors an SBSS-style business-credit-card portfolio so you can talk through it:
  1. Development: bin → WoE/IV → variable selection → logistic regression → scaled points (PDO).
  2. Performance testing on train / in-time test / out-of-time (OOT).
  3. Ongoing monitoring on a recent quarter with population shift AND relationship drift.
  4. Validation: calibration by grade (binomial / Jeffreys), HL, VIF, challenger GBM + DeLong test.
  5. Auto-drafted findings with RAG ratings.

Run:  python demo_end_to_end.py        (≈10–20 seconds)
Needs: numpy, pandas, scipy, statsmodels, scikit-learn
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import HistGradientBoostingClassifier

import validation_toolkit as vt

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 20)
pd.set_option("display.float_format", lambda v: f"{v:,.4f}")

INDUSTRY_EFFECT = {"Retail": 0.20, "Services": 0.00, "Construction": 0.50, "Healthcare": -0.30, "Transport": 0.30}
FEATURES = ["vendor_score", "utilization", "months_in_business", "delinq_12m", "inquiries_6m", "industry"]


# ---------------------------------------------------------------------------
# 0. Synthetic portfolio
# ---------------------------------------------------------------------------
def simulate(n: int, seed: int, shift: float = 0.0, drift: float = 0.0) -> pd.DataFrame:
    """shift = population (input) shift; drift = change in the true risk relationship.

    A latent 'financial health' factor h makes the characteristics correlated (realistic VIFs).
    """
    rng = np.random.default_rng(seed)
    h = rng.normal(0, 1, n) - 0.5 * shift  # latent health; shift moves the population riskier
    vendor_score = np.clip(195 + 30 * h + rng.normal(0, 22, n), 0, 300).round()  # SBSS-like, higher = safer
    utilization = 1 / (1 + np.exp(-(-0.9 - 0.6 * h + rng.normal(0, 0.8, n))))
    months_in_business = np.clip(rng.gamma(2.5, 40, n) * np.exp(0.15 * h), 3, 480).round()
    delinq_12m = rng.poisson(np.exp(-1.5 - 0.6 * h))
    inquiries_6m = rng.poisson(np.exp(-0.1 - 0.25 * h + 0.4 * shift))
    industry = rng.choice(list(INDUSTRY_EFFECT), n, p=[0.25, 0.30, 0.15, 0.15, 0.15])

    z = (
        -3.15
        - 0.020 * (vendor_score - 195)
        + 2.0 * (utilization - 0.3)
        - 0.004 * (months_in_business - 100)
        + 0.45 * delinq_12m
        + 0.05 * inquiries_6m
        + pd.Series(industry).map(INDUSTRY_EFFECT).to_numpy()
        # interaction an additive WoE scorecard cannot capture: young business AND high utilisation
        + 1.4 * ((utilization > 0.5) & (months_in_business < 36))
        # drift: vendor score loses power + macro level shift + risk the model never saw (noise)
        + drift * (0.010 * (vendor_score - 195) + 0.25 + rng.normal(0, 0.6, n))
    )
    bad = rng.binomial(1, 1 / (1 + np.exp(-z)))

    df = pd.DataFrame(
        {
            "vendor_score": vendor_score,
            "utilization": utilization,
            "months_in_business": months_in_business,
            "delinq_12m": delinq_12m,
            "inquiries_6m": inquiries_6m,
            "industry": industry,
            "bad": bad,
        }
    )
    # 4% missing time-in-business (e.g., new digital channel not capturing it)
    df.loc[rng.random(n) < 0.04, "months_in_business"] = np.nan
    return df


# ---------------------------------------------------------------------------
# 1. Development
# ---------------------------------------------------------------------------
def build_binning(train: pd.DataFrame) -> dict:
    edges = {
        "vendor_score": vt.quantile_bins(train["vendor_score"], 5),
        "utilization": vt.quantile_bins(train["utilization"], 5),
        "months_in_business": vt.quantile_bins(train["months_in_business"], 5),
        "delinq_12m": np.array([-np.inf, 0.5, 1.5, np.inf]),  # 0 | 1 | 2+
        "inquiries_6m": np.array([-np.inf, 0.5, 1.5, 2.5, np.inf]),  # 0 | 1 | 2 | 3+
    }
    return edges


def to_bins(df: pd.DataFrame, edges: dict) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for col, e in edges.items():
        out[col] = vt.apply_bins(df[col], e)
    out["industry"] = df["industry"].astype(str)
    return out


def to_woe(binned: pd.DataFrame, woe_maps: dict) -> pd.DataFrame:
    out = pd.DataFrame(index=binned.index)
    for col, m in woe_maps.items():
        out[col] = binned[col].map(m).fillna(0.0)  # unseen bin → neutral WoE (flag in monitoring!)
    return out


def scale_points(params: pd.Series, woe_tables: dict, pdo=20, base_score=600, base_odds=50):
    """points_ij = −(β_i·WoE_ij + β0/n)·Factor + Offset/n   (model predicts log-odds of BAD)."""
    factor = pdo / np.log(2)
    offset = base_score - factor * np.log(base_odds)
    n = len(woe_tables)
    b0 = params["const"]
    pts = {}
    for col, t in woe_tables.items():
        pts[col] = (-(params[col] * t["woe"] + b0 / n) * factor + offset / n).round().astype(int)
    return pts, factor, offset


def score(binned: pd.DataFrame, points: dict) -> pd.Series:
    total = pd.Series(0, index=binned.index, dtype=float)
    for col, p in points.items():
        total += binned[col].map(p).fillna(0)
    return total


def main():
    print("=" * 100)
    print("STEP 0 — DATA")
    dev = simulate(30_000, seed=1)
    oot = simulate(10_000, seed=2, shift=0.2, drift=0.0)
    recent = simulate(10_000, seed=3, shift=1.5, drift=1.0)
    rng = np.random.default_rng(11)
    is_train = rng.random(len(dev)) < 0.7
    train, test = dev[is_train].copy(), dev[~is_train].copy()
    for name, d in [("train", train), ("test", test), ("oot", oot), ("recent", recent)]:
        print(f"  {name:<7} n={len(d):>6,}  bad rate={d['bad'].mean():.2%}")

    # ---- binning, WoE, IV
    print("\nSTEP 1 — BINNING, WoE, IV (Siddiqi convention: WoE = ln(%Good/%Bad))")
    edges = build_binning(train)
    b_train = to_bins(train, edges)
    woe_tables, iv = {}, {}
    for col in FEATURES:
        t, v = vt.woe_iv(b_train[col], train["bad"])
        woe_tables[col], iv[col] = t, v
    iv_s = pd.Series(iv, name="IV").sort_values(ascending=False)
    print(iv_s.to_frame().assign(strength=lambda d: pd.cut(d["IV"], [0, 0.02, 0.1, 0.3, 0.5, 9],
                                                             labels=["useless", "weak", "medium", "strong", "suspicious"])))
    print("\n  WoE table — vendor_score:")
    print(woe_tables["vendor_score"][["n", "bads", "bad_rate", "woe", "iv_contrib"]])

    selected = [c for c in FEATURES if iv[c] >= 0.02]
    woe_maps = {c: woe_tables[c]["woe"].to_dict() for c in selected}

    # ---- logistic regression on WoE
    print("\nSTEP 2 — LOGISTIC REGRESSION ON WoE (expect NEGATIVE coefficients, ≈ −1)")
    X_train = to_woe(b_train[selected], woe_maps)
    logit = sm.Logit(train["bad"], sm.add_constant(X_train)).fit(disp=0)
    print(pd.DataFrame({"coef": logit.params, "p_value": logit.pvalues}))
    wrong_sign = [c for c in selected if logit.params[c] >= 0]
    print(f"  Sign check: {'OK' if not wrong_sign else 'WRONG SIGN on ' + ', '.join(wrong_sign)}")
    print("\n  VIF on WoE variables:")
    print(vt.vif(X_train).round(2).to_frame())

    # ---- points
    points, factor, offset = scale_points(logit.params, {c: woe_tables[c] for c in selected})
    print(f"\nSTEP 3 — SCALING: PDO=20, 600 points at 50:1 good:bad → Factor={factor:.2f}, Offset={offset:.2f}")
    print("  Points — utilization:", points["utilization"].to_dict())

    # ---- apply to all samples
    def run(d: pd.DataFrame):
        b = to_bins(d, edges)
        xw = to_woe(b[selected], woe_maps)
        pdv = logit.predict(sm.add_constant(xw, has_constant="add"))
        sc = score(b, points)
        return b, pdv, sc

    res = {name: run(d) for name, d in [("train", train), ("test", test), ("oot", oot), ("recent", recent)]}
    data = {"train": train, "test": test, "oot": oot, "recent": recent}

    # ---- performance across samples
    print("\nSTEP 4 — PERFORMANCE (discrimination + calibration) ACROSS SAMPLES")
    rows = []
    for name in ["train", "test", "oot", "recent"]:
        y = data[name]["bad"].to_numpy()
        _, pdv, sc = res[name]
        lo, hi = vt.bootstrap_gini_ci(y, -sc, n_boot=200)
        hl, hl_p, _ = vt.hosmer_lemeshow(y, pdv)
        gt = vt.gains_table(y, -sc)
        rows.append({
            "sample": name, "n": len(y), "bad_rate": y.mean(), "avg_pd": pdv.mean(),
            "KS": vt.ks_statistic(y, -sc), "Gini": vt.gini_score(y, -sc), "Gini_CI_lo": lo, "Gini_CI_hi": hi,
            "HL_p": hl_p, "rank_breaks": vt.rank_order_breaks(gt), "Brier": vt.brier_score(y, pdv),
        })
    perf = pd.DataFrame(rows).set_index("sample")
    print(perf)
    print("\n  Gains table — recent quarter (bin 1 = riskiest 10%):")
    print(vt.gains_table(recent["bad"], -res["recent"][2])[["n", "bads", "bad_rate", "cum_bad_pct", "cum_good_pct", "ks", "lift"]])

    # ---- stability
    print("\nSTEP 5 — STABILITY: PSI on score, CSI on characteristics (reference = train)")
    psi_oot = vt.psi(res["train"][2], res["oot"][2])
    psi_recent, psi_tbl = vt.psi(res["train"][2], res["recent"][2], return_table=True)
    print(f"  PSI score  train→oot = {psi_oot:.3f} [{vt.rag(psi_oot, 0.10, 0.25)}]   "
          f"train→recent = {psi_recent:.3f} [{vt.rag(psi_recent, 0.10, 0.25)}]")
    print(psi_tbl.round(4))
    csi = {c: vt.csi_categorical(res["train"][0][c], res["recent"][0][c])[0] for c in selected}
    csi_s = pd.Series(csi, name="CSI").sort_values(ascending=False)
    print("\n  CSI train→recent:")
    print(csi_s.to_frame().assign(RAG=lambda d: d["CSI"].apply(lambda v: vt.rag(v, 0.10, 0.25))))

    # ---- calibration by grade on recent
    print("\nSTEP 6 — PD BACK-TEST BY GRADE (recent): binomial & Jeffreys, H1 = PD too low")
    grade_edges = np.quantile(res["train"][1], np.linspace(0, 1, 8))
    grade_edges[0], grade_edges[-1] = 0, 1
    labels = [f"G{i}" for i in range(1, 8)]  # G1 = safest
    rec = pd.DataFrame({"pd": res["recent"][1].to_numpy(), "bad": recent["bad"].to_numpy()})
    rec["grade"] = pd.cut(rec["pd"], grade_edges, labels=labels, include_lowest=True)
    gtest = vt.grade_calibration_tests(rec, "grade", "pd", "bad")
    print(gtest[["N", "D", "PD", "DR", "binomial_p", "jeffreys_p", "result"]])

    # ---- challenger
    print("\nSTEP 7 — CHALLENGER: monotonic gradient boosting on raw features + DeLong test")
    def raw(d):
        X = d[FEATURES].copy()
        X["industry"] = X["industry"].map({k: i for i, k in enumerate(INDUSTRY_EFFECT)})
        return X
    mono = [-1, 1, -1, 1, 1, 0]  # vendor_score↓risk, util↑, tenure↓, delinq↑, inquiries↑, industry free
    gbm = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=300,
                                         monotonic_cst=mono, categorical_features=[5], random_state=0)
    gbm.fit(raw(train), train["bad"])
    rows = []
    for name in ["test", "oot", "recent"]:
        y = data[name]["bad"].to_numpy()
        champ = -res[name][2].to_numpy()
        chall = gbm.predict_proba(raw(data[name]))[:, 1]
        a1, a2, zz, pv = vt.delong_test(y, champ, chall)
        rows.append({"sample": name, "Gini_scorecard": 2 * a1 - 1, "Gini_challenger": 2 * a2 - 1,
                     "DeLong_z": zz, "p_value": pv})
    chal = pd.DataFrame(rows).set_index("sample")
    print(chal)

    # ---- findings
    print("\nSTEP 8 — DRAFT FINDINGS (auto-generated; a validator would refine wording and severity)")
    g_dev, g_rec = perf.loc["test", "Gini"], perf.loc["recent", "Gini"]
    rel_drop = (g_dev - g_rec) / g_dev
    ratio = perf.loc["recent", "bad_rate"] / perf.loc["recent", "avg_pd"]
    red_grades = gtest.index[gtest["result"] == "RED"].tolist()
    shifted = csi_s[csi_s > 0.10].index.tolist()
    findings = []
    if rel_drop > 0.10:
        sev = "HIGH" if rel_drop > 0.20 else "MEDIUM"
        findings.append((sev, "Discrimination deterioration",
                         f"Gini fell from {g_dev:.3f} (in-time test) to {g_rec:.3f} in the recent quarter "
                         f"({rel_drop:.0%} relative); recent 95% CI [{perf.loc['recent','Gini_CI_lo']:.3f}, "
                         f"{perf.loc['recent','Gini_CI_hi']:.3f}] excludes the development value.",
                         "Root-cause by segment and characteristic; assess redevelopment; tighten monitoring to monthly."))
    if ratio > 1.2 or red_grades:
        findings.append(("HIGH", "PD under-estimation (calibration)",
                         f"Observed bad rate is {ratio:.2f}x the average predicted PD; Jeffreys test RED in grades "
                         f"{', '.join(red_grades) or 'none'}.",
                         "Interim overlay / recalibration to recent default experience; re-run back-test after 2 quarters."))
    if psi_recent > 0.25:
        findings.append(("MEDIUM", "Population shift",
                         f"Score PSI {psi_recent:.3f} (RED > 0.25); CSI > 0.10 for {', '.join(shifted)}.",
                         "Confirm with business whether acquisition strategy/channel changed; refresh reference population if intended."))
    if (chal["p_value"] < 0.05).any() and (chal["Gini_challenger"] > chal["Gini_scorecard"]).any():
        findings.append(("LOW", "Benchmark outperforms",
                         "Monotonic GBM challenger shows statistically higher Gini (DeLong p < 0.05) in at least one sample.",
                         "Consider redevelopment with richer specification; challenger informs, not replaces, the champion."))
    miss = res["recent"][0]["months_in_business"].eq("MISSING").mean()
    findings.append(("LOW", "Missing-value treatment",
                     f"{miss:.1%} of recent accounts have missing time-in-business, scored via a MISSING bin.",
                     "Confirm source-system root cause; monitor missing rate as a KRI."))
    for i, (sev, title, obs, rec_txt) in enumerate(findings, 1):
        print(f"\n  F{i} [{sev}] {title}\n     Observation: {obs}\n     Recommendation: {rec_txt}")

    verdict = "APPROVE WITH CONDITIONS" if any(f[0] == "HIGH" for f in findings) else "APPROVE"
    print(f"\n  Proposed outcome: {verdict} — overlay + remediation plan with due dates; re-review in 2 quarters.")
    print("=" * 100)


if __name__ == "__main__":
    main()
