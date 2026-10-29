"""Flatten strategy results into gate-friendly summary metrics."""

from __future__ import annotations

from .models import EvalCase
from .strategies import evaluate_strategy


def strategy_summary(cases: list[EvalCase], strategy: str) -> dict:
    result = evaluate_strategy(cases, strategy)
    retrieval = result.get("retrieval", {})
    answer = result.get("answer", {})
    judge = result.get("judge", {})
    return {
        "strategy": strategy,
        "recall_at_k": retrieval.get("recall_at_k", 0.0),
        "ndcg_at_k": retrieval.get("ndcg_at_k", 0.0),
        "labeled_hit_rate": retrieval.get("labeled_hit_rate", 0.0),
        "groundedness_rate": answer.get("groundedness_rate", 0.0),
        "citation_alignment_rate": answer.get("citation_alignment_rate", 0.0),
        "abstain_correct_rate": answer.get("abstain_correct_rate", 0.0),
        "judge_pass_rate": judge.get("judge_pass_rate", 0.0),
    }


def build_summary(cases: list[EvalCase], strategies: tuple[str, ...]) -> dict[str, dict]:
    return {s: strategy_summary(cases, s) for s in strategies}
