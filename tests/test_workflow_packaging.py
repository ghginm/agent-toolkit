"""Packaging regressions for opt-in workflow skills and the instruction policy."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NAMES = ("agent-efficiency", "tidy-dev", "project-brief")


class WorkflowPackagingCase(unittest.TestCase):
    def test_independent_discovery_validation_and_installation(self):
        for name in NAMES:
            with self.subTest(skill=name), tempfile.TemporaryDirectory(prefix="atk-workflow-") as tmp:
                root = Path(tmp) / "source"
                source = root / "skills" / name
                shutil.copytree(REPO / "skills" / name, source)
                target = Path(tmp) / "project"
                target.mkdir()
                instructions = target / "AGENTS.md"
                original = "# Team instructions\n\nPreserve this section.\n"
                instructions.write_text(original, encoding="utf-8")
                for tool, args in (
                    ("validate.py", []),
                    ("install.py", ["--target", str(target), "--list"]),
                    ("install.py", ["--target", str(target), "--skills", name]),
                ):
                    result = subprocess.run(
                        [sys.executable, str(REPO / "tools" / tool), "--root", str(root), *args],
                        capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn(name, result.stdout)
                installed = target / ".agents" / "skills"
                self.assertEqual(
                    {p.name for p in installed.iterdir() if p.is_dir()}, {name}
                )
                source_files = {p.relative_to(source) for p in source.rglob("*") if p.is_file()}
                copied_files = {p.relative_to(installed / name)
                                for p in (installed / name).rglob("*") if p.is_file()}
                self.assertEqual(copied_files, source_files)
                for relative in source_files:
                    self.assertEqual((installed / name / relative).read_bytes(),
                                     (source / relative).read_bytes())
                self.assertEqual(instructions.read_text(encoding="utf-8"), original)
                self.assertFalse((target / "policies").exists())
                self.assertFalse((target / ".agent").exists())

    def test_policy_appends_verbatim_without_replacing_instructions(self):
        policy = (REPO / "policies" / "focused-changes.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="atk-policy-") as tmp:
            target = Path(tmp) / "AGENTS.md"
            original = "# Existing instructions\n\nTeam conventions.\n"
            target.write_text(original, encoding="utf-8")
            # Portable equivalent of the documented one-time shell append.
            with target.open("a", encoding="utf-8") as stream:
                stream.write("\n" + policy)
            self.assertEqual(target.read_text(encoding="utf-8"), original + "\n" + policy)


if __name__ == "__main__":
    unittest.main()
