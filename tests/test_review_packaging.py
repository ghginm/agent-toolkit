"""Structural contracts, not generated-document quality or harness activation."""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class ReviewPackagingCase(unittest.TestCase):
    def test_workshop_lifecycle_all_destinations(self):
        for harness, directory in (("generic", ".agents"), ("codex", ".agents"),
                                   ("claude", ".claude"), ("copilot", ".github"),
                                   ("devin", ".devin")):
            with self.subTest(harness=harness), tempfile.TemporaryDirectory(prefix="atk-review-") as tmp:
                root = Path(tmp) / "source"
                source = root / "skills" / "decision-workshop"
                shutil.copytree(REPO / "skills/decision-workshop", source)
                target = Path(tmp) / "project"
                artifact = target / "discussion/decisions.md"
                artifact.parent.mkdir(parents=True)
                artifact.write_text("Authored decisions\n")
                args = [sys.executable, str(REPO / "tools/install.py"),
                        "--root", str(root), "--target", str(target),
                        "--skills", "decision-workshop", "--harness", harness]

                def run(*extra):
                    return subprocess.run([*args, *extra], capture_output=True, text=True)

                preview = run("--dry-run")
                self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
                self.assertFalse((target / directory).exists())
                first = run()
                self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
                dest = target / directory / "skills"
                self.assertEqual({p.name for p in dest.iterdir() if p.is_dir()},
                                 {"decision-workshop"})
                installed = dest / "decision-workshop/SKILL.md"
                self.assertEqual(installed.read_bytes(), (source / "SKILL.md").read_bytes())
                self.assertIn("up-to-date: decision-workshop", run().stdout)
                updated_text = (source / "SKILL.md").read_text() + "\nSource revision.\n"
                (source / "SKILL.md").write_text(updated_text)
                update = run()
                self.assertEqual(update.returncode, 0, update.stdout + update.stderr)
                self.assertIn("updated: decision-workshop", update.stdout)
                self.assertEqual(installed.read_text(), updated_text)
                custom = updated_text + "\nTeam customization.\n"
                installed.write_text(custom)
                conflict = run()
                self.assertEqual(conflict.returncode, 3, conflict.stdout + conflict.stderr)
                self.assertIn("skipped-conflict: decision-workshop", conflict.stdout)
                self.assertEqual(installed.read_text(), custom)
                forced = run("--force")
                self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
                self.assertEqual(installed.read_text(), updated_text)
                self.assertEqual(artifact.read_text(), "Authored decisions\n")

    def test_brief_reference_is_bundled_without_changing_overview_template(self):
        skill = REPO / "skills/project-brief"
        text = (skill / "SKILL.md").read_text()
        self.assertIn("`overview` (default)", text)
        self.assertIn("`deep-dive`", text)
        self.assertIn("references/deep-dive.md", text)
        self.assertTrue((skill / "references/deep-dive.md").is_file())
        template = (skill / "assets/brief-template.md").read_text()
        self.assertEqual(re.findall(r"^## File: (.+)$", template, re.M),
                         ["README.md", "pipeline.md", "roadmap.md"])

    def test_contract_document_navigation(self):
        readme = (REPO / "README.md").read_text()
        self.assertNotIn("## Optional Map → Audit → Brief workflow", readme)
        self.assertIn("docs/recommended-contract-examples.md", readme)
        self.assertIn("skills/decision-workshop/SKILL.md", readme)
        contracts = REPO / "docs/recommended-contract-examples.md"
        self.assertTrue(contracts.is_file())
        self.assertIn("deep-dive", contracts.read_text())
        for path in (REPO / "README.md", contracts):
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" not in link and not link.startswith("#"):
                    self.assertTrue((path.parent / link.split("#")[0]).exists(),
                                    f"{path.name}: {link}")


if __name__ == "__main__":
    unittest.main()
