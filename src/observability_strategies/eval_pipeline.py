"""Ingest fixture runs and score retrieval, answer, output, cost/latency aggregates."""

from __future__ import annotations

from . import answer_metrics, retrieval_metrics, tracing_metrics
from pathlib import Path

from .data import load_runs, load_traces
from .models import EvalCase, RunFixture


def score_run(case: EvalCase, run: RunFixture) -> dict:
    merged = EvalCase(
        id=case.id,
        query=case.query,
        retrieved_doc_ids=run.retrieved_doc_ids,
        relevant_doc_ids=case.relevant_doc_ids,
        answer_text=run.answer_text,
        citations=run.citations,
        expected_abstain=case.expected_abstain,
        expected_grounded=case.expected_grounded,
        expected_output_valid=case.expected_output_valid,
        tags=case.tags,
        rubric_pass_threshold=case.rubric_pass_threshold,
        rubric_scores=case.rubric_scores,
    )
    retrieval = retrieval_metrics.score_case(merged)
    answer = answer_metrics.score_case(merged)
    output_ok = run.output_valid if case.expected_output_valid is None else run.output_valid == case.expected_output_valid
    return {
        "case_id": case.id,
        "strategy": run.strategy,
        "retrieval": retrieval,
        "answer": answer,
        "output_valid_match": output_ok,
    }


def orchestrate(root: Path, cases: list[EvalCase]) -> dict:
    runs = load_runs(root / "data/runs.json")
    traces = load_traces(root / "data/traces.json")
    by_id = {c.id: c for c in cases}
    run_rows = []
    for run in runs:
        case = by_id.get(run.case_id)
        if case:
            run_rows.append(score_run(case, run))
    trace_rollups = tracing_metrics.aggregate(traces)
    return {
        "run_scores": run_rows,
        "trace_rollups": trace_rollups,
        "run_count": len(run_rows),
    }
