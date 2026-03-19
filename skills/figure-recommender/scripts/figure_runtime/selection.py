from __future__ import annotations

from typing import Any


SUPPORT_LEVEL_PRIORITY = {
    "tier1": 0,
    "tier2": 1,
    "tier3": 2,
}


def resolve_fallback_chart(primary_chart: dict[str, Any], charts: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    fallback_chart = primary_chart.get("fallback_chart")
    return charts[fallback_chart] if fallback_chart else None


def discover_candidates(brief: dict[str, Any], charts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    story_goal = brief["story_goal"]
    data_shape = brief["data_shape"]
    return [
        chart
        for chart in charts.values()
        if story_goal in chart.get("story_goals", []) or data_shape in chart.get("data_shapes", [])
    ]


def sort_candidates(brief: dict[str, Any], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def rank(chart: dict[str, Any]) -> tuple[int, int, int, str]:
        return (
            SUPPORT_LEVEL_PRIORITY[chart["support_level"]],
            0 if brief["story_goal"] in chart.get("story_goals", []) else 1,
            0 if brief["data_shape"] in chart.get("data_shapes", []) else 1,
            chart["chart_id"],
        )

    return sorted(candidates, key=rank)


def select_charts(
    brief: dict[str, Any],
    charts: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    explicit_candidates = [charts[chart_id] for chart_id in brief.get("candidate_chart_types", []) if chart_id in charts]

    if explicit_candidates:
        ranked_explicit = sort_candidates(brief, explicit_candidates)
        requested_chart = explicit_candidates[0]
        if requested_chart["support_level"] == "tier1":
            return ranked_explicit[0], ranked_explicit[0], None, None

        fallback_chart = resolve_fallback_chart(requested_chart, charts)
        if fallback_chart is not None:
            return fallback_chart, fallback_chart, None, requested_chart

        ranked_discovered = sort_candidates(brief, discover_candidates(brief, charts))
        executable = next((chart for chart in ranked_discovered if chart["support_level"] == "tier1"), ranked_discovered[0])
        return executable, executable, None, requested_chart

    ranked_candidates = sort_candidates(brief, discover_candidates(brief, charts))
    executable = next((chart for chart in ranked_candidates if chart["support_level"] == "tier1"), ranked_candidates[0])
    return executable, executable, None, None
