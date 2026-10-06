# 05.3 · SAS Essentials for Monitoring & Validation

You use SAS daily, so this file is about **(1) the interview traps** and **(2) clean, reusable validation code** you can talk through. Snippets are standard Base SAS / SAS/STAT syntax (SAS 9.4). Not executed here (no SAS licence in this environment) — run them once on your machine before an interview. Use `ods trace on;` to confirm ODS table names in your version.

---

## 1. DATA step — the 12 things interviewers probe

| # | Concept | What to say |
|---|---|---|
| 1 | **WHERE vs IF** | WHERE filters *before* the observation enters the PDV (faster, works in PROCs, uses indexes) but can't reference variables created in the same step or `FIRST./LAST.`; subsetting IF works on PDV values. |
| 2 | **Missing numeric is the smallest value** | `if score < 150 then band='LOW';` puts **missing** scores in LOW. Always handle `missing(x)` first. (Classic bucket-assignment bug.) |
| 3 | **MERGE + BY** | Requires sorted inputs; `in=` flags control join type. Without BY it's a positional merge (dangerous). Many-to-many MERGE doesn't produce a Cartesian product — use PROC SQL. |
| 4 | **RETAIN / sum statement** | `cum + bads;` is auto-retained and initialised to 0. |
| 5 | **FIRST./LAST.** | Need BY + sorted data. Used for per-account first/last record, counters. |
| 6 | **LAG pitfall** | `LAG()` is a queue; calling it inside an IF gives the value from the last time the IF was true. Compute unconditionally, then reset on `first.id`. |
| 7 | **_N_ / _ERROR_** | Iteration counter / error flag. |
| 8 | **INPUT vs PUT** | char→num: `input(c, best12.)`; num→char: `put(n, 8.)`. |
| 9 | **Dates** | SAS date = days since 01-Jan-1960. `intnx('month', d, 12, 'e')` (end of month 12 ahead), `intck('month', d1, d2)` (months between). |
| 10 | **Arrays + DO loops** | Apply the same transform to many variables (`array v{*} x1-x20;`). |
| 11 | **KEEP/DROP/RENAME early** | Efficiency on big monitoring datasets. |
| 12 | **Hash objects** | In-memory lookups without sorting — mention as an efficiency tool. |

**Macro facts:** `%LET` resolves at compile time; `CALL SYMPUTX` creates the macro variable at execution time (available only after the step ends). Debug with `options mprint mlogic symbolgen;`. `PROC SQL ... INTO :mv TRIMMED` avoids leading blanks.

---

## 2. PROCs you should be able to write from memory

```sas
/* frequency + chi-square */
proc freq data=dev;  tables segment*bad / chisq nocol nopercent; run;

/* summary by class */
proc means data=dev n mean min p50 max nmiss;  class segment;  var utilization score; run;

/* deciles: groups=10, DESCENDING → rank 0 = highest value (riskiest if var is PD) */
proc rank data=scored groups=10 descending out=r;  var pd;  ranks decile; run;

/* fixed buckets with a format (missing handled explicitly) */
proc format;
  value dpdb .='MISSING' 0='0 Current' 1-29='1 1-29' 30-59='2 30-59' 60-89='3 60-89' 90-high='4 90+';
run;

/* logistic regression: event, stepwise, HL test, ROC, save model for scoring */
proc logistic data=train outmodel=pd_model;
  model bad(event='1') = woe_score woe_util woe_tib woe_delq
        / selection=stepwise slentry=0.05 slstay=0.05 lackfit outroc=roc_dev;
  ods output Association=assoc LackFitChiSq=hl ParameterEstimates=pe;
run;
/* Association table: c = AUC; Somers' D = Gini (= 2c − 1) */

/* score new data with the saved model */
proc logistic inmodel=pd_model;  score data=recent out=recent_scored; run;   /* P_1 = predicted PD */

/* KS: two-sample EDF test */
proc npar1way data=recent_scored edf;  class bad;  var P_1;
  ods output KolSmir2Stats=ks;    /* D = KS statistic */
run;

/* VIF / tolerance */
proc reg data=train;  model bad = woe_score woe_util woe_tib woe_delq / vif tol collin; run; quit;

/* correlations (Spearman for rank relationships) */
proc corr data=train spearman;  var score utilization tib; run;
```

