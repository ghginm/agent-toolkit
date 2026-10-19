"""Concrete checker limits and ground truth; not agent-behavior certification."""
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests/fixtures/source-drift"


class SourceVerificationCase(unittest.TestCase):
    def test_mechanically_valid_map_can_have_false_behavior(self):
        result = subprocess.run(
            [sys.executable, str(REPO / "skills/project-map/scripts/map_check.py"),
             "--repo", str(FIXTURE),
             "--map-dir", str(FIXTURE / ".agent/project-map"), "--json"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["problems"], [])
        card = (FIXTURE / ".agent/project-map/modules/ingest.md").read_text()
        self.assertIn("deduplicated", card)
        load = runpy.run_path(str(FIXTURE / "app/ingest.py"))["load_records"]
        with tempfile.TemporaryDirectory(prefix="atk-source-") as tmp:
            csv = Path(tmp) / "invoices.csv"
            csv.write_text("id,amount\n7,1.25\n7,1.25\n", encoding="utf-8")
            rows = load(csv)
            self.assertNotIsInstance(rows, list)
            self.assertEqual(list(rows), [
                {"id": "7", "amount_cents": 125},
                {"id": "7", "amount_cents": 125},
            ])

    def test_source_fixture_assertions_execute_without_private_transport(self):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=FIXTURE, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Ran 1 test", result.stderr)
        self.assertFalse((FIXTURE / "private_invoice_transport.py").exists())

    def test_discovery_catalog_and_profiles_include_workshop(self):
        toolkit = runpy.run_path(str(REPO / "tools/skillkit.py"))
        discovered = {path.name for path, _ in toolkit["discover"](REPO)}
        self.assertIn("decision-workshop", discovered)
        for name in ("software-development", "ml-development"):
            profile = json.loads((REPO / "profiles" / (name + ".json")).read_text())
            self.assertIn("decision-workshop", profile["skills"])
            self.assertTrue(set(profile["skills"]) <= discovered)
        for path in ("README.md", "docs/architecture.md", "docs/installation.md"):
            self.assertIn("decision-workshop", (REPO / path).read_text())


if __name__ == "__main__":
    unittest.main()
