def lab_maturity_snapshot() -> dict:
    return {
        "stage": "reference_regression_corpus",
        "capabilities": {
            "offline_golden_eval": True,
            "fixture_traces": True,
            "ci_observability_eval_profile": True,
            "live_langsmith_tenant": False,
            "otel_collector_deploy": False,
            "production_warehouse": False,
        },
        "production_deployment_only": [
            "Live LangSmith/Langfuse tenants and retention policies",
            "Full OpenTelemetry collector + backend deploy",
            "Production metrics warehouse and PII scrubbing pipelines",
            "Human review queues for judge calibration",
        ],
        "reference_doc": "observability-decision-based.md",
    }
