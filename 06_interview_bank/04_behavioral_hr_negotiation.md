# 06.4 · Behavioural, HR & Negotiation (to land ≥ ₹40L fixed)

> Behavioural rounds rarely win you the offer, but they often lose it — and **negotiation decides whether the offer meets your 40-fixed floor.** The psychology: interviewers fear *risk* (will this person be independent, credible with regulators, not a "metric runner"?). Every story should reduce that fear with evidence.

---

## 1. STAR-L format (VP-bar version)
**S**ituation (1 line) → **T**ask (your responsibility) → **A**ction (what *you* did — 60% of the answer; decisions, not activities) → **R**esult (a number) → **L**earning (what you'd do differently/now do by default). 90–120 seconds.

## 2. Ten story slots — fill each from your real work (never invent)
| # | Competency probed | Prompt to fill | Must include |
|---|---|---|---|
| S1 | Analytical depth | A breach you diagnosed (PSI/Gini/calibration) | Metric, root cause, how you ruled out data issues, action, approval |
| S2 | **Effective challenge** | You challenged a developer/client/senior with evidence | Their position, your evidence, how you kept the relationship, outcome |
| S3 | Rigour | An error others missed (data, code, definition) | How you spotted it, impact quantified |
| S4 | Ownership / efficiency | Automation or process improvement | Before/after time or error rate |
| S5 | Pressure | Tight regulatory deadline (CCAR/ECL quarter-end) | Prioritisation, trade-offs, result |
| S6 | Communication | Explaining a technical issue to non-technical stakeholders | The analogy/visual you used, decision enabled |
| S7 | Self-awareness | A mistake you made | Ownership, fix, control you introduced |
| S8 | Leadership | Mentoring/reviewing juniors | What changed in their work |
| S9 | Collaboration / conflict | Disagreement inside your team | How you resolved it |
| S10 | Learning agility | Learned a new tool/method fast (e.g., Python, ML, new regulation) | Timeline, application |

**Example skeleton for S2 (replace brackets with facts):**
> *S:* Quarterly monitoring of the [BCC SBSS] model showed [PSI 0.2x] and the client's modeller attributed it to seasonality. *T:* I owned the monitoring commentary to MRM. *A:* I split the shift by channel and vintage, showed [x%] came from [new digital applications with younger businesses], and that bad rates for that group were running [y] vs expected. I proposed channel-level monitoring and an early-read check rather than a "seasonal" note. *R:* MRM accepted; the client added [channel segmentation]; [the next quarter's early reads confirmed the gap / informed a cut-off change of z]. *L:* I now decompose every stability breach by segment before writing a cause.

---

## 3. The "why" questions — answer frameworks
- **Why leave after 5 years?** "I've built depth in performance monitoring across provisioning, capital and stress-testing models. The next step is owning independent validation end-to-end inside a bank — closer to governance, committees and regulators. Your role offers exactly that." *(Never criticise the current employer.)*
- **Why validation (vs development)?** "I'm strongest at the questions validation asks — is this right, is it robust, what breaks it — and I want my judgment to carry independent weight."
- **Why us?** One specific fact about their model landscape/regulatory scope/AI validation work + one about the team. Research it (see `07_jd_analysis/`).
- **Why should we hire you over someone with direct validation experience?** "Breadth across IFRS 9, IRB and CCAR models, plus vendor-model experience; I've done the outcomes and monitoring pillars hands-on and practised full validations — here's how I'd validate your [model type] in the first 90 days…"
- **Strengths/weakness?** Strength: root-cause analysis under ambiguity. Weakness (real, being fixed): "Python depth — I've moved my metric code to Python over the last months and use it for [x]."
- **Where in 5 years?** "Leading validations for a model family and mentoring a small team; deep in AI/ML validation as it becomes core to MRM."

---

## 4. HR screen — numbers and facts ready
| Question | Your line |
|---|---|
| Current CTC | State it exactly as per payslips/offer letter — BGV verifies. Separate fixed and variable if asked. |
| Expected CTC | "For a Lead/VP-band role with this scope, I'm targeting **₹40–45L fixed**. I'm open on structure if the level and role are right." *(Anchor high-but-defensible; the band data in `00_strategy/01_market_reality_and_targets.md` supports it.)* |
| "That's a big jump from 26.5" | "It reflects the level, not a hike on my current role — I'm moving from a vendor-side role to an in-house second-line role, and I'm benchmarking against the band for this grade." |
| Notice period | "Three months, and my contract doesn't allow a buy-out. I'll plan a clean handover and can start earlier if my employer agrees to release me." Say it in the first call — never hide it. |
| Other offers | Truthful: "I'm in late stages with two banks." (Only if true.) |

---

## 5. Negotiation playbook

**Rules**
1. **Level first, money second.** A VP/Lead grade moves the whole band (fixed, bonus %, RSUs, future hikes). Ask: "What would it take to be considered at the [Lead/VP] grade?"
2. **Never accept on the call.** "Thank you — I'm excited about this. Could you share the written breakup? I'll come back within 48 hours."
3. **Negotiate fixed before variable.** Variable payouts vary; your floor is fixed.
4. **Use competing offers truthfully.** Specific numbers, specific deadlines.
5. **Joining bonus** to cover the variable you forfeit by leaving mid-cycle — easier for HR to approve than fixed. (Your notice can't be bought out, so don't trade money for an earlier start.)
6. **Get everything in writing:** fixed, target variable %, historical payout %, joining/retention bonus (clawback terms), RSUs/deferred comp, notice period, level/title, location, WFH.
7. **BGV:** no inflation of current pay or titles — offers are revoked over this.

**Scripts**
- *They offer ₹34L fixed:* "I appreciate it. Based on the scope we discussed — independent validation of [Tier-1 IFRS 9/CCAR] models — and the band for this grade, I was expecting 40–42 fixed. I also have a process at [Bank B] at that level. Is there flexibility on fixed, or on the grade?"
- *"We can't go beyond a 30% hike":* "I understand the policy for in-grade moves. This is a level change from a vendor-side role, so I'd ask you to benchmark against the internal band for this grade rather than my current CTC."
- *They raise to 37 fixed:* "Thank you — we're close. If we can get fixed to 40, I'm ready to sign this week. Alternatively, 38 fixed with a ₹3L joining bonus would also work." *(Only offer alternatives you'd accept.)*
- *Counter-offer from current employer:* decide your answer before resigning; counter-offers rarely fix the reason you're leaving.

**Decide your walk-away rule now (your call — suggestion only):** a written decision matrix, e.g., accept if *fixed ≥ 40* **or** *(fixed ≥ 37 and grade = VP/Lead and strong brand/AI-validation exposure)*. Pre-deciding protects you from anchoring on the first offer. **[Assumption — adapt to your priorities]**

**Offer comparison sheet (columns):** company · grade/title · fixed · target variable % · last 2 years' payout % · joining/retention bonus (clawback) · RSUs/deferred · benefits (insurance, PF treatment in CTC) · notice period · location/WFH · team/manager quality · model types · AI/ML exposure · growth path.

---

## 6. Abroad offers — extra items
- **UAE/Saudi:** basic vs allowances (housing, transport), annual flights, medical, schooling, **end-of-service gratuity**, visa costs, notice; tax-free — compare on take-home + cost of living.
- **Singapore:** Employment Pass eligibility (COMPASS), relocation, housing cost reality.
- **UK:** sponsorship (Skilled Worker), relocation support, pension, London vs Glasgow cost of living.

---

## 7. Questions to ask at the end (signal seniority)
See `00_strategy/04_positioning_resume_and_stories.md` §8 — pick two per round, never ask about salary in technical rounds.
