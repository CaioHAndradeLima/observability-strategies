import unittest

from observability_strategies.models import EvalCase
from observability_strategies import answer_metrics as am


class TestAnswerMetrics(unittest.TestCase):
    def test_abstain_detection(self):
        self.assertTrue(am._is_abstain_text("I do not have enough information."))

    def test_citation_in_retrieved(self):
        case = EvalCase(
            id="c",
            query="q",
            retrieved_doc_ids=("d1",),
            relevant_doc_ids=("d1",),
            citations=("d1",),
            answer_text="ok",
        )
        self.assertTrue(am.citation_in_retrieved(case))

    def test_citation_forbidden(self):
        case = EvalCase(
            id="c",
            query="q",
            retrieved_doc_ids=("d1",),
            relevant_doc_ids=("d1",),
            citations=("d2",),
            answer_text="ok",
        )
        self.assertFalse(am.citation_in_retrieved(case))

    def test_abstain_correct(self):
        case = EvalCase(
            id="a",
            query="q",
            retrieved_doc_ids=(),
            relevant_doc_ids=(),
            answer_text="cannot answer",
            expected_abstain=True,
        )
        row = am.score_case(case)
        self.assertTrue(row["abstain_correct"])

    def test_aggregate_rates(self):
        cases = [
            EvalCase(
                id="1",
                query="q",
                retrieved_doc_ids=("d",),
                relevant_doc_ids=("d",),
                answer_text="text [d]",
                citations=("d",),
            )
        ]
        agg = am.aggregate(cases)
        self.assertEqual(agg["count"], 1)


if __name__ == "__main__":
    unittest.main()
