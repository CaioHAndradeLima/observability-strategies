"""Baseline vs candidate metric bundle for regression and canary gates."""

from __future__ import annotations


def _delta(candidate: float, baseline: float) -> float:
    return round(candidate - baseline, 6)


def compare_metric_bundles(baseline: dict, candidate: dict, *, tolerances: dict | None = None) -> dict:
    tolerances = tolerances or {}
    regressions: list[str] = []
    checks: list[dict] = []
    for key, base_val in baseline.items():
        if not isinstance(base_val, (int, float)):
            continue
        cand_val = float(candidate.get(key, 0.0))
        tol = float(tolerances.get(key, 0.0))
        min_allowed = base_val - tol
        ok = cand_val >= min_allowed
        checks.append(
            {
                "metric": key,
                "baseline": base_val,
                "candidate": cand_val,
                "delta": _delta(cand_val, base_val),
                "min_allowed": min_allowed,
                "passed": ok,
            }
        )
        if not ok:
            regressions.append(f"{key} regressed: {cand_val:.4f} < {min_allowed:.4f}")
    return {
        "passed": not regressions,
        "regressions": regressions,
        "checks": checks,
        "reference_doc": "regression-and-canary-releases.md",
    }


def evaluate_canary_fixtures(payload: dict, candidate: dict) -> dict:
    baseline = payload.get("baseline_metrics", {})
    tolerances = payload.get("tolerances", {})
    result = compare_metric_bundles(baseline, candidate, tolerances=tolerances)
    result["canary_id"] = payload.get("canary_id", "default")
    return result
