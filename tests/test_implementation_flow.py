import unittest

from observability_strategies.implementation_flow import summarize_implementation_flow
from observability_strategies.maturity import lab_maturity_snapshot
from observability_strategies.evaluation import evaluate_implementation_checklist
from observability_strategies.data import load_golden
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestImplementationFlow(unittest.TestCase):
    def test_flow_stages(self):
        out = summarize_implementation_flow({"complete": True})
        self.assertGreaterEqual(len(out["stages"]), 5)

    def test_maturity_production_only_list(self):
        m = lab_maturity_snapshot()
        self.assertFalse(m["capabilities"]["otel_collector_deploy"])
        self.assertGreater(len(m["production_deployment_only"]), 2)

    def test_checklist_complete_on_fixture(self):
        cases = load_golden(ROOT / "data/golden.json")
        chk = evaluate_implementation_checklist(cases, traces_count=2)
        self.assertTrue(chk["complete"])


if __name__ == "__main__":
    unittest.main()
