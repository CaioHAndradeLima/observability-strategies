from __future__ import annotations

from pathlib import Path

from .data import load_canary_baselines, load_incident_scenarios
from .failure_investigation import evaluate_incidents
from .metrics import strategy_summary
from .models import EvalCase
from .poor_retrieval import diagnose_golden
from .regression_canary import evaluate_canary_fixtures


def evaluate_poor_retrieval_scenarios(cases: list[EvalCase]) -> dict:
    poor_cases = [c for c in cases if c.tags and "poor_retrieval" in c.tags]
    target = poor_cases if poor_cases else cases[:2]
    return diagnose_golden(target)


def evaluate_incident_scenarios(root: Path) -> dict:
    traces = load_incident_scenarios(root / "data/incident_scenarios.json")
    return evaluate_incidents(traces)


def evaluate_canary_scenario(root: Path, cases: list[EvalCase]) -> dict:
    payload = load_canary_baselines(root / "data/canary_baselines.json")
    candidate = strategy_summary(cases, "e2e_offline")
    return evaluate_canary_fixtures(payload, candidate)
