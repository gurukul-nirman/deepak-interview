# 04.1 · Model Risk Management: SR 11-7 → SR 26-2 (and how MRM works in practice)

> **Big news most candidates will miss:** on **17 April 2026** the Fed, OCC and FDIC replaced SR 11-7 with **SR 26-2** (OCC Bulletin 2026-13, FDIC FIL-15-2026). Interviewers still use SR 11-7 vocabulary (most bank policies were built on it), so you need **both**: SR 11-7 concepts + what changed. **[Certain — primary text read]**

---

## 1. SR 11-7 (2011) — the concepts every MRM interview still uses
- **Model definition:** "a quantitative method, system, or approach that applies statistical, economic, financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates." Three components: **inputs → processing → reporting/outputs**.
- **Model risk:** potential adverse consequences from decisions based on **incorrect or misused** model outputs. Two sources: **fundamental errors** and **inappropriate use**.
- **Effective challenge:** critical analysis by objective, informed parties; depends on **incentives, competence and influence**.
- **Development, implementation & use:** clear purpose, sound theory, data quality, testing, documentation; users understand limitations; conservatism/overlays where uncertain.
- **Validation (three core elements):**
  1. **Evaluation of conceptual soundness** (incl. developmental evidence)
  2. **Ongoing monitoring** (incl. **process verification** and **benchmarking**)
  3. **Outcomes analysis** (incl. **back-testing**)
  - Validation independent from development; scope/rigour commensurate with risk; **periodic review at least annually**; vendor models validated too.
- **Governance:** board & senior management oversight, policies/procedures, roles (owners, developers, users, control functions), **internal audit**, external resources, **model inventory**, **documentation**.
- Also: **aggregate model risk**, limitations, compensating controls.

**Companions now rescinded by SR 26-2:** OCC 2011-12 (same text for national banks) · FDIC FIL-22-2017 (adoption) · SR 21-8 / OCC 2021-19 / FDIC FIL-27-2021 (BSA/AML model risk statement) · OCC 1997-24 (credit-scoring model guidance) · OCC Comptroller's Handbook "Model Risk Management" booklet. **[Certain — per Orrick analysis]**

---

