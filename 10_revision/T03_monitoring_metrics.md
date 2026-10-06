# T03 · Monitoring metrics — quick refresher
**Study:** `03_monitoring_validation/01_performance_monitoring_metrics.md` · **Test:** `START TOPIC T03`

## 60-second summary
- Four questions: **stability** (same population?), **discrimination** (ranks?), **calibration** (levels right?), **usage** (used as designed?).
- Never conclude from one family; **rule out data issues first**; check **significance** (bootstrap/DeLong) before acting.
- Action ladder: monitor → overlay → recalibrate → redevelop → restrict use — with owner, date and governance.

## Quick Q → short answer
| Q | A |
|---|---|
| KS? | Max |cum% bads − cum% goods|; best single cut-off's separation |
| Gini vs AUC? | Gini = 2·AUC − 1 = AR = Somers' D |
| AUC meaning? | P(random bad scored riskier than random good) |
| PSI formula & bands? | Σ(A−E)·ln(A/E) on reference bins; <0.1 / 0.1–0.25 / >0.25 |
| PSI 0.27, Gini stable? | Population shift, ranking intact → check calibration, business change; maybe re-baseline |
| Gini drop, PSI low? | Relationship change, data issue or truncation → drill to characteristics |
| CSI? | PSI per characteristic → which input moved |
| Characteristic analysis? | Σ(A%−E%)·points → points moved per characteristic |
| Calibration tests? | A/E by grade, binomial/Jeffreys, HL, Brier, traffic lights |
| Overall A/E fine but low grades fail? | Slope flattening → discrimination weakening |
| Why Gini falls after tighter cut-off? | Truncation — booked population more homogeneous |
| TTC model fails in a downturn? | Expected; compare to long-run average, check migrations |
| Long performance window? | Early-read metrics (3/6/9 MOB), stability, matured-cohort back-tests |
| Empty PSI bin? | ln(0) undefined → floor at ε or merge; report it |
| PSI symmetric? | Yes |
| Example KS/AUC table (G 50/100/200/300/350; B 30/25/20/15/10)? | KS 40; AUC 0.76; Gini 0.52 |
| PSI example E 20% each, A 30/25/20/15/10? | 0.135 (Amber) |
| Binomial example N 1,000, PD 2%, D 30? | p ≈ 0.021 (exact), Jeffreys ≈ 0.016 → Amber at 5% |

## Traps
- Treating PSI as a performance metric ✗ · Bins from the current sample ✗ · Acting on a Gini move without a CI ✗

## From my mock interviews (auto-updated)
_No entries yet._
