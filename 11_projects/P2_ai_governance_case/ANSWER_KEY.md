# ⚠️ ANSWER KEY — Project P2 (CreditCopilot AI risk assessment)

> **Spoiler.** Open this only after your assessment and recommendation are written. Not for a public portfolio.
> Labels: **[Certain]** quote-able · **[Likely]** well supported, verify before quoting · **[Assumption]** illustrative.
> Not legal advice. Regulatory positions are as of Oct 2026.

---

## 1. Self-scoring (100 points)

| Component | Points | How to score |
|---|---|---|
| Critical issues found (I1–I6) | 36 | 6 each — the issue and the case-pack evidence |
| Major issues found (I7–I12) | 24 | 4 each |
| Other issues (I13–I14) | 4 | 2 each |
| Claims challenged (template §6) | 10 | At least 8 intake / vendor / pilot claims challenged correctly |
| Recommendation and conditions | 16 | Scope-limited approval with testable conditions (see §3), or a well-argued alternative |
| Precision and labelling | 10 | Correct roles and legal hooks; confidence labels; no over-claiming (e.g., "the EU AI Act bans this") |

**Bands:** ≥ 85 portfolio-ready · 70–84 fix the gaps · < 70 redo. Log misses in `09_progress/gap_log.md`.

---

## 2. Issues the case pack plants

### Critical
**I1 — The "suggested grade" is an unvalidated rating model.**
- **Why it matters:**
  - It produces a quantitative credit assessment that pre-fills a decision field.
  - Pilot: an 81% match and 96% within ±1 notch. Officers anchor on the pre-filled value, so agreement is partly
    circular.
  - The pilot has no default outcomes, so the grade's discrimination and calibration are unknown.
  - An LLM reading the methodology document is not an implementation of the rating methodology.
- **Expected response:**
  - Remove the grade suggestion, or hide it until the officer records an independent grade.
  - If the bank wants it, bring it into MRM as a rating model, with full validation and override monitoring.
  - "Out of MRM scope" is wrong whichever policy applies.

**I2 — Personal data is processed: the "no personal data" claim is false.**
- **What is in the pack:**
  - promoter and guarantor consumer bureau reports;
  - KYC (PAN, Aadhaar-masked, passports);
  - bank statements of proprietorships (individuals);
  - adverse-media searches on named people.
- **Hooks:**
  - DPDP Act 2023 + Rules 2025: notice and consent or a legitimate use, purpose limitation, security safeguards, breach
    reporting. Phased obligations run to May 2027 **[Certain]**.
  - GDPR (Amsterdam), including a DPIA for this processing **[Likely]**.
  - PDPA (Singapore) **[Certain]**.
  - Credit-information rules on the permitted use and sharing of bureau reports (CICRA) **[Likely]**.
- **Expected response:**
  - Run a DPIA / privacy assessment.
  - Apply data minimisation: does the LLM need full KYC images?
  - Define retention.
  - Specify vendor data-use terms.

