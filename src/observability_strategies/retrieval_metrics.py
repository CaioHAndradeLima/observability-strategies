"""Independent retrieval metrics on golden query → relevant doc IDs."""

from __future__ import annotations

import math

from .models import EvalCase


def recall_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    if not relevant:
        return 1.0
    top = retrieved[:k]
    hits = len(relevant.intersection(top))
    return hits / len(relevant)


def dcg_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    score = 0.0
    for i, doc_id in enumerate(retrieved[:k]):
        if doc_id in relevant:
            score += 1.0 / math.log2(i + 2)
    return score


def ndcg_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    ideal = dcg_at_k(relevant, list(relevant), min(k, len(relevant) or 1))
    if ideal == 0:
        return 1.0 if not relevant else 0.0
    return dcg_at_k(relevant, retrieved, k) / ideal


def labeled_hit_rate(relevant: set[str], retrieved: list[str]) -> float:
    if not relevant:
        return 1.0
    return 1.0 if relevant.intersection(retrieved) else 0.0


def score_case(case: EvalCase, *, k: int = 5) -> dict:
    relevant = set(case.relevant_doc_ids)
    retrieved = list(case.retrieved_doc_ids)
    return {
        "case_id": case.id,
        "recall_at_k": recall_at_k(relevant, retrieved, k),
        "ndcg_at_k": ndcg_at_k(relevant, retrieved, k),
        "labeled_hit_rate": labeled_hit_rate(relevant, retrieved),
    }


def aggregate(cases: list[EvalCase], *, k: int = 5) -> dict:
    if not cases:
        return {"count": 0, "recall_at_k": 0.0, "ndcg_at_k": 0.0, "labeled_hit_rate": 0.0}
    rows = [score_case(c, k=k) for c in cases]
    n = len(rows)
    return {
        "count": n,
        "k": k,
        "recall_at_k": sum(r["recall_at_k"] for r in rows) / n,
        "ndcg_at_k": sum(r["ndcg_at_k"] for r in rows) / n,
        "labeled_hit_rate": sum(r["labeled_hit_rate"] for r in rows) / n,
        "cases": rows,
    }
