#!/usr/bin/env python3
"""check_report.py — mechanical contract checks for a written audit report.

Verifies the deterministic parts of the audit's finish-line checklist so the
agent can spend attention on the judgment parts:

  * report files match the modes recorded in index.md (nothing missing, nothing extra)
  * every mode report has a "Coding agent handoff" section
  * finding IDs are AUD-(ARCH|ML|EXP)-NNN and unique
  * every finding carries status/priority/confidence/evidence fields
  * statuses come from the lifecycle vocabulary (draft|reviewed|accepted|deferred|rejected|implemented-verified)
  * every cited repo path (path::symbol / path:line) exists in the project
  * no leftover template markers (<...> placeholders or HTML comments)

Judgment rules (context-sensitivity gate, absence-claim scope, reasoning
quality) are NOT checkable here — read the reports yourself.

Usage:
  check_report.py --project <repo> --run <.agent/audits/run-id-dir> [--json]
Exit: 0 = clean, 1 = problems, 2 = usage/environment.
"""
import argparse
import json
import re
import sys
from pathlib import Path

MODE_FILES = {"architecture": "architecture.md", "ml": "ml.md", "exploratory": "exploratory.md"}
LIFECYCLE = {"draft", "reviewed", "accepted", "deferred", "rejected", "implemented-verified"}
ID_RE = re.compile(r"^### (AUD-(?:ARCH|ML|EXP)-\d{3})\b[^\n]*\n(.*?)(?=^### |^## |\Z)", re.DOTALL | re.MULTILINE)
CITE_RE = re.compile(r"([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)(?:::|\:\d+)")
PLACEHOLDER_RE = re.compile(r"<[a-z][a-z0-9_ ./-]*>")

NEED_FIELDS = ("status:", "priority:", "confidence:", "evidence:")


def check_run(project: Path, run_dir: Path):
    problems, stats = [], {"findings": 0}
    index = run_dir / "index.md"
    if not index.is_file():
        return [f"{run_dir}: index.md missing (every audit run has one)"], stats
    index_text = index.read_text(errors="replace")
    m = re.search(r"modes:\s*([a-z, \-]+)", index_text, re.I)
    if not m:
        problems.append("index.md: no 'modes:' line found — report set cannot be verified")
        modes = set(MODE_FILES)
    else:
        raw = m.group(1).lower()
        modes = set(MODE_FILES) if "all" in raw else {p.strip() for p in raw.split(",") if p.strip()}
        bad = modes - set(MODE_FILES)
        if bad:
            problems.append(f"index.md: unknown modes {sorted(bad)}")
    present = {p.name for p in run_dir.glob("*.md")} - {"index.md"}
    expected = {MODE_FILES[md] for md in modes if md in MODE_FILES}
    for missing in sorted(expected - present):
        problems.append(f"modes say {missing} should exist, but file is absent")
    for extra in sorted(present - expected):
        problems.append(f"unexpected report file '{extra}' (not a listed mode)")

    seen_ids = {}
    for fname in sorted(expected & present):
        text = (run_dir / fname).read_text(errors="replace")
        if "Coding agent handoff" not in text:
            problems.append(f"{fname}: missing 'Coding agent handoff' section")
        if "<!--" in text:
            problems.append(f"{fname}: leftover HTML template comments")
        ph = PLACEHOLDER_RE.findall(text)
        if ph:
            problems.append(f"{fname}: unfilled template placeholders: {sorted(set(ph))[:5]}")
        for fm in ID_RE.finditer(text):
            fid, body = fm.group(1), fm.group(2)
            stats["findings"] += 1
            if fid in seen_ids:
                problems.append(f"{fname}: duplicate finding id {fid} (also in {seen_ids[fid]})")
            seen_ids[fid] = fname
            head = body.splitlines()[0] if body.splitlines() else ""
            for fld in NEED_FIELDS:
                if fld not in body:
                    problems.append(f"{fid}: missing '{fld}' field")
            sm = re.search(r"status:\s*([a-z-]+)", head + body[:400])
            if sm and sm.group(1) not in LIFECYCLE:
                problems.append(f"{fid}: status '{sm.group(1)}' not in lifecycle vocabulary")

    # cited paths must exist in the project (audit artifacts under .agent/ included)
    all_text = "\n".join((p.read_text(errors="replace") for p in run_dir.glob("*.md")))
    for cite in sorted(set(CITE_RE.findall(all_text))):
        c = cite.strip("./")
        if (project / c).exists() or (run_dir / Path(c).name).exists():
            continue
        problems.append(f"cited path does not exist: {c}")
    return problems, stats


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical contract checks for an audit report run.")
    ap.add_argument("--project", default=".", help="audited repo root")
    ap.add_argument("--run", required=True, help="the .agent/audits/<run-id> directory")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args(argv)
    project, run_dir = Path(args.project).resolve(), Path(args.run)
    if not run_dir.is_dir():
        print(f"ERROR: run dir not found: {run_dir}", file=sys.stderr)
        return 2
    problems, stats = check_run(project, run_dir)
    if args.as_json:
        print(json.dumps({"problems": problems, **stats}, indent=2))
    else:
        for p in problems:
            print(f"PROBLEM: {p}")
        print(f"findings checked: {stats['findings']}; problems: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
