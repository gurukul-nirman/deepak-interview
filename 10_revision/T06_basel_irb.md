# T06 · Basel IRB — quick refresher
**Study:** `02_credit_risk/03_basel_irb.md` · **Test:** `START TOPIC T06`

## 60-second summary
- Capital covers **unexpected** loss at 99.9%/1 year (ASRF/Vasicek); EL is covered by provisions → subtract PD in K.
- Calibration: rank model → **LRADR/central tendency** (cycle incl. downturns, ≥5 yrs) → grade calibration → **MoC** (EBA A/B/C) → floors.
- **Downturn LGD**; DoD 90 DPD + UTP (retail €100 + 1%); PIT vs TTC drives what calibration tests mean.

## Quick Q → short answer
| Q | A |
|---|---|
| Your IRB models were at a US bank — which rules? | US advanced approaches (12 CFR 217 subpart E), A-IRB only, Collins floor; EBA MoC/DoD are EU/UK concepts |
| US endgame re-proposal (Mar 2026)? | Would delete AIRB for Cat I–II → ERBA (standardised); final pending — use change ⇒ model-use review, re-tier, monitoring redesign **[Likely]** |
| K formula? | LGD·[N((N⁻¹(PD)+√R·N⁻¹(0.999))/√(1−R)) − PD]·MA; RWA = 12.5·K·EAD |
| Correlations? | Mortgage 0.15 · QRRE 0.04 · other retail 0.03–0.16 · corporate 0.12–0.24 |
| Why R falls with PD? | High-PD defaults are idiosyncratic; low-PD defaults are systemic |
| RW examples? | Other retail PD 2%/LGD 45% ≈ 58% · QRRE PD 2%/LGD 80% ≈ 51% · mortgage PD 1%/LGD 15% ≈ 19% |
| PD floor (Basel III final)? | 0.05% (0.10% QRRE revolvers) |
| LGD floors? | Corp unsecured 25% · mortgages 5% · QRRE 50% · other retail unsecured 30% |
| Data history? | PD ≥5 yrs; LGD/EAD retail ≥5, corporate ≥7 |
| MoC A/B/C? | Data/method deficiencies · relevant changes · general estimation error |
| ECB validation tests? | PD Jeffreys per grade; AUC vs initial validation; migration/HHI; LGD t-test & gAUC; CCF t-test |
| PIT vs TTC test? | Migration frequency vs cycle; DR stability per grade |
| LDP? | Pluto–Tasche, external benchmarks, expert judgment + conservatism |
| Use test? | IRB parameters used in approval, limits, pricing, capital allocation |
| Output floor? | IRB RWA ≥ 72.5% of standardised (phased) |

## From my mock interviews (auto-updated)
_No entries yet._
