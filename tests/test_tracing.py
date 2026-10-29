import unittest

from observability_strategies.models import SpanNode, TraceFixture
from observability_strategies.tracing import build_span_tree, parse_all


class TestTracing(unittest.TestCase):
    def _sample_trace(self):
        return TraceFixture(
            trace_id="t1",
            spans=(
                SpanNode("1", "api.request", None, 0, 100, {}),
                SpanNode("2", "agent.retrieve", "1", 10, 50, {}),
            ),
        )

    def test_build_tree_roots(self):
        tree = build_span_tree(self._sample_trace())
        self.assertEqual(tree["span_count"], 2)
        self.assertEqual(len(tree["roots"]), 1)

    def test_child_duration(self):
        tree = build_span_tree(self._sample_trace())
        child = tree["roots"][0]["children"][0]
        self.assertEqual(child["duration_ms"], 40)

    def test_parse_all_success(self):
        out = parse_all([self._sample_trace()])
        self.assertEqual(out["parse_success_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
