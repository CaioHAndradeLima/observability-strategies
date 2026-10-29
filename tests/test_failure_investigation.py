import unittest

from observability_strategies.models import SpanNode, TraceFixture
from observability_strategies.failure_investigation import investigate, evaluate_incidents


class TestFailureInvestigation(unittest.TestCase):
    def test_retrieval_error_layer(self):
        trace = TraceFixture(
            trace_id="e",
            expected_failure_layer="retrieval",
            spans=(
                SpanNode("1", "api.request", None, 0, 100, {}),
                SpanNode("2", "agent.retrieve", "1", 5, 50, {"error": True}),
            ),
        )
        diag = investigate(trace)
        self.assertEqual(diag.hypothesized_layer, "retrieval")

    def test_output_validation_error(self):
        trace = TraceFixture(
            trace_id="o",
            expected_failure_layer="output_validation",
            spans=(
                SpanNode("1", "api.request", None, 0, 100, {}),
                SpanNode("2", "output.validate", "1", 80, 90, {"status": "error"}),
            ),
        )
        diag = investigate(trace)
        self.assertEqual(diag.hypothesized_layer, "output_validation")

    def test_evaluate_incidents_match_rate(self):
        traces = [
            TraceFixture(
                trace_id="e",
                expected_failure_layer="retrieval",
                spans=(SpanNode("1", "agent.retrieve", None, 0, 10, {"error": True}),),
            )
        ]
        out = evaluate_incidents(traces)
        self.assertEqual(out["layer_match_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