## 2. SR 26-2 (17 Apr 2026) — what it says
| Area | SR 26-2 position (quoted/paraphrased from the text) |
|---|---|
| **Applicability** | "Most relevant to banking organizations with over **$30 billion** in total assets"; may apply to smaller firms with significant model risk (previous practice: most relevant above ~$1bn). |
| **Legal status** | "Does not set forth enforceable standards or prescriptive requirements; accordingly, **non-compliance with this guidance will not result in supervisory criticism**" — but unsafe/unsound practices or violations of law can still trigger action. |
| **Model definition (narrower)** | "A **complex** quantitative method, system, or approach that applies **statistical, economic, or financial** theories to process input data into quantitative estimates." "Mathematical" dropped; **excludes** simple arithmetic (incl. spreadsheets), deterministic rule-based processes, and software without statistical/economic/financial theory. |
| **AI scope** | **Generative AI and agentic AI are out of scope** ("novel and rapidly evolving"); principles apply to traditional statistical models and **non-generative, non-agentic AI**. GenAI governed by broader risk management. Agencies plan an **RFI on MRM and AI** (incl. GenAI/agentic). |
| **Risk framework** | Model risk = **inherent risk** (assumptions, complexity, input quality, data constraints) in the context of **materiality = exposure + purpose**. Immaterial models may get lighter treatment (identify + monitor). Consider **aggregate** model risk. |
| **Effective challenge** | Requires **appropriate expertise, sufficient independence to maintain objectivity, and organizational standing and influence** to effect change. |
| **Development** | Clear statement of purpose; user input; testing (out-of-sample, out-of-time, alternative assumptions/methods, data quality) with rigour commensurate to complexity/materiality. |
| **Use** | Understand limitations; using a model **beyond its intended purpose** needs additional analysis and control review. |
| **Validation** | Nature/rigour align with **approach, use, materiality**; generally **before first use** (urgent exceptions allowed with limits, extra monitoring, stakeholder notice); **timing/frequency vary** (purpose, methodology, change frequency, data) — **no default annual cycle**; quality depends on **rigour and effectiveness, not organisational structure**. |
| **Validation components** | **Conceptual soundness** (interpretability measures or benchmarking may be more practical than theory for some models) · **Outcomes analysis** (back-testing, outlier analysis; breaches of thresholds → adjustment/recalibration/redevelopment) · **Ongoing monitoring** (performance under changing products/clients/data/markets; overlays, adjustment or redevelopment per policy). |
| **Governance** | Policies & procedures; clear roles and **conflict-of-interest** management; **internal audit evaluates** whether MRM is rigorous and effective (doesn't duplicate validation); oversight of external resources; **model inventory** sufficient to understand risk individually and in aggregate; adequate **documentation**. |
| **Vendor models** | Principles remain applicable even without code/data access: understand conceptual soundness, design, development data, performance; **ongoing monitoring + outcomes analysis**; document, justify and evaluate **customisations**. |
| **BSA/AML** | 2021 statement rescinded without replacement; AML models meeting the definition fall under the general framework. |

**Removed or de-emphasised vs SR 11-7 [Certain — Orrick/KPMG analyses]:** detailed discussion of VaR back-testing, parallel outcomes analysis, early-warning metrics, process verification of code, override analysis and benchmarking procedures; detailed board/senior-management duties; annual policy review; enumerated internal-audit tasks; reporting-line separation and compensation expectations for validators.

---

## 3. SR 11-7 vs SR 26-2 — the comparison table to memorise
| Topic | SR 11-7 (2011) | SR 26-2 (2026) |
|---|---|---|
| Nature | Principles, applied prescriptively in practice | Explicitly principles-based; non-compliance ≠ supervisory criticism |
| Scope | Broad; relevant to most banks | Most relevant > $30bn assets |
| Model definition | Statistical, economic, financial **or mathematical** methods | **Complex** methods using statistical/economic/financial theory; carve-outs |
| AI | Not addressed specifically | GenAI & agentic AI **excluded**; non-generative AI included |
| Risk assessment | Materiality/complexity implied | Explicit **inherent risk × materiality (exposure + purpose)** |
| Effective challenge | Incentives, competence, influence | Expertise, independence, organisational standing & influence |
| Validation cadence | **At least annual** review | **Risk-based**; varies with materiality, change, data |
| Independence | Detailed structural expectations | Rigour > organisational structure |
| Validation detail | Long: process verification, benchmarking, back-testing, overrides | Concise three components |
| Board/senior mgmt | Detailed duties | High-level governance principles |
| Internal audit | Enumerated tasks | Evaluate rigour/effectiveness; no duplication |
| Vendor models | Section within validation | Stand-alone section; customisations emphasised |
| BSA/AML | 2021 interagency statement | Rescinded; general framework applies |

---

## 4. Your 2-minute answer: "What changed with SR 26-2, and what does it mean for us?"
> "In April the agencies replaced SR 11-7 with SR 26-2. Four changes matter most. **First, scope and status:** it's framed as most relevant above $30 billion and explicitly not a source of supervisory criticism on its own — so it's a recalibration, not a relaxation of safety-and-soundness expectations. **Second, a narrower model definition** — 'complex' methods using statistical, economic or financial theory, carving out simple spreadsheets and deterministic rules — so inventories will be re-baselined. **Third, risk-based intensity:** model risk is inherent risk in the context of materiality — exposure plus purpose — and validation cadence follows that, replacing the de-facto annual cycle. **Fourth, GenAI and agentic AI are out of scope**, pending an RFI — so banks need their own governance for those under broader risk management.
> For a global bank like yours, I'd expect the core of the framework to stay — PRA SS1/23, ECB and OSFI E-23 still apply to group entities — but I'd use SR 26-2 to re-tier the inventory, move Tier 2–3 models to evidence-based cadences, and focus validator time on the material models, while building a separate control framework for GenAI use cases."

---

## 5. How an MRM framework works in practice (bank view)
**Lifecycle:** identification → tiering → development → **validation** → approval (committee) → implementation (testing) → use → **ongoing monitoring** → change management → periodic review → decommissioning.

**Core components:**
| Component | What it contains | Interview angle |
|---|---|---|
| Policy & standards | Model definition, tiering, validation standards, roles, findings severity, exceptions | "Walk me through your MRM policy." |
| **Model inventory** | Every model/tool with key attributes (below) | Completeness is a common audit finding |
| **Tiering** | Inherent risk × materiality → Tier 1/2/3 | Drives validation depth & cadence |
| Validation standards | Scope by tier; evidence expectations | Proportionality |
| **Findings management** | Severity, owners, due dates, closure validation, overdue escalation | KRIs |
| **Model use exceptions** | Temporary approvals; use before validation; use beyond scope | SR 26-2 allows with controls |
| **Change management** | Material vs non-material changes; re-validation triggers | "Is re-estimation a model change?" |
| **Overlays / PMAs** | Quantification, approval, monitoring, sunset | PRA & ECB focus area |
| Non-models / tools / EUCs | Controls proportional to risk (PRA SS1/23 refers to simple calculators as "deterministic quantitative methods", DQMs **[Likely]**) | Inventory boundary debates |
| **Vendor models** | Same principles; local validation | Your SBSS strength |
| Aggregate model risk | Shared data/assumptions/methods across models | Reported to committee/board |
| Reporting & committees | Model Risk Committee; board risk committee | Escalation path |

**Typical inventory fields:** model ID & name · description & purpose · uses (decisions, regulatory, financial reporting) · owner / developer / user / validator · tier & rationale · methodology & key inputs · vendor? version · implementation platform · upstream/downstream dependencies · validation dates & outcome · open findings & restrictions · monitoring frequency & last results · overlays · status (in use / retired).

**MRM KRIs:** % Tier-1 models overdue for validation · # open High findings and % overdue · # models used with restrictions/exceptions · # monitoring breaches unresolved · % inventory with complete attributes · overlay size as % of output.

---

## 6. Interview questions (governance)
1. **What is a model? Is a spreadsheet a model?** Depends on the definition: SR 11-7 broad (statistical/mathematical methods); SR 26-2 excludes simple arithmetic/spreadsheets and deterministic rules; PRA SS1/23 covers models and expects proportionate controls on DQMs.
2. **Three lines of defence in MRM?** 1st: owners/developers/users · 2nd: MRM/validation (+ policy) · 3rd: internal audit (tests whether MRM is effective).
3. **What is effective challenge? How do you evidence it?** §1/§2; documented questions, responses, and resulting model changes or restrictions.
4. **How do you tier a model?** Inherent risk × materiality (exposure + purpose) + complexity/uncertainty → Tier → depth & cadence.
5. **Validation cadence after SR 26-2?** Risk-based: materiality, change velocity, data availability, monitoring results; explicit triggers.
6. **Model used before validation — allowed?** In urgent cases with restrictions, extra monitoring, stakeholder notification, time-bound (SR 26-2).
7. **What makes a change "material"?** Changes to methodology, variables, segmentation, data sources, use, or output impact above a threshold → re-validation; minor recalibration within approved methodology → lighter review with monitoring.
8. **What is aggregate model risk?** Risk from shared assumptions/data/methods across models (e.g., one macro scenario feeding ECL, CCAR and ICAAP).
9. **How do you validate a vendor model?** §2 vendor row + `03_monitoring_validation/02_...` §10.
10. **Who owns model risk?** Model owner (1st line) owns the model's risk; MRM sets framework and challenges; board sets appetite and oversight.
11. **What's internal audit's role in MRM?** Assess whether the MRM framework is rigorous and effective and policies are followed — not re-validate models.
12. **How should GenAI be governed now that SR 26-2 excludes it?** Under the bank's broader risk management (AI policy, use-case risk assessment, controls, monitoring), informed by NIST AI RMF/ISO 42001 and other jurisdictions (EU AI Act, OSFI E-23, RBI draft, MAS draft) — see `03_ai_ml_genai_model_risk.md`.
