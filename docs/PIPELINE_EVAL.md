# Observability pipeline evaluation (`evaluate-pipeline`)

`evaluate-pipeline --profile ci-observability-eval` produces a **three-layer scorecard** on bundled fixtures:

1. **Core quality** (`scorecard.core_quality`) — retrieval Recall@K, nDCG@K, labeled hit rate, answer groundedness, citation alignment, abstain correctness.
2. **Scenarios** (`scenarios`) — poor-retrieval branch hints, incident layer match from fixture traces, canary baseline comparison.
3. **Optional live judges** — not run in this command; extend `llm_judge.py` when `OPENAI_API_KEY` or `CURSOR_API_KEY` is set (CI stays offline).

## Scorecard fields

| Field | Meaning |
| --- | --- |
| `recall_at_k` | Fraction of labeled relevant docs found in top-K |
| `ndcg_at_k` | Rank-sensitive retrieval quality at K |
| `labeled_hit_rate` | Query has at least one relevant doc in retrieved set |
| `groundedness_rate` | Answers match abstain/grounding expectations on golden rows |
| `citation_alignment_rate` | Citation IDs ⊆ retrieved doc IDs |
| `abstain_correct_rate` | Abstain vs answer decision matches label |

Trace rollups (`trace_rollups`) add mean latency, token, and cost aggregates from fixture spans ([tracing-for-observability-metrics.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/tracing-for-observability-metrics.md)).

## Scenario gates (`ci-observability-eval`)

| Gate | Source |
| --- | --- |
| `min_layer_match_rate` | `scenarios.incident.layer_match_rate` |
| `min_canary_pass` | `scenarios.canary.passed` |

Thresholds live in [config/measure_profiles.json](../config/measure_profiles.json).

## Related docs

- [evaluate-retrieval-independently-metrics.md](https://github.com/CaioHAndradeLima/AI-System-Architecturing-Engineering/blob/main/observability-evaluation/evaluate-retrieval-independently-metrics.md)
- [LAB_COVERAGE.md](./LAB_COVERAGE.md)
