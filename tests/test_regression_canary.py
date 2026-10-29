import unittest

from observability_strategies.regression_canary import compare_metric_bundles, evaluate_canary_fixtures


class TestRegressionCanary(unittest.TestCase):
    def test_no_regression_when_improved(self):
        out = compare_metric_bundles({"recall_at_k": 0.7}, {"recall_at_k": 0.8})
        self.assertTrue(out["passed"])

    def test_regression_detected(self):
        out = compare_metric_bundles({"recall_at_k": 0.8}, {"recall_at_k": 0.5}, tolerances={"recall_at_k": 0.0})
        self.assertFalse(out["passed"])

    def test_canary_fixture(self):
        payload = {"baseline_metrics": {"recall_at_k": 0.5}, "tolerances": {"recall_at_k": 0.2}}
        out = evaluate_canary_fixtures(payload, {"recall_at_k": 0.6})
        self.assertTrue(out["passed"])


if __name__ == "__main__":
    unittest.main()
