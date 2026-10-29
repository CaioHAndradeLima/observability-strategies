import argparse
import json
import platform
import sys
from pathlib import Path

from .data import load_golden, validate_golden
from .evaluation import evaluate
from .full_evaluation import run_full_evaluation
from .measure_profiles import evaluate_gates, load_measure_profiles
from .measurement_pipeline import run_measurement_pipeline
from .pipeline_evaluation import run_observability_pipeline_eval
from .scenario_evaluation import (
    evaluate_canary_scenario,
    evaluate_incident_scenarios,
    evaluate_poor_retrieval_scenarios,
)
from .strategies import select_strategies

ROOT = Path(__file__).resolve().parents[2]
PROFILES_PATH = ROOT / "config" / "measure_profiles.json"


def _resolve_profile(name: str):
    profiles = load_measure_profiles(PROFILES_PATH)
    if name not in profiles:
        raise SystemExit(f"Unknown profile '{name}'. Choose from: {', '.join(sorted(profiles))}")
    return profiles[name]


def _environment_note() -> dict:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "note": "Synthetic regression fixtures; metrics score offline eval logic, not live production traffic.",
    }


def _run_evaluate(args: argparse.Namespace) -> dict:
    cases = load_golden(Path(args.golden))
    validate_golden(cases)
    strategies = select_strategies([s.strip() for s in args.strategies.split(",") if s.strip()] or None)
    report = evaluate(cases, strategies=strategies)
    report["environment"] = _environment_note()
    return report


def _run_evaluate_scenarios(args: argparse.Namespace) -> dict:
    cases = load_golden(Path(args.golden))
    validate_golden(cases)
    return {
        "poor_retrieval": evaluate_poor_retrieval_scenarios(cases),
        "incident": evaluate_incident_scenarios(ROOT),
        "canary": evaluate_canary_scenario(ROOT, cases),
        "environment": _environment_note(),
    }


def _run_measure(args: argparse.Namespace) -> dict:
    cases = load_golden(Path(args.golden))
    validate_golden(cases)
    profile = _resolve_profile(args.profile) if args.profile else None
    strategies = select_strategies(list(profile.strategies) if profile else None)
    report = run_measurement_pipeline(cases, strategies=strategies)
    if profile:
        report["profile"] = {"name": profile.name, "description": profile.description}
    report["environment"] = _environment_note()
    return report


def _run_evaluate_pipeline(args: argparse.Namespace) -> dict:
    if not args.profile:
        raise SystemExit("evaluate-pipeline requires --profile (e.g. ci-observability-eval)")
    profile = _resolve_profile(args.profile)
    report = run_observability_pipeline_eval(ROOT, profile)
    report["environment"] = _environment_note()
    return report


def _run_check_measure(args: argparse.Namespace) -> dict:
    if not args.report or not args.profile:
        raise SystemExit("check-measure requires --profile and --report")
    report = json.loads(Path(args.report).read_text())
    profile = _resolve_profile(args.profile)
    return evaluate_gates(report, profile)


def main() -> None:
    parser = argparse.ArgumentParser(description="Observability and offline evaluation reference CLI")
    parser.add_argument(
        "command",
        choices=[
            "evaluate",
            "evaluate-scenarios",
            "evaluate-full",
            "evaluate-pipeline",
            "measure",
            "check-measure",
        ],
    )
    parser.add_argument("--golden", default=str(ROOT / "data/golden.json"))
    parser.add_argument("--output", default="")
    parser.add_argument("--strategies", default="", help="Comma-separated strategy names for evaluate/measure")
    parser.add_argument("--profile", default="", help="Measure profile from config/measure_profiles.json")
    parser.add_argument("--report", default="", help="JSON report for check-measure")
    args = parser.parse_args()

    if args.command == "evaluate":
        report = _run_evaluate(args)
    elif args.command == "evaluate-scenarios":
        report = _run_evaluate_scenarios(args)
    elif args.command == "measure":
        report = _run_measure(args)
    elif args.command == "evaluate-full":
        report = run_full_evaluation(ROOT)
        report["environment"] = _environment_note()
    elif args.command == "evaluate-pipeline":
        report = _run_evaluate_pipeline(args)
    elif args.command == "check-measure":
        report = _run_check_measure(args)
    else:
        raise SystemExit(f"unknown command {args.command}")

    text = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n")
    else:
        print(text)

    if args.command == "check-measure" and not report.get("passed", True):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
