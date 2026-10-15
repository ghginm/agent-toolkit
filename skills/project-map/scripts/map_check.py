#!/usr/bin/env python3
"""map_check.py — mechanical freshness & reference checks for a project map.

Validates STRUCTURE and REFERENCES only: a clean run means paths resolve and
metadata is well-formed — it does NOT verify that card claims match code
behavior. Semantic validation is the agent's job (see the skill's validate
workflow).

Usage:
  map_check.py                       # check map in ./.agent/project-map against ./
  map_check.py --map-dir D --repo R  # explicit locations
  map_check.py --json                # machine-readable output
  map_check.py --affected --working  # cards affected by uncommitted/untracked changes
  map_check.py --affected --rev SHA  # cards affected by commits since SHA (+ working tree)
  map_check.py --affected --files p1 p2 ...  # no-git: judge these paths

Checks: metadata block present/well-formed; status in vocabulary; sources/
tests/config paths exist relative to --repo; markdown card links resolve;
depends-on references known modules; module/capability id matches filename;
L2/L3 cards contain at least one inline `path::symbol` or `path:line`
citation; verified_revision known to git and vs HEAD; dirty files intersecting
a card's sources are reported. Non-card .md files (bootstrap notes etc.)
outside index.md / modules/ / capabilities/ are ignored.

Exit codes: 0 = no problems, 1 = problems found, 2 = usage/environment error.
Stdlib only; git required only for revision/changed-path modes (skipped with
a warning when absent).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

VALID_STATUSES = {"verified-static", "verified-executed", "inferred", "proposed", "stale"}

FENCE_RE = re.compile(r"^```[ \t]*\n(.*?)\n```", re.DOTALL | re.MULTILINE)
LIST_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CITATION_RE = re.compile(r"[A-Za-z0-9_./-]+\.(?:py|md|txt|ya?ml|toml|json|ipynb|R|jl)(?:::|\:)")


def run_git(repo: Path, args, nul=False):
    """Return lines or NUL-delimited fields; None on git/environment failure."""
    try:
        p = subprocess.run(["git", "-C", str(repo)] + args,
                           capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode != 0:
        return None
    text = os.fsdecode(p.stdout)
    if nul:
        return text.split("\0")[:-1]
    return [ln for ln in text.splitlines() if ln.strip()]


def _clean(val: str) -> str:
    """Strip trailing inline '#' comments and surrounding quotes from a value."""
    val = re.split(r"\s+#", val, maxsplit=1)[0].strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        val = val[1:-1]
    return val


def parse_meta(text: str):
    """Parse the first fenced block of a card: flat keys, inline-comment tolerant,
    block lists ('key:' + '  - item') and flow lists ('key: [a, b]')."""
    m = FENCE_RE.search(text)
    if not m:
        return None
    meta, key = {}, None
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        km = LIST_KEY_RE.match(line)
        if km and not raw.startswith((" ", "\t")):
            key, inline = km.group(1), _clean(km.group(2))
            if inline == "":
                meta[key] = []                      # block list; expect '- item' lines
            elif inline.startswith("[") and inline.endswith("]"):
                inner = inline[1:-1].strip()
                meta[key] = [x.strip() for x in inner.split(",") if x.strip()] if inner else []
            else:
                meta[key] = inline
            continue
        if line.lstrip().startswith("- ") and isinstance(meta.get(key), list):
            meta[key].append(_clean(line.lstrip()[2:].strip()))
            continue
        meta.setdefault("_bad_lines", []).append(line)
    return meta


class Card:
    def __init__(self, md_path: Path, map_dir: Path):
        self.path = md_path
        self.rel = md_path.relative_to(map_dir).as_posix()
        self.text = md_path.read_text(encoding="utf-8", errors="replace")
        self.meta = parse_meta(self.text)
        self.id = md_path.stem if self.meta is None else self.meta.get("module") or self.meta.get("capability") or md_path.stem

    def listed(self, key):
        v = (self.meta or {}).get(key)
        return v if isinstance(v, list) else []


def is_card(rel: str) -> bool:
    """Only index.md and files under modules/ or capabilities/ are cards;
    other .md files in the map dir (bootstrap notes etc.) are ignored."""
    return rel == "index.md" or rel.startswith("modules/") or rel.startswith("capabilities/")


def iter_cards(map_dir: Path):
    for p in sorted(map_dir.rglob("*.md")):
        if is_card(p.relative_to(map_dir).as_posix()):
            yield p


def non_card_md(map_dir: Path):
    out = []
    for p in sorted(map_dir.rglob("*.md")):
        rel = p.relative_to(map_dir).as_posix()
        if not is_card(rel):
            out.append(rel)
    return out


def strip_anchor(target: str):
    return target.split("#", 1)[0]


def path_exists(repo: Path, rel: str):
    rel = strip_anchor(rel)
    if not rel or rel.startswith(("http://", "https://", "mailto:")):
        return None  # not a filesystem check
    pure = PurePosixPath(rel)
    if pure.is_absolute():
        return (Path(rel).exists(), rel)
    return ((repo / rel).exists(), rel)


def check(map_dir: Path, repo: Path):
    problems, notes, cards = [], [], {}
    head_lines = run_git(repo, ["rev-parse", "HEAD"])
    git_ok = head_lines is not None
    head = (head_lines or [None])[0]
    dirty = set()
    if git_ok:
        dirty.update(changed_paths(repo, working=True)[0] or [])
    if not git_ok:
        notes.append("git unavailable or not a repo: revision/dirty checks skipped")

    for p in iter_cards(map_dir):
        card = Card(p, map_dir)
        cards[card.id] = card
        if card.meta is None:
            problems.append(f"{card.rel}: missing metadata fenced block (module/status/verified_revision/sources)")
            continue
        if card.meta.get("_bad_lines"):
            notes.append(f"{card.rel}: unparsable metadata lines: {card.meta['_bad_lines']}")
        status = card.meta.get("status")
        if status is None:
            problems.append(f"{card.rel}: 'status' missing")
        elif status not in VALID_STATUSES:
            problems.append(f"{card.rel}: unknown status '{status}' (valid: {sorted(VALID_STATUSES)})")
        if "verified_revision" not in card.meta:
            problems.append(f"{card.rel}: 'verified_revision' missing (use 'none' without git)")
        is_index = card.rel.endswith("index.md")
        if "sources" not in card.meta and not is_index:
            problems.append(f"{card.rel}: 'sources' missing")

        for key in ("sources", "tests", "config"):
            for rel in card.listed(key):
                res = path_exists(repo, rel)
                if res and not res[0]:
                    problems.append(f"{card.rel}: {key} path does not exist: {rel}")

        # markdown links: card-relative .md links must resolve; repo paths checked too
        for target in MDLINK_RE.findall(card.text):
            t = strip_anchor(target)
            if not t or t.startswith(("http://", "https://", "mailto:")):
                continue
            if t.endswith(".md"):
                if not ((p.parent / t).exists() or (map_dir / t).exists()):
                    problems.append(f"{card.rel}: broken card link: {target}")
            elif PurePosixPath(t).is_absolute():
                notes.append(f"{card.rel}: absolute path reference skipped: {t}")
            else:
                if not (repo / t).exists():
                    problems.append(f"{card.rel}: referenced repo path missing: {t}")

        if card.rel.startswith(("modules/", "capabilities/")):
            id_key = "module" if card.rel.startswith("modules/") else "capability"
            cid = card.meta.get(id_key)
            if cid and cid != card.path.stem:
                problems.append(f"{card.rel}: {id_key} id '{cid}' does not match file stem '{card.path.stem}'")
            body_wo_meta = FENCE_RE.sub("", card.text, count=1)
            if not CITATION_RE.search(body_wo_meta):
                problems.append(f"{card.rel}: no inline source citation (path::symbol or path:line) outside the metadata block")

        rev = card.meta.get("verified_revision")
        if git_ok and rev and rev != "none":
            if run_git(repo, ["cat-file", "-t", rev]) is None:
                problems.append(f"{card.rel}: verified_revision '{rev}' unknown to git")
            elif head and rev.strip()[:40] != head.strip()[:40]:
                if run_git(repo, ["merge-base", "--is-ancestor", rev, "HEAD"]) is None:
                    notes.append(f"{card.rel}: baseline '{rev}' is not an ancestor of HEAD (history rewritten?)")
                else:
                    notes.append(f"{card.rel}: baseline '{rev}' is behind HEAD; claims may predate current code")
        elif (not git_ok) and rev and rev != "none":
            notes.append(f"{card.rel}: revision recorded but git unavailable to confirm")

        touched = sorted(set(card.listed("sources")) & dirty)
        if touched:
            notes.append(f"{card.rel}: dirty working-tree files in scope: {', '.join(touched)}")

    for card in cards.values():
        for dep in card.listed("depends-on") + card.listed("depended-on-by"):
            if dep not in cards:
                problems.append(f"{card.rel}: depends-on references unknown module id '{dep}'")

    skipped = non_card_md(map_dir)
    if skipped:
        notes.append(f"non-card .md files ignored (not index.md / modules/* / capabilities/*): {skipped}")

    return problems, notes, cards


def changed_paths(repo: Path, rev=None, working=False, files=None):
    if files is not None:
        return [PurePosixPath(f).as_posix() for f in files], "provided paths"
    if not run_git(repo, ["rev-parse", "HEAD"]):
        return None, "git unavailable — pass --files or let the agent inspect the repo directly"
    paths = []
    # uncommitted/untracked state counts whenever git change detection is used
    status = run_git(repo, ["status", "--porcelain=v1", "-z", "--untracked-files=all"], nul=True)
    if status is None:
        return None, "git status failed — pass --files or inspect the repo directly"
    records = iter(status)
    for record in records:
        paths.append(record[3:])
        # Porcelain -z emits destination first, then source for renames/copies.
        if "R" in record[:2] or "C" in record[:2]:
            paths.append(next(records))
    if rev:
        # Disable rename collapsing: deletion + addition retains both paths.
        got = run_git(repo, ["diff", "--name-only", "--no-renames", "-z", f"{rev}..HEAD", "--"], nul=True)
        if got is None:
            return None, f"baseline '{rev}' invalid or not a repo"
        paths.extend(got)
    basis = f"since {rev} + working tree" if rev else "working tree"
    return sorted(set(p for p in paths if p)), basis


def affected(cards, changed):
    """Match cards to changed paths by exact or prefix (directory) overlap."""
    out = {}
    for cid, card in cards.items():
        listed = card.listed("sources") + card.listed("tests") + card.listed("config")
        hits = []
        for ch in changed:
            for rel in listed:
                rel = strip_anchor(rel)
                if rel == ch or ch.startswith(rel.rstrip("/") + "/") or rel.startswith(ch.rstrip("/") + "/"):
                    hits.append(ch)
                    break
        if hits:
            out[cid] = {"card": card.rel, "changed": sorted(set(hits))}
    covered = set()
    for cid, card in cards.items():
        for rel in card.listed("sources"):
            rel = strip_anchor(rel)
            for ch in changed:
                if ch == rel or ch.startswith(rel.rstrip("/") + "/") or rel.startswith(ch.rstrip("/") + "/"):
                    covered.add(ch)
    uncovered = sorted(set(changed) - covered)
    return out, uncovered


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], add_help=True)
    ap.add_argument("--map-dir", default=".agent/project-map")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--affected", action="store_true", help="report cards affected by changes instead of full check")
    ap.add_argument("--working", action="store_true", help="with --affected: uncommitted + untracked changes")
    ap.add_argument("--rev", help="with --affected: commits since revision (plus working tree)")
    ap.add_argument("--files", nargs="+", help="with --affected: explicit changed paths (no-git fallback)")
    args = ap.parse_args(argv)

    map_dir, repo = Path(args.map_dir), Path(args.repo)
    if not map_dir.is_dir():
        print(f"ERROR: map dir not found: {map_dir}", file=sys.stderr)
        return 2

    cards = {c.id: c for c in (Card(p, map_dir) for p in iter_cards(map_dir))}

    if args.affected:
        if not (args.working or args.rev or args.files):
            args.working = True  # sensible default: uncommitted changes
        changed, basis = changed_paths(repo, rev=args.rev, working=args.working, files=args.files)
        if changed is None:
            print(f"ERROR: {basis}", file=sys.stderr)
            return 2
        aff, uncov = affected(cards, changed)
        if args.as_json:
            print(json.dumps({"basis": basis, "affected": aff, "changed_uncovered": uncov}, indent=2))
        else:
            print(f"basis: {basis}; changed paths: {len(changed)}")
            for cid, info in sorted(aff.items()):
                print(f"  AFFECTED {cid}: {info['card']} <- {', '.join(info['changed'])}")
            if uncov:
                print("  changed but not covered by any card (consider new/updated cards):")
                for pth in uncov:
                    print(f"    - {pth}")
            if not aff:
                print("  no cards matched")
        return 0

    problems, notes, checked_cards = check(map_dir, repo)
    if args.as_json:
        print(json.dumps({"problems": problems, "notes": notes}, indent=2))
    else:
        for pb in problems:
            print(f"PROBLEM: {pb}")
        for nt in notes:
            print(f"note: {nt}")
        print(f"cards checked: {len(checked_cards)}; problems: {len(problems)}; notes: {len(notes)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
