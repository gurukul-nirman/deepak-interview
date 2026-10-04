# 04.3 · AI, ML and GenAI Model Risk — what to say, what to test

> **Positioning for you:** you're not applying for GenAI-validator roles (Citi's ask 2+ years of hands-on GenAI). But almost every 2026 validation interview has one AI question. A structured, honest answer here is a cheap differentiator. Traditional ML validation is covered in `01_foundations/03_ml_for_credit_risk.md` §7.

---

## 1. Where regulators stand (Oct 2026)
| Regulator | Position on AI |
|---|---|
| **US (SR 26-2)** | Principles apply to traditional and **non-generative, non-agentic AI**; **GenAI & agentic AI out of scope**, to be governed by broader risk management; an interagency **RFI on MRM and AI** is planned. **[Certain]** |
| **UK (PRA SS1/23)** | AI/ML models are models; PRA focus on tiering and inventories for AI (Nov 2025 roundtable). **[Likely]** |
| **EU** | ECB guide (2025): ML in internal models must be explainable and justify complexity; **AI Act** high-risk rules for credit scoring from **2 Dec 2027**. **[Certain]** |
| **Canada (OSFI E-23)** | AI/ML explicitly inside the model definition; effective 1 May 2027. **[Certain]** |
| **India (RBI draft, Jun 2026)** | Covers AI/ML incl. third-party; explainability & human oversight for AI decisions; GenAI safeguards. **[Likely — summaries]** |
| **Singapore (MAS draft)** | AI risk-management guidelines for all FIs (final pending). **[Likely]** |

---

## 2. Risk taxonomy for GenAI / LLM use cases
| Risk | Example in a bank |
|---|---|
| **Hallucination / factual error** | Chatbot invents a fee; credit memo summary misstates a covenant |
| **Grounding failure (RAG)** | Retrieves the wrong policy version |
| **Bias / toxicity** | Different tone or outcomes by customer group |
| **Robustness** | Small prompt changes flip answers |
| **Security** | **Prompt injection**, jailbreaks, data exfiltration via tools |
| **Privacy** | PII leakage in outputs/logs |
| **Non-determinism / reproducibility** | Same input, different outputs; vendor silently updates the model |
| **Third-party / concentration** | Opaque training data; dependence on one foundation-model vendor |
| **Over-reliance (automation bias)** | Analysts stop checking outputs |
| **Agentic risk** | An agent takes an action (sends, books, changes) beyond its authority |

---

## 3. How to validate a GenAI use case — your 5-pillar answer
1. **Use-case scoping & materiality** — what decision or customer outcome does it influence? Human in the loop? Customer-facing? → tier it.
2. **Data & knowledge sources** — RAG corpus quality, versioning, access rights, retrieval precision/recall.
3. **Performance evaluation** — task-specific metrics on a **golden dataset** (accuracy, groundedness/faithfulness, answer relevance, hallucination rate, completeness); human expert review; **LLM-as-judge only if calibrated against human ratings**; compare against a baseline (rules, search, smaller model).
4. **Robustness, safety & fairness** — red-teaming (prompt injection, jailbreaks), perturbation tests, toxicity and bias tests across demographic variants, PII-leakage tests.
5. **Controls & monitoring** — guardrails (input/output filters), human review thresholds, logging and audit trail, **version pinning** and change management for model/prompt/retrieval changes, drift and incident monitoring, user feedback loops, fallback/kill-switch, vendor management.

**Extra for agentic AI:** least-privilege permissions, tool-call validation, sandboxing, step/spend limits, human approval for high-impact actions, full action logs.

**Frameworks to name:** NIST AI RMF (**Govern, Map, Measure, Manage**) + GenAI profile · ISO/IEC 42001 (AI management system) · EU AI Act high-risk requirements.

---

## 4. Model answer — "How would you validate an LLM-based credit memo summariser?"
> "First I'd scope it: it drafts summaries that a credit officer reviews, so it influences but doesn't make decisions — medium tier, with human review as a key control. Then I'd test it like any model, adapted for language: a golden set of memos with expert reference summaries; measure factual accuracy and **faithfulness** — every number and covenant traceable to the source — plus completeness of key risk factors; track hallucination rate. I'd stress it with messy inputs and prompt-injection text embedded in documents, check consistency across repeated runs, and test for PII leakage. On controls: version pinning, logging, a mandatory officer sign-off, sampling-based QA in production, and drift monitoring when the vendor updates the model. Under SR 26-2 this sits outside the MRM guidance's formal scope, so I'd govern it under the bank's AI risk framework — but with the same evidence standards I'd apply to a model."

---

## 5. Model answer — "How would you validate an XGBoost PD model?"
> "Same pillars as a scorecard, plus ML-specific checks: justification of complexity versus a logistic benchmark with an out-of-time DeLong test; leakage tests; hyperparameter tuning governance; monotonic constraints on key drivers; calibration after training; SHAP-based global and local explanations checked against business intuition, and reason codes for adverse action; fairness testing on lawful proxies; stability across seeds and time; training–serving parity in implementation; and monitoring for feature drift, SHAP drift and performance on matured outcomes, with a clear rule for when retraining counts as a model change."

---

## 6. Using GenAI as a validator (productivity — appears in the WF LQAS JD)
Good uses: drafting code to re-implement metrics, documentation review checklists, summarising long MDDs, generating test cases. **Controls:** never paste confidential data into unapproved tools; verify every line of generated code (independent re-computation); keep humans accountable for conclusions.
**Interview line:** "I use approved GenAI tools to speed up code and documentation work, but every output is independently checked — the validator remains accountable."

---

## 7. Rapid-fire
1. *Is GenAI in scope of SR 26-2?* No — explicitly excluded; governed under broader risk management; RFI pending.
2. *Biggest LLM risk in a bank?* Context-dependent; for customer-facing: hallucination + prompt injection; for internal: over-reliance and data leakage.
3. *How do you measure hallucination?* Golden set + factual-consistency checks against sources (human or calibrated automated judges); report rate with CIs.
4. *Can you use an LLM to judge an LLM?* Yes, as a scalable screen, if its agreement with human experts is measured and acceptable.
5. *What's different about validating agentic AI?* Actions and permissions — validate what it can *do*, not just what it *says*.
