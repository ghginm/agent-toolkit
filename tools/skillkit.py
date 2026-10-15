#!/usr/bin/env python3
"""skillkit — tiny shared helpers for validate.py / install.py (stdlib only).

Lenient frontmatter parsing (flat keys, quoted strings, one-level nested maps
like `metadata:`), skill discovery, and content fingerprinting. Deliberately
not a YAML implementation: skills in this toolkit use a minimal frontmatter
subset, and heavier YAML errors should surface in the official validators.
"""
import hashlib
import re
from pathlib import Path

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def split_frontmatter(text: str):
    """Return (frontmatter_text|None, body, error|None)."""
    if not text.startswith("---"):
        return None, text, "file must start with '---' (no leading blank line/BOM)"
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?", text, re.DOTALL)
    if not m:
        return None, text, "unterminated frontmatter (missing closing '---')"
    return m.group(1), text[m.end():], None


def parse_frontmatter(text: str):
    """Parse the supported frontmatter subset. Returns (dict, errors:list)."""
    fm_text, _, err = split_frontmatter(text)
    if err or fm_text is None:
        return None, [err or "unterminated frontmatter"]
    data, errors, section = {}, [], None  # section: None | 'metadata'
    for i, raw in enumerate(fm_text.splitlines(), 1):
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if m and not raw.startswith((" ", "\t")):
            key, val = m.group(1), m.group(2).strip()
            section = None
            if key == "metadata" and val == "":
                section = "metadata"
                data[key] = {}
            elif val == "":
                errors.append(f"line {i}: empty value for '{key}'")
            else:
                data[key] = _unquote(val)
            continue
        m2 = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if m2 and section == "metadata":
            data["metadata"][m2.group(1)] = _unquote(m2.group(2).strip())
            continue
        if raw.startswith(" ") and section is None:
            errors.append(f"line {i}: unexpected indented line outside 'metadata:'")
        else:
            errors.append(f"line {i}: unparsable frontmatter line: {raw!r}")
    return data, errors


def _unquote(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def validate_name(name: str):
    errs = []
    if not isinstance(name, str) or not name:
        return ["'name' must be a non-empty string"]
    if len(name) > 64:
        errs.append(f"name too long ({len(name)} > 64)")
    if not NAME_RE.match(name):
        errs.append(f"name '{name}' must be lowercase letters/digits/hyphens, no leading/trailing/consecutive hyphens")
    return errs


def discover(root: Path):
    """Yield (skill_dir, skill_md_path) for each skills/<name>/SKILL.md under root."""
    skills_dir = Path(root) / "skills"
    if not skills_dir.is_dir():
        return
    for d in sorted(skills_dir.iterdir()):
        md = d / "SKILL.md"
        if d.is_dir() and md.is_file():
            yield d, md


def fingerprint(skill_dir: Path) -> str:
    """Stable content hash over all files in a skill directory."""
    h = hashlib.sha256()
    for p in sorted(Path(skill_dir).rglob("*")):
        if p.is_file():
            h.update(p.relative_to(skill_dir).as_posix().encode())
            h.update(b"\0")
            h.update(p.read_bytes())
            h.update(b"\0")
    return h.hexdigest()
