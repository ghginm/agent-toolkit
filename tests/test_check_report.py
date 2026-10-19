"""Unit tests for skills/project-audit/scripts/check_report.py."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "project-audit" / "scripts" / "check_report.py"

GOOD_INDEX = """# Audit — demo — 2026-10-15 — modes: architecture, ml

- Run id: 20261015-1430-arch-ml

## Coverage
Inspected: src/. Not inspected: tests/.
"""

GOOD_ARCH = """# Audit 1 — architecture — demo — 2026-10-15

### AUD-ARCH-001 — config couples everything
status: draft · priority: P1 · confidence: high — read directly · evidence: verified-static

- **Observed:** global dict imported by all modules, `config.py::CONFIG`.
- **Proposed action:** parameterize per run (proposed).

## Coding agent handoff
### For AUD-ARCH-001
- Touch points: `config.py::CONFIG`
"""

GOOD_ML = """# Audit 2 — ml — demo — 2026-10-15

### AUD-ML-001 — scaler fitted before split
status: draft · priority: P0 · confidence: high · evidence: verified-static

- **Observed:** `src/data.py::build_dataset` fits StandardScaler before train_test_split.
- **Category:** justified-now

## Coding agent handoff
### For AUD-ML-001
- Touch points: `src/data.py::build_dataset`
"""


class CheckReportCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="atk-report-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.proj = self.tmp / "proj"
        (self.proj / "src").mkdir(parents=True)
        (self.proj / "config.py").write_text("CONFIG = {}\n")
        (self.proj / "src" / "data.py").write_text("def build_dataset():\n    pass\n")
        self.rundir = self.proj / ".agent" / "audits" / "20261015-1430-arch-ml"

    def write(self, name, text):
        self.rundir.mkdir(parents=True, exist_ok=True)
        (self.rundir / name).write_text(text)

    def check(self):
        return subprocess.run([sys.executable, str(SCRIPT), "--project", str(self.proj),
                               "--run", str(self.rundir)], capture_output=True, text=True)

    def test_clean_report_passes(self):
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH)
        self.write("ml.md", GOOD_ML)
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_mode_file_flagged(self):
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH)  # modes say ml too
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("ml.md", r.stdout)

    def test_valid_citation_is_not_implementation_proof(self):
        # data.py contains only pass, despite the report's scaler-fit claim.
        # This is intentionally accepted: the checker is structural, not an agent.
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH)
        self.write("ml.md", GOOD_ML)
        self.assertEqual((self.proj / "src/data.py").read_text(),
                         "def build_dataset():\n    pass\n")
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_summary_tables_and_handoff_references_do_not_duplicate_findings(self):
        summary = """## Executive summary
The sampled configuration has one significant coupling risk.

## Findings at a glance
| ID / detail | Priority | Confidence | Evidence | Status |
|---|---|---|---|---|
| [AUD-ARCH-001](#aud-arch-001--config-couples-everything) | P1 | high | verified-static | draft |

## Coverage and evidence
Inspected: `config.py::CONFIG`. Executed: not run; static review only.

## Sound areas to preserve
No sound area was established in scope.

## First priorities
1. AUD-ARCH-001 after acceptance; see the finding for validation.

"""
        self.write("index.md", GOOD_INDEX + summary)
        self.write("architecture.md", GOOD_ARCH.replace("### AUD-ARCH-001", summary + "### AUD-ARCH-001", 1)
                   + "\n- Tests/verification: see AUD-ARCH-001 Validation.\n")
        self.write("ml.md", GOOD_ML)
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("findings checked: 2; problems: 0", r.stdout)

    def test_summary_first_report_with_no_findings_passes(self):
        self.write("index.md", GOOD_INDEX.replace("architecture, ml", "architecture"))
        self.write("architecture.md", """# Audit — architecture
## Executive summary
No significant findings in the inspected sample; no execution was performed.
## Findings at a glance
No significant findings.
## Coverage and evidence
Inspected: `config.py::CONFIG`. Not inspected: runtime consumers.
## Sound areas to preserve
None established in scope.
## First priorities
No action justified by this audit.
## Findings
None.
## Watch items / unknowns
Runtime behavior is unknown; inspect consumers before drawing conclusions.
## Coding agent handoff
No implementation is proposed.
""")
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("findings checked: 0; problems: 0", r.stdout)

    def test_missing_run_dir_usage_error(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--project", str(self.proj),
                            "--run", str(self.proj / "nope")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_extra_report_file_flagged(self):
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH)
        self.write("exploratory.md", "not a mode we ran\n")
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("unexpected report file", r.stdout)

    def test_dangling_citation_flagged(self):
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH.replace("config.py::CONFIG", "config_ghost.py::CONFIG"))
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("cited path does not exist", r.stdout)

    def test_dot_prefixed_project_citation_preserved(self):
        card = self.proj / ".agent/project-map/modules/core.md"
        card.parent.mkdir(parents=True)
        card.write_text("# Core\n")
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH
                   + "\nMap claim: `.agent/project-map/modules/core.md:1`.\n")
        self.write("ml.md", GOOD_ML)
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        card.unlink()
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("cited path does not exist: .agent/project-map/modules/core.md", r.stdout)

    def test_missing_fields_and_handoff_flagged(self):
        ml = GOOD_ML.replace(
            "status: draft · priority: P0 · confidence: high · evidence: verified-static",
            "status: totally-done")
        ml = ml.split("## Coding agent handoff")[0]  # drop the handoff section entirely
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH)
        self.write("ml.md", ml)
        r = self.check()
        self.assertEqual(r.returncode, 1)
        out = r.stdout
        self.assertIn("missing 'priority:'", out)
        self.assertIn("missing 'Coding agent handoff'", out)
        self.assertIn("not in lifecycle vocabulary", out)

    def test_duplicate_ids_flagged(self):
        dup = ("\n### AUD-ARCH-001 — dup title\n"
               "status: draft · priority: P2 · confidence: low · evidence: inferred\n\n"
               "- **Observed:** again `config.py::CONFIG`.\n")
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH.replace("## Coding agent handoff", dup + "\n## Coding agent handoff"))
        r = self.check()
        self.assertIn("duplicate finding id AUD-ARCH-001", r.stdout)

    def test_template_leftovers_flagged(self):
        self.write("index.md", GOOD_INDEX)
        self.write("architecture.md", GOOD_ARCH + "\n<some placeholder>\n<!-- TODO -->\n")
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("placeholders", r.stdout)
        self.assertIn("HTML template comments", r.stdout)


if __name__ == "__main__":
    unittest.main()
