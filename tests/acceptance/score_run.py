#!/usr/bin/env python3
"""Cross-check an acceptance run's reports against expected-leaky-ml.json.

Usage: python score_run.py a1 <run-dir-with-.agent/audits> [--json]
For each planted defect, "found" = its cited code file appears in the report
set AND a distinguishing token from the planted location (symbol or pattern)
appears in the same finding block. Citation integrity: every `path::sym` /
`path:line` reference whose path is not in the fixture is reported (unless it
points into .agent/ artifacts). Mechanical only — semantic verdict stays with
the evaluator.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"([A-Za-z0-9_./-]+(?:\.[A-Za-z]{2,4}))(?:::[A-Za-z0-9_.]+)?(?::\d+)?")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score an acceptance audit run against planted defects.")
    ap.add_argument("scenario", choices=["a1", "a2"])
    ap.add_argument("run_dir", help="project dir containing .agent/audits (or the audit run dir itself)")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--expected", default=str(Path(__file__).parent / "expected-leaky-ml.json"))
    args = ap.parse_args(argv)

    expected = json.loads(Path(args.expected).read_text())
    run = Path(args.run_dir)
    audit_dir = run if (run / "index.md").exists() else next(iter(sorted((run / ".agent" / "audits").glob("*"))), None)
    if audit_dir is None or not audit_dir.is_dir():
        print(f"ERROR: no audit dir found under {run}", file=sys.stderr)
        return 2
    reports = {p.name: p.read_text(errors="replace") for p in audit_dir.glob("*.md")}
    all_text = "\n".join(reports.values())
    per_mode = {"architecture": reports.get("architecture.md", ""), "ml": reports.get("ml.md", ""),
                "exploratory": reports.get("exploratory.md", ""), "all": all_text}
    results = []
    for d in expected["defects"]:
        f = Path(d["location"].split(" ")[0])
        file_ok = f.name in all_text or str(f) in all_text
        # distinguishing token: use the symbol or a keyword from location text
        m = re.search(r"::([A-Za-z_][A-Za-z0-9_]*)", d["location"])
        token = m.group(1) if m else d["location"].split("(")[-1].split(",")[0].strip().split(" ")[0]
        block_ok = token in all_text if token else False
        want = d["expected_audit"].split()[0]  # ml/architecture/... first token
        in_mode = ""
        for mode, txt in per_mode.items():
            if mode == "all":
                continue
            if (f.name in txt) and (block_ok and token in txt):
                in_mode = mode
                break
        accept_modes = d["expected_audit"].replace(" or ", ",").replace(" (cross-cutting; any audit citing both files is fine)", "").split("(")[0]
        results.append({
            "id": d["id"], "defect_file_seen": bool(file_ok), "token_seen": bool(block_ok),
            "found": bool(file_ok and block_ok), "first_mode_with_full_cite": in_mode or None,
            "expected": accept_modes.strip() or d["expected_audit"],
        })

    # citation integrity: paths cited that don't exist in the project fixture
    bad_cites = []
    for path_token in set(TOKEN.findall(all_text)):
        if not path_token.startswith(("src/", "tests/", "app/", ".agent/", "data/")):
            continue
        if not (run / path_token).exists():
            bad_cites.append(path_token)
    out = {"defects": results, "found": sum(r["found"] for r in results),
           "total": len(results), "reports_present": sorted(reports),
           "cited_missing_paths": sorted(set(bad_cites))}
    if args.as_json:
        print(json.dumps(out, indent=2))
    else:
        for r in results:
            print(f"{'FOUND ' if r['found'] else 'missed'} {r['id']} (expected: {r['expected']}, seen in: {r['first_mode_with_full_cite'] or '-'})")
        print(f"found {out['found']}/{out['total']}; reports: {out['reports_present']}")
        if out["cited_missing_paths"]:
            print("cited paths that don't exist in the fixture: " + ", ".join(out["cited_missing_paths"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
