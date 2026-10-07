# T05 · IFRS 9 / ECL & CECL — quick refresher
**Study:** `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` · **Test:** `START TOPIC T05`

## 60-second summary
- Stage 1: 12m ECL · Stage 2 (SICR since origination): lifetime ECL · Stage 3 (credit-impaired): lifetime, interest on net.
- SICR is **relative to origination**; quantitative + qualitative + **30 DPD backstop**; default rebuttable at **90 DPD**.
- ECL = Σ PD_marg × LGD × EAD × DF(EIR), **probability-weighted over scenarios** (losses convex → Jensen).
- IFRS 9 PD = PIT, forward-looking, unbiased (no MoC/downturn); TTC→PIT via **Vasicek Z-factor**.
- **RBI ECL:** final 27 Apr 2026, effective 1 Apr 2027; Stage 2 = 30–90 DPD with 5% floor; Stage 1 floor 0.40% (std corporate/retail); CET1 add-back taper 4/5→1/5 over FY28–FY31; legacy loans to EIR by Mar 2030 **[Likely on floors/taper]**.

## Quick Q → short answer
| Q | A |
|---|---|
| Why multiple scenarios? | Losses are convex in the economy → avg of scenario ECLs > ECL at avg scenario |
| TTC→PIT? | PD_PIT = N((N⁻¹(PD_TTC) − √ρ·Z)/√(1−ρ)); Z<0 bad economy |
| Example: PD_TTC 2%, ρ 0.10, Z = −1? | ≈ 3.35% (Z=−2: 6.70%; Z=+1: 0.62%; Z=0: 1.52%) |
| Lifetime PD methods? | Markov transition matrices, survival/hazard, vintage curves + macro |
| Validate SICR? | Hit rate (defaults previously in S2), time in S2, false positives, backstop share, stability |
| 85% of S2 via backstop? | Finding — quantitative SICR not detecting early deterioration |
| Overlay challenge? | Which limitation, quantification, approval, sunset, double counting, monitoring |
| Cards lifetime? | Behavioural life (period of exposure), not contractual |
| IFRS 9 vs CECL? | CECL: lifetime from day 1, no stages, R&S forecast then reversion, Q-factors, unfunded only if not unconditionally cancellable |
| ECL movement drivers? | Volume/mix, stage transfers, parameters, macro, overlays, write-offs |
| Toy ECL (cum PD 2/4.5/7%, EAD 100/70/40, LGD 40%, EIR 10%)? | 12m 0.73; lifetime 1.61 |
| Scenario example (base/up/down ECL 1.00/0.80/2.00, weights 50/30/20)? | Weighted 1.14 → 14% above base; upside must be below base |
| RBI floors bind — so is model validation pointless? | No: report floor-binding vs model-driven exposure; SICR and Stage 2/3 lifetime ECL stay model-driven |
| CECL effective? | 2020 SEC filers (ex-SRCs); 2023 others |

## From my mock interviews (auto-updated)
_No entries yet._
