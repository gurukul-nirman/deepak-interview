"""
common.py — data loading for Project P1 (UCI "Default of Credit Card Clients", Taiwan 2005).

Real data (use this for your portfolio):
  Option A:  pip install ucimlrepo   → load_data(source="ucimlrepo")
  Option B:  download the .xls from https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
             → load_data(source="path/to/default of credit card clients.xls")   (needs: pip install xlrd)
  Option C:  any CSV with the same columns → load_data(source="file.csv")
Fallback:   load_data(source="synthetic") — schema-identical SYNTHETIC data, only for testing the code.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

for _stream in (sys.stdout, sys.stderr):  # Windows consoles/pipes default to cp1252 and crash on → ≈ −
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

COLUMNS =(["LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
            "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
           + [f"BILL_AMT{i}" for i in range(1, 7)] + [f"PAY_AMT{i}" for i in range(1, 7)])
TARGET = "default"
X_NAMES = {f"X{i + 1}": c for i, c in enumerate(COLUMNS)}  # UCI variable names X1..X23


def add_toolkit_to_path() -> None:
    """Make validation_toolkit importable from the repo (05_coding/code) or from this folder (e.g., Colab)."""
    here = Path(__file__).resolve().parent
    for p in [here, *(q / "05_coding" / "code" for q in here.parents)]:
        if (p / "validation_toolkit.py").exists():
            sys.path.insert(0, str(p))
            return
    raise ImportError("validation_toolkit.py not found — copy 05_coding/code/validation_toolkit.py next to this file.")


def _standardise(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=X_NAMES)
    df = df.rename(columns={"default payment next month": TARGET, "Y": TARGET, "PAY_1": "PAY_0"})
    df = df.drop(columns=[c for c in ["ID"] if c in df.columns])
    missing = [c for c in COLUMNS + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"Unexpected schema — missing columns: {missing}")
    return df[COLUMNS + [TARGET]].apply(pd.to_numeric)


def synthetic(n: int = 30_000, seed: int = 2005) -> pd.DataFrame:
    """Schema-identical synthetic data (NOT the real dataset) so the scripts can be tested anywhere."""
    rng = np.random.default_rng(seed)
    h = rng.normal(size=n)                                   # latent creditworthiness
    limit = np.round(np.exp(11.6 + 0.7 * h + rng.normal(0, 0.5, n)), -4).clip(10_000, 1_000_000)
    sex = rng.choice([1, 2], n, p=[0.4, 0.6])
    edu = rng.choice([0, 1, 2, 3, 4, 5, 6], n, p=[0.001, 0.35, 0.47, 0.16, 0.004, 0.01, 0.005])
    mar = rng.choice([0, 1, 2, 3], n, p=[0.002, 0.455, 0.532, 0.011])
    age = np.clip(np.round(35 + 9 * rng.standard_normal(n) + 2 * h), 21, 79)
    pay = np.zeros((n, 6), int)
    base = np.clip(np.round(-0.3 - 0.9 * h + rng.normal(0, 1.1, n)), -2, 8)
    for j in range(6):  # recent month first (PAY_0 = Sept … PAY_6 = April)
        pay[:, j] = np.clip(base + np.round(rng.normal(0, 0.6, n)), -2, 8)
    later = pay[:, 1:]  # view: mimic the real file, where code 1 is common in PAY_0 but rare in PAY_2–PAY_6
    ones = later == 1
    later[ones] = np.where(rng.random(ones.sum()) < 0.5, 0, 2)
    bill = np.zeros((n, 6))
    b0 = limit * rng.beta(2, 3, n) * (1 + 0.2 * (pay[:, 0] > 0))
    for j in range(6):
        bill[:, j] = np.round(b0 * rng.uniform(0.85, 1.1, n))
    credit_bal = rng.random(n) < 0.02  # a few negative bills (credit balances), as in the real file
    bill[credit_bal] = -np.round(rng.uniform(0, 5_000, (credit_bal.sum(), 6)))
    payamt = np.round(np.clip(bill * rng.uniform(0.02, 0.4, (n, 6)) * (pay <= 0), 0, None))
    z = (-1.55 + 0.75 * np.clip(pay[:, 0], -2, 4) + 0.25 * np.clip(pay[:, 1], -2, 4)
         - 0.35 * (np.log(limit) - 11.6) - 0.15 * h + 0.05 * (sex == 1) + 0.002 * (age - 35))
    y = rng.binomial(1, 1 / (1 + np.exp(-z)))
    df = pd.DataFrame(np.column_stack([limit, sex, edu, mar, age, pay, bill, payamt, y]),
                      columns=COLUMNS + [TARGET])
    return df.apply(pd.to_numeric)


def load_data(source: str = "synthetic") -> tuple[pd.DataFrame, str]:
    """Return (data, label). label tells you whether results are REAL or SYNTHETIC."""
    if source == "synthetic":
        return synthetic(), "SYNTHETIC (testing only — not for your portfolio)"
    if source == "ucimlrepo":
        from ucimlrepo import fetch_ucirepo  # pip install ucimlrepo
        d = fetch_ucirepo(id=350)
        df = pd.concat([d.data.features, d.data.targets], axis=1)
        return _standardise(df), "REAL — UCI dataset 350"
    path = Path(source)
    if path.suffix.lower() in {".xls", ".xlsx"}:
        return _standardise(pd.read_excel(path, header=1)), f"REAL — {path.name}"
    return _standardise(pd.read_csv(path)), f"REAL — {path.name}"
