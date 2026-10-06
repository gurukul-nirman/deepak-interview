# 02.3 · Basel IRB — capital models, calibration, and validation

> Expect IRB depth at European/UK banks (Barclays, HSBC, StanChart, DB, UBS, SocGen, BNP) and Big 4. Even US-bank GCCs ask the basics (PIT vs TTC, capital formula intuition).

---

## 1. Basel in five lines
- **Basel I (1988):** crude risk weights. **Basel II (2004):** three pillars + **IRB**. **Basel III (2010–2017):** capital quality, buffers, leverage, liquidity; **2017 finalisation** adds the **72.5% output floor**, IRB input floors, and limits on A-IRB for some exposures. **[Certain]**
- **Implementation (as of Oct 2026):** EU CRR3 from Jan 2025 (output floor phased in); UK "Basel 3.1" from **1 Jan 2027** **[Likely — verify]**; US "endgame" timing still in flux **[verify]**.
- **Pillar 1** minimum capital · **Pillar 2** ICAAP/SREP (incl. stress testing, model risk) · **Pillar 3** disclosure.

## 2. Approaches for credit risk
| Approach | Bank estimates | Supervisor provides |
|---|---|---|
| Standardised | — | Risk weights (often from external ratings) |
| **F-IRB** (non-retail) | PD | LGD (e.g., 40% senior unsecured corporate under Basel III final, 45% for financial institutions), EAD/CCF, M |
| **A-IRB** | PD, LGD, EAD/CCF, (M) | Floors |
| **Retail IRB** | PD, LGD, EAD (no "foundation" option for retail) | Floors |

**Retail sub-classes:** residential mortgage · **QRRE** (qualifying revolving retail — cards) · other retail (incl. small business below a threshold — relevant to SBSS-type books).

## 3. The capital formula — intuition first
**ASRF / Vasicek one-factor model:** each borrower's credit quality depends on one systematic factor (the economy) and an idiosyncratic shock. Capital covers losses in a **1-in-1,000-year (99.9%) one-year** economic downturn, **minus EL** (EL is covered by provisions).

```
K   = LGD × [ N( (N⁻¹(PD) + √R · N⁻¹(0.999)) / √(1 − R) ) − PD ] × MA      (MA = 1 for retail)
RWA = 12.5 × K × EAD
```
- **R (asset correlation):** mortgages **0.15** · QRRE **0.04** · other retail 0.03–0.16 (falls as PD rises) · corporates 0.12–0.24 (falls as PD rises; SME size adjustment).
- **MA (maturity adjustment, non-retail):** b = (0.11852 − 0.05478·ln PD)²; MA = (1 + (M − 2.5)·b) / (1 − 1.5·b).
- **Why correlation falls with PD:** high-PD borrowers default for idiosyncratic reasons; low-PD ones default mainly in systemic downturns.
- Basel II applied a 1.06 scaling factor to IRB credit RWA; the Basel III finalisation removes it. **[Likely — check jurisdiction]**

**Worked risk weights (verified):** other retail PD 2%, LGD 45% → R = 9.5%, K = 4.64% → **RW ≈ 58%** · QRRE PD 2%, LGD 80% → **RW ≈ 51%** · mortgage PD 1%, LGD 15% → **RW ≈ 19%**.

**Defaulted exposures (A-IRB):** K = max(0, LGD_in-default − ELBE) (best-estimate expected loss).
**EL vs provisions:** shortfall (EL > provisions) is deducted from CET1; excess can count towards Tier 2 (capped).

## 4. Floors and data requirements (Basel III final; check local rules)
- **PD floor:** **0.05%** corporate & retail (0.10% for QRRE revolvers); Basel II used 0.03%. **[Likely]**
- **A-IRB LGD floors:** corporate unsecured **25%**; retail mortgages **5%**, **QRRE 50%**, other retail unsecured **30%**; secured exposures by collateral type. **[Likely]**
- **EAD/CCF input floor:** on-balance + 50% of off-balance exposure using the standardised CCF. **[Likely]**
- **History length (Basel II minimums):** PD ≥ **5 years**; LGD/EAD: retail ≥ **5 years**, corporate ≥ **7 years**. **[Certain]**
- **Rating scale (non-retail):** ≥ **7 non-default grades + 1 default grade**; avoid excessive concentration in one grade. **[Certain]**