**I3 — Indirect prompt injection is already happening (pilot #147).**
- **Evidence:** customers upload documents through the portal straight into the model. An out-of-place sentence
  recommending "grade 2" appeared in a draft — the signature of hidden instructions in a document (OWASP LLM01).
- **Expected response:**
  - Treat all uploaded content as untrusted.
  - Sanitise inputs: hidden text, white-on-white text, metadata.
  - Isolate instructions from data.
  - Constrain outputs: the grade comes from a controlled path or is removed.
  - Red-team with adversarial documents before go-live.
  - Investigate #147 as a security incident.

**I4 — Hallucinated and cross-application content in credit memos (pilot #203, #211).**
- **Evidence:**
  - EBITDA was misstated by about 3× and caught only by the committee.
  - A covenant from another borrower's sanction letter appeared in this memo. That points to the **single shared vector
    index** (OWASP LLM08), which is also a confidentiality breach between customers.
- **Expected response:**
  - Deterministic extraction and reconciliation of key financial figures against source, with a block on mismatch.
  - Mandatory citations.
  - Per-application index or strict metadata filtering with access control.
  - A leakage test.

**I5 — Human oversight is not effective; automation bias is designed in.**
- **Design problems:**
  - A pre-filled grade.
  - Throughput rising from 25 to 45 memos per officer per month.
  - "Edited in only 18%" is read as accuracy, when it may be rubber-stamping.
  - The #203 error passed the officer.
- **Hooks:**
  - NIST AI 600-1 "human–AI configuration" **[Certain]**.
  - EU AI Act Art. 14 (provider design for human oversight) and Art. 26 (deployer oversight by competent, trained staff)
    **[Certain]**.
  - GDPR Art. 22: a human who rubber-stamps does not make the decision "not solely automated". The CJEU in *SCHUFA*
    (C-634/21, Dec 2023) treated a score that plays a determining role as an automated decision **[Certain]**.
  - RBI FREE-AI sutra on individuals' final authority to override AI **[Likely wording]**.
- **Expected response:**
  - Officer records an independent view first.
  - 5–10% blind dual-review sample.
  - KRIs on edit rate, overrides and time-on-memo.
  - Throughput target tied to measured quality.
  - Training (AI literacy and oversight).

**I6 — The regulatory scoping is wrong in three places.**
- **(a) SR 26-2** is US Federal Reserve guidance. Kestrel has no US operations, so it does not apply. Even where it
  applies, GenAI being out of its scope ≠ ungoverned. The bank's own AI policy (RBI FREE-AI-aligned) and MRM policy
  govern **[Certain]**.
- **(b) EU AI Act — "only consumer credit".** Annex III 5(b) covers AI used to evaluate the creditworthiness of
  **natural persons** **[Certain]**. Sole proprietors, promoters and guarantors assessed from consumer bureau reports are
  natural persons. So the Amsterdam use is **likely high-risk** **[Likely — interpretive; check the Commission's Art. 6
  guidelines]**.
  - The Art. 6(3) "preparatory task" derogation is unavailable where the system profiles natural persons, and is weak
    anyway when the output pre-fills a grade **[Certain on the rule]**.
  - High-risk obligations apply from **2 Dec 2027** **[Certain]**: deployer duties (Art. 26), including logs kept for at
    least 6 months **[Certain]**; a **FRIA before first use** (Art. 27 names deployers of 5(b) systems) **[Certain]**; and
    explanation rights (Art. 86) **[Certain]**.
  - **Role trap — provider status:** if Kestrel repurposes a general document-summarisation product for creditworthiness
    evaluation, or puts its name on it, it may become the **provider** of a high-risk system under Art. 25, with
    provider obligations (QMS, technical documentation, conformity assessment, registration) **[Certain on the rule;
    application Likely]**.
  - AI literacy (Art. 4) has applied since 2 Feb 2025, softened by the AI Omnibus to "support the development of" AI
    literacy **[Certain]**.
- **(c) Singapore.** MAS AI risk-management guidelines were consulted on but are not final; FEAT principles and the PDPA
  apply **[Likely — check status]**.

### Major
**I7 — Vendor and third-party risk is unmanaged.**
- **Problems:**
  - Monthly silent model updates.
  - No audit rights; SOC 2 only.
  - A vendor-run benchmark ("< 1%").
  - Proprietary model.
  - 30-day "service improvement" retention, with opt-out on a higher tier only.
- **Hooks:** RBI Master Direction on outsourcing of IT services (2023) — access and audit rights for the bank and RBI,
  confidentiality, exit **[Likely detail]**; MAS outsourcing guidelines **[Likely]**.
- **Expected response:**
  - Version pinning and advance change notice.
  - Bank-owned regression suite run on every version.
  - Zero data retention, no training on bank data.
  - Audit rights.
  - Exit and fallback plan.
  - Independent testing on the bank's documents.

**I8 — Cross-border transfer and hosting.**
- **The issue:** US-region hosting of Indian, EU and Singapore personal and confidential data.
- **Hooks:**
  - DPDP s.16 permits transfers except to countries the Government restricts **[Certain]**.
  - GDPR Chapter V transfer mechanism (SCCs or the EU–US Data Privacy Framework) **[Certain]**.
  - PDPA transfer-limitation obligation **[Certain]**.
  - Bank secrecy and confidentiality.
- **Expected response:** a legal transfer assessment per jurisdiction; consider in-country or regional hosting.

**I9 — The agentic adverse-media search (pilot #188) has excessive agency.**
- **Problems:**
  - Open-web search on personal names produces misidentification (namesakes), defamation and privacy risk (NIST
    information integrity; OWASP LLM06).
- **Expected response:**
  - Use approved, licensed screening sources with entity resolution.
  - Require human verification before anything reaches a memo.
  - Disable autonomous browsing.

**I10 — The pilot evidence does not support the claims.**
- **Gaps:**
  - n = 220, one region, no confidence intervals.
  - Edit rate used as accuracy.
  - Grade agreement measured after anchoring.
  - "No complaints" — customers never see the memo.
  - No outcomes.
  - The vendor's hallucination rate was measured on the vendor's own benchmark.
- **Expected response:** a pre-production test plan on the bank's documents with defined metrics and thresholds (template
  §8).

**I11 — Bias and homogenisation are untested.**
- **Gaps:**
  - 12% of applications contain non-English documents and OCR quality was not measured. Worse extraction on them can
    mean worse memos and grades for smaller or regional businesses.
  - One model's style also homogenises credit judgement across 60 officers (NIST "harmful bias and homogenisation").
- **Expected response:** segment-level testing by language, region, sector and size; OCR quality metrics; monitoring.

**I12 — Explainability and customer rights.**
- **Gaps:** the grade suggestion is opaque. Citations explain the memo text, not the grade.
- **Hooks:**
  - Reasons for rejection must be conveyable to the applicant (RBI Fair Practices Code requires main reasons in writing
    **[Likely]**).
  - EU Art. 86 for natural persons once high-risk applies **[Certain]**.
- **Expected response:** the final decision rationale is written by the officer and grounded in documented factors.

### Other
- **I13 — Tiering, inventory and governance.**
  - The "Low" tier is wrong: material credit decisions, personal data, a third-party foundation model, agentic features,
    multi-jurisdiction. Expect High inherent risk.
  - The AI inventory is "being built". Register the use case with an owner, tier and review date.
- **I14 — Operational resilience and cost.**
  - No fallback if the vendor fails.
  - No consumption limits (OWASP LLM10).
  - No incident playbook or kill switch.

---

## 3. A strong recommendation looks like this

**Decision:** approve with conditions, **India only, scope-limited**. **Inherent tier: High.**
- **In scope:** drafting of memo narrative and financial analysis.
- **Out of scope:**
  - **Grade suggestion:** removed until validated as a rating model.
  - **Adverse-media agent:** disabled.
  - **Amsterdam and Singapore:** not approved pending local assessments, plus a FRIA (EU) if high-risk is confirmed.

| # | Condition before go-live | Owner |
|---|---|---|
| C1 | Grade field not pre-filled. The officer's independent grade is recorded first. Any future grade feature goes through MRM validation | Business + MRM |
| C2 | Prompt-injection defences, and a red-team pass on adversarial documents (threshold agreed with the CISO). Pilot #147 investigated | CISO |
| C3 | Deterministic reconciliation of key figures (revenue, EBITDA, debt, DSCR inputs) against source. Memo blocked on mismatch | Business + IT |
| C4 | Per-application data isolation in retrieval, with a leakage test passed | Vendor + IT |
| C5 | DPIA; per-jurisdiction cross-border assessment; contract changes: zero retention, no training on bank data, version pinning with notice, audit rights, exit plan | DPO + Legal + Procurement |
| C6 | Oversight design: 5–10% blind dual review; edit-rate, override and time-on-memo KRIs; throughput target tied to quality; AI-literacy and oversight training | Business |
| C7 | Monitoring, incident playbook, kill switch and fallback to the manual process | Business + AI risk |
| C8 | Bank-run test results on its own documents meet thresholds before rollout beyond the pilot region | AI risk / validation |

**Residual tier after conditions:** Medium. Re-assess before any scope expansion, and at least annually.

---

## 4. Common mistakes
1. Saying the EU AI Act "doesn't apply because borrowers are companies". Guarantors, promoters and sole proprietors are
   natural persons.
2. Saying it "bans" this use. It doesn't — high-risk means obligations, not prohibition.
3. Applying SR 26-2 to a bank with no US operations, or reading its GenAI exclusion as "no governance needed".
4. Treating "human in the loop" as a control without testing whether the human actually checks.
5. Missing the cross-application leak (#211). It is both a data breach and a sign of an architecture flaw.
6. Rejecting outright without a path. Good governance enables safe value: scope down, add conditions, expand on evidence.

---

## 5. Interview kit

**60-second pitch:**
> "I wrote an AI risk assessment for a GenAI credit-memo assistant at a fictional multi-jurisdiction bank. The pilot data
> showed the three classic GenAI failure modes in one place:
> - an indirect prompt injection from a customer-uploaded document;
> - a hallucinated EBITDA that passed the credit officer;
> - another borrower's covenant leaking in through a shared vector index.
>
> I reclassified it from 'Low, out of scope' to High inherent risk. I treated the suggested grade as an unvalidated rating
> model, and showed why the EU AI Act can apply to SME lending through guarantors. I recommended an India-only,
> narrative-only approval with eight testable conditions, and residual risk dropping to Medium."

**Drill-downs to rehearse:**

| Question | Crisp answer |
|---|---|
| Is a GenAI tool a "model"? | The component that produces a quantitative estimate used in decisions (the grade) is a model under most MRM policies. The narrative drafting falls under AI-policy governance. Either way, it is governed. |
| How do you validate an LLM? | Define the task. Build a bank-specific test set. Measure extraction accuracy, faithfulness and hallucination, robustness and injection resistance, segment performance and human-review effectiveness. Pin the version; regression-test every change; monitor in production. |
| Why is human-in-the-loop not enough? | Automation bias. Measure it: blind dual reviews, edit and override rates, time-on-task. Design against it: independent view first. |
| Provider or deployer? | Deployer by default. Provider if Kestrel puts its name on the system, substantially modifies it, or repurposes it into a high-risk use (Art. 25). |
| What is a FRIA? | Fundamental rights impact assessment before first use (Art. 27). Required for deployers of credit-scoring systems for natural persons. |
| What KRIs would you track? | Reconciliation-break rate; injection detections; leakage-test results; edit and override rates; dual-review disagreement; segment quality gaps; vendor version changes; incidents; cost per memo. |

**Résumé line (personal case — say so):** "AI governance case study (fictional bank): assessed a GenAI credit-memo
assistant across RBI FREE-AI, EU AI Act, DPDP/GDPR and NIST AI 600-1 / OWASP LLM Top 10. Reclassified it to High risk
and designed a scope-limited approval with eight testable controls and a validation plan."
