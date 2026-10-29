from __future__ import annotations

from .evaluation import evaluate
from .models import EvalCase


def run_measurement_pipeline(cases: list[EvalCase], *, strategies: tuple[str, ...]) -> dict:
    return evaluate(cases, strategies=strategies)
