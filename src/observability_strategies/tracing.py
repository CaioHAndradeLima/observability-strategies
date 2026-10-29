"""Parse fixture traces into span trees."""

from __future__ import annotations

from .models import SpanNode, TraceFixture


def build_span_tree(trace: TraceFixture) -> dict:
    by_id = {s.span_id: s for s in trace.spans}
    children: dict[str | None, list[SpanNode]] = {}
    for span in trace.spans:
        children.setdefault(span.parent_id, []).append(span)
    for key in children:
        children[key].sort(key=lambda s: s.start_ms)

    def node(span: SpanNode) -> dict:
        return {
            "span_id": span.span_id,
            "name": span.name,
            "duration_ms": span.end_ms - span.start_ms,
            "attributes": span.attributes,
            "children": [node(c) for c in children.get(span.span_id, [])],
        }

    roots = children.get(None, [])
    return {
        "trace_id": trace.trace_id,
        "roots": [node(r) for r in roots],
        "span_count": len(trace.spans),
    }


def parse_all(traces: list[TraceFixture]) -> dict:
    trees = [build_span_tree(t) for t in traces]
    ok = all(t["span_count"] > 0 for t in trees)
    return {
        "trace_count": len(traces),
        "parse_success_rate": 1.0 if ok else 0.0,
        "trees": trees,
        "reference_doc": "tracing-for-observability.md",
    }
