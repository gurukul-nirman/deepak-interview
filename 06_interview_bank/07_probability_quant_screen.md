# 06.7 · Probability & Quant Screen (for Goldman, JPMorgan and similar online tests)

> Priority **P3** — only if you're interviewing at GS/JPM/MS-style quant-leaning MRM teams. Do these with pen and paper; the method matters more than speed. Answers at the end.

## Problems
1. A test for a fraud pattern detects 95% of frauds and flags 2% of genuine transactions. Fraud prevalence is 0.5%. If a transaction is flagged, what's the probability it's fraud?
2. Two independent loans default with probability 5% each. What's the probability at least one defaults? If their default correlation is positive, does this probability go up or down?
3. A portfolio has 1,000 loans, PD 2% each, independent. Mean and standard deviation of the number of defaults? Roughly how many defaults would make you suspicious at the 95% level?
4. You flip a fair coin until you get two heads in a row. Expected number of flips?
5. X ~ N(0,1). What's P(X > 1.96)? P(|X| > 1.96)?
6. A model's predicted PDs average 4%, the observed default rate is 5% on 2,500 accounts. Is the difference significant at 5% (two-sided)?
7. Expected value: a loan of 100 with PD 3%, LGD 40%, earns 6% interest if no default (paid at year-end, no interest on default). Expected profit?
8. Why is Gini = 2·AUC − 1? Show it from the ROC/CAP areas in two lines.
9. You have 3 independent models each 70% accurate on a binary decision. Majority-vote accuracy?
10. If log-odds = −3 + 0.5·x, what PD at x = 2? By how much do the odds change when x increases by 1?

## Answers (cover before attempting)
1. P(F|flag) = 0.95·0.005 / (0.95·0.005 + 0.02·0.995) = 0.00475 / 0.02465 ≈ **19.3%**.
2. 1 − 0.95² = **9.75%**. Positive correlation → defaults cluster → P(at least one) **goes down** (joint default more likely, the union shrinks for fixed marginals).
3. Mean 20, SD √(1000·0.02·0.98) ≈ **4.43**; one-sided 95% (normal approx.) ≈ 20 + 1.645·4.43 ≈ **27.3** → ~28; the exact binomial test first rejects at **29** defaults.
4. **6** flips (solve E = ½(1 + E) + ¼(2 + E) + ¼·2 → E = 6).
5. **2.5%** and **5%**.
6. SE = √(0.04·0.96/2500) = 0.00392; z = 0.01/0.00392 ≈ **2.55** → significant (p ≈ 0.011).
7. E = 0.97·6 − 0.03·40 = 5.82 − 1.2 = **4.62**.
8. AUC = area under ROC; AR (Gini) = (area between model CAP and diagonal) / (area between perfect CAP and diagonal) — algebra gives AR = 2·AUC − 1; intuitively Gini rescales AUC so random = 0, perfect = 1.
9. P(at least 2 of 3 right) = 3·0.7²·0.3 + 0.7³ = 0.441 + 0.343 = **78.4%** (only if errors are independent).
10. PD = 1/(1 + e^{2}) = **11.9%**; odds multiply by e^{0.5} ≈ **1.65** per unit of x.
