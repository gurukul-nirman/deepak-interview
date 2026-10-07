# 07 · Evidence bank, résumé v1 and LinkedIn — fill these first

> **Why this file exists (audit, 7 Oct 2026):** the kit's knowledge material is strong, but the material that decides
> offers is about **you**: your numbers, your decisions, your level. About 30% of interview time is spent drilling your
> own work, and the résumé decides whether you get interviews at all. This file turns your memory into defensible
> evidence. **Only you can fill it. Claude must never invent a number, a model or a story here** (CLAUDE.md rule 8).
>
> Time: about 90 minutes for §1, 60 minutes for the first résumé draft (§2). Then ask Claude `REVIEW RESUME`.

---

## 0. Confidentiality rules (read before writing anything)
- Use **ranges and orders of magnitude** ("~15 models", "~$X bn card book", "Gini down ~6 points"), not exact
  client-confidential figures.
- **No client name** unless your contract allows it. "A top-10 US bank" is normal and accepted.
- **Never copy client documents, code, templates or data** into this repo. Write from memory, in your own words.
- If you can't say something without breaching confidentiality, say what kind of thing it was ("a vendor-score input
  definition change") and the effect, not the details.

---

## 1. Evidence-mining worksheet (answer in 1–2 lines each)

### A. Scope and scale
| # | Question | Your answer |
|---|---|---|
| A1 | How many models did you personally work on in the last 12 months, by type (SBSS BCC, SBSS non-BCC, CECL/IFRS 9 PD/LGD/EAD, IRB PD/LGD/EAD, CCAR loss/balance)? | |
| A2 | Portfolio behind them: accounts, balances or exposure (order of magnitude) | |
| A3 | Frequency (monthly / quarterly / annual) and number of monitoring packs a year | |
| A4 | What did you **own end to end** vs execute? (data pull · code · metrics · breach diagnosis · commentary · presenting) | |
| A5 | Who used your output? (model owner · MRM/validation · committee · internal audit · regulator) Did you ever present it? | |

### B. Judgment and impact (these become your STAR-L stories)
| # | Question | Your answer |
|---|---|---|
| B1 | Breach 1: metric and value → how you ruled out data issues → root cause → action → who approved → outcome | |
| B2 | Breach 2 (different model family if possible) | |
| B3 | Breach 3 | |
| B4 | A time your recommendation changed a decision (overlay, recalibration, threshold, monitoring design, redevelopment) | |
| B5 | An error you found that others missed (data, definition, code, implementation) — how you spotted it, impact | |
| B6 | Numbers you can attach: hours saved by automation, manual steps removed, findings closed, validation/audit requests supported, juniors reviewed or trained | |

### C. Regime clarity — interviewers will ask "which rules, which entity?"
| # | Question | Your answer |
|---|---|---|
| C1 | **CECL or IFRS 9** — which one, for which entity and portfolio? (US books report under CECL; IFRS 9 applies only to non-US entities or parents.) | |
| C2 | **IRB** — US advanced approaches (12 CFR 217) or a UK/EU subsidiary's IRB? Which asset classes (wholesale, QRRE, other retail)? See `02_credit_risk/03_basel_irb.md` §1b | |
| C3 | **CCAR** — which models (loss, balance, PPNR)? Top-down or bottom-up? Which portfolios? Which tests did you run? | |
| C4 | **SBSS** — which decision does the score drive (approval cut-off, line, pricing, SBA prescreen)? Bad definition and performance window for BCC vs non-BCC | |
| C5 | What happened to the SBSS models after SBA stopped SBSS screening for 7(a) small loans on 1 Mar 2026? (If you don't know, find out — it's an obvious question.) | |

### D. Depth ranking — be honest, it decides what you lead with
| Model family | Years | Depth 1–5 (5 = survives 15 minutes of drill-down) | Lead · support · mention only |
|---|---|---|---|
| SBSS — BCC | | | |
| SBSS — non-BCC | | | |
| CECL / IFRS 9 | | | |
| IRB | | | |
| CCAR stress testing | | | |
| SmarterPay | 0 | 0 | **Mention only** — "being onboarded; KT this month" |

**Rule:** lead every "walk me through your work" answer with a depth-5 model. For anything at depth ≤ 3, say "I supported
X; my part was Y" — never stretch. Breadth across five model families at 5 years is a strength only if the depth claim
holds on the one you lead with.

### E. Level evidence (VP / Lead bar)
| # | Question | Your answer |
|---|---|---|
| E1 | Have you led a workstream, a deliverable or a small team? Size, scope, result | |
| E2 | Code or output reviews you did for others; standards or checklists you created | |
| E3 | Escalations you handled with the client (model owner, MRM, audit) | |
| E4 | Any direct interaction with internal audit, second-line validators or regulators? What exactly did you do? | |

---

## 2. Résumé v1 skeleton (2 pages; replace every `[…]` from §1)

