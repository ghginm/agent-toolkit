"""Unit tests for tools/install.py — discovery, copy semantics, safe updates."""
import json
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
        self.assertIn("project-brief", r.stdout)
        self.assertIn("not installed", r.stdout)
        self.assertIn("profiles:", r.stdout)

    def test_default_installs_all_skills_with_generic_harness(self):
        r = run(["--target", str(self.tmp)])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        expected = {p.parent.name for p in (REPO / "skills").glob("*/SKILL.md")}
        dest = self._dest(".agents")
        self.assertEqual({p.name for p in dest.iterdir() if p.is_dir()}, expected)
        lock = json.loads((dest / "agent-toolkit.lock.json").read_text())
        self.assertEqual(set(lock["entries"]), expected)
        self.assertTrue(all(entry["harness"] == "generic" for entry in lock["entries"].values()))

    def test_explicit_all_skills_and_profiles(self):
        expected = {p.parent.name for p in (REPO / "skills").glob("*/SKILL.md")}
        for i, flags in enumerate((["--skills", "all"], ["--skills", "all", "--profile", "all"])):
            with self.subTest(flags=flags):
                target = self.tmp / str(i)
                r = run(["--target", str(target), *flags])
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                dest = target / ".agents" / "skills"
                self.assertEqual({p.name for p in dest.iterdir() if p.is_dir()}, expected)
                self.assertEqual(r.stdout.count("[ok] installed:"), len(expected))

    def test_all_profiles_union_without_duplicates(self):
        root = self.tmp / "source"
        shutil.copytree(REPO / "skills", root / "skills")
        profiles = root / "profiles"
        profiles.mkdir()
        for name, skills in (("first", ["project-map"]),
                             ("second", ["project-map", "tidy-dev"])):
            (profiles / f"{name}.json").write_text(json.dumps({"skills": skills}))
        target = self.tmp / "project"
        r = run(["--root", str(root), "--target", str(target), "--profile", "all"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        dest = target / ".agents" / "skills"
        self.assertEqual({p.name for p in dest.iterdir() if p.is_dir()}, {"project-map", "tidy-dev"})
        self.assertEqual(r.stdout.count("[ok] installed:"), 2)

    def test_named_profile_limits_default_selection(self):
        r = run(["--target", str(self.tmp), "--profile", "software-development"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual({p.name for p in self._dest(".agents").iterdir() if p.is_dir()},
                         {"project-audit", "project-map", "project-brief", "decision-workshop"})

    def test_explicit_skills_and_profile_are_combined_once(self):
        r = run(["--target", str(self.tmp), "--skills", "project-map,tidy-dev,tidy-dev",
                 "--profile", "ml-development"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual({p.name for p in self._dest(".agents").iterdir() if p.is_dir()},
                         {"project-audit", "project-map", "project-brief", "decision-workshop", "tidy-dev"})
        self.assertEqual(r.stdout.count("[ok] installed:"), 5)

    def test_default_discovers_new_skill_without_profiles(self):
        r = run(["--root", str(FIX / "skillset"), "--target", str(self.tmp)])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self._dest(".agents") / "mini-skill" / "SKILL.md").is_file())

    def test_default_dry_run_writes_nothing(self):
        r = run(["--target", str(self.tmp), "--dry-run"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        expected = len(list((REPO / "skills").glob("*/SKILL.md")))
        self.assertEqual(r.stdout.count("[dry] installed:"), expected)
        self.assertEqual(list(self.tmp.iterdir()), [])

    def test_unknown_explicit_selection_fails_before_writing(self):
        for flags in (["--skills", "unknown"], ["--profile", "unknown"],
                      ["--skills", "unknown", "--profile", "ml-development"]):
            with self.subTest(flags=flags):
                r = run(["--target", str(self.tmp), *flags])
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertEqual(list(self.tmp.iterdir()), [])

    def test_install_single_skill_independent(self):
        other = self.tmp / ".devin" / "skills" / "project-audit"
        other.mkdir(parents=True)
        (other / "SKILL.md").write_text("team copy")
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("installed: project-audit", r.stdout)
        self.assertIn("duplicate-warning: project-audit", r.stdout)
        self.assertIn(str(other), r.stdout)
        self.assertIn("Destination: " + str(self._dest(".agents")), r.stdout)
        self.assertEqual((other / "SKILL.md").read_text(), "team copy")
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
            self.assertTrue((t / sub / "skills" / "project-brief" / "SKILL.md").is_file())
            self.assertTrue((t / sub / "skills" / "decision-workshop" / "SKILL.md").is_file())

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
        self.assertIn("up-to-date: project-audit", r.stdout)
        self.assertNotIn("duplicate-warning", r.stdout)
        # user edits the installed copy (outside lock record) -> skip-conflict, content preserved
        victim = d / "project-audit" / "SKILL.md"
        original = victim.read_text()
        victim.write_text(original + "\nUSER NOTE: my own customization\n")
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic"])
        self.assertEqual(r.returncode, 3)
        self.assertIn("user-modified", r.stdout)
        self.assertIn("skipped-conflict: project-audit", r.stdout)
        self.assertNotIn("Installed to", r.stdout)
        self.assertIn("USER NOTE", victim.read_text())
        # lock still says installed-content differs; --force replaces
        r = run(["--target", str(self.tmp), "--skills", "project-audit", "--harness", "generic", "--force"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("USER NOTE", victim.read_text())
        self.assertIn("updated: project-audit", r.stdout)

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
        self.assertIn("updated: project-audit", r.stdout)
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

    def test_brief_alone_all_harnesses_preserves_artifacts_and_conflicts(self):
        cases = {"generic": ".agents", "codex": ".agents", "claude": ".claude",
                 "copilot": ".github", "devin": ".devin"}
        for harness, directory in cases.items():
            with self.subTest(harness=harness):
                target = self.tmp / harness
                target.mkdir()
                preserved = {
                    "AGENTS.md": "Team instructions\n",
                    "CLAUDE.md": "Team Claude instructions\n",
                    "policies/focused-changes.md": "Local policy\n",
                    "docs/project-brief/README.md": "Authored guide\n",
                    ".agent/project-map/index.md": "Local map\n",
                }
                for relative, content in preserved.items():
                    path = target / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
                args = ["--target", str(target), "--skills", "project-brief",
                        "--harness", harness]
                result = run(args)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                destination = target / directory / "skills"
                self.assertEqual({p.name for p in destination.iterdir() if p.is_dir()},
                                 {"project-brief"})
                for relative in ("SKILL.md", "references/synthesis.md", "assets/brief-template.md"):
                    self.assertEqual((destination / "project-brief" / relative).read_bytes(),
                                     (REPO / "skills/project-brief" / relative).read_bytes())
                self.assertIn("up-to-date: project-brief", run(args).stdout)
                victim = destination / "project-brief" / "references/synthesis.md"
                custom = victim.read_text() + "\nTeam customization\n"
                victim.write_text(custom)
                conflict = run(args)
                self.assertEqual(conflict.returncode, 3, conflict.stdout + conflict.stderr)
                self.assertEqual(victim.read_text(), custom)
                forced = run([*args, "--force"])
                self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
                self.assertNotIn("Team customization", victim.read_text())
                for relative, content in preserved.items():
                    self.assertEqual((target / relative).read_text(encoding="utf-8"), content)

    def test_skill_md_and_scripts_survive(self):
        run(["--target", str(self.tmp), "--skills", "project-map", "--harness", "generic"])
        script = self._dest(".agents") / "project-map" / "scripts" / "map_check.py"
        r = subprocess.run([sys.executable, str(script), "--map-dir", str(self.tmp) + "/nonexistent"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("map dir not found", r.stderr)


if __name__ == "__main__":
    unittest.main()
