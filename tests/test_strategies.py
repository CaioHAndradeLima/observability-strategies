import unittest

from observability_strategies.models import EvalCase
from observability_strategies.strategies import select_strategies, evaluate_strategy, STRATEGY_NAMES


class TestStrategies(unittest.TestCase):
    def test_select_default(self):
        self.assertEqual(len(select_strategies(None)), 3)

    def test_select_subset(self):
        self.assertEqual(select_strategies(["retrieval_only"]), ("retrieval_only",))

    def test_unknown_strategy(self):
        with self.assertRaises(ValueError):
            select_strategies(["nope"])

    def test_retrieval_only_shape(self):
        case = EvalCase(id="1", query="q", retrieved_doc_ids=("a",), relevant_doc_ids=("a",))
        out = evaluate_strategy([case], "retrieval_only")
        self.assertIn("retrieval", out)
        self.assertNotIn("answer", out)

    def test_e2e_has_answer(self):
        case = EvalCase(id="1", query="q", retrieved_doc_ids=("a",), relevant_doc_ids=("a",), answer_text="x")
        out = evaluate_strategy([case], "e2e_offline")
        self.assertIn("answer", out)

    def test_strategy_names_stable(self):
        self.assertIn("judge_augmented", STRATEGY_NAMES)


if __name__ == "__main__":
    unittest.main()
