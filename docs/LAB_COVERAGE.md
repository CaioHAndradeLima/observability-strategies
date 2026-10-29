# Observability docs → reference implementation coverage

Maps each guide under [AI-System-Architecturing-Engineering/observability-evaluation](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/tree/main/observability-evaluation) to code and CLI output.

| Guide | Module / command | `evaluate-full` key |
| --- | --- | --- |
| [evaluate-retrieval-independently-metrics.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/evaluate-retrieval-independently-metrics.md) | `retrieval_metrics.py`, `evaluate` / scorecard | `retrieval_independent_metrics` |
| [poor-retrieval-scores.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/poor-retrieval-scores.md) | `poor_retrieval.py`, `evaluate-scenarios` | `poor_retrieval_scores`, `scenarios.poor_retrieval` |
| [evaluate-answer-metrics.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/evaluate-answer-metrics.md) | `answer_metrics.py` | `evaluate_answer_metrics` |
| [llm-as-judge-vs-human.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/llm-as-judge-vs-human.md) | `llm_judge.py` (offline rubric; optional live when keys set) | `llm_judge_vs_human` |
| [tracing-for-observability.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/tracing-for-observability.md) | `tracing.py`, `data/traces.json` | `tracing_for_observability` |
| [tracing-for-observability-metrics.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/tracing-for-observability-metrics.md) | `tracing_metrics.py` | `tracing_metrics` |
| [investigate-failure-by-observability-data.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/investigate-failure-by-observability-data.md) | `failure_investigation.py`, `data/incident_scenarios.json` | `investigate_failure`, `scenarios.incident` |
| [observability-tools.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/observability-tools.md) | `observability_tools.py` (capability matrix) | `observability_tools` |
| [regression-and-canary-releases.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/regression-and-canary-releases.md) | `regression_canary.py`, `data/canary_baselines.json` | `regression_and_canary`, `scenarios.canary` |
| [observability-implementation-flow.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/observability-implementation-flow.md) | `implementation_flow.py`, `evaluation.evaluate_implementation_checklist` | `implementation_flow`, `implementation_checklist` |
| [observability-decision-based.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/observability-decision-based.md) | `maturity.py` | `maturity`, `decision_based` |

**Coverage:** 11/11 guides — `evaluate-full` → `coverage.lab_coverage_percent` is **100** (regression syllabus; live LangSmith/Langfuse tenants, OTel collector deploy, and production warehouses are listed under `maturity.production_deployment_only`).

Run everything:

```bash
python -m observability_strategies.cli evaluate-full --output reports/full.json
```

Recommended PR gate:

```bash
python -m observability_strategies.cli evaluate-pipeline --profile ci-observability-eval --output reports/pipeline-eval.json
python -m observability_strategies.cli check-measure --profile ci-observability-eval --report reports/pipeline-eval.json
```
