"""Decision branches when independent retrieval metrics are weak."""

from __future__ import annotations

from .retrieval_metrics import aggregate, score_case


def next_fix_branch(metrics: dict) -> str:
    recall = metrics.get("recall_at_k", 0.0)
    ndcg = metrics.get("ndcg_at_k", 0.0)
    hit = metrics.get("labeled_hit_rate", 0.0)
    if hit == 0:
        return "index_or_filter_miss"
    if recall < 0.5:
        return "chunking_or_embedding_recall"
    if ndcg < 0.6:
        return "rerank_or_fusion_ordering"
    if recall < 0.8:
        return "increase_top_k_or_hybrid"
    return "retrieval_ok_investigate_downstream"


def diagnose_case(case_metrics: dict) -> dict:
    branch = next_fix_branch(case_metrics)
    return {"case_id": case_metrics["case_id"], "recommended_next_step": branch}


def diagnose_golden(cases, *, k: int = 5) -> dict:
    summary = aggregate(cases, k=k)
    per_case = [diagnose_case(score_case(c, k=k)) for c in cases]
    return {
        "summary_branch": next_fix_branch(summary),
        "aggregate": summary,
        "per_case": per_case,
        "reference_doc": "poor-retrieval-scores.md",
    }
