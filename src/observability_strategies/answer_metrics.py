"""Answer quality: groundedness, abstain alignment, citation overlap."""

from __future__ import annotations

from .models import EvalCase


def _is_abstain_text(text: str) -> bool:
    lowered = text.lower()
    markers = (
        "don't know",
        "do not know",
        "cannot answer",
        "insufficient",
        "not enough information",
        "do not have enough information",
    )
    return any(m in lowered for m in markers) or not text.strip()


def citation_in_retrieved(case: EvalCase) -> bool:
    if not case.citations:
        return True
    retrieved = set(case.retrieved_doc_ids)
    return all(c in retrieved for c in case.citations)


def groundedness_heuristic(case: EvalCase) -> bool:
    if case.expected_abstain:
        return _is_abstain_text(case.answer_text)
    if not case.answer_text.strip():
        return False
    if not citation_in_retrieved(case):
        return False
    return case.expected_grounded


def score_case(case: EvalCase) -> dict:
    abstain_pred = _is_abstain_text(case.answer_text)
    grounded = groundedness_heuristic(case)
    cite_ok = citation_in_retrieved(case)
    abstain_ok = abstain_pred == case.expected_abstain
    return {
        "case_id": case.id,
        "groundedness": grounded,
        "citation_in_retrieved": cite_ok,
        "abstain_correct": abstain_ok,
        "expected_abstain": case.expected_abstain,
    }


def aggregate(cases: list[EvalCase]) -> dict:
    if not cases:
        return {
            "count": 0,
            "groundedness_rate": 0.0,
            "citation_alignment_rate": 0.0,
            "abstain_correct_rate": 0.0,
        }
    rows = [score_case(c) for c in cases]
    n = len(rows)
    return {
        "count": n,
        "groundedness_rate": sum(1 for r in rows if r["groundedness"]) / n,
        "citation_alignment_rate": sum(1 for r in rows if r["citation_in_retrieved"]) / n,
        "abstain_correct_rate": sum(1 for r in rows if r["abstain_correct"]) / n,
        "cases": rows,
        "reference_doc": "evaluate-answer-metrics.md",
    }
