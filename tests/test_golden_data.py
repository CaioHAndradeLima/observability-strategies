import unittest
from pathlib import Path

from observability_strategies.data import load_golden, load_traces, load_runs, validate_golden

ROOT = Path(__file__).resolve().parents[1]


class TestGoldenData(unittest.TestCase):
    def test_golden_loads(self):
        cases = load_golden(ROOT / "data/golden.json")
        validate_golden(cases)
        self.assertGreaterEqual(len(cases), 5)

    def test_traces_load(self):
        traces = load_traces(ROOT / "data/traces.json")
        self.assertGreaterEqual(len(traces), 2)

    def test_runs_load(self):
        runs = load_runs(ROOT / "data/runs.json")
        self.assertGreaterEqual(len(runs), 1)

    def test_duplicate_ids_fail(self):
        from observability_strategies.models import EvalCase

        with self.assertRaises(ValueError):
            validate_golden(
                [
                    EvalCase(id="dup", query="q", retrieved_doc_ids=(), relevant_doc_ids=()),
                    EvalCase(id="dup", query="q2", retrieved_doc_ids=(), relevant_doc_ids=()),
                ]
            )


if __name__ == "__main__":
    unittest.main()
