# 02.1 · Credit Risk Fundamentals (from zero)

> Interviewers open with these to calibrate you. Fumbling a basic (e.g., EAD for a card, or when cards charge off) costs more than missing an advanced point.

---

## 1. What credit risk is
The risk of loss because a borrower or counterparty fails to meet obligations. Sub-types: **default risk**, **migration/downgrade risk**, **concentration risk** (name, sector, geography), **counterparty credit risk** (derivatives), **settlement risk**.

## 2. Lending lifecycle and the models at each stage
| Stage | Decisions | Models |
|---|---|---|
| Marketing / acquisition | Who to target, approve, limit, price | Response, application scorecards, vendor scores (FICO, SBSS), affordability, fraud |
| Account management | Line increase/decrease, authorisations, cross-sell, early warning | Behavioural scores, line-management models |
| Collections | Who to call, when, how | Collections scores, roll-rate models, cure models |
| Recovery | Sell, settle, litigate | Recovery/LGD models |
| Portfolio / finance / regulatory | Provisions, capital, stress tests | IFRS 9/CECL ECL, Basel IRB PD/LGD/EAD, CCAR/ICAAP loss models |

## 3. Products
- **Secured vs unsecured** (mortgage/auto vs cards/personal loans).
- **Revolving vs instalment:** cards, lines of credit (balance moves, limit matters → CCF) vs term loans (amortising schedule).
- **Retail vs SME vs wholesale:** retail is pooled and scored; wholesale is rated name-by-name (expert + financials); small business (your SBSS world) blends the two — owner's personal credit + business data.

## 4. Delinquency, default, charge-off
- **DPD buckets:** Current · 1–29 · 30–59 · 60–89 · 90–119 · 120–149 · 150–179 · 180+.
- **US charge-off timing (FFIEC Uniform Retail Credit Classification policy):** open-end (cards) at **180 DPD**; closed-end (instalment) at **120 DPD**. **[Certain]**
- **Default definitions:**
  - **Basel:** 90 DPD on a material obligation **or** unlikely to pay.
  - **EBA DoD (EU):** materiality thresholds — retail **€100 absolute + 1% relative**; non-retail **€500 + 1%**; probation ≥ 3 months (12 months for distressed restructuring). **[Certain]**
  - **IFRS 9:** rebuttable presumption at 90 DPD; align with internal risk management.
  - **RBI:** NPA at 90 DPD (and ECL Stage 3).
- **Bad (scorecard) vs default (regulatory):** a scorecard "bad" (e.g., 60+ DPD ever in 12 months) can differ from the regulatory default — reconcile them when one model feeds another.

## 5. The loss equation
```
EL  = PD × LGD × EAD                 (expected loss → covered by provisions/pricing)
UL  = loss volatility around EL       (unexpected loss → covered by capital)
```
- **PD** — probability of default over a horizon (12-month or lifetime).
  - **Cumulative vs marginal:** cumulative PD(t) = 1 − Π_{k≤t}(1 − h_k), where h_k is the conditional (hazard) default rate in period k; marginal PD(t) = cumPD(t) − cumPD(t−1).
  - **PIT vs TTC:** point-in-time moves with the cycle; through-the-cycle is stable across it (details in `03_basel_irb.md`).
- **LGD** — loss as % of EAD = 1 − recovery rate.
  - **Workout LGD** = 1 − (PV of recoveries − PV of direct costs)/EAD, discounted to default date.
  - **Retail with cures:** LGD = (1 − cure rate) × LGD_non-cured (+ small cost for cured).
  - Distributions are often **bimodal** (near 0 and near 100%) → beta regression, two-stage (cure/no-cure) models.
  - Drivers: collateral/LTV, seniority, product, time in default, macro (house prices).
- **EAD** — exposure at default. For revolving products: `EAD = Drawn + CCF × (Limit − Drawn)`.
  - Realised CCF = (EAD − Drawn_ref)/(Limit − Drawn_ref), reference date 12 months before default; issues: negative values, limit changes, drawn ≈ limit (division by ~0).

## 6. Portfolio analytics you must be able to read and build
| Tool | What it shows | Credit use |
|---|---|---|
| **Vintage analysis** | Cumulative bad rate by months-on-book per origination cohort | Choose performance window; compare cohort quality; early warning |
| **Roll rates / flow rates** | % moving from bucket k to k+1 month-on-month | Collections forecasting; bad definition ("point of no return") |
| **Transition (migration) matrix** | Grade-to-grade movement over a period | Lifetime PD (Markov); rating stability |
| **Bad rate by score band** | Rank-ordering | Monitoring; cut-offs |
| **Swap-set analysis** | Who is approved by new vs old score | Cut-off strategy for a new scorecard |
| **NCO rate** | Net charge-offs ÷ average balances | Portfolio performance; stress-test target variable |

## 7. Bureaus and scores
- **US consumer:** Experian, Equifax, TransUnion; FICO (300–850), VantageScore.
- **US small business:** **FICO SBSS (0–300)** — blends principal(s)' consumer credit, business bureau data (D&B, Experian Business, Equifax), financial and application data. SBA used it to prescreen 7(a) small loans (minimum raised 155 → 165 in 2025) and **discontinued SBSS screening from 1 Mar 2026** (Procedural Notice 5000-875701; supplemental 5000-876777) — lenders now use their own credit policies/internal scoring that doesn't rely solely on consumer scores. **[Certain]**
- **India:** CIBIL (TransUnion), CRIF High Mark, Experian, Equifax; consumer scores 300–900; MSME: CIBIL MSME Rank (CMR, 1 best–10 worst). **[Likely]**

## 8. Capital in one page
- **Regulatory capital** absorbs unexpected loss; **provisions** absorb expected loss.
- **RWA** (risk-weighted assets) = Σ risk weight × exposure; capital ratios = capital ÷ RWA (CET1, Tier 1, Total).
- **Basel pillars:** Pillar 1 minimum capital · Pillar 2 supervisory review (ICAAP/SREP) · Pillar 3 disclosure.
- **Standardised vs IRB:** risk weights from tables/external ratings vs from internal PD/LGD/EAD (see `03_basel_irb.md`).

## 9. "How does a card issuer make money?" (AmEx favourite)
Revenue: **interest income** on revolving balances · **interchange / merchant discount revenue** (AmEx's largest line, because it runs a closed-loop network and charges merchants directly) · **card fees** (annual, late, FX). Costs: funding cost · **credit losses** · rewards and marketing · operating costs. Credit risk models drive approval, limits, pricing and loss provisions — i.e., both the revenue and the loss lines. **[Likely — check AmEx 10-K for current mix]**

## 10. Glossary (one line each)
- **Observation point / window, performance window:** when you take the snapshot / history used for predictors / period over which you measure the outcome.
- **Indeterminate:** neither clearly good nor bad (e.g., max 30–59 DPD) — excluded from development.
- **Cure:** a defaulted/delinquent account returning to performing.
- **Forbearance / restructuring:** concessions to a borrower in difficulty — a default/SICR trigger in many regimes.
- **Coverage ratio:** provisions ÷ non-performing (or total) loans.
- **Concentration:** single-name, sector or geography exposure share (HHI = Σ shares²).
- **Through-the-door population:** all applicants, before decisions.
