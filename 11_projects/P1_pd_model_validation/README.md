# P1 · Independent validation of a credit-card PD model (portfolio project)

**What you do:** play the second-line validator. A simulated "developer" hands you a PD model (CC-PD-01) and its
documentation (MDD). The MDD contains planted errors. Your job:
1. Replicate the model.
2. Test it.
3. Find the issues.
4. Write a committee-style validation report.

**Why it matters for you:**
- It turns "I monitor models" into "I have independently validated a model end to end" — the single biggest gap between
  your profile and a ≥ ₹40L validation/MRM role.
- It gives you a deep, number-backed story for technical rounds.
- It answers degree screens with evidence.

**Time:** about 13 hours across weeks 2–4 of the plan (`00_strategy/03_six_week_plan.md`). If your Python is still
slow, the six TODOs are where the hours go — do the harness drills P01–P06 first.
**Data:** public UCI "Default of Credit Card Clients" (Taiwan, 2005; 30,000 accounts, 23 variables).

---

## Rules
- **Public data only.** Never use employer data, code, templates or model documents — not even "anonymised".
- **Label it honestly** as a personal project on public data: in the report, résumé, LinkedIn and interviews. Never present
  it as employer work.
- **Check your employment contract's IP / outside-work clause** before publishing. Personal projects on your own time
  with public data are usually fine, but your contract governs **[Assumption — check yours]**.
- **Spoiler discipline:** don't open `ANSWER_KEY.md` until your findings list and conclusion are written.

## Files
| File | What it is |
|---|---|
| `common.py` | Loads the real data (UCI download or `ucimlrepo`) or a schema-identical **synthetic** set for testing |
| `developer_model.py` | The model under review. Builds CC-PD-01 and writes the developer's evidence pack to `outputs/` |
| `validator_starter.py` | Your validation script. Runs end to end, writes `outputs/validation_evidence.md`; six `TODO(you)` exercises |
| `REPORT_TEMPLATE.md` | Validation report skeleton (CCCER findings, outcome, conditions) |
| `ANSWER_KEY.md` | ⚠️ Spoiler: planted findings, self-scoring rubric, interview kit, TODO solutions |
| `outputs/` | Generated; git-ignored. Re-create it any time by re-running the scripts |

## Setup

**Local** (one command per line; Windows PowerShell 5.1 doesn't accept `&&`):
```bash
pip install -r 05_coding/code/requirements.txt ucimlrepo xlrd
```
```bash
cd 11_projects/P1_pd_model_validation
```
```bash
python developer_model.py --data synthetic
```
```bash
python validator_starter.py --data synthetic
```
The last two together are the ~30-second pipeline check. The scripts write UTF-8 files and force UTF-8 console output, so
they also run on Windows (fixed 7 Oct 2026; earlier versions crashed on `≥`/`→` under the cp1252 code page).

**Google Colab (no local Python needed):**
1. Upload `common.py`, `developer_model.py`, `validator_starter.py` and `05_coding/code/validation_toolkit.py` into one
   folder.
2. Run `!pip install ucimlrepo`.
3. Run `!python developer_model.py --data ucimlrepo` and then `!python validator_starter.py --data ucimlrepo`.

**Getting the real data:**
- **Option A:** `--data ucimlrepo` (needs internet).
- **Option B:** download the `.xls` from the [UCI page](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
  and pass `--data "default of credit card clients.xls"`.

Synthetic data is only for testing the pipeline. **Every number in your report must come from the real data.** The
report header and evidence file show which data was used.

---

## Steps

| # | Step | Time | Output |
|---|---|---|---|
| 1 | Run the pipeline on synthetic data, then get the real data and run `developer_model.py --data ucimlrepo` | 0.5 h | `outputs/` evidence pack |
| 2 | Read `outputs/MDD_developer_summary.md` as a sceptic. For every claim, write "evidence?" next to it, and list the questions you'd ask the developer | 1.5 h | Challenge list (goes into report §9) |
| 3 | Run `validator_starter.py --data ucimlrepo`, read every table, then complete TODO #1–#6 (re-run after each) | 5–6 h | `outputs/validation_evidence.md` |
| 4 | Draft your findings list (title + severity + one-line evidence) and an overall outcome **before** writing prose | 1 h | Findings list |
| 5 | Write the report: copy `REPORT_TEMPLATE.md` → `report/VALIDATION_REPORT.md` | 4–5 h | The report |
| 6 | Self-score against `ANSWER_KEY.md` §1; log every miss in `09_progress/gap_log.md`; fix the report | 1 h | Score and fixes |
| 7 | Ask Claude: `REVIEW PROJECT P1` — a Head-of-MRM style review and score | 0.5 h | Review notes |
| 8 | Prepare the 60-second pitch and the drill-downs (ANSWER_KEY §6); add the résumé line | 1 h | Pitch |

**Stuck on a TODO for more than 30 minutes?** Read the hint in its docstring. Then ask Claude `EXPLAIN <concept>` (for
example, "EXPLAIN prior correction"). Look at the solution in `ANSWER_KEY.md` §7 only as a last resort, and note it in
your gap log.

## Using it in interviews
- **Where it fits:**
  - "Tell me about a validation you've done."
  - "How do you challenge a developer?"
  - "Walk me through calibration testing."
  - "Give an example of an implementation issue."
- **Lead with the conclusion and the four High findings,** then let the interviewer pick a thread. Every drill-down
  should end in a number from your report.
- **Pair it with your real experience:** "At work I monitor CECL/IFRS 9, IRB, CCAR and SBSS models. This project is
  where I practised the full independent-validation cycle." (Use the regimes you actually worked on — evidence bank C1–C2.)
- **Say what it is.** It's a training case: a deliberately flawed model on public data with a hidden answer key, not a
  real bank's model. "Structured validation exercise on a deliberately flawed model" is accurate and still impressive.
  The full wording is in `00_strategy/07_evidence_bank_and_resume.md` §6.
- **The dataset is famous.** The UCI Taiwan card data is a Kaggle classic, so interviewers have seen many models built on
  it. What's rare is a *validation* of one — lead with the findings and the governance judgment, never with the Gini.

## Publishing (after self-score ≥ 85)
Create a public GitHub repo (e.g., `credit-pd-model-validation`) and include:
- `common.py`
- `developer_model.py`
- your completed `validator_starter.py`
- `report/VALIDATION_REPORT.md` (or a PDF)
- a short README with the disclaimer **and an honest split of the work**: "Scaffold (data loader, simulated developer
  model, evidence pipeline, challenger functions) supplied as a training case; my work: TODO #1–#6, the analysis, the
  findings and the report."

**Rule before you publish:** you must be able to explain every line of every file in the public repo — the WoE and GBM
challengers, the DeLong call, the bootstrap. An interviewer who opens the repo and finds code you can't explain will
treat it as a fabricated claim, which ends a process. If a function is beyond you today, rewrite it in your own simpler
code or leave it out.

**Exclude `ANSWER_KEY.md`.** Link the repo from your résumé and LinkedIn "Featured" section.
