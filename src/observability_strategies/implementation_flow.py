def summarize_implementation_flow(checklist: dict) -> dict:
    return {
        "stages": [
            "golden_queries_and_labels",
            "retrieval_only_benchmark",
            "answer_and_output_metrics",
            "trace_attributes_and_rollups",
            "incident_investigation_playbook",
            "regression_and_canary_gates",
        ],
        "checklist_complete": checklist.get("complete", False),
        "reference_doc": "observability-implementation-flow.md",
    }
