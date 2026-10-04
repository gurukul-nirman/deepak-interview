# 06.6 · One-Page Cheat Sheet (read the night before every interview)

## Formulas
```
EL = PD × LGD × EAD            EAD(revolving) = Drawn + CCF × (Limit − Drawn)
logit: ln(p/(1−p)) = β0 + Σβx   odds ratio = e^β
WoE = ln(%G/%B)   IV = Σ(%G−%B)·WoE   (single-var WoE LR coefficient = −1 exactly)
Score = Offset + Factor·ln(odds_good); Factor = PDO/ln2; Offset = Base − Factor·ln(BaseOdds)
      → 600 @ 50:1, PDO 20: Factor 28.85, Offset 487.12; PD 2%≈599, 5%≈572, 10%≈551
KS = max|F_bad − F_good|    Gini = 2·AUC − 1 = AR = Somers' D
PSI = Σ(A−E)·ln(A/E)  (<0.10 | 0.10–0.25 | >0.25)     CSI = PSI per characteristic
Binomial p = P(X ≥ D | N, PD)     Jeffreys p = BetaCDF(PD; D+½, N−D+½)   (small p → PD too low)
HL = Σ(O−E)²/(n·p̄(1−p̄)) ~ χ²(g−2)          VIF = 1/(1−R²)
PIT PD = N((N⁻¹(PD_TTC) − √ρ·Z)/√(1−ρ))     (Z<0 = bad economy)
ECL = Σ_s w_s Σ_t PD_marg·LGD·EAD·DF(EIR)
IRB K = LGD·[N((N⁻¹(PD)+√R·N⁻¹(0.999))/√(1−R)) − PD]·MA; RWA = 12.5·K·EAD
R: mortgage 0.15 · QRRE 0.04 · other retail 0.03–0.16 · corporate 0.12–0.24
AR(1) long-run effect = β/(1−ρ)        Oversampling: β0 + ln(π1/π0) − ln(ρ1/ρ0)
```

## Worked numbers you can quote
KS example 40, AUC 0.76 / Gini 0.52 · PSI example 0.135 · Binomial (N 1,000, PD 2%, D 30): p 0.021, Jeffreys 0.016 · Demo: Gini 0.589 → 0.504 (CI 0.478–0.534), PSI 0.346, Jeffreys RED G2–G4 · Other-retail PD 2%/LGD 45% → RW ≈ 58%.

## Regulatory dates (Oct 2026)
- **SR 26-2** (Fed/OCC 2026-13/FDIC FIL-15-2026): **17 Apr 2026**, replaces SR 11-7; > $30bn; "complex" model definition; GenAI/agentic out of scope; risk-based cadence.
- **PRA SS1/23:** effective **17 May 2024**; 5 principles; SMF; PMAs.
- **ECB Guide to internal models:** revised **28 Jul 2025** (ML expectations).
- **OSFI E-23:** final 11 Sep 2025; effective **1 May 2027**; includes AI/ML.
- **RBI ECL:** final **27 Apr 2026**; effective **1 Apr 2027**; Stage 2 = 30–90 DPD, 5% floor **[Likely — verify floors]**.
- **RBI draft MRM guidance:** **24 Jun 2026**; all REs; AI/ML & third-party models.
- **EU AI Act:** credit scoring high-risk obligations → **2 Dec 2027**.
- **Fed stress test (30 Sep 2026):** public comment on scenarios/models; two market shocks; **SCB averaging from 2028**.
- **SBA:** SBSS screening for 7(a) small loans **discontinued 1 Mar 2026**.
- IFRS 9 since 2018 · CECL 2020 (SEC filers) / 2023 (others) · EU DoD retail €100 + 1% · US charge-off: cards 180 DPD, instalment 120 DPD.

## Frameworks
- **DIFW** (technical): Definition → Intuition → Formula → Where it breaks.
- **SCOPE-D** (cases): Situate → Check data → Outcomes → Probe concept → Examine alternatives → Decide.
- **Diagnosis:** PSI↑ + Gini stable = population shift · Gini↓ = relationship/data/truncation · calibration level off = cycle/definition · slope flattening = weakening discrimination.
- **Findings:** Condition · Criteria · Cause · Effect · Recommendation · Severity · Owner/Date.
- **Outcomes:** Approve · Approve with conditions · Reject.
- **STAR-L:** …and always the Learning.

## Five talking points that signal VP-level
1. "I separate population drift, relationship drift and calibration drift before recommending action."
2. "Severity is about evidence; remediation path is where I'm flexible."
3. "SR 26-2 moves us to materiality-based cadence — I'd re-tier, not cut rigour on material models."
4. "For vendor models like SBSS, I validate locally — and the March 2026 SBA change is a model-use review trigger."
5. "For ML, uplift must be significant out-of-time and worth the governance cost — then constrained, calibrated, explained, fairness-tested."