## 5. Rating philosophy: PIT vs TTC vs hybrid
| | Point-in-time (PIT) | Through-the-cycle (TTC) |
|---|---|---|
| Grade assignment | Moves with the cycle | Stable across the cycle |
| Default rate within a grade | Stable | Varies with the cycle |
| Capital | Pro-cyclical | Stable |
| Typical use | IFRS 9, business decisions | IRB capital (often hybrid in practice) |

**How to tell which you have:** grade migration rates vs the cycle (PIT = many migrations in downturns), stability of the grade distribution, volatility of default rates per grade.

## 6. Calibration — the IRB sequence
1. **Rank-ordering model** (score/grades).
2. **Central tendency (CT) = long-run average default rate (LRADR)** over a period that includes good and bad years (representative of the cycle).
3. **Calibrate** grade PDs so the portfolio average matches CT (e.g., logit/odds shift: odds_new = odds_old × odds_CT / odds_current).
4. **Margin of Conservatism (MoC)** for estimation uncertainty — EBA GL/2017/16 categories: **A** data & methodological deficiencies · **B** relevant changes (underwriting, collections, environment) · **C** general estimation error. **[Certain]**
5. **Floors.**

**LGD:** long-run average over the cycle **and** a **downturn LGD** (EBA GL/2019/03 on downturn LGD; RTS on identifying downturn periods). Incomplete workouts must be treated (not ignored). **CCF/EAD:** similar logic, downturn consideration.

## 7. Definition of default (EU DoD)
90 DPD on a material obligation (**retail: €100 + 1%; non-retail: €500 + 1%**) **or** unlikeliness to pay (bankruptcy, distressed restructuring, specific provisions, sale at a material credit loss); **probation** ≥ 3 months (12 for distressed restructuring); retail contagion rules for joint obligations. **[Certain]**
→ A DoD change breaks time series: re-simulate history under the new definition and test the impact on PD/LGD.

## 8. Low-default portfolios (LDPs)
Too few defaults to estimate PD (banks, sovereigns, large corporates, some prime mortgages): **Pluto–Tasche** "most prudent estimation" (upper confidence bounds per grade), Bayesian methods, mapping to external ratings/agency default studies, expert judgment with conservatism.

## 9. Governance & use
- **Use test:** IRB parameters used in credit approval, limits, pricing, provisioning inputs, capital allocation.
- **Validation function independence**, annual review, internal audit review; **material model changes need supervisory approval** (EU: Delegated Regulation 529/2014). **[Likely]**
- **ECB TRIM (2016–2021)** harmonised supervisory expectations; the **ECB Guide to internal models** sets current expectations. **[Certain]**

## 10. Validating IRB models — tests regulators expect
| Parameter | Discrimination | Calibration | Stability / other |
|---|---|---|---|
| **PD** | AUC/Gini; **current vs initial-validation AUC** (test on the difference) | **Jeffreys test** per grade and portfolio; binomial / traffic-light | Migration matrices; **concentration (Herfindahl index)**; override rates; representativeness |
| **LGD** | **Generalised AUC** (ranking of LGD pools) | **t-test** realised vs estimated LGD; downturn adequacy | Cure-rate stability; workout completeness |
| **CCF/EAD** | Rank-ordering | **t-test** realised vs estimated | Limit-change effects |

*Tests listed follow the ECB's 2019 "Instructions for reporting the validation results of internal models" for IRB Pillar 1 models.* **[Likely]**

## 11. Interview questions
1. **Why 99.9% and one year?** Regulatory choice for a target solvency standard; one-year capital planning horizon.
2. **Why subtract PD in K?** EL is covered by provisions; capital covers *unexpected* loss.
3. **Why does correlation fall with PD?** Idiosyncratic vs systemic defaults.
4. **PIT vs TTC — which for IRB, which for IFRS 9?** IRB tends TTC/hybrid; IFRS 9 PIT + forward-looking.
5. **What is LRADR and how many years?** Average of annual default rates over a representative cycle; ≥ 5 years minimum, longer if needed to include a downturn.
6. **What is MoC? Give an example of each category.** A: missing variables in old data; B: new underwriting policy; C: sampling error.
7. **Downturn LGD — how?** Identify downturn periods (macro + realised loss data), estimate LGD in those periods or apply a calibrated add-on.
8. **How do you validate an LDP PD?** Pluto–Tasche bounds, benchmarking to external ratings, expert review, conservative calibration.
9. **What does the output floor do?** Caps how far IRB RWA can fall below 72.5% of standardised RWA (in aggregate).
10. **Your PD model fails the Jeffreys test in 3 grades — what next?** Check significance pattern (low vs high grades), cycle position (TTC expectation), data/DoD changes, then recalibrate or add MoC; report per policy.
