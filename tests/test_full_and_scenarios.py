import unittest
from pathlib import Path

from observability_strategies.full_evaluation import run_full_evaluation
from observability_strategies.scenario_evaluation import evaluate_canary_scenario, evaluate_incident_scenarios
from observability_strategies.data import load_golden

ROOT = Path(__file__).resolve().parents[1]


class TestFullAndScenarios(unittest.TestCase):
    def test_full_coverage_100(self):
        report = run_full_evaluation(ROOT)
        self.assertEqual(report["coverage"]["lab_coverage_percent"], 100)
        self.assertEqual(report["coverage"]["observability_guides"], "11/11")

    def test_full_has_all_guide_keys(self):
        report = run_full_evaluation(ROOT)
        for key in (
            "retrieval_independent_metrics",
            "poor_retrieval_scores",
            "evaluate_answer_metrics",
            "llm_judge_vs_human",
            "tracing_for_observability",
            "tracing_metrics",
            "investigate_failure",
            "observability_tools",
            "regression_and_canary",
            "implementation_flow",
            "decision_based",
        ):
            self.assertIn(key, report)

    def test_incident_scenarios(self):
        out = evaluate_incident_scenarios(ROOT)
        self.assertGreaterEqual(out["count"], 1)

    def test_canary_scenario(self):
        cases = load_golden(ROOT / "data/golden.json")
        out = evaluate_canary_scenario(ROOT, cases)
        self.assertIn("passed", out)


if __name__ == "__main__":
    unittest.main()
