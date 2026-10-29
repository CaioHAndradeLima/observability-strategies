import unittest

from observability_strategies.observability_tools import summarize_tools, TOOL_MATRIX


class TestObservabilityTools(unittest.TestCase):
    def test_matrix_not_empty(self):
        self.assertGreaterEqual(len(TOOL_MATRIX), 4)

    def test_summarize_has_tools(self):
        s = summarize_tools()
        self.assertIn("tools", s)
        self.assertGreater(len(s["tools"]), 0)


if __name__ == "__main__":
    unittest.main()