**Stress-testing / time-series PROCs:**
```sas
/* OLS + autocorrelation + normality + heteroskedasticity + stationarity diagnostics */
proc autoreg data=macro_q;
  model nco = nco_lag1 d_unemp gdp_yoy / godfrey=4 lagdep=nco_lag1 normal archtest
                                          stationarity=(adf=3);
run;
/* lagdep= gives Durbin's h — plain DW is biased when a lagged dependent variable is a regressor.
   Run KPSS separately with stationarity=(kpss) and read ADF + KPSS together. */

/* ADF on a series */
proc arima data=macro_q;  identify var=nco stationarity=(adf=(0,1,2,3)); run; quit;
```

---

## 3. Validation macros (reusable, explainable)

### 3.1 Gains table + KS
```sas
%macro gains_ks(data=, pd=P_1, target=bad, groups=10);
  proc rank data=&data(keep=&pd &target) groups=&groups descending out=_r;
    var &pd; ranks decile;               /* decile 0 = riskiest */
  run;
  proc sql;
    create table _dec as
    select decile, count(*) as n, sum(&target) as bads,
           calculated n - calculated bads as goods,
           min(&pd) as min_pd, max(&pd) as max_pd
    from _r group by decile order by decile;
    select sum(bads), sum(goods) into :tb trimmed, :tg trimmed from _dec;
  quit;
  data _dec;
    set _dec;
    cum_b + bads;  cum_g + goods;        /* sum statements: auto-retained */
    bad_rate     = bads / n;
    cum_bad_pct  = cum_b / &tb;
    cum_good_pct = cum_g / &tg;
    ks           = abs(cum_bad_pct - cum_good_pct);
  run;
  proc sql; select max(ks) format=8.4 as KS from _dec; quit;
  proc print data=_dec noobs; run;
%mend gains_ks;
```

### 3.2 PSI (bins from the reference sample; missing in its own bin)
```sas
%macro psi(dev=, cur=, var=, groups=10);
  /* 1) bin edges from DEV only */
  proc rank data=&dev(keep=&var where=(not missing(&var))) groups=&groups out=_r;
    var &var; ranks _bin;
  run;
  proc sql noprint;
    select max(&var) into :cut1- from _r group by _bin order by _bin;
    %let nb = &sqlobs;
  quit;

  /* 2) apply the same edges to both samples */
  data _both;
    set &dev(in=d keep=&var) &cur(keep=&var);
    length sample $3;
    sample = ifc(d, 'DEV', 'CUR');
    if missing(&var) then _bin = 0;          /* missing → own bin (avoid the 'missing < any number' trap) */
    else do;
      _bin = &nb;                            /* top bin catches values above the last DEV cut */
      %do i = %eval(&nb - 1) %to 1 %by -1;
        if &var <= &&cut&i then _bin = &i;
      %end;
    end;
  run;

  /* 3) distribution by sample and PSI */
  proc freq data=_both noprint;  tables sample*_bin / outpct out=_f; run;
  proc sql;
    create table _psi as
    select coalesce(e._bin, a._bin) as bin,
           max(coalesce(e.pct_row, 0) / 100, 1e-6) as e_pct,
           max(coalesce(a.pct_row, 0) / 100, 1e-6) as a_pct,
           (calculated a_pct - calculated e_pct) * log(calculated a_pct / calculated e_pct) as psi_contrib
    from (select _bin, pct_row from _f where sample = 'DEV') as e
         full join
         (select _bin, pct_row from _f where sample = 'CUR') as a
      on e._bin = a._bin
    order by bin;
    select sum(psi_contrib) format=8.4 as PSI from _psi;
  quit;
%mend psi;
/* usage: %psi(dev=dev_scored, cur=recent_scored, var=score); */
```

