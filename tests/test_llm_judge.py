import unittest

from observability_strategies.models import EvalCase
from observability_strategies.llm_judge import offline_rubric_score, aggregate_offline_judge, live_judge_available


class TestLlmJudge(unittest.TestCase):
    def test_offline_rubric_pass(self):
        case = EvalCase(
            id="j",
            query="q",
            retrieved_doc_ids=("d",),
            relevant_doc_ids=("d",),
            rubric_scores={"faithfulness": 0.9, "completeness": 0.9, "style": 0.9},
        )
        row = offline_rubric_score(case)
        self.assertTrue(row["passes_threshold"])

    def test_aggregate_judge(self):
        cases = [
            EvalCase(
                id="j",
                query="q",
                retrieved_doc_ids=("d",),
                relevant_doc_ids=("d",),
                rubric_scores={"faithfulness": 0.9, "completeness": 0.9, "style": 0.9},
            )
        ]
        agg = aggregate_offline_judge(cases)
        self.assertEqual(agg["judge_pass_rate"], 1.0)

    def test_live_not_required_in_ci(self):
        self.assertIsInstance(live_judge_available(), bool)


if __name__ == "__main__":
    unittest.main()
