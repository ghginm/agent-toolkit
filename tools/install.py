#!/usr/bin/env python3
"""Install toolkit skills into a project (or user home) for a target harness.

Canonical source is this repo's skills/ directory; the installer only copies
selected skills to the destination convention of the harness — one skill per
directory, unchanged content. No symlinks (Windows-safe), no framework.

Usage:
  python tools/install.py --target /path/to/project --skills project-audit,project-map --harness codex
  python tools/install.py --target . --profile ml-development --harness claude --dry-run
  python tools/install.py --list --harness copilot [--target project-dir]

Harnesses (project / user scope):
  claude    .claude/skills      ~/.claude/skills
  codex     .agents/skills      ~/.agents/skills
  copilot   .github/skills      ~/.copilot/skills
  devin     .devin/skills       ~/.config/devin/skills
  generic   .agents/skills      ~/.agents/skills   (cross-client convention)

Update safety: an existing installed skill whose content differs from the
source is SKIPPED with a warning unless --force replaces it (replace removes
locally-added files inside that skill dir — the warning says so). Nothing
outside the selected skill directories is ever written, except the installer's
own lock file (<dest>/agent-toolkit.lock.json) that tracks fingerprints.
"""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skillkit
from validate import check_skill

HARNESS_DIRS = {  # verified against product docs, 2026-10; see docs/installation.md
    "claude": (".claude/skills", "~/.claude/skills"),
    "codex": (".agents/skills", "~/.agents/skills"),
    "copilot": (".github/skills", "~/.copilot/skills"),
    "devin": (".devin/skills", "~/.config/devin/skills"),
    "generic": (".agents/skills", "~/.agents/skills"),
}
LOCK_NAME = "agent-toolkit.lock.json"


def load_lock(dest: Path):
    p = dest / LOCK_NAME
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"entries": {}}
    return {"entries": {}}


def save_lock(dest: Path, lock):
    dest.mkdir(parents=True, exist_ok=True)
    (dest / LOCK_NAME).write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_dest(root: Path, harness: str, scope: str):
    proj, user = HARNESS_DIRS[harness]
    if scope == "project":
        return (root / proj).resolve()
    return Path(user).expanduser().resolve()


def plan_actions(skills, dest: Path, force: bool):
    """Classify each skill: install | up-to-date | skip-conflict | replace."""
    lock = load_lock(dest)
    actions = []
    for d in skills:
        src_fp = skillkit.fingerprint(d)
        target = dest / d.name
        entry = lock.get("entries", {}).get(d.name)
        if not target.exists():
            actions.append(("install", d, target, src_fp))
        elif skillkit.fingerprint(target) == src_fp:
            actions.append(("up-to-date", d, target, src_fp))
        elif entry and skillkit.fingerprint(target) == entry.get("sha256"):
            actions.append(("replace", d, target, src_fp))  # matches our last install; source moved on
        elif force:
            actions.append(("replace", d, target, src_fp))
        else:
            actions.append(("skip-conflict", d, target, src_fp))
    return actions, lock


