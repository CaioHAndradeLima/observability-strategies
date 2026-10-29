from __future__ import annotations

from . import answer_metrics, llm_judge, retrieval_metrics
from .models import EvalCase

STRATEGY_NAMES = ("retrieval_only", "e2e_offline", "judge_augmented")

DEFAULT_STRATEGIES = ("retrieval_only", "e2e_offline", "judge_augmented")


def select_strategies(names: list[str] | None) -> tuple[str, ...]:
    if not names:
        return DEFAULT_STRATEGIES
    out = []
    for n in names:
        if n not in STRATEGY_NAMES:
            raise ValueError(f"unknown strategy {n}")
        out.append(n)
    return tuple(out)


def evaluate_strategy(cases: list[EvalCase], strategy: str) -> dict:
    if strategy == "retrieval_only":
        return {"strategy": strategy, "retrieval": retrieval_metrics.aggregate(cases)}
    if strategy == "e2e_offline":
        return {
            "strategy": strategy,
            "retrieval": retrieval_metrics.aggregate(cases),
            "answer": answer_metrics.aggregate(cases),
        }
    if strategy == "judge_augmented":
        return {
            "strategy": strategy,
            "retrieval": retrieval_metrics.aggregate(cases),
            "answer": answer_metrics.aggregate(cases),
            "judge": llm_judge.aggregate_offline_judge(cases),
        }
    raise ValueError(strategy)
