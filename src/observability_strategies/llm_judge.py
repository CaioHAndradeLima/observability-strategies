"""Rubric scoring and optional live judge adapter (skipped in CI without keys)."""

from __future__ import annotations

import os

from .models import EvalCase

RUBRIC_DIMENSIONS = ("faithfulness", "completeness", "style")


def offline_rubric_score(case: EvalCase) -> dict:
    scores = case.rubric_scores or {}
    if not scores:
        scores = {d: 0.85 if case.expected_grounded and not case.expected_abstain else 0.4 for d in RUBRIC_DIMENSIONS}
    dim_vals = [float(scores.get(d, 0.0)) for d in RUBRIC_DIMENSIONS]
    mean = sum(dim_vals) / len(dim_vals)
    return {
        "case_id": case.id,
        "dimensions": {d: scores.get(d, dim_vals[i]) for i, d in enumerate(RUBRIC_DIMENSIONS)},
        "mean_score": mean,
        "passes_threshold": mean >= case.rubric_pass_threshold,
        "mode": "offline_rubric",
    }


def aggregate_offline_judge(cases: list[EvalCase]) -> dict:
    if not cases:
        return {"count": 0, "judge_pass_rate": 0.0}
    rows = [offline_rubric_score(c) for c in cases]
    n = len(rows)
    return {
        "count": n,
        "judge_pass_rate": sum(1 for r in rows if r["passes_threshold"]) / n,
        "cases": rows,
        "reference_doc": "llm-as-judge-vs-human.md",
    }


def live_judge_available() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("CURSOR_API_KEY"))


def run_live_judge_if_configured(case: EvalCase) -> dict | None:
    if not live_judge_available():
        return None
    # Optional path documented for adopters; CI remains offline-only.
    return {
        "case_id": case.id,
        "mode": "live_skipped_in_reference",
        "note": "Set OPENAI_API_KEY and extend llm_judge.run_live_judge for production.",
    }