```
[NAME] · [City] · [phone] · [email] · LinkedIn: [url]
Credit Risk Model Monitoring & Validation | CECL / IFRS 9 · Basel IRB · CCAR Stress Testing | SAS · SQL · Python

SUMMARY
Credit risk modelling professional with 5 years in model performance monitoring for a top-10 US bank, across
provisioning ([CECL/IFRS 9 — per C1]), capital ([IRB — per C2]) and stress-testing (CCAR) models, plus FICO SBSS
small-business scorecards. Diagnoses discrimination, calibration and stability breaches and writes the findings that go
to model owners and MRM. Moving into independent model validation / MRM.

EXPERIENCE
[Title], [KPO company] — embedded with a top-10 US bank's credit risk team          [MMM YYYY] – Present
• Owned quarterly performance monitoring for [A1: N] credit risk models ([types]) covering [A2: scale]; tested
  discrimination (KS/Gini), calibration (binomial/Jeffreys/A-E) and stability (PSI/CSI) against MRM thresholds.
• Diagnosed a [B1: metric + value] breach in [segment], traced to [root cause] after ruling out data issues;
  recommended [action], adopted by [model owner / MRM]; [outcome with a number].
• [B4: decision you changed — overlay / recalibration / threshold change], [impact].
• Found [B5: error] in [data / definition / implementation]; [impact quantified]; added [control].
• Automated [what] in [SAS/SQL/Python], cutting cycle time from [X] to [Y] days / removing [N] manual steps.
• Supported [N] [MRM validation / internal audit] requests with evidence and responses; [E2/E3 if true].
[Earlier role, if any — 2–3 bullets]

PROJECTS (personal, public data)
• Independent validation of a credit-card PD model (UCI data, Python) — [line from P1 ANSWER_KEY §6, with your numbers]
• [Optional] AI-governance risk assessment of a GenAI credit-memo assistant (fictional case) — [P2 line]

SKILLS
Regulatory: SR 26-2 (formerly SR 11-7), CECL, IFRS 9, Basel IRB / US advanced approaches, CCAR/DFAST, PRA SS1/23 (awareness)
Techniques: logistic regression & scorecards, WoE/IV, KS/Gini/PSI, calibration tests, time-series diagnostics, GBM/SHAP
Tools: SAS (Base, macros, STAT) · SQL · Python (pandas, statsmodels, scikit-learn) · Tableau (basic)

EDUCATION
B.Tech, Electrical & Electronics Engineering — [College], [Year]
```

**Do not put on the résumé:** CTC, notice period, photo, date of birth, SmarterPay as experience, "validated" for work
that was monitoring, tools you haven't used (PySpark only after you've practised it — see `05_coding/04_pyspark_primer.md`).

---

## 3. Review checklists (run both before sending)

**6-second recruiter scan**
- [ ] Headline uses the JD's words: model validation, model risk, CECL / IFRS 9, IRB, CCAR.
- [ ] Years of experience and "top-10 US bank" are visible in the first three lines.
- [ ] Current title and employer are unambiguous; dates are month + year.
- [ ] Two pages maximum; no dense blocks.

**2-minute hiring-manager read**
- [ ] A number in every experience bullet.
- [ ] It is clear what **you** did (owned / diagnosed / recommended) versus what the team did.
- [ ] Validation vocabulary used correctly and only where true (outcomes analysis, effective challenge, benchmarking).
- [ ] No over-claiming: monitoring is called monitoring; personal projects are labelled personal.
- [ ] Every line survives the question "tell me more about that" for five minutes.
- [ ] Removed: "responsible for", "worked on", "exposure to", tool lists without outcomes.

---

## 4. LinkedIn (after the résumé)
- **Headline:** Credit Risk Model Monitoring & Validation | CECL / IFRS 9 | Basel IRB | CCAR Stress Testing | SAS · SQL · Python
- **About (4 lines):** positioning sentence · scale (A1/A2) · two achievements with numbers (B1, B4) · "Open to model
  validation / MRM roles (India; Europe/Singapore later)".
- **Featured:** the P1 repository, once self-scored ≥ 85 (see the honesty rule in §6).
- **Open to Work → recruiters only.** Top skills: Model Validation · Credit Risk · IFRS 9 / CECL.

---

## 5. Lines for the questions your profile invites (rehearse aloud)
| Question | Honest, strong answer (adapt) |
|---|---|
| "Have you ever signed off a validation?" | "No — sign-off sits with the bank's MRM. I've owned the ongoing-monitoring and outcomes-analysis work that feeds validation, supported [N] validation and audit reviews, and completed a full independent validation end to end as a personal project. I can walk you through it." |
| "Your title is [X] at a vendor. What level were you really working at?" | Scope, not title: models owned, decisions influenced, who consumed your work (A4, A5, B4, E1–E4). |
| "Which IRB rules — US or EU?" | Answer C2 precisely. If US: advanced approaches, Collins floor, and what the March 2026 re-proposal means for the models' use. |
| "Why IFRS 9 at a US bank?" | Answer C1 precisely (which entity reports under IFRS). If it was CECL only, say CECL. |

More profile-specific questions (no Master's, no certifications, the CTC jump, notice) are scripted in
`06_interview_bank/04_behavioral_hr_negotiation.md` §3b.

---

## 6. Portfolio provenance — say it straight
- **P1 is a training case**, not a real bank's model: a deliberately flawed developer model and documentation on public
  UCI data, with a hidden answer key. Describe it as "a structured validation exercise on a deliberately flawed model".
  The judgment, findings, code you wrote (the six TODOs) and the report are yours; the scaffold (data loader, developer
  model, evidence pipeline, challenger functions) was supplied.
- If asked who built the flawed model: "It's a training case built with an AI tutor, with a hidden answer key. I wrote
  my findings before opening the key and scored myself against it."
- **Before you publish P1 or put it on your résumé, be able to explain every line of every file you publish.** If you
  can't explain the GBM challenger or the DeLong call, rewrite it yourself or leave it out. An interviewer who opens your
  repository and finds code you can't explain will treat it as a fabricated claim — a red flag that ends a process.
