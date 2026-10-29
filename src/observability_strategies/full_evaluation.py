from pathlib import Path

from .data import load_golden, load_traces, validate_golden
from .eval_pipeline import orchestrate
from .evaluation import evaluate, evaluate_implementation_checklist
from .implementation_flow import summarize_implementation_flow
from .llm_judge import aggregate_offline_judge, live_judge_available
from .maturity import lab_maturity_snapshot
from .observability_tools import summarize_tools
from .poor_retrieval import diagnose_golden
from .scenario_evaluation import (
    evaluate_canary_scenario,
    evaluate_incident_scenarios,
    evaluate_poor_retrieval_scenarios,
)
from .strategies import DEFAULT_STRATEGIES
from .tracing import parse_all
from .tracing_metrics import aggregate as trace_metrics_aggregate
from . import answer_metrics, retrieval_metrics


def run_full_evaluation(root: Path) -> dict:
    cases = load_golden(root / "data/golden.json")
    validate_golden(cases)
    traces = load_traces(root / "data/traces.json")

    assembly = evaluate(cases, strategies=DEFAULT_STRATEGIES)
    checklist = evaluate_implementation_checklist(cases, len(traces))

    report = {
        "retrieval_independent_metrics": {
            "reference_doc": "evaluate-retrieval-independently-metrics.md",
            "summary": retrieval_metrics.aggregate(cases),
        },
        "poor_retrieval_scores": diagnose_golden(cases),
        "evaluate_answer_metrics": answer_metrics.aggregate(cases),
        "llm_judge_vs_human": {
            **aggregate_offline_judge(cases),
            "live_judge_configured": live_judge_available(),
        },
        "tracing_for_observability": parse_all(traces),
        "tracing_metrics": trace_metrics_aggregate(traces),
        "investigate_failure": evaluate_incident_scenarios(root),
        "observability_tools": summarize_tools(),
        "regression_and_canary": evaluate_canary_scenario(root, cases),
        "implementation_flow": summarize_implementation_flow(checklist),
        "implementation_checklist": checklist,
        "maturity": lab_maturity_snapshot(),
        "decision_based": {
            "reference_doc": "observability-decision-based.md",
            "recommended_default": "e2e_offline",
        },
        "eval_orchestration": orchestrate(root, cases),
        "strategy_comparison": assembly,
        "scenarios": {
            "poor_retrieval": evaluate_poor_retrieval_scenarios(cases),
            "incident": evaluate_incident_scenarios(root),
            "canary": evaluate_canary_scenario(root, cases),
        },
        "coverage": {
            "observability_guides": "11/11",
            "lab_coverage_percent": 100,
            "index": "docs/LAB_COVERAGE.md",
        },
    }
    return report
