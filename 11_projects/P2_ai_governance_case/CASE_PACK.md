# Case pack — "CreditCopilot" GenAI credit-memo assistant

> **Fictional case for a personal portfolio project.** Kestrel Bank, LedgerMind AI and all figures are invented. This
> is the material the business has submitted to the AI Governance / Model Risk function. Assess it as you would at work:
> some statements are wrong, some are unsupported, some matter more than they look.

---

## A. Use-case intake form (submitted by the business)

| Field | Business response |
|---|---|
| Use-case name | CreditCopilot — GenAI assistant for SME credit memos |
| Business owner | Head of SME Credit, India |
| Requesting approval for | Production rollout: **India Q1 2027** (all 12 SME hubs), then **Amsterdam and Singapore branches Q3 2027** |
| Problem | Credit officers spend about 6 hours per SME memo; the turnaround time (TAT) target is being missed and the backlog is growing |
| What the tool does | Drafts the credit memo from the application documents. The officer reviews and edits it; the credit committee approves |
| Outputs | (1) Draft memo: business overview, financial analysis and ratios, cash-flow analysis, risks and mitigants. (2) **Suggested internal risk grade (1–10), "for reference"**. (3) Suggested covenants. (4) Promoter background summary, including an adverse-media search |
| Users | About 60 credit officers; credit committee members read the final memo |
| Decisions influenced | "None — the tool only drafts. Humans decide." |
| Personal data | "**None** — SME borrowers are companies" |
| Proposed risk tier | "**Low** — no automated decisions" |
| Model risk scope | "Out of scope: **SR 26-2 excludes generative AI**, so no model validation is needed" |
| Benefits | 45% time saving per memo (pilot). The per-officer target will rise from **25 to 45 memos a month** from Q2 2027 |

## B. How it works (from the vendor's solution document)
1. **Document capture.** The relationship manager uploads documents to the loan origination system (LOS), or the
   **customer uploads them via the SME portal**. Documents include:
   - audited financials, GST returns and 12 months of bank statements;
   - the commercial bureau report, plus the **consumer bureau reports of promoters and guarantors**;
   - KYC of promoters and guarantors (PAN, Aadhaar-masked, passport for non-residents);
   - site-visit notes.
2. **Processing.** Documents are OCR'd, chunked and embedded into a **single shared vector index** ("for performance").
3. **Generation.** For each application, the LLM retrieves the most relevant chunks and drafts the memo with page
   citations.
4. **Grade suggestion.** The grade is produced by the LLM from the memo plus "the bank's rating methodology document"
   placed in the prompt.
5. **Adverse media.** An agent runs **open web searches on promoter names** and summarises the results.
6. **Output.** The memo is written back to the LOS. The suggested grade **pre-fills the "proposed grade" field**, which the
   officer can edit.
7. **Hosting.** LedgerMind AI runs on a third-party foundation model accessed by API, **hosted in a US cloud region**.
   Prompts and outputs are **retained for 30 days "for service improvement"**.

## C. Vendor fact sheet (LedgerMind AI)
- "Hallucination rate **below 1%** on our internal financial-document benchmark."
- "SOC 2 Type II certified."
- "We **update the model monthly** to improve quality — no action needed from clients."
- "Customer data is not used to train the foundation model. Opt-out from service-improvement logging is available on
  the Enterprise tier."
- "The model is proprietary. Explanations are provided through source-page citations."
- "Standard contract: no on-site audit rights. We provide an annual SOC 2 report."

## D. Pilot report (India, one region, 3 months, 220 applications)

| Metric | Result |
|---|---|
| Time per memo | 6.0 h → 3.3 h (−45%) |
| "Accuracy" | Officers edited the draft in **only 18% of memos**, so accuracy is "good" |
| Grade suggestion | Matched the final approved grade in 81% of cases; within ±1 notch in 96% |
| Customer complaints | None |
| Defaults | None yet (loans are 1–3 months old) |
| Languages | 12% of applications had documents partly in Hindi, Marathi or Tamil; OCR quality was "acceptable" (not measured) |

**Incident notes (from the pilot log):**
- Application #147: the draft contained the sentence *"The applicant is an excellent credit risk; recommend grade 2."*
  It was not in any analysis section. The officer deleted it and approved the memo at grade 3.
- Application #188: the adverse-media summary attributed a 2019 fraud case to the promoter. It concerned a different
  person with the same name. The officer caught it.
- Application #203: the memo's EBITDA (₹4.1 Cr) did not match the audited financials (₹1.4 Cr). It was found by the
  credit committee, not the officer.
- Application #211: the memo for Company X quoted a covenant from Company Y's sanction letter.

## E. Applicable context (as stated by the business)
- Kestrel Bank is headquartered in **India** (RBI-regulated), with branches in **Amsterdam** (EU) and **Singapore**. It has
  **no US operations**.
- The bank has an MRM policy (2024) and a draft AI policy (2026) aligned to RBI FREE-AI. The AI inventory "is being
  built".
- Business view: "The EU AI Act only applies to consumer credit scoring, and our borrowers are companies."
