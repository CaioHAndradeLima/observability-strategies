import unittest

from observability_strategies.models import EvalCase
from observability_strategies import retrieval_metrics as rm


class TestRetrievalMetrics(unittest.TestCase):
    def test_recall_at_k_full_hit(self):
        self.assertEqual(rm.recall_at_k({"a", "b"}, ["a", "b", "c"], 2), 1.0)

    def test_recall_at_k_partial(self):
        self.assertEqual(rm.recall_at_k({"a", "b"}, ["a"], 5), 0.5)

    def test_recall_empty_relevant(self):
        self.assertEqual(rm.recall_at_k(set(), ["a"], 5), 1.0)

    def test_ndcg_perfect_order(self):
        self.assertAlmostEqual(rm.ndcg_at_k({"a"}, ["a", "b"], 5), 1.0)

    def test_labeled_hit_rate_miss(self):
        self.assertEqual(rm.labeled_hit_rate({"a"}, ["b"]), 0.0)

    def test_aggregate_on_case(self):
        case = EvalCase(
            id="x",
            query="q",
            retrieved_doc_ids=("d1", "d2"),
            relevant_doc_ids=("d1",),
        )
        agg = rm.aggregate([case])
        self.assertEqual(agg["count"], 1)
        self.assertGreaterEqual(agg["recall_at_k"], 0.5)


if __name__ == "__main__":
    unittest.main()
