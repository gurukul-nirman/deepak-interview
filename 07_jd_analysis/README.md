# 07 · JD Analysis — turn each job description into a targeted prep pack

**When you share a JD with me** (paste text or a link), I'll create `07_jd_analysis/<company>_<role>.md` using the template below and update your plan. You can also run the process yourself in ~45 minutes per JD.

---

## 1. The process (per JD)
1. **Extract** every requirement (skills, model types, regulations, tools, years, degree, soft skills).
2. **Map** each to a prep file (table in §3) and rate your readiness: ✅ ready · 🟡 revise · 🔴 gap.
3. **Predict questions:** for each 🟡/🔴 requirement, list the 3 most likely questions (use the Tier-1 bank + ladders).
4. **Company dossier** (§4).
5. **Tailor** the 90-second pitch, 3 resume bullets and 2 "why us" points.
6. **Mock** the predicted questions with me.

---

## 2. Template — copy into `<company>_<role>.md`
```
# <Company> — <Role title> (<Location>, Req ID)
Grade/level: ____    Line: 1st / 2nd    Team: ____    Recruiter/referrer: ____
Pay signal (band data from 00_strategy/01): ____    Our ask: ____

## Requirements → readiness
| JD requirement (verbatim) | Topic | Prep file | Readiness | Action |
|---|---|---|---|---|

## Hard screens (degree, years, tools) and how we address them
-

## Predicted questions (top 15) and my answer notes
1.

## Company dossier
- Regulator(s) & key regs:
- Main portfolios/products & model types:
- Recent news (results, regulatory actions, AI initiatives, restructuring):
- Interview pattern (rounds, tests) — from recruiter/Glassdoor/AmbitionBox:
- People on the panel (LinkedIn): background → likely focus

## Tailored pitch (90 sec) + 3 resume bullets + 2 "why us"

## Questions I'll ask them (2 per round)
```

---

## 3. Keyword → topic → file map
| JD keyword | Topic | File |
|---|---|---|
| model validation, effective challenge, conceptual soundness, outcomes analysis | Validation process & findings | `03_monitoring_validation/02_independent_validation_playbook.md` |
| ongoing monitoring, KS, Gini, PSI, back-testing, calibration | Metrics & diagnosis | `03_monitoring_validation/01_performance_monitoring_metrics.md` |
| scorecard, PD model, logistic regression, WoE/IV | Scorecards | `01_foundations/02_logistic_regression_and_scorecards.md` |
| IFRS 9, CECL, ECL, SICR, staging, Ind AS 109, RBI ECL | Provisioning | `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` |
| IRB, Basel, RWA, LGD, EAD, CCF, MoC, downturn | Capital models | `02_credit_risk/03_basel_irb.md` |
| CCAR, DFAST, stress testing, ICAAP, PPNR, time series | Stress testing | `02_credit_risk/04_stress_testing_ccar.md` |
| SR 11-7, SR 26-2, OCC 2011-12, MRM framework, model inventory, tiering | Governance | `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md` |
| PRA SS1/23, ECB, EBA, OSFI E-23, RBI, EU AI Act, MAS | Regulations | `04_governance_regulation/02_global_regulations_quick_reference.md` |
| machine learning, XGBoost, SHAP, explainability, fairness, fraud | ML validation | `01_foundations/03_ml_for_credit_risk.md` |
| GenAI, LLM, agentic AI | AI model risk | `04_governance_regulation/03_ai_ml_genai_model_risk.md` |
| Python, PySpark, pandas | Coding | `05_coding/01_python_for_validation.md` |
| SQL, Teradata, Oracle, Snowflake, Hive | SQL | `05_coding/02_sql_for_credit_risk.md` |
| SAS, Base SAS, macros | SAS | `05_coding/03_sas_essentials.md` |
| statistics, econometrics, hypothesis testing | Stats | `01_foundations/01_statistics_from_scratch.md` |
| stakeholder management, communication, leadership | Behavioural | `06_interview_bank/04_behavioral_hr_negotiation.md` |

**Not yet covered in depth (tell me if a JD needs them):** market risk / counterparty credit risk model validation (VaR, FRTB, CVA, PFE), AML/transaction-monitoring model validation, pricing/ALM models, operational-risk models, PySpark at scale. I'll add a focused module the moment a JD you're pursuing requires one.

---

## 4. Company dossier checklist (20 minutes)
- [ ] Regulator(s) and which MRM/IRB/ECL rules apply to the entity you'd support
- [ ] Portfolio/product mix → which models you'd likely validate
- [ ] Latest annual report: credit losses trend, ECL/allowance drivers, CET1, any regulatory actions
- [ ] AI initiatives (press releases, careers pages — e.g., Citi's GenAI validation team)
- [ ] India centre: size, location, teams (LinkedIn search: "<Company> model risk Bengaluru")
- [ ] Interview reports (AmbitionBox/Glassdoor/LinkedIn) — rounds, tests
- [ ] Panel members' backgrounds → tune examples
