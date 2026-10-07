"""
grade.py — auto-grader for coding mock interviews.

Usage (run from this folder or anywhere):
  python grade.py list [python|sql]          list problems
  python grade.py show <ID>                   print the statement (safe to show the candidate)
  python grade.py run <ID> <submission>       run VISIBLE tests on a .py or .sql submission
  python grade.py run <ID> <submission> --all run visible + HIDDEN tests (after the interview)
  python grade.py solution <ID>               print the reference solution (after the interview)
"""
from __future__ import annotations

import copy
import inspect
import signal
import sqlite3
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "05_coding" / "code"))

for _stream in (sys.stdout, sys.stderr):  # Windows consoles/pipes default to cp1252 and crash on → ≈ −
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

import problems as pb  # noqa: E402
import solutions as ref  # noqa: E402

TIME_LIMIT = 30  # seconds per test
HAS_ALARM = hasattr(signal, "SIGALRM")  # POSIX only; on Windows the limit is checked after the call returns


class Timeout(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise Timeout()


def load_function(path: Path, name: str):
    ns: dict = {"__name__": "submission"}
    code = path.read_text(encoding="utf-8")
    exec(compile(code, str(path), "exec"), ns)  # noqa: S102 — trusted local practice code
    if name not in ns:
        raise NameError(f"function `{name}` not found in {path.name}")
    return ns[name]


def run_python(p: pb.Problem, sub: Path, include_hidden: bool) -> bool:
    fn = load_function(sub, p.func_name)
    tests = [("visible", t) for t in p.visible()]
    if include_hidden:
        tests += [("hidden", t) for t in p.hidden()]
    all_ok = True
    for kind, t in tests:
        exp = p.reference(*copy.deepcopy(t.args), **copy.deepcopy(t.kwargs))
        if HAS_ALARM:
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(TIME_LIMIT)
        start = time.perf_counter()
        try:
            out = fn(*copy.deepcopy(t.args), **copy.deepcopy(t.kwargs))
            ok, msg = p.compare(out, exp)
        except Timeout:
            ok, msg = False, f"timed out (> {TIME_LIMIT}s)"
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f"error: {type(e).__name__}: {e} | {traceback.format_exc().strip().splitlines()[-2].strip()}"
        finally:
            if HAS_ALARM:
                signal.alarm(0)
        dur = time.perf_counter() - start
        if not HAS_ALARM and dur > TIME_LIMIT:
            ok, msg = False, f"too slow ({dur:.0f}s > {TIME_LIMIT}s limit)"
        all_ok &= ok
        print(f"  [{kind:7}] {'PASS' if ok else 'FAIL'}  {t.name:<40} {dur:6.2f}s  {msg}")
    return all_ok


def _db(seed: int) -> sqlite3.Connection:
    import sql_practice
    path = HERE / f"_practice_seed{seed}.sqlite"
    if not path.exists():
        sql_practice.build(seed=seed, path=path).close()
    con = sqlite3.connect(path)
    con.create_function("LN", 1, lambda v: float(np.log(v)) if v is not None and v > 0 else None)
    return con


def _same_result(out: pd.DataFrame, exp: pd.DataFrame, order: bool) -> tuple[bool, str]:
    if out.shape[1] != exp.shape[1]:
        return False, f"expected {exp.shape[1]} columns, got {out.shape[1]}"
    if len(out) != len(exp):
        return False, f"expected {len(exp)} rows, got {len(out)}"
    o, e = out.copy(), exp.copy()
    o.columns = e.columns = range(e.shape[1])
    if not order:
        o = o.sort_values(list(o.columns)).reset_index(drop=True)
        e = e.sort_values(list(e.columns)).reset_index(drop=True)
    for c in e.columns:
        ec, oc = e[c], o[c]
        if pd.api.types.is_numeric_dtype(ec) and pd.api.types.is_numeric_dtype(oc):
            if not np.allclose(oc.astype(float), ec.astype(float), rtol=1e-6, atol=1e-6, equal_nan=True):
                return False, f"values differ in column {c + 1}"
        elif not (oc.astype(str).to_numpy() == ec.astype(str).to_numpy()).all():
            return False, f"values differ in column {c + 1}"
    return True, ""


def _edge_db(pid: str) -> sqlite3.Connection:
    path = HERE / f"_practice_seed7_{pid}.sqlite"
    if not path.exists():
        src = _db(7)
        dst = sqlite3.connect(path)
        src.backup(dst)
        src.close()
        dst.executescript(pb.SQL_HIDDEN_MODS[pid])
        dst.commit()
        dst.close()
    con = sqlite3.connect(path)
    con.create_function("LN", 1, lambda v: float(np.log(v)) if v is not None and v > 0 else None)
    return con


def run_sql(p: pb.Problem, sub: Path, include_hidden: bool) -> bool:
    sql = sub.read_text(encoding="utf-8")
    runs = [("visible", 2026)] + ([("hidden", 7)] if include_hidden else [])
    if include_hidden and p.pid in pb.SQL_HIDDEN_MODS:
        runs.append(("hidden", "edge"))
    all_ok = True
    for kind, seed in runs:
        con = _edge_db(p.pid) if seed == "edge" else _db(seed)
        try:
            exp = pd.read_sql_query(ref.SQL[p.pid], con)
            start = time.perf_counter()
            out = pd.read_sql_query(sql, con)
            ok, msg = _same_result(out, exp, p.order_matters)
        except Exception as e:  # noqa: BLE001
            ok, msg = False, f"error: {type(e).__name__}: {e}"
            start = time.perf_counter()
        finally:
            con.close()
        all_ok &= ok
        label = {2026: "practice DB (seed 2026)", 7: "re-seeded DB (seed 7)", "edge": "edge-case DB"}[seed]
        print(f"  [{kind:7}] {'PASS' if ok else 'FAIL'}  {label:<40} {time.perf_counter() - start:6.2f}s  {msg}")
        if kind == "visible":
            print("            your first rows:")
            try:
                con = _db(seed)
                print("            " + pd.read_sql_query(sql, con).head(5).to_string(index=False).replace("\n", "\n            "))
                con.close()
            except Exception:  # noqa: BLE001
                pass
    return all_ok


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "list":
        lang = argv[1] if len(argv) > 1 else None
        for p in pb.PROBLEMS.values():
            if lang in (None, p.language):
                print(f"{p.pid:4} {p.language:6} {p.difficulty:6} {p.area}  {p.title}")
        return 0
    p = pb.PROBLEMS.get(argv[1].upper()) if len(argv) > 1 else None
    if p is None:
        print("Unknown problem ID. Use `python grade.py list`.")
        return 2
    if cmd == "show":
        sig = f"\nFunction to implement: `{p.func_name}`\n" if p.language == "python" else ""
        print(f"[{p.pid}] {p.title}  ({p.language}, {p.difficulty}, {p.area})\n\n{p.statement}\n{sig}")
        if p.language == "python":
            print("Visible test cases:", ", ".join(t.name for t in p.visible()))
        return 0
    if cmd == "solution":
        print(ref.SQL[p.pid] if p.language == "sql" else inspect.getsource(p.reference))
        return 0
    if cmd == "run":
        if len(argv) < 3:
            print("Usage: python grade.py run <ID> <submission> [--all]")
            return 2
        sub = Path(argv[2])
        hidden = "--all" in argv
        print(f"Grading {p.pid} — {p.title} ({'visible + hidden' if hidden else 'visible only'})")
        ok = run_python(p, sub, hidden) if p.language == "python" else run_sql(p, sub, hidden)
        print("RESULT:", "ALL PASSED" if ok else "SOME TESTS FAILED")
        return 0 if ok else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
