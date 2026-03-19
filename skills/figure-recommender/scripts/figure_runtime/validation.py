from __future__ import annotations

from typing import Any

from .contracts import ALLOWED_FIGURE_ROLES, ALLOWED_STYLE_MODES, resolve_field_name
from .errors import FigureContractError


def validate_known_values(
    brief: dict[str, Any],
    *,
    supported_story_goals: set[str],
    known_palettes: set[str],
    known_charts: set[str],
) -> None:
    if brief["story_goal"] not in supported_story_goals:
        raise FigureContractError(
            f"Unknown story_goal '{brief['story_goal']}'. Allowed: {', '.join(sorted(supported_story_goals))}"
        )
    if brief["figure_role"] not in ALLOWED_FIGURE_ROLES:
        raise FigureContractError(
            f"Unknown figure_role '{brief['figure_role']}'. Allowed: {', '.join(sorted(ALLOWED_FIGURE_ROLES))}"
        )
    if brief["style_mode"] not in ALLOWED_STYLE_MODES:
        raise FigureContractError(
            f"Unknown style_mode '{brief['style_mode']}'. Allowed: {', '.join(sorted(ALLOWED_STYLE_MODES))}"
        )
    if brief["palette_mode"] != "auto" and brief["palette_mode"] not in known_palettes:
        raise FigureContractError(
            f"Unknown palette_mode '{brief['palette_mode']}'. Allowed: {', '.join(sorted(known_palettes | {'auto'}))}"
        )

    unknown_candidates = [chart_id for chart_id in brief.get("candidate_chart_types", []) if chart_id not in known_charts]
    if unknown_candidates:
        raise FigureContractError(
            "Unknown candidate_chart_types: " + ", ".join(sorted(unknown_candidates))
        )


def validate_required_fields(brief: dict[str, Any], chart: dict[str, Any]) -> None:
    field_mapping = brief["field_mapping"]
    missing = [field for field in chart.get("required_fields", []) if resolve_field_name(field_mapping, field) is None]
    if missing:
        missing_text = ", ".join(missing)
        raise FigureContractError(
            f"Chart '{chart['chart_id']}' requires field_mapping keys: {missing_text}"
        )


def choose_palette_or_error(
    brief: dict[str, Any],
    code_chart: dict[str, Any],
    palettes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    requested = brief["palette_mode"]
    allowed = code_chart.get("palette_modes") or []

    if requested == "auto":
        if allowed:
            return palettes[allowed[0]]
        return palettes["paper-neutral"]

    if requested not in allowed:
        allowed_text = ", ".join(allowed) if allowed else "none"
        raise FigureContractError(
            f"Palette '{requested}' is not allowed for chart '{code_chart['chart_id']}'. Allowed: {allowed_text}"
        )

    return palettes[requested]