### 3.3 WoE / IV for one variable
```sas
%macro woe_iv(data=, var=, target=bad, groups=5);
  proc rank data=&data(keep=&var &target) groups=&groups out=_r;
    var &var; ranks _bin;
  run;
  data _r; set _r; if missing(&var) then _bin = -1; run;      /* MISSING bin */
  proc sql noprint;
    create table _w as
    select _bin, count(*) as n, sum(&target) as bads, calculated n - calculated bads as goods,
           min(&var) as lo, max(&var) as hi
    from _r group by _bin;
    select sum(bads), sum(goods) into :tb trimmed, :tg trimmed from _w;
  quit;
  data _w;
    set _w;
    pct_good   = max(goods / &tg, 1e-6);
    pct_bad    = max(bads  / &tb, 1e-6);
    woe        = log(pct_good / pct_bad);      /* Siddiqi convention: higher WoE = safer */
    iv_contrib = (pct_good - pct_bad) * woe;
  run;
  proc sql; select "&var" as variable, sum(iv_contrib) format=8.4 as IV from _w; quit;
%mend woe_iv;
```

### 3.4 PD back-test by grade: binomial, Jeffreys, normal approximation
```sas
proc sql;
  create table _g as
  select grade, count(*) as N, sum(bad) as D, mean(pd) as PD
  from recent_scored group by grade;
quit;
data grade_backtest;
  set _g;
  DR         = D / N;
  binom_p    = 1 - cdf('BINOMIAL', D - 1, PD, N);         /* P(X >= D | N, PD) */
  jeffreys_p = cdf('BETA', PD, D + 0.5, N - D + 0.5);     /* ECB-style; small p → PD too low */
  z          = (DR - PD) / sqrt(PD * (1 - PD) / N);
  length result $5;
  if jeffreys_p < 0.01 then result = 'RED';
  else if jeffreys_p < 0.05 then result = 'AMBER';
  else result = 'GREEN';
run;
```

### 3.5 Roll-rate matrix (month t → t+1)
```sas
proc sort data=perf; by acct_id month; run;
data trans;
  set perf;
  by acct_id;
  bucket = put(dpd, dpdb.);
  prev_bucket = lag(bucket);                 /* LAG computed unconditionally … */
  if first.acct_id then prev_bucket = ' ';   /* … then reset at the account boundary */
  if not missing(prev_bucket);
run;
proc freq data=trans;  tables prev_bucket*bucket / nocol nopercent; run;   /* row % = roll rates */
```

---

## 4. SAS interview questions (answers in one line)

1. **WHERE vs IF?** See table row 1 — and WHERE can be used in PROCs and with indexes.
2. **How does SAS treat missing numerics in comparisons?** As smaller than any number → silent misbucketing.
3. **MERGE vs PROC SQL join?** MERGE needs sorted BY vars and handles one-to-one/one-to-many; PROC SQL handles many-to-many and non-equi joins, no pre-sort.
4. **What does `in=` do?** Creates a temporary 0/1 flag showing whether the record came from that dataset → control inner/left/anti joins.
5. **RETAIN vs sum statement?** Sum statement auto-retains and treats missing as 0.
6. **Why is LAG inside IF dangerous?** Queue only updates when executed.
7. **CALL SYMPUT vs SYMPUTX?** SYMPUTX trims blanks and lets you set scope.
8. **When is a macro variable created by CALL SYMPUTX available?** After the DATA step finishes.
9. **How to get the c-statistic / Gini from PROC LOGISTIC?** `ods output Association=...` → `c` and Somers' D (= Gini).
10. **How to compute KS in SAS?** PROC NPAR1WAY EDF (two-sample) or a gains table with cumulative %.
11. **How to run Hosmer–Lemeshow?** `/ lackfit` on the MODEL statement.
12. **How to score a holdout?** `outmodel=` then `proc logistic inmodel=...; score data=... out=...;`.
13. **PROC MEANS vs PROC SUMMARY?** Same engine; MEANS prints by default, SUMMARY doesn't.
14. **How do you speed up a slow monitoring job?** Subset early (WHERE/KEEP), indexes or hash lookups, avoid repeated sorts, compress, push work to the database (SQL pass-through).
15. **How do you debug a macro?** `options mprint mlogic symbolgen;` and `%put _user_;`.
16. **How do you validate someone's SAS code (implementation testing)?** Independent re-code of key steps, row-count reconciliations at each step, compare outputs to tolerance, test edge cases (missing, boundaries), review logs for NOTE: uninitialized / merge warnings / numeric-to-character conversions.
