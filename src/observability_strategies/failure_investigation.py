"""Top-down trace walk to hypothesize failing layer."""

from __future__ import annotations

from .models import LayerDiagnosis, TraceFixture

LAYER_BY_SPAN = {
    "api.request": "ingress",
    "supervisor.route": "routing",
    "agent.retrieve": "retrieval",
    "agent.assemble_context": "context",
    "llm.generate": "generation",
    "output.validate": "output_validation",
    "tool.execute": "tools",
}


def _slowest_leaf_path(trace: TraceFixture) -> list[str]:
    by_parent: dict[str | None, list] = {}
    for s in trace.spans:
        by_parent.setdefault(s.parent_id, []).append(s)
    path: list[str] = []

    def walk(parent_id: str | None) -> None:
        children = by_parent.get(parent_id, [])
        if not children:
            return
        slowest = max(children, key=lambda s: s.end_ms - s.start_ms)
        path.append(slowest.name)
        walk(slowest.span_id)

    walk(None)
    return path


def _error_span_layer(trace: TraceFixture) -> str | None:
    for s in trace.spans:
        if s.attributes.get("error") or s.attributes.get("status") == "error":
            return LAYER_BY_SPAN.get(s.name, "unknown")
    return None


def investigate(trace: TraceFixture) -> LayerDiagnosis:
    err_layer = _error_span_layer(trace)
    path = _slowest_leaf_path(trace)
    if err_layer:
        return LayerDiagnosis(
            hypothesized_layer=err_layer,
            confidence=0.9,
            span_path=path,
            notes="error attribute on span",
        )
    if path:
        layer = LAYER_BY_SPAN.get(path[-1], "unknown")
        return LayerDiagnosis(hypothesized_layer=layer, confidence=0.65, span_path=path)
    return LayerDiagnosis(hypothesized_layer="unknown", confidence=0.0, span_path=[])


def evaluate_incidents(traces: list[TraceFixture]) -> dict:
    if not traces:
        return {"count": 0, "layer_match_rate": 0.0}
    matches = 0
    rows = []
    for t in traces:
        diag = investigate(t)
        expected = t.expected_failure_layer
        ok = expected is None or diag.hypothesized_layer == expected
        if ok:
            matches += 1
        rows.append(
            {
                "trace_id": t.trace_id,
                "expected_layer": expected,
                "hypothesized_layer": diag.hypothesized_layer,
                "confidence": diag.confidence,
                "span_path": diag.span_path,
                "match": ok,
            }
        )
    n = len(traces)
    return {
        "count": n,
        "layer_match_rate": matches / n,
        "cases": rows,
        "reference_doc": "investigate-failure-by-observability-data.md",
    }
