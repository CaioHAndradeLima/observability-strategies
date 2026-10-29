import json
import unittest
from pathlib import Path

from observability_strategies.data import load_golden
from observability_strategies.measure_profiles import load_measure_profiles, evaluate_gates
from observability_strategies.pipeline_evaluation import run_observability_pipeline_eval

ROOT = Path(__file__).resolve().parents[1]


class TestMetricsAndGates(unittest.TestCase):
    def test_ci_profile_passes(self):
        profiles = load_measure_profiles(ROOT / "config/measure_profiles.json")
        profile = profiles["ci-observability-eval"]
        report = run_observability_pipeline_eval(ROOT, profile)
        gate = evaluate_gates(report, profile)
        self.assertTrue(gate["passed"], gate.get("failures"))

    def test_unknown_profile_file_structure(self):
        profiles = load_measure_profiles(ROOT / "config/measure_profiles.json")
        self.assertIn("ci-all-strategies", profiles)

    def test_scorecard_core_fields(self):
        profiles = load_measure_profiles(ROOT / "config/measure_profiles.json")
        report = run_observability_pipeline_eval(ROOT, profiles["ci-observability-eval"])
        core = report["scorecard"]["core_quality"]
        self.assertIsNotNone(core["recall_at_k"])

    def test_measure_report_roundtrip(self):
        profiles = load_measure_profiles(ROOT / "config/measure_profiles.json")
        profile = profiles["ci-observability-eval"]
        path = ROOT / "reports/test-gate.json"
        path.parent.mkdir(exist_ok=True)
        report = run_observability_pipeline_eval(ROOT, profile)
        path.write_text(json.dumps(report))
        loaded = json.loads(path.read_text())
        gate = evaluate_gates(loaded, profile)
        self.assertTrue(gate["passed"])


if __name__ == "__main__":
    unittest.main()
