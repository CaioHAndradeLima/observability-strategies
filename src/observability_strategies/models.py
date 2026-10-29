from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvalCase:
    id: str
    query: str
    retrieved_doc_ids: tuple[str, ...]
    relevant_doc_ids: tuple[str, ...]
    answer_text: str = ""
    citations: tuple[str, ...] = ()
    expected_abstain: bool = False
    expected_grounded: bool = True
    expected_output_valid: bool | None = None
    tags: tuple[str, ...] = ()
    rubric_pass_threshold: float = 0.7
    rubric_scores: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class SpanNode:
    span_id: str
    name: str
    parent_id: str | None
    start_ms: float
    end_ms: float
    attributes: dict = field(default_factory=dict)


@dataclass(frozen=True)
class TraceFixture:
    trace_id: str
    spans: tuple[SpanNode, ...]
    expected_failure_layer: str | None = None
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunFixture:
    case_id: str
    strategy: str
    retrieved_doc_ids: tuple[str, ...]
    answer_text: str
    citations: tuple[str, ...] = ()
    output_valid: bool = True
    trace_id: str | None = None


@dataclass
class LayerDiagnosis:
    hypothesized_layer: str
    confidence: float
    span_path: list[str]
    notes: str = ""
