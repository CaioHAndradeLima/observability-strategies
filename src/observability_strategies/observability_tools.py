"""Capability mapping for tracing/metrics/eval platforms (no vendor SDK deploy)."""

from __future__ import annotations

TOOL_MATRIX: tuple[dict, ...] = (
    {
        "name": "LangSmith",
        "tracing": "strong",
        "metrics_dashboards": "medium",
        "offline_eval": "strong",
        "multi_agent": "strong",
        "self_host": False,
    },
    {
        "name": "Langfuse",
        "tracing": "strong",
        "metrics_dashboards": "strong",
        "offline_eval": "medium",
        "multi_agent": "medium",
        "self_host": True,
    },
    {
        "name": "OpenTelemetry",
        "tracing": "strong",
        "metrics_dashboards": "via_backend",
        "offline_eval": "none",
        "multi_agent": "strong",
        "self_host": True,
    },
    {
        "name": "Prometheus/Grafana",
        "tracing": "via_exemplars",
        "metrics_dashboards": "strong",
        "offline_eval": "none",
        "multi_agent": "medium",
        "self_host": True,
    },
    {
        "name": "Custom warehouse + golden CI",
        "tracing": "export_required",
        "metrics_dashboards": "strong",
        "offline_eval": "strong",
        "multi_agent": "strong",
        "self_host": True,
    },
)


def summarize_tools() -> dict:
    return {
        "tools": list(TOOL_MATRIX),
        "recommended_pairing": "OTel export + offline golden CI (this repo) + optional Langfuse/LangSmith for dev traces",
        "reference_doc": "observability-tools.md",
    }
