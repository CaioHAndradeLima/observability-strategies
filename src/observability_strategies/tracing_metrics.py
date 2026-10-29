"""Roll up latency, cost, and token attributes from fixture spans."""

from __future__ import annotations

from .models import TraceFixture


def rollup_trace(trace: TraceFixture) -> dict:
    total_latency = max((s.end_ms for s in trace.spans), default=0.0)
    tokens_in = sum(int(s.attributes.get("tokens_in", 0)) for s in trace.spans)
    tokens_out = sum(int(s.attributes.get("tokens_out", 0)) for s in trace.spans)
    cost_usd = sum(float(s.attributes.get("cost_usd", 0.0)) for s in trace.spans)
    by_name: dict[str, float] = {}
    for s in trace.spans:
        by_name[s.name] = by_name.get(s.name, 0.0) + (s.end_ms - s.start_ms)
    return {
        "trace_id": trace.trace_id,
        "total_latency_ms": total_latency,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round(cost_usd, 6),
        "latency_by_span_name_ms": by_name,
    }


def aggregate(traces: list[TraceFixture]) -> dict:
    if not traces:
        return {"count": 0, "mean_latency_ms": 0.0, "mean_cost_usd": 0.0, "mean_tokens": 0.0}
    rows = [rollup_trace(t) for t in traces]
    n = len(rows)
    return {
        "count": n,
        "mean_latency_ms": sum(r["total_latency_ms"] for r in rows) / n,
        "mean_cost_usd": sum(r["cost_usd"] for r in rows) / n,
        "mean_tokens": sum(r["tokens_in"] + r["tokens_out"] for r in rows) / n,
        "traces": rows,
        "reference_doc": "tracing-for-observability-metrics.md",
    }
