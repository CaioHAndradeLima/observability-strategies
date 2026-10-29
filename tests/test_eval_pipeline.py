import unittest
from pathlib import Path

from observability_strategies.data import load_golden
from observability_strategies.eval_pipeline import orchestrate, score_run
from observability_strategies.models import EvalCase, RunFixture

ROOT = Path(__file__).resolve().parents[1]


class TestEvalPipeline(unittest.TestCase):
    def test_score_run_output_match(self):
        case = EvalCase(
            id="c",
            query="q",
            retrieved_doc_ids=("d",),
            relevant_doc_ids=("d",),
            expected_output_valid=True,
        )
        run = RunFixture(case_id="c", strategy="e2e_offline", retrieved_doc_ids=("d",), answer_text="a", output_valid=True)
        row = score_run(case, run)
        self.assertTrue(row["output_valid_match"])

    def test_orchestrate_loads_runs(self):
        cases = load_golden(ROOT / "data/golden.json")
        out = orchestrate(ROOT, cases)
        self.assertGreaterEqual(out["run_count"], 1)


if __name__ == "__main__":
    unittest.main()
