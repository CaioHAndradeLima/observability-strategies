"""Observability pipeline scorecard: core quality + scenario fixtures."""

from pathlib import Path

from .data import load_golden, load_traces, validate_golden
from .eval_pipeline import orchestrate
from .measure_profiles import MeasureProfile
from .measurement_pipeline import run_measurement_pipeline
from .scenario_evaluation import (
    evaluate_canary_scenario,
    evaluate_incident_scenarios,
    evaluate_poor_retrieval_scenarios,
)
from .tracing_metrics import aggregate as trace_metrics_aggregate


def build_scorecard(measure_report: dict, *, primary_strategy: str = "e2e_offline") -> dict:
    core = measure_report.get("summary", {}).get(primary_strategy, {})
    return {
        "primary_strategy": primary_strategy,
        "core_quality": {
            "recall_at_k": core.get("recall_at_k"),
            "ndcg_at_k": core.get("ndcg_at_k"),
            "labeled_hit_rate": core.get("labeled_hit_rate"),
            "groundedness_rate": core.get("groundedness_rate"),
            "citation_alignment_rate": core.get("citation_alignment_rate"),
            "abstain_correct_rate": core.get("abstain_correct_rate"),
        },
        "reference_doc": "evaluate-retrieval-independently-metrics.md",
    }


def run_observability_pipeline_eval(root: Path, profile: MeasureProfile) -> dict:
    cases = load_golden(root / "data/golden.json")
    validate_golden(cases)
    traces = load_traces(root / "data/traces.json")

    strategies = profile.strategies
    measure_report = run_measurement_pipeline(cases, strategies=strategies)
    primary = strategies[0] if strategies else "e2e_offline"
    scorecard = build_scorecard(measure_report, primary_strategy=primary)
    orchestration = orchestrate(root, cases)
    trace_rollups = trace_metrics_aggregate(traces)

    return {
        **measure_report,
        "eval_type": "observability_pipeline",
        "profile": {"name": profile.name, "description": profile.description},
        "scorecard": scorecard,
        "trace_rollups": trace_rollups,
        "eval_orchestration": orchestration,
        "scenarios": {
            "poor_retrieval": evaluate_poor_retrieval_scenarios(cases),
            "incident": evaluate_incident_scenarios(root),
            "canary": evaluate_canary_scenario(root, cases),
        },
    }
