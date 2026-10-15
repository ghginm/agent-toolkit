"""Unit tests for tools/install.py — discovery, copy semantics, safe updates."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIX = REPO / "tests" / "fixtures"
INSTALL = REPO / "tools" / "install.py"


def run(args, cwd=None):
    return subprocess.run([sys.executable, str(INSTALL), *args],
                          capture_output=True, text=True, cwd=cwd)


class InstallCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="atk-install-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _dest(self, harness_dir, scope="project"):
        if scope == "project":
            return self.tmp / harness_dir / "skills"
        return Path.home()  # user scope never exercised against real home in tests

    def test_list(self):
        r = run(["--list", "--target", str(self.tmp), "--harness", "codex"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("project-audit", r.stdout)
        self.assertIn("project-map", r.stdout)
        self.assertIn("not installed", r.stdout)
        self.assertIn("profiles:", r.stdout)

    def test_install_single_skill_independent(self):
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        d = self._dest(".agents")
        self.assertTrue((d / "project-audit" / "SKILL.md").is_file())
        self.assertFalse((d / "project-map").exists())  # installing one must not require the other

    def test_install_both_harness_dirs(self):
        cases = {"claude": ".claude", "codex": ".agents", "copilot": ".github", "devin": ".devin", "generic": ".agents"}
        for i, (h, sub) in enumerate(cases.items()):
            t = self.tmp / f"p{i}"
            r = run(["--target", str(t), "--profile", "ml-development", "--harness", h])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue((t / sub / "skills" / "project-audit" / "SKILL.md").is_file())
            self.assertTrue((t / sub / "skills" / "project-map" / "SKILL.md").is_file())

    def test_dry_run_writes_nothing(self):
        r = run(["--target", str(self.tmp), "--skills", "project-map", "--harness", "generic", "--dry-run"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("dry-run", r.stdout)
        self.assertEqual(list(self.tmp.glob("**/*")), [])

    def test_up_to_date_and_conflict_protection(self):
        run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic"])
        d = self._dest(".agents")
        # second run: unchanged -> "up to date"
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("already installed and unchanged", r.stdout)
        # user edits the installed copy (outside lock record) -> skip-conflict, content preserved
        victim = d / "project-audit" / "SKILL.md"
        original = victim.read_text()
        victim.write_text(original + "\nUSER NOTE: my own customization\n")
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 3)
        self.assertIn("user-modified", r.stdout)
        self.assertIn("USER NOTE", victim.read_text())
        # lock still says installed-content differs; --force replaces
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic", "--force"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("USER NOTE", victim.read_text())

    def test_replace_after_source_update_is_silent(self):
        """A newer source version replaces our previous install without conflict warnings."""
        src_root = self.tmp / "srcroot"
        (src_root / "skills").mkdir(parents=True)
        shutil.copytree(REPO / "skills" / "project-audit", src_root / "skills" / "project-audit")
        target = self.tmp / "proj"
        r = run(["--root", str(src_root), "--target", str(target), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # simulate a toolkit source update
        src_md = src_root / "skills" / "project-audit" / "SKILL.md"
        src_md.write_text(src_md.read_text() + "\nNEW: updated source\n")
        r = run(["--root", str(src_root), "--target", str(target), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("replace", r.stdout)
        self.assertIn("NEW: updated source",
                      (target / ".agents" / "skills" / "project-audit" / "SKILL.md").read_text())

    def test_unrelated_files_untouched(self):
        d = self.tmp / ".agents" / "skills"
        d.mkdir(parents=True)
        (d / "team-owned-skill").mkdir()
        (d / "team-owned-skill" / "SKILL.md").write_text("mine")
        (d / "keep.txt").write_text("keep")
        run(["--target", str(self.tmp), "--skills", "project-map", "--harness", "generic"])
        self.assertEqual((d / "team-owned-skill" / "SKILL.md").read_text(), "mine")
        self.assertEqual((d / "keep.txt").read_text(), "keep")
        self.assertTrue((d / "project-map" / "SKILL.md").is_file())

    def test_new_skill_installs_without_code_changes(self):
        r = run(["--root", str(FIX / "skillset"), "--target", str(self.tmp),
                 "--skills", "mini-skill", "--harness", "generic"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self._dest(".agents") / "mini-skill" / "SKILL.md").is_file())

    def test_bundled_resources_referenced_after_copy(self):
        run(["--target", str(self.tmp), "--skills", "project-map", "--harness", "generic"])
        d = self._dest(".agents") / "project-map"
        for rel in ("scripts/map_check.py", "references/map-format.md",
                    "references/workflows.md", "assets/l2-module-template.md",
                    "assets/bootstrap-snippet.md"):
            self.assertTrue((d / rel).is_file(), rel)

    def test_skill_md_and_scripts_survive(self):
        run(["--target", str(self.tmp), "--skills", "project-map", "--harness", "generic"])
        script = self._dest(".agents") / "project-map" / "scripts" / "map_check.py"
        r = subprocess.run([sys.executable, str(script), "--map-dir", str(self.tmp) + "/nonexistent"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("map dir not found", r.stderr)


if __name__ == "__main__":
    unittest.main()
