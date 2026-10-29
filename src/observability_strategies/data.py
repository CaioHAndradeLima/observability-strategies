from __future__ import annotations

import json
from pathlib import Path

from .models import EvalCase, RunFixture, SpanNode, TraceFixture


def _tuple_ids(raw: list | None) -> tuple[str, ...]:
    return tuple(raw or [])


def load_golden(path: Path) -> list[EvalCase]:
    payload = json.loads(path.read_text())
    cases = []
    for row in payload.get("cases", []):
        cases.append(
            EvalCase(
                id=row["id"],
                query=row["query"],
                retrieved_doc_ids=_tuple_ids(row.get("retrieved_doc_ids")),
                relevant_doc_ids=_tuple_ids(row.get("relevant_doc_ids")),
                answer_text=row.get("answer_text", ""),
                citations=_tuple_ids(row.get("citations")),
                expected_abstain=bool(row.get("expected_abstain", False)),
                expected_grounded=bool(row.get("expected_grounded", True)),
                expected_output_valid=row.get("expected_output_valid"),
                tags=tuple(row.get("tags", [])),
                rubric_pass_threshold=float(row.get("rubric_pass_threshold", 0.7)),
                rubric_scores=dict(row.get("rubric_scores", {})),
            )
        )
    return cases


def load_traces(path: Path) -> list[TraceFixture]:
    payload = json.loads(path.read_text())
    traces = []
    for row in payload.get("traces", []):
        spans = tuple(
            SpanNode(
                span_id=s["span_id"],
                name=s["name"],
                parent_id=s.get("parent_id"),
                start_ms=float(s["start_ms"]),
                end_ms=float(s["end_ms"]),
                attributes=dict(s.get("attributes", {})),
            )
            for s in row.get("spans", [])
        )
        traces.append(
            TraceFixture(
                trace_id=row["trace_id"],
                spans=spans,
                expected_failure_layer=row.get("expected_failure_layer"),
                tags=tuple(row.get("tags", [])),
            )
        )
    return traces


def load_runs(path: Path) -> list[RunFixture]:
    payload = json.loads(path.read_text())
    runs = []
    for row in payload.get("runs", []):
        runs.append(
            RunFixture(
                case_id=row["case_id"],
                strategy=row.get("strategy", "e2e_offline"),
                retrieved_doc_ids=_tuple_ids(row.get("retrieved_doc_ids")),
                answer_text=row.get("answer_text", ""),
                citations=_tuple_ids(row.get("citations")),
                output_valid=bool(row.get("output_valid", True)),
                trace_id=row.get("trace_id"),
            )
        )
    return runs


def load_incident_scenarios(path: Path) -> list[TraceFixture]:
    return load_traces(path)


def load_canary_baselines(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_golden(cases: list[EvalCase]) -> None:
    if not cases:
        raise ValueError("golden set is empty")
    ids = [c.id for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case ids in golden set")
