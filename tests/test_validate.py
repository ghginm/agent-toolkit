"""Unit tests for tools/validate.py — metadata, references, and creators."""
import contextlib
import io
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
FIX = REPO / "tests" / "fixtures"
VALIDATE = REPO / "tools" / "validate.py"


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(VALIDATE), *args],
                          capture_output=True, text=True, cwd=cwd)


class TestCreatorValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Temporary validators do not need PyYAML; keep CLI tests independent
        # of any installed creator or third-party Python package.
        (self.root / "yaml.py").write_text("", encoding="utf-8")
        self.env = dict(os.environ, PYTHONPATH=str(self.root))
        self.creators = self.root / "creators"
        self.calls = self.root / "calls.txt"

    def creator(self, name, body):
        script = self.creators / f"skill-creator-{name}" / "scripts" / "quick_validate.py"
        script.parent.mkdir(parents=True)
        script.write_text(
            "import sys\nfrom pathlib import Path\n"
            "skill = Path(sys.argv[1])\n"
            f"with open({str(self.calls)!r}, 'a') as log:\n"
            f"    log.write({name!r} + ':' + str(skill) + '\\n')\n"
            + body, encoding="utf-8")

    def validate(self):
        return subprocess.run(
            [sys.executable, str(VALIDATE), "--skills", "project-audit,project-map",
             "--creators", str(self.creators)],
            capture_output=True, text=True, env=self.env)

    def test_second_skill_failure_sets_exit_code(self):
        self.creator("anthropic", "print(skill.name)\nsys.exit(1 if skill.name == 'project-map' else 0)\n")
        r = self.validate()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("skill-creator-anthropic on project-audit: PASS", r.stdout)
        self.assertIn("skill-creator-anthropic on project-map: FAIL", r.stdout)
        self.assertIn("result: FAILED", r.stdout)
        self.assertEqual(self.calls.read_text().splitlines(), [
            f"anthropic:{REPO / 'skills' / name}" for name in ("project-audit", "project-map")])

    def test_all_discovered_skills_checked_by_both_creators(self):
        for name in ("anthropic", "openai"):
            self.creator(name, "print(skill.name)\n")
        r = subprocess.run(
            [sys.executable, str(VALIDATE), "--creators", str(self.creators)],
            capture_output=True, text=True, env=self.env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        skills = sorted(p.parent for p in (REPO / "skills").glob("*/SKILL.md"))
        self.assertEqual(self.calls.read_text().splitlines(), [
            f"{creator}:{skill}" for creator in ("anthropic", "openai") for skill in skills])
        self.assertEqual(r.stdout.count(": PASS"), len(skills) * 2)
        for creator in ("anthropic", "openai"):
            for skill in skills:
                self.assertIn(f"skill-creator-{creator} on {skill.name}: PASS", r.stdout)

    def test_first_failure_does_not_stop_later_checks(self):
        self.creator("anthropic", "sys.exit(1 if skill.name == 'project-audit' else 0)\n")
        self.creator("openai", "print('ok')\n")
        r = self.validate()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("skill-creator-anthropic on project-audit: FAIL", r.stdout)
        self.assertIn("skill-creator-anthropic on project-map: PASS", r.stdout)
        self.assertEqual(len(self.calls.read_text().splitlines()), 4)

    def test_one_creator_failure_overrides_other_creator_pass(self):
        self.creator("anthropic", "print('ok')\n")
        self.creator("openai", "print('invalid', file=sys.stderr)\nsys.exit(1)\n")
        r = self.validate()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for skill in ("project-audit", "project-map"):
            self.assertIn(f"skill-creator-anthropic on {skill}: PASS", r.stdout)
            self.assertIn(f"skill-creator-openai on {skill}: FAIL", r.stdout)
        self.assertIn("invalid", r.stdout)

    def test_crash_is_error_and_other_checks_continue(self):
        self.creator("anthropic", "raise RuntimeError('validator crashed')\n")
        self.creator("openai", "print('ok')\n")
        r = self.validate()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for skill in ("project-audit", "project-map"):
            self.assertIn(f"skill-creator-anthropic on {skill}: ERROR", r.stdout)
            self.assertIn(f"skill-creator-openai on {skill}: PASS", r.stdout)
        self.assertIn("RuntimeError: validator crashed", r.stdout)
        self.assertEqual(len(self.calls.read_text().splitlines()), 4)

    def test_missing_creators_are_skipped_without_false_pass(self):
        r = self.validate()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout.count(": SKIPPED"), 4)
        self.assertNotIn(": PASS", r.stdout)
        self.assertFalse(self.calls.exists())

    def test_no_yaml_interpreter_is_skipped(self):
        self.creator("anthropic", "print('ok')\n")
        validate = runpy.run_path(str(VALIDATE))
        with mock.patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1)):
            report, failures = validate["try_creator_validators"](
                [REPO / "skills" / "project-audit"], self.creators)
        self.assertEqual(failures, 0)
        self.assertIn("SKIPPED — no PyYAML-capable interpreter", report[0])
        self.assertFalse(self.calls.exists())

    def test_execution_errors_fail_main_and_continue(self):
        self.creator("anthropic", "print('ok')\n")
        self.creator("openai", "print('ok')\n")
        validate = runpy.run_path(str(VALIDATE))
        for error in (OSError("cannot execute"), subprocess.TimeoutExpired("validator", 60)):
            with self.subTest(error=type(error).__name__):
                def execute(cmd, **kwargs):
                    if cmd[1] == "-c":
                        return subprocess.CompletedProcess(cmd, 0)
                    raise error
                out = io.StringIO()
                with mock.patch.object(subprocess, "run", side_effect=execute), contextlib.redirect_stdout(out):
                    code = validate["main"]([
                        "--skills", "project-audit,project-map", "--creators", str(self.creators)])
                self.assertEqual(code, 1)
                self.assertEqual(out.getvalue().count(": ERROR"), 4)
                self.assertIn("result: FAILED", out.getvalue())
                self.assertNotIn(": PASS", out.getvalue())

    def test_abnormal_exit_is_error(self):
        self.creator("anthropic", "sys.exit(2)\n")
        r = self.validate()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertEqual(r.stdout.count(": ERROR"), 2)

    def test_builtin_failure_not_masked_by_creator_success(self):
        self.creator("anthropic", "print('ok')\n")
        r = subprocess.run(
            [sys.executable, str(VALIDATE), "--root", str(FIX / "skillset-broken"),
             "--creators", str(self.creators)], capture_output=True, text=True, env=self.env)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(": PASS", r.stdout)
        self.assertIn("result: FAILED", r.stdout)

    def test_no_selected_skills_produces_no_creator_pass(self):
        self.creator("anthropic", "print('ok')\n")
        r = subprocess.run(
            [sys.executable, str(VALIDATE), "--skills", "no-such-skill", "--creators", str(self.creators)],
            capture_output=True, text=True, env=self.env)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn(": PASS", r.stdout)
        self.assertFalse(self.calls.exists())


class TestValidate(unittest.TestCase):
    def test_toolkit_skills_pass(self):
        r = run()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("project-audit", r.stdout)
        self.assertIn("project-map", r.stdout)
        self.assertIn("project-brief", r.stdout)
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
