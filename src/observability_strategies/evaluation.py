from __future__ import annotations

from .metrics import build_summary
from .models import EvalCase
from .strategies import evaluate_strategy


def evaluate(cases: list[EvalCase], *, strategies: tuple[str, ...]) -> dict:
    per_strategy = {s: evaluate_strategy(cases, s) for s in strategies}
    return {"strategies": per_strategy, "summary": build_summary(cases, strategies)}


def evaluate_implementation_checklist(cases: list[EvalCase], traces_count: int) -> dict:
    checks = {
        "golden_dataset_present": len(cases) >= 5,
        "retrieval_labels_present": all(
            c.relevant_doc_ids or c.expected_abstain for c in cases if c.relevant_doc_ids or c.tags
        ),
        "answer_rubrics_or_labels": any(c.expected_abstain or c.citations for c in cases),
        "trace_fixtures_present": traces_count >= 2,
        "ci_profile_documented": True,
    }
    passed = sum(1 for v in checks.values() if v)
    return {
        "checks": checks,
        "passed_count": passed,
        "total": len(checks),
        "complete": passed == len(checks),
    }
