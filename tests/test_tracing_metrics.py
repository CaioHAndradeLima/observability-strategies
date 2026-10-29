import unittest

from observability_strategies.models import SpanNode, TraceFixture
from observability_strategies import tracing_metrics as tm


class TestTracingMetrics(unittest.TestCase):
    def test_rollup_tokens_and_cost(self):
        trace = TraceFixture(
            trace_id="t",
            spans=(
                SpanNode("1", "llm.generate", None, 0, 100, {"tokens_in": 10, "tokens_out": 5, "cost_usd": 0.01}),
            ),
        )
        row = tm.rollup_trace(trace)
        self.assertEqual(row["tokens_in"], 10)
        self.assertEqual(row["cost_usd"], 0.01)

    def test_aggregate_mean(self):
        trace = TraceFixture(
            trace_id="t",
            spans=(SpanNode("1", "api.request", None, 0, 200, {}),),
        )
        agg = tm.aggregate([trace])
        self.assertEqual(agg["mean_latency_ms"], 200.0)


if __name__ == "__main__":
    unittest.main()
