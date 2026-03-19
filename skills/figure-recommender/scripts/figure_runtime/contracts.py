from __future__ import annotations

from typing import Any

from .errors import FigureContractError


DEFAULT_BRIEF_ID = "figure-brief"
DEFAULT_FIGURE_ROLE = "paper-main"
DEFAULT_STYLE_MODE = "readable"
DEFAULT_PALETTE_MODE = "auto"

ALLOWED_FIGURE_ROLES = {
    "paper-main",
    "supplement",
    "slides",
}

ALLOWED_STYLE_MODES = {
    "readable",
    "dense",
    "style-forward",
}

FIELD_ALIASES: dict[str, list[str]] = {
    "category": ["category", "group", "parent"],
    "subgroup": ["subgroup", "child"],
    "value": ["value", "fraction", "score"],
    "x": ["x", "timepoint", "pseudotime"],
    "y": ["y", "value", "signal", "auc", "latency"],
    "series": ["series", "gene", "method"],
    "row": ["row", "gene"],
    "column": ["column", "sample"],
    "label": ["label", "method"],
    "source": ["source", "sender", "feature_a"],
    "target": ["target", "receiver", "feature_b"],
    "weight": ["weight", "interaction_score", "correlation"],
    "significance": ["significance", "p_value"],
    "x_error": ["x_error", "accuracy_std"],
    "y_error": ["y_error", "latency_std"],
}


def ensure_brief_object(raw_brief: Any) -> dict[str, Any]:
    if isinstance(raw_brief, list):
        raise FigureContractError("Input file must contain a single brief object, not an array.")
    if not isinstance(raw_brief, dict):
        raise FigureContractError("Figure input must be a JSON object.")
    return raw_brief


def normalize_brief(raw_brief: dict[str, Any]) -> dict[str, Any]:
    brief = dict(raw_brief)

    if "story_goal" not in brief:
        raise FigureContractError("Missing required figure_brief field: story_goal")
    if "field_mapping" not in brief:
        raise FigureContractError("Missing required figure_brief field: field_mapping")
    if not isinstance(brief["field_mapping"], dict) or not brief["field_mapping"]:
        raise FigureContractError("figure_brief.field_mapping must be a non-empty object.")

    brief.setdefault("id", DEFAULT_BRIEF_ID)
    brief.setdefault("figure_role", DEFAULT_FIGURE_ROLE)
    brief.setdefault("style_mode", DEFAULT_STYLE_MODE)
    brief.setdefault("palette_mode", DEFAULT_PALETTE_MODE)

    if "data_shape" not in brief:
        raise FigureContractError("Missing required figure_brief field: data_shape")

    candidate_chart_types = brief.get("candidate_chart_types")
    if candidate_chart_types is None:
        brief["candidate_chart_types"] = []
    elif not isinstance(candidate_chart_types, list):
        raise FigureContractError("figure_brief.candidate_chart_types must be an array when provided.")

    return brief


def resolve_field_name(field_mapping: dict[str, str], field_name: str) -> str | None:
    for alias in FIELD_ALIASES.get(field_name, [field_name]):
        if alias in field_mapping:
            return field_mapping[alias]
    return None

