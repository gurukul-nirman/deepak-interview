# 02.5 · Wholesale & Commercial Credit Models (primer for validators)

> Why: some target roles (e.g., Wells Fargo Corporate Model Risk) validate **commercial** credit models. Your SBSS small-business experience sits between retail and wholesale — use this to bridge. Priority **P2**.

---

## 1. How wholesale differs from retail
| | Retail | Wholesale / commercial |
|---|---|---|
| Unit | Pools of many similar accounts | Individual obligors (and facilities) |
| Data | Large, behavioural, bureau | Few defaults, financial statements, qualitative judgment |
| Models | Statistical scorecards | Rating models (scorecard + expert judgment), LGD by collateral/seniority |
| Defaults | Plenty → statistical calibration | **Low-default portfolios (LDPs)** → benchmarking, conservatism |
| Overrides | Policy rules | **Rating overrides** by credit officers — a key monitoring area |

## 2. Rating systems
- **Two dimensions:** **obligor rating** (PD) and **facility rating** (LGD/EAD — collateral, seniority, structure).
- **Master scale:** maps internal grades to PD ranges (often aligned to agency scales, e.g., grade 3 ≈ BBB). Lets you compare models and aggregate risk.
- **Typical PD model for mid-market/corporates:** a scorecard on **financial ratios** + **qualitative factors**:
  - Leverage (debt/EBITDA, debt/equity) · coverage (EBITDA/interest, DSCR) · liquidity (current ratio) · profitability (EBITDA margin, ROA) · size (revenue, assets) · trends.
  - Qualitative: management quality, industry outlook, market position, financial flexibility, parent support.
  - Overrides & notching (e.g., parent/sovereign support).
- **Commercial real estate (CRE):** DSCR, LTV, debt yield, property type, occupancy; loss severity tied to collateral values (stress with property-price paths).
- **Small business (SBSS world):** blends owner's personal credit with business data — often scored like retail but monitored with business indicators; SBA's 2026 change means more lenders use internal scoring here.

## 3. Calibration with few defaults
- External benchmarks: agency default studies, mapping to external ratings (where obligors are rated).
- **Pluto–Tasche** upper confidence bounds per grade (most prudent estimation).
- Expert-judgment calibration with conservatism (MoC under IRB).
- Pooling years/segments; Bayesian methods.

## 4. Validation specifics (what you'd test)
| Area | Tests |
|---|---|
| Discrimination | AUC/Gini when defaults allow; **rank-order agreement with external ratings** (Spearman/Kendall, % within ±1 notch) |
| Calibration | Default rates by grade vs PD with wide CIs; benchmark PD vs agency default rates for mapped grades |
| Stability | **Migration matrices** (upgrades/downgrades; concentration on the diagonal), grade concentration (HHI) |
| **Overrides** | Override rate and direction by officer/region; performance of overridden ratings (did overrides predict better?) |
| Qualitative factors | Consistency of scoring across analysts; documentation; inter-rater agreement |
| Financial data | Spreading accuracy, stale statements, adjustments (EBITDA add-backs) |
| Use | Ratings used consistently in approval, limits, pricing, provisioning |

## 5. Commercial models in CCAR / CECL / IFRS 9
- **C&I loss models:** PD by rating grade conditioned on macro (e.g., via migration matrices shifted by a Z-factor), LGD by collateral and seniority, EAD via utilisation of commitments (drawdowns rise in stress).
- **CRE loss models:** PD driven by DSCR/LTV under property-price and rate paths; refinancing risk at maturity.
- **CECL/IFRS 9:** lifetime PD from rating-migration matrices; forward-looking adjustments; individually assessed large impaired loans (DCF/collateral approach) vs pooled.

## 6. Interview questions
1. *How do you validate a PD model with 12 defaults?* Benchmark to external ratings, Pluto–Tasche bounds, expert review, conservative calibration, focus on rank-ordering and override analysis.
2. *What are rating overrides and why monitor them?* Officer changes to model ratings; frequent or one-directional overrides signal model weakness or judgment bias — test whether overrides improved accuracy.
3. *Obligor vs facility rating?* Default likelihood of the borrower vs loss severity of a specific facility.
4. *How do commercial EADs behave in stress?* Borrowers draw on committed lines → utilisation rises → CCF higher in downturns.
5. *Which ratios matter most for a mid-market PD?* Leverage and coverage typically dominate, then liquidity and size — but justify with data and industry.
