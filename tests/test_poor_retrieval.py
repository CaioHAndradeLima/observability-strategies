import unittest

from observability_strategies.poor_retrieval import next_fix_branch, diagnose_golden
from observability_strategies.models import EvalCase


class TestPoorRetrieval(unittest.TestCase):
    def test_index_miss_branch(self):
        self.assertEqual(
            next_fix_branch({"labeled_hit_rate": 0.0, "recall_at_k": 0.0, "ndcg_at_k": 0.0}),
            "index_or_filter_miss",
        )

    def test_recall_branch(self):
        self.assertEqual(
            next_fix_branch({"labeled_hit_rate": 1.0, "recall_at_k": 0.3, "ndcg_at_k": 0.8}),
            "chunking_or_embedding_recall",
        )

    def test_ndcg_branch(self):
        self.assertEqual(
            next_fix_branch({"labeled_hit_rate": 1.0, "recall_at_k": 0.7, "ndcg_at_k": 0.4}),
            "rerank_or_fusion_ordering",
        )

    def test_ok_branch(self):
        self.assertEqual(
            next_fix_branch({"labeled_hit_rate": 1.0, "recall_at_k": 0.9, "ndcg_at_k": 0.9}),
            "retrieval_ok_investigate_downstream",
        )

    def test_diagnose_golden(self):
        cases = [
            EvalCase(
                id="p",
                query="q",
                retrieved_doc_ids=("wrong",),
                relevant_doc_ids=("right",),
                tags=("poor_retrieval",),
            )
        ]
        out = diagnose_golden(cases)
        self.assertIn("summary_branch", out)


if __name__ == "__main__":
    unittest.main()
