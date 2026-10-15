"""Unit tests for tools/validate.py — skill metadata and reference integrity."""
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIX = REPO / "tests" / "fixtures"
VALIDATE = REPO / "tools" / "validate.py"


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(VALIDATE), *args],
                          capture_output=True, text=True, cwd=cwd)


class TestValidate(unittest.TestCase):
    def test_toolkit_skills_pass(self):
        r = run()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("project-audit", r.stdout)
        self.assertIn("project-map", r.stdout)
        self.assertIn("result: OK", r.stdout)

    def test_new_unrelated_skill_discovered(self):
        # mini-skill lives in a different root: discovery is directory-scan, no registry edits
        r = run("--root", str(FIX / "skillset"))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("mini-skill", r.stdout)
        self.assertIn("result: OK", r.stdout)

    def test_broken_fixtures_flagged(self):
        r = run("--root", str(FIX / "skillset-broken"))
        self.assertEqual(r.returncode, 1)
        out = r.stdout
        self.assertIn("must be lowercase letters/digits/hyphens", out)          # Bad_Name
        self.assertIn("missing/empty 'description'", out)                      # missing-desc
        self.assertIn("referenced path missing: references/does-not-exist.md", out)  # broken-ref
        self.assertIn("non-spec frontmatter keys: ['author']", out)               # extra-key

    def test_subset_selection(self):
        r = run("--skills", "project-audit")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("project-map", r.stdout.split("skills found")[1].split("result")[0])

    def test_unknown_skill_requested(self):
        r = run("--skills", "no-such-skill")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not found", r.stdout)


if __name__ == "__main__":
    unittest.main()
