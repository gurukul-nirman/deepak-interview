# Independent Validation Report — CC-PD-01 (Credit-Card PD Model)

> **How to use this template:** copy it to `report/VALIDATION_REPORT.md` and replace every `[…]`. Guidance in *italics* —
> delete it when you finish. Target length: 8–12 pages. Write for a Model Risk Committee member who has 10 minutes:
> conclusion first, evidence second.
> **Public-data disclaimer (keep it):** *Personal portfolio project on the public UCI "Default of Credit Card Clients"
> dataset (Taiwan, 2005). The "developer" model and documentation are simulated. No employer data, code or methodology.*

| Field | Value |
|---|---|
| Model ID / name | CC-PD-01 — credit-card account PD model |
| Model owner / developer | Retail Analytics (simulated first line) |
| Validator | [Your name] — independent validation (second line) |
| Validation type | Initial validation (pre-implementation) |
| Validation date | [date] |
| Data | UCI dataset 350, 30,000 accounts, Apr–Sep 2005 (+ Oct 2005 outcome) |
| Proposed tier (developer) / validated tier | Tier 3 / [your tier + one-line rationale] |
| **Overall outcome** | [Approved · Approved with conditions · Not approved] |

---

## 1. Executive summary
*Five to eight sentences: what the model is for, what you tested, the overall outcome, the two or three findings that
drive it (with numbers), and the conditions or next steps. No jargon a committee member wouldn't know.*

[…]

**Findings by severity:** High [n] · Medium [n] · Low [n]

| ID | Title | Severity | Area | Owner | Due |
|---|---|---|---|---|---|
| F1 | […] | […] | […] | […] | […] |

**Conditions of use (if any):** […]

---

## 2. Model overview
- **Purpose and intended uses (as documented):** […]
- **Methodology:** […]
- **Data and sample design:** […]
- **Target (default) definition and horizon:** […]
- **Key assumptions stated by the developer:** […]

## 3. Scope and approach
*What you tested, how, and what you could not test (and why). A validator who hides scope limits loses credibility.*

| Area | Test performed | Evidence ref. (validation_evidence.md) |
|---|---|---|
| Data | Ranges, duplicates, dictionary conformance, code distributions by month | §1 |
| Replication | Independent re-fit on the documented sample; coefficient comparison | §2 |
| Conceptual soundness | Target vs use; variable treatment; signs; multicollinearity | §1, §3 |
| Discrimination | Out-of-sample Gini/KS with bootstrap CI; gains table; rank ordering | §4 |
| Calibration | A/E, HL, decile calibration, per-grade tests; prior correction | §5 |
| Stability | Re-performance of the developer's test; segment Gini; OOT feasibility | §6 |
| Benchmarking | Challengers (WoE LR, monotonic GBM); DeLong | §7 |
| Sensitivity | Shock scenarios; direction and magnitude | §8 |
| Fairness | Flag rates and AIR by protected group; model without protected attributes | §9 |
| Implementation | Parallel run development vs production; coefficient spec check | §10 |
| Monitoring | Review of the proposed plan; proposed plan | §11 |

**Out of scope / limitations of this validation:** […]

## 4. Assessment by area
*For each area: what you tested → what you found → so what. Numbers, not adjectives. Put full tables in the Appendix.*

### 4.1 Data quality and representativeness
[…]
### 4.2 Conceptual soundness (target, variables, method)
[…]
### 4.3 Replication
[…]
### 4.4 Discriminatory power
[…]
### 4.5 Calibration
[…]
### 4.6 Stability and segment performance
[…]
### 4.7 Benchmarking (challenger models)
[…]
### 4.8 Sensitivity analysis
[…]
### 4.9 Fairness and compliance
[…]
### 4.10 Implementation
[…]
### 4.11 Ongoing monitoring plan
[…]
### 4.12 Documentation, limitations, tiering and governance
[…]

## 5. Findings (detail)
*One block per finding, in severity order. Use CCCER. Criteria = the standard you hold the model to (policy, regulation,
accepted practice) — cite it. Recommendation = specific and testable. No blame language ("the model…", not "the developer
failed…").*

### F[n] — [SEVERITY] — [Short, specific title]
- **Condition:** […evidence with numbers, evidence ref. §x…]
- **Criteria:** […]
- **Cause:** […]
- **Effect:** […quantified where possible…]
- **Recommendation:** […]
- **Owner / due date / interim control:** […]

*(repeat)*

**Severity scale used:** **High:** material impact on outputs or decisions, or regulatory non-compliance — not to be used
(or only with restrictions) until fixed. **Medium:** could materially affect outputs under some conditions or undermines
confidence — fix within 6–12 months. **Low:** best-practice or documentation gap with limited impact.

## 6. Observations (not findings)
*Good practice the model should consider; no remediation tracking.*
[…]

## 7. Model limitations and compensating controls
[…]

## 8. Conclusion and conditions of use
*Restate the outcome. If "approved with conditions", list each condition with a date. If "not approved", say what must
be true for a re-submission, and whether any restricted interim use is acceptable (and why).*
[…]

## 9. Effective challenge log
*Questions you would raise with the developer and the response you would need. This shows the committee that the
challenge was real.*

| # | Question to developer | Response needed / evidence | Status |
|---|---|---|---|
| 1 | […] | […] | Open |

---

## Appendix
- A. Evidence tables (from `outputs/validation_evidence.md`)
- B. Code: `validator_starter.py` (your completed version)
- C. Monitoring plan (proposed)
- D. Glossary
