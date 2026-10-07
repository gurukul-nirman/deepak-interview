# 11 · Portfolio projects

**Should you build projects? Yes — two, small and targeted.**
- Your profile gaps are:
  - **monitoring → independent validation**;
  - **no AI-governance exposure**;
  - **B.Tech, no Master's or certifications**.
- Each project closes one gap with evidence you can talk through for 20 minutes under drill-down.
- More projects than these two would eat time better spent on mock interviews.

| | P1 · PD-model validation report | P2 · AI-governance risk assessment |
|---|---|---|
| Folder | `P1_pd_model_validation/` | `P2_ai_governance_case/` |
| You play | Second-line validator of a flawed credit-card PD model | Second-line AI / model-risk reviewer of a GenAI credit-memo tool |
| Data | Public UCI dataset (Taiwan 2005) + simulated developer pack | Fictional case pack |
| Hands-on | Python: replication, Gini/KS, calibration, prior correction, challengers, DeLong, fairness, parallel run | Classification across RBI / EU / SG, NIST AI 600-1, OWASP LLM Top 10, controls, test plan |
| Deliverable | `report/VALIDATION_REPORT.md` (8–12 pages) | `report/AI_RISK_ASSESSMENT.md` (6–10 pages) |
| Time | ~13 h (weeks 2–4) | ~3 h compressed memo (week 4); full version ~5 h only for AI-heavy roles |
| Planted issues | 13 findings (4 High) | 14 issues (6 Critical) |
| Proves | You can run a full validation and write findings that stand up | You can govern GenAI with a jurisdiction-aware, practical lens |

## How it works
1. Each project has a README with steps and a template.
2. Each project has an **answer key you open only after writing your deliverable**.
3. Self-score with the rubric, log misses in `09_progress/gap_log.md`, then ask Claude for a Head-of-MRM review:
   `REVIEW PROJECT P1` or `REVIEW PROJECT P2`.
4. Track the stage in `09_progress/skills_matrix.md` → "Portfolio projects".

**Priority (audit, 7 Oct 2026):** P1 is the one that moves offers — it answers "you've only monitored". P2 is a
differentiator; keep it compressed unless an AI-governance role is in your pipeline. Neither replaces your real work
stories (`00_strategy/07_evidence_bank_and_resume.md`), which carry more interview weight than both projects together.

## Rules that protect you
- **Public or fictional data only.** Never employer data, code, templates or documents.
- **Always label them as personal projects** — on the résumé, LinkedIn and in interviews. Presenting them as employer
  work is a red flag that can end a process (and an offer, at background check).
- **Check your employment contract** for IP or outside-work clauses before publishing anything **[Assumption — contracts
  vary]**.
- **Never publish the answer keys.**
- **Describe them as what they are** — training cases with planted issues — and publish only code you can explain line
  by line (`00_strategy/07_evidence_bank_and_resume.md` §6).

## How they show up in interviews
- **Résumé:** a "Projects" section with one line each (see each answer key §6 / §5). Link the public repo.
- **Technical rounds:**
  - "Walk me through a validation" → P1.
  - "How would you govern GenAI?" → P2.
  - Lead with the conclusion, then the top findings with numbers.
- **Hiring-manager round:** it shows initiative and self-directed upskilling. Frame it as "I wanted hands-on independent
  validation experience before moving into a validation role".
- **Mock practice:** `START TOPIC T12` (your projects deep-dive) drills both projects once they're written.
