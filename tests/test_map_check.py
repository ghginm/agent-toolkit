"""Unit tests for skills/project-map/scripts/map_check.py (mechanical checks)."""
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parent.parent
FIX = REPO / "tests" / "fixtures"
SCRIPT = REPO / "skills" / "project-map" / "scripts" / "map_check.py"
MAP_CHECK = SimpleNamespace(**runpy.run_path(str(SCRIPT)))


def run(args, cwd):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, cwd=cwd)


class MapCheckCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="atk-map-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.proj = self.tmp / "proj"
        shutil.copytree(FIX / "map-sample", self.proj)
        self.map = ".agent/project-map"

    def card(self, rel):
        return self.proj / self.map / rel

    def git(self, *args):
        return subprocess.run(["git", *args], capture_output=True, text=True,
                              cwd=self.proj, check=True).stdout.strip()

    def test_pristine_map_passes(self):
        r = run(["--json"], cwd=self.proj)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["problems"], [])
        # no git around the copy? tmpdir may sit under a repo on some systems; notes differ, problems stay clean
        self.assertEqual(r.returncode, 0)

    def test_dead_source_path_flagged(self):
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace("  - app/core.py", "  - app/ghost.py\n  - app/core.py"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ghost.py", r.stdout)
        self.assertIn("does not exist", r.stdout)

    def test_broken_card_link_flagged(self):
        p = self.card("index.md")
        p.write_text(p.read_text().replace("modules/core.md", "modules/gone.md"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("gone.md", r.stdout)

    def test_unknown_status_and_missing_meta_flagged(self):
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace("status: verified-static", "status: totally-verified"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown status", r.stdout)
        (self.card("modules/extra.md")).write_text("# extra\n\nno metadata block at all\n")
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing metadata fenced block", r.stdout)

    def test_unknown_module_dependency_flagged(self):
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace("depends-on: []", "depends-on:\n  - not-a-module"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown module id", r.stdout)

    def test_affected_by_files(self):
        r = run(["--affected", "--files", "app/core.py"], cwd=self.proj)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("AFFECTED core", r.stdout)
        self.assertNotIn("not covered by any card", r.stdout)  # core.py is covered by the core card
        r = run(["--affected", "--files", "app/report.py", "--json"], cwd=self.proj)
        out = json.loads(r.stdout)
        self.assertIn("app/report.py", out["changed_uncovered"])

    def test_affected_with_git_rev_and_working_tree(self):
        if shutil.which("git") is None:
            self.skipTest("git unavailable")
        self.git("init", "-q")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        base = self.git("rev-parse", "HEAD")
        # committed change touching a card source
        (self.proj / "app" / "core.py").write_text((self.proj / "app" / "core.py").read_text() + "\n# touched\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "change")
        r = run(["--affected", "--rev", base], cwd=self.proj)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("AFFECTED core", r.stdout)
        # uncommitted new file shows as uncovered change
        (self.proj / "app" / "brand_new.py").write_text("x = 1\n")
        r = run(["--affected", "--working", "--json"], cwd=self.proj)
        out = json.loads(r.stdout)
        self.assertIn("app/brand_new.py", out["changed_uncovered"])

    def test_rename_paths_working_and_committed(self):
        if shutil.which("git") is None:
            self.skipTest("git unavailable")
        self.git("init", "-q")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        base = self.git("rev-parse", "HEAD")
        self.git("mv", "app/core.py", "app/renamed core.py")
        expected = ["app/core.py", "app/renamed core.py"]
        self.assertEqual(MAP_CHECK.changed_paths(self.proj, working=True)[0], expected)
        old_card = MAP_CHECK.Card(self.card("modules/core.md"), self.proj / self.map)
        new_card = MAP_CHECK.Card(self.card("modules/core.md"), self.proj / self.map)
        new_card.meta["sources"] = ["app/renamed core.py"]
        hits, uncovered = MAP_CHECK.affected({"old": old_card, "new": new_card}, expected)
        self.assertEqual(set(hits), {"old", "new"})
        self.assertEqual(uncovered, [])
        r = run(["--json"], cwd=self.proj)
        self.assertIn("dirty working-tree files in scope: app/core.py", r.stdout)
        r = run(["--affected", "--working", "--json"], cwd=self.proj)
        self.assertEqual(json.loads(r.stdout)["affected"]["core"]["changed"], ["app/core.py"])
        self.git("commit", "-qm", "rename")
        self.assertEqual(MAP_CHECK.changed_paths(self.proj, rev=base)[0], expected)
        r = run(["--affected", "--rev", base, "--json"], cwd=self.proj)
        self.assertEqual(json.loads(r.stdout)["affected"]["core"]["changed"], ["app/core.py"])

    def test_revision_checks_with_git(self):
        if shutil.which("git") is None:
            self.skipTest("git unavailable")
        self.git("init", "-q")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        head = self.git("rev-parse", "HEAD")
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace("verified_revision: none", f"verified_revision: {head}"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 0, r.stdout)  # exact HEAD match: clean
        p.write_text(p.read_text().replace(head, "0" * 40))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown to git", r.stdout)

    def test_changed_paths_preserve_filenames_and_all_change_states(self):
        if shutil.which("git") is None:
            self.skipTest("git unavailable")
        self.git("init", "-q")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")
        tracked = ["staged edit.py", "unstaged edit.py", "staged delete.py",
                   "unstaged delete.py", ' old "é"\tname.py ']
        for name in tracked:
            (self.proj / name).write_text("original\n")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        for name in tracked[:2]:
            (self.proj / name).write_text("changed\n")
        self.git("add", "--", tracked[0])
        self.git("rm", "--", tracked[2])
        (self.proj / tracked[3]).unlink()
        renamed = ' new "é"\nname.py '
        self.git("mv", "--", tracked[4], renamed)
        (self.proj / "staged add.py").write_text("added\n")
        self.git("add", "--", "staged add.py")
        (self.proj / "new dir").mkdir()
        (self.proj / "new dir" / "untracked file.py").write_text("new\n")
        expected = sorted(tracked + [renamed, "staged add.py", "new dir/untracked file.py"])
        self.assertEqual(MAP_CHECK.changed_paths(self.proj, working=True)[0], expected)
        self.assertIsNone(MAP_CHECK.changed_paths(self.proj, rev="nonexistent-baseline")[0])
        self.assertEqual(MAP_CHECK.changed_paths(self.tmp, files=["app/core.py"]),
                         (["app/core.py"], "provided paths"))
        self.assertIsNone(MAP_CHECK.changed_paths(self.tmp, working=True)[0])

    def test_dirty_tree_note(self):
        if shutil.which("git") is None:
            self.skipTest("git unavailable")
        self.git("init", "-q")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        (self.proj / "app" / "core.py").write_text("# dirty now\n")
        r = run([], cwd=self.proj)
        self.assertIn("dirty working-tree files in scope", r.stdout)

    def test_missing_map_dir_usage_error(self):
        r = run(["--map-dir", "nope"], cwd=self.proj)
        self.assertEqual(r.returncode, 2)
        self.assertIn("map dir not found", r.stderr)

    def test_flow_style_depends_on_is_checked(self):
        # regression: reviewer-probed hole — flow lists used to parse as scalars,
        # silently disabling the unknown-module check
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace("depends-on: []", "depends-on: [ghost, phantom]"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown module id 'ghost'", r.stdout)
        self.assertIn("unknown module id 'phantom'", r.stdout)

    def test_inline_comments_in_metadata_tolerated(self):
        # regression: copying a template comment must not hard-fail the card
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace(
            "status: verified-static",
            "status: verified-static   # verified-static | verified-executed | inferred"))
        r = run([], cwd=self.proj)
        self.assertNotIn("unknown status", r.stdout)

    def test_non_card_md_files_ignored(self):
        (self.card("README-bootstrap.md")).write_text("# bootstrap note\n\nno metadata here\n")
        r = run(["--json"], cwd=self.proj)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("README-bootstrap.md", " | ".join(json.loads(r.stdout)["notes"]))

    def test_module_id_must_match_filename(self):
        p = self.card("modules/core.md")
        p.write_text(p.read_text().replace("module: core", "module: feature-engineering"))
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("does not match file stem", r.stdout)

    def test_uncited_card_flagged(self):
        p = self.card("modules/core.md")
        text = "\n".join(ln for ln in p.read_text().splitlines() if "::" not in ln)
        p.write_text(text)
        r = run([], cwd=self.proj)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no inline source citation", r.stdout)


if __name__ == "__main__":
    unittest.main()