def execute(actions, lock, dest: Path, harness, scope, dry_run):
    lines, did = [], False
    for kind, src, target, src_fp in actions:
        if kind == "install":
            lines.append(f"[{'dry' if dry_run else 'ok'}] {kind}: {src.name} -> {target}")
            if not dry_run:
                shutil.copytree(src, target)
                lock.setdefault("entries", {})[src.name] = {
                    "sha256": src_fp, "harness": harness, "scope": scope,
                    "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "source_repo": "agent-toolkit",
                }
            did = True
        elif kind == "up-to-date":
            lines.append(f"[skip] {src.name} already installed and unchanged at {target}")
        elif kind == "replace":
            lines.append(f"[{'dry' if dry_run else 'ok'}] replace: {target} (previous install by this tool or --force)")
            if not dry_run:
                shutil.rmtree(target)
                shutil.copytree(src, target)
                lock.setdefault("entries", {})[src.name] = {
                    "sha256": src_fp, "harness": harness, "scope": scope,
                    "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "source_repo": "agent-toolkit",
                }
            did = True
        else:  # skip-conflict
            lines.append(f"[WARN] {src.name}: {target} exists with different content and no install record — "
                         f"likely user-modified. Not touched. Re-run with --force to replace "
                         f"(removes files added inside that skill directory).")
    if not dry_run and did:
        save_lock(dest, lock)
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install agent-toolkit skills into a target project or user home.")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="toolkit repo root (canonical skills source)")
    ap.add_argument("--target", default=".", help="destination project directory")
    ap.add_argument("--skills", help="comma-separated skill names")
    ap.add_argument("--profile", help="profile name under profiles/ (JSON with 'skills' list)")
    ap.add_argument("--harness", choices=sorted(HARNESS_DIRS), default="generic")
    ap.add_argument("--scope", choices=["project", "user"], default="project")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="replace existing destinations that differ")
    ap.add_argument("--list", action="store_true", dest="do_list")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    all_skills = [d for d, _ in skillkit.discover(root)]
    by_name = {d.name: d for d in all_skills}

    if args.do_list:
        dest = resolve_dest(Path(args.target).resolve(), args.harness, args.scope)
        lock = load_lock(dest) if dest.is_dir() else {"entries": {}}
        print(f"available skills ({root}/skills): {', '.join(sorted(by_name)) or '(none)'}")
        profiles_dir = root / "profiles"
        if profiles_dir.is_dir():
            print("profiles: " + ", ".join(sorted(p.stem for p in profiles_dir.glob("*.json"))))
        print(f"harness '{args.harness}' {args.scope} destination: {dest}")
        for name in sorted(by_name):
            state = "not installed"
            if (dest / name).is_dir():
                state = ("installed (up to date)" if skillkit.fingerprint(dest / name) == skillkit.fingerprint(by_name[name])
                         else "installed (differs from source)")
            print(f"  {name}: {state}")
        return 0

    if args.profile:
        prof = root / "profiles" / f"{args.profile}.json"
        if not prof.is_file():
            print(f"ERROR: profile not found: {prof}", file=sys.stderr)
            return 2
        names = json.loads(prof.read_text(encoding="utf-8")).get("skills", [])
    elif args.skills:
        names = [s.strip() for s in args.skills.split(",") if s.strip()]
    else:
        print("ERROR: pass --skills a,b or --profile name", file=sys.stderr)
        return 2

    skills = []
    for n in names:
        if n not in by_name:
            print(f"ERROR: skill not found under {root}/skills: {n}", file=sys.stderr)
            return 2
        skills.append(by_name[n])

    # validate before installing (fail fast, honest)
    problems = []
    for d in skills:
        p, _w = check_skill(d)
        problems += p
    if problems:
        print("ERROR: selected skills failed validation; fix or run tools/validate.py:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    dest = resolve_dest(Path(args.target).resolve(), args.harness, args.scope)
    actions, lock = plan_actions(skills, dest, args.force)
    for line in execute(actions, lock, dest, args.harness, args.scope, args.dry_run):
        print(line)
    if args.dry_run:
        print("dry-run: nothing written")
    else:
        print(f"\nInstalled to {dest}")
        print("Activate: most harnesses pick skills up automatically (restart the CLI if not;")
        print("Claude Code hot-reloads, Devin re-scans on clone).")
        print("Verify: ask the agent to list/summarize available skills, or check the SKILL.md path above.")
        print("Optional: paste the project-map bootstrap snippet into AGENTS.md/CLAUDE.md")
        print("(skills/project-map/assets/bootstrap-snippet.md) — the installer never edits those files.")
    kinds = {a[0] for a in actions}
    return 0 if "skip-conflict" not in kinds else 3


if __name__ == "__main__":
    sys.exit(main())
