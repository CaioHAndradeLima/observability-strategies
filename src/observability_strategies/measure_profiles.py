import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StrategyGate:
    min_recall_at_k: float | None = None
    min_ndcg_at_k: float | None = None
    min_labeled_hit_rate: float | None = None
    min_groundedness_rate: float | None = None
    min_citation_alignment_rate: float | None = None
    min_abstain_correct_rate: float | None = None
    min_judge_pass_rate: float | None = None
    max_mean_latency_ms: float | None = None


@dataclass(frozen=True)
class ScenarioGates:
    min_layer_match_rate: float | None = None
    min_canary_pass: float | None = None
    min_poor_retrieval_branch_rate: float | None = None


@dataclass(frozen=True)
class MeasureProfile:
    name: str
    description: str
    strategies: tuple[str, ...]
    gates: dict[str, StrategyGate]
    scenario_gates: ScenarioGates | None = None


def load_measure_profiles(path: Path) -> dict[str, MeasureProfile]:
    payload = json.loads(path.read_text())
    profiles = {}
    for name, row in payload.get("profiles", {}).items():
        gates = {}
        for strategy, gate_row in row.get("gates", {}).items():
            gates[strategy] = StrategyGate(
                min_recall_at_k=gate_row.get("min_recall_at_k"),
                min_ndcg_at_k=gate_row.get("min_ndcg_at_k"),
                min_labeled_hit_rate=gate_row.get("min_labeled_hit_rate"),
                min_groundedness_rate=gate_row.get("min_groundedness_rate"),
                min_citation_alignment_rate=gate_row.get("min_citation_alignment_rate"),
                min_abstain_correct_rate=gate_row.get("min_abstain_correct_rate"),
                min_judge_pass_rate=gate_row.get("min_judge_pass_rate"),
                max_mean_latency_ms=gate_row.get("max_mean_latency_ms"),
            )
        scenario_row = row.get("scenario_gates") or {}
        scenario_gates = ScenarioGates(
            min_layer_match_rate=scenario_row.get("min_layer_match_rate"),
            min_canary_pass=scenario_row.get("min_canary_pass"),
            min_poor_retrieval_branch_rate=scenario_row.get("min_poor_retrieval_branch_rate"),
        )
        if not any(
            v is not None
            for v in (
                scenario_gates.min_layer_match_rate,
                scenario_gates.min_canary_pass,
                scenario_gates.min_poor_retrieval_branch_rate,
            )
        ):
            scenario_gates = None
        profiles[name] = MeasureProfile(
            name=name,
            description=row.get("description", ""),
            strategies=tuple(row.get("strategies", ["e2e_offline"])),
            gates=gates,
            scenario_gates=scenario_gates,
        )
    return profiles


def _check_min(values: dict, key: str, expected_min: float, strategy: str, failures: list, checks: list) -> None:
    actual = values.get(key, 0)
    ok = actual >= expected_min
    checks.append({"strategy": strategy, "metric": key, "expected_min": expected_min, "actual": actual, "passed": ok})
    if not ok:
        failures.append(f"{strategy} {key} {actual:.3f} < {expected_min}")


def _check_max(values: dict, key: str, expected_max: float, strategy: str, failures: list, checks: list) -> None:
    actual = values.get(key, 0)
    ok = actual <= expected_max
    checks.append({"strategy": strategy, "metric": key, "expected_max": expected_max, "actual": actual, "passed": ok})
    if not ok:
        failures.append(f"{strategy} {key} {actual:.3f} > {expected_max}")


def evaluate_gates(report: dict, profile: MeasureProfile) -> dict:
    summary = report.get("summary", {})
    failures: list[str] = []
    checks: list[dict] = []

    for strategy, gate in profile.gates.items():
        values = summary.get(strategy)
        if values is None and report.get("scorecard"):
            sc = report["scorecard"].get("core_quality", {})
            if strategy == report.get("scorecard", {}).get("primary_strategy"):
                values = sc
        if values is None:
            failures.append(f"missing strategy summary '{strategy}'")
            continue
        if gate.min_recall_at_k is not None:
            _check_min(values, "recall_at_k", gate.min_recall_at_k, strategy, failures, checks)
        if gate.min_ndcg_at_k is not None:
            _check_min(values, "ndcg_at_k", gate.min_ndcg_at_k, strategy, failures, checks)
        if gate.min_labeled_hit_rate is not None:
            _check_min(values, "labeled_hit_rate", gate.min_labeled_hit_rate, strategy, failures, checks)
        if gate.min_groundedness_rate is not None:
            _check_min(values, "groundedness_rate", gate.min_groundedness_rate, strategy, failures, checks)
        if gate.min_citation_alignment_rate is not None:
            _check_min(values, "citation_alignment_rate", gate.min_citation_alignment_rate, strategy, failures, checks)
        if gate.min_abstain_correct_rate is not None:
            _check_min(values, "abstain_correct_rate", gate.min_abstain_correct_rate, strategy, failures, checks)
        if gate.min_judge_pass_rate is not None:
            _check_min(values, "judge_pass_rate", gate.min_judge_pass_rate, strategy, failures, checks)
        if gate.max_mean_latency_ms is not None:
            lat = report.get("trace_rollups", {}).get("mean_latency_ms", 0)
            _check_max({"mean_latency_ms": lat}, "mean_latency_ms", gate.max_mean_latency_ms, strategy, failures, checks)

    if profile.scenario_gates is not None:
        scenarios = report.get("scenarios", {})
        sg = profile.scenario_gates
        if sg.min_layer_match_rate is not None:
            actual = scenarios.get("incident", {}).get("layer_match_rate")
            if actual is None:
                failures.append("missing scenarios.incident")
            else:
                ok = actual >= sg.min_layer_match_rate
                checks.append(
                    {
                        "scope": "scenarios.incident",
                        "metric": "layer_match_rate",
                        "expected_min": sg.min_layer_match_rate,
                        "actual": actual,
                        "passed": ok,
                    }
                )
                if not ok:
                    failures.append(f"layer_match_rate {actual:.3f} < {sg.min_layer_match_rate}")
        if sg.min_canary_pass is not None:
            actual = 1.0 if scenarios.get("canary", {}).get("passed") else 0.0
            ok = actual >= sg.min_canary_pass
            checks.append(
                {
                    "scope": "scenarios.canary",
                    "metric": "canary_pass",
                    "expected_min": sg.min_canary_pass,
                    "actual": actual,
                    "passed": ok,
                }
            )
            if not ok:
                failures.append("canary regression gate failed")

    return {"profile": profile.name, "passed": not failures, "failures": failures, "checks": checks}
