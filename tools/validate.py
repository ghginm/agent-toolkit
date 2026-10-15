#!/usr/bin/env python3
"""Validate toolkit skills: Agent Skills spec metadata + local reference integrity.

Discovers skills by scanning skills/*/SKILL.md (no central registry — adding a
skill directory is enough). Optionally delegates to skill-creator quick
validators when their paths are provided and a Python with PyYAML is reachable.

Usage:
  python tools/validate.py                      # all skills in this repo
  python tools/validate.py --skills project-audit
  python tools/validate.py --root /path/to/toolkit
  python tools/validate.py --creators ../skill-creator/skills
Exit: 0 = all valid, 1 = problems found. Warnings never fail the run.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skillkit

SKILL_MD_MAX_LINES = 500
REF_TOKEN_RE = re.compile(r"`((?:references|scripts|assets)/[\w./-]+)`")
LINK_RE = re.compile(r"\[[^\]]*\]\(((?:references|scripts|assets)/[\w./-]+)\)")


def check_skill(skill_dir: Path):
    """Return (problems, warnings) for one skill directory."""
    problems, warnings = [], []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return [f"{skill_dir.name}: SKILL.md not found"], warnings
    text = md.read_text(encoding="utf-8")
    fm, errs = skillkit.parse_frontmatter(text)
    problems += [f"{skill_dir.name}: frontmatter: {e}" for e in errs]
    if fm is None:
        return problems, warnings

    extra = set(fm) - skillkit.SPEC_KEYS
    if extra:
        problems.append(f"{skill_dir.name}: non-spec frontmatter keys: {sorted(extra)}")
    if "name" not in fm:
        problems.append(f"{skill_dir.name}: missing 'name'")
    else:
        problems += [f"{skill_dir.name}: {e}" for e in skillkit.validate_name(fm["name"])]
        if fm.get("name") != skill_dir.name:
            problems.append(f"{skill_dir.name}: name '{fm['name']}' != directory name")
    desc = fm.get("description")
    if not desc:
        problems.append(f"{skill_dir.name}: missing/empty 'description'")
    else:
        if len(desc) > 1024:
            problems.append(f"{skill_dir.name}: description {len(desc)} > 1024 chars")
        if "<" in desc or ">" in desc:
            problems.append(f"{skill_dir.name}: description contains angle brackets")
        if len(desc) < 20:
            warnings.append(f"{skill_dir.name}: description is very short — weak triggering risk")
    if len((fm.get("compatibility") or "")) > 500:
        problems.append(f"{skill_dir.name}: compatibility > 500 chars")
    meta = fm.get("metadata") or {}
    if not isinstance(meta, dict):
        problems.append(f"{skill_dir.name}: metadata must be a mapping")
    if desc and not re.search(r"use when|used when|when the user|when asked|trigger", desc, re.I):
        warnings.append(f"{skill_dir.name}: description lacks explicit 'use when' trigger phrasing")

    body_lines = text.count("\n")
    if body_lines > SKILL_MD_MAX_LINES:
        problems.append(f"{skill_dir.name}: SKILL.md {body_lines} lines > {SKILL_MD_MAX_LINES}")
    if len(text) > 32000:
        warnings.append(f"{skill_dir.name}: SKILL.md is large ({len(text)} chars) — consider splitting references")

    # local reference integrity: every `references/...`/scripts/assets token must exist
    for ref in set(REF_TOKEN_RE.findall(text)) | set(LINK_RE.findall(text)):
        if (skill_dir / ref).exists():
            continue
        if ref.endswith("/") and (skill_dir / ref.rstrip("/")).is_dir():
            continue
        problems.append(f"{skill_dir.name}: referenced path missing: {ref}")
    # references must stay one level deep (no reference chain pointing into another reference)
    for rp in (skill_dir / "references").glob("*.md") if (skill_dir / "references").is_dir() else []:
        for ref in set(REF_TOKEN_RE.findall(rp.read_text(encoding="utf-8"))):
            if ref.startswith("references/") and (skill_dir / ref).exists() and ref != rp.relative_to(skill_dir).as_posix():
                warnings.append(f"{skill_dir.name}: {rp.name} chains to {ref} (keep references one level from SKILL.md)")
    # hygiene: no compiled/stray artifacts shipped inside a skill
    for junk in skill_dir.rglob("*"):
        if junk.is_file() and (junk.suffix in {".pyc", ".pyo"} or "__pycache__" in junk.parts):
            problems.append(f"{skill_dir.name}: stray build artifact in skill dir: {junk.relative_to(skill_dir)}")
    for sp in (skill_dir / "scripts").glob("*") if (skill_dir / "scripts").is_dir() else []:
        if sp.suffix == ".py" and "python" not in sp.read_text(encoding="utf-8").splitlines()[0].lower():
            warnings.append(f"{skill_dir.name}: {sp.name} has no python shebang")
    return problems, warnings


def try_creator_validators(skill_dirs, creators_root: Path):
    """Run upstream quick_validate.py scripts if a PyYAML-capable python exists."""
    report = []
    candidates = [creators_root / "skill-creator-anthropic" / "scripts" / "quick_validate.py",
                  creators_root / "skill-creator-openai" / "scripts" / "quick_validate.py"]
    pythons = [sys.executable, "/usr/bin/python3", "python3"]
    for v in candidates:
        if not v.is_file():
            report.append(f"skip (not found): {v}")
            continue
        ran = None
        for py in pythons:
            try:
                p = subprocess.run([py, "-c", "import yaml"], capture_output=True, timeout=20)
                if p.returncode != 0:
                    continue
            except Exception:
                continue
            for d in skill_dirs:
                r = subprocess.run([py, str(v), str(d)], capture_output=True, text=True, timeout=60)
                ran = (py, r)
                break
            break
        if ran is None:
            report.append(f"skip (no PyYAML-capable interpreter): {v.name}")
        else:
            py, r = ran
            status = "PASS" if r.returncode == 0 else "FAIL"
            report.append(f"{v.parent.parent.name} on {', '.join(d.name for d in skill_dirs)}: {status} — {r.stdout.strip()[:120]}")
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate toolkit skills against the Agent Skills spec and local references.")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="toolkit repo root")
    ap.add_argument("--skills", help="comma-separated subset; default: all discovered")
    ap.add_argument("--creators", help="path to dir containing skill-creator-*/ for optional upstream validation")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    want = set(s.strip() for s in args.skills.split(",")) if args.skills else None
    found, problems, warnings = [], [], []
    for d, _md in skillkit.discover(root):
        if want and d.name not in want:
            continue
        found.append(d)
        p, w = check_skill(d)
        problems += p
        warnings += w
    if want:
        missing = want - {d.name for d in found}
        if missing:
            problems.append(f"requested skills not found under {root}/skills: {sorted(missing)}")

    print(f"skills found: {[d.name for d in found]}")
    for w in warnings:
        print(f"WARNING: {w}")
    for p in problems:
        print(f"PROBLEM: {p}")
    if args.creators:
        print("--- upstream creator validators ---")
        for line in try_creator_validators(found, Path(args.creators)):
            print(line)
    print(f"result: {'OK' if not problems else 'FAILED'} ({len(problems)} problems, {len(warnings)} warnings)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
