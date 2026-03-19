#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_ROOT / "references"
TEMPLATES_DIR = SKILL_ROOT / "templates"

REQUIRED_BRIEF_FIELDS = [
    "id",
    "story_goal",
    "data_shape",
    "field_mapping",
    "figure_role",
    "style_mode",
    "palette_mode",
]

CHART_SELECTION_BY_STORY = {
    "compare_group_difference": "contrast_dot",
    "compare_composition": "stacked_bar",
    "show_distribution": "raincloud",
    "show_trend": "line",
    "show_multi_trend": "multi_trend",
    "show_matrix_pattern": "heatmap",
    "benchmark_tradeoff_with_uncertainty": "benchmark_scatter_error",
    "show_network_relations": "correlation_network",
    "show_hierarchy": "sunburst",
    "show_flow_relationship": "chord",
}

TITLE_BY_CHART = {
    "contrast_dot": "Group comparison",
    "stacked_bar": "Composition across groups",
    "raincloud": "Distribution across groups",
    "line": "Trend across ordered axis",
    "multi_trend": "Coordinated trajectories",
    "heatmap": "Matrix pattern overview",
    "benchmark_scatter_error": "Benchmark trade-off with uncertainty",
    "correlation_network": "Correlation relation map",
}

ALIASES = {
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registries() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    charts = {item["chart_id"]: item for item in load_json(REFERENCES_DIR / "chart-registry.json")["charts"]}
    palettes = {
        item["palette_mode"]: item for item in load_json(REFERENCES_DIR / "palette-registry.json")["palettes"]
    }
    return charts, palettes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate structured figure recommendations and plotting code.")
    parser.add_argument("--brief-file", type=Path, help="Path to a JSON file containing a figure_brief object.")
    parser.add_argument("--brief-json", help="Inline JSON string containing a figure_brief object.")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def load_brief(args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.brief_file) == bool(args.brief_json):
      raise ValueError("Provide exactly one of --brief-file or --brief-json.")
    brief = load_json(args.brief_file) if args.brief_file else json.loads(args.brief_json)
    for field in REQUIRED_BRIEF_FIELDS:
      if field not in brief:
        raise ValueError(f"Missing required figure_brief field: {field}")
    if not isinstance(brief["field_mapping"], dict) or not brief["field_mapping"]:
      raise ValueError("figure_brief.field_mapping must be a non-empty object.")
    return brief


def choose_primary_chart(brief: dict[str, Any], charts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    candidates = brief.get("candidate_chart_types") or []
    for candidate in candidates:
      if candidate in charts:
        return charts[candidate]

    story_goal = brief["story_goal"]
    if story_goal in CHART_SELECTION_BY_STORY:
      return charts[CHART_SELECTION_BY_STORY[story_goal]]

    for chart in charts.values():
      if story_goal in chart.get("story_goals", []) or brief["data_shape"] in chart.get("data_shapes", []):
        return chart

    return charts["contrast_dot"]


def resolve_fallback_chart(primary_chart: dict[str, Any], charts: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    fallback_chart = primary_chart.get("fallback_chart")
    return charts[fallback_chart] if fallback_chart else None


def resolve_code_chart(primary_chart: dict[str, Any], charts: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    if primary_chart["support_level"] == "tier1":
      return primary_chart, None

    fallback_chart = resolve_fallback_chart(primary_chart, charts)
    if fallback_chart:
      return fallback_chart, fallback_chart

    return charts["contrast_dot"], charts["contrast_dot"]


def choose_palette(brief: dict[str, Any], code_chart: dict[str, Any], palettes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    requested = brief["palette_mode"]
    allowed = code_chart.get("palette_modes") or []
    if requested in palettes and requested in allowed:
      return palettes[requested]
    if allowed:
      return palettes[allowed[0]]
    return palettes["paper-neutral"]


def build_placeholder_map(brief: dict[str, Any], palette: dict[str, Any], chart_id: str) -> dict[str, str]:
    mapping = brief["field_mapping"]
    title = TITLE_BY_CHART.get(chart_id, "Scientific figure")

    def resolve_field(*names: str) -> str | None:
      for name in names:
        for alias in ALIASES.get(name, [name]):
          if alias in mapping:
            return mapping[alias]
      return None

    replacements = {
        "__PALETTE__": json.dumps(palette["colors"], ensure_ascii=False),
        "__TITLE__": json.dumps(title, ensure_ascii=False),
    }

    default_labels = {
        "__X_LABEL__": resolve_field("category", "x", "column", "source") or "x",
        "__Y_LABEL__": resolve_field("value", "y", "weight") or "value",
    }
    replacements.update({key: json.dumps(value, ensure_ascii=False) for key, value in default_labels.items()})

    for key, value in mapping.items():
      token = f"__{key.upper()}_COL__"
      replacements[token] = json.dumps(value, ensure_ascii=False)
    semantic_tokens = {
        "__CATEGORY_COL__": resolve_field("category"),
        "__SUBGROUP_COL__": resolve_field("subgroup"),
        "__VALUE_COL__": resolve_field("value"),
        "__X_COL__": resolve_field("x"),
        "__Y_COL__": resolve_field("y"),
        "__SERIES_COL__": resolve_field("series"),
        "__ROW_COL__": resolve_field("row"),
        "__COLUMN_COL__": resolve_field("column"),
        "__LABEL_COL__": resolve_field("label"),
        "__SOURCE_COL__": resolve_field("source"),
        "__TARGET_COL__": resolve_field("target"),
        "__WEIGHT_COL__": resolve_field("weight"),
    }
    for token, value in semantic_tokens.items():
      if value is not None:
        replacements[token] = json.dumps(value, ensure_ascii=False)
    if "x_error" in mapping:
      replacements["__XERR_COL__"] = json.dumps(mapping["x_error"], ensure_ascii=False)
    elif resolve_field("x_error") is not None:
      replacements["__XERR_COL__"] = json.dumps(resolve_field("x_error"), ensure_ascii=False)
    if "y_error" in mapping:
      replacements["__YERR_COL__"] = json.dumps(mapping["y_error"], ensure_ascii=False)
    elif resolve_field("y_error") is not None:
      replacements["__YERR_COL__"] = json.dumps(resolve_field("y_error"), ensure_ascii=False)
    replacements["__SIGNIFICANCE_COL__"] = (
        json.dumps(resolve_field("significance"), ensure_ascii=False) if resolve_field("significance") else "None"
    )
    return replacements


def render_template(code_chart: dict[str, Any], brief: dict[str, Any], palette: dict[str, Any]) -> str:
    template_path = SKILL_ROOT / code_chart["template_file"]
    template = template_path.read_text(encoding="utf-8")
    rendered = template
    for placeholder, value in build_placeholder_map(brief, palette, code_chart["chart_id"]).items():
      rendered = rendered.replace(placeholder, value)
    unresolved = sorted(set(re.findall(r"__[A-Z0-9_]+__", rendered)))
    if unresolved:
      raise ValueError(f"Unresolved placeholders remain in template: {unresolved}")
    return rendered


def build_adaptation_notes(primary_chart: dict[str, Any], code_chart: dict[str, Any], fallback_chart: dict[str, Any] | None) -> list[str]:
    notes = []
    if primary_chart["support_level"] != "tier1":
      notes.append(
          f"Primary chart `{primary_chart['chart_id']}` is {primary_chart['support_level']} and does not ship direct codegen in v1."
      )
      if fallback_chart:
        notes.append(f"Python code is generated from fallback chart `{fallback_chart['chart_id']}`.")
    else:
      notes.append("Primary chart is Tier 1 and ships direct codegen.")
    notes.append("Replace axis labels, title, and aggregation rules if your paper uses stricter nomenclature.")
    return notes


def build_markdown_response(result: dict[str, Any]) -> str:
    fallback = result["fallback_chart"]
    fallback_lines = [
        "## Optional fallback",
        f"- Chart ID: `{fallback['chart_id']}`",
        f"- Display name: {fallback['display_name']}",
        f"- Source notebook: `{fallback['source_notebook']}`",
    ] if fallback else [
        "## Optional fallback",
        "- None. The primary figure already has Tier 1 codegen support.",
    ]

    adaptation_notes = "\n".join(f"- {note}" for note in result["adaptation_notes"])
    dependencies = ", ".join(result["dependencies"])
    palette_colors = ", ".join(result["palette"]["colors"])

    return "\n".join(
        [
            "## Primary figure",
            f"- Chart ID: `{result['primary_chart']['chart_id']}`",
            f"- Display name: {result['primary_chart']['display_name']}",
            f"- Support level: `{result['primary_chart']['support_level']}`",
            f"- Source notebook: `{result['primary_chart']['source_notebook']}`",
            "",
            *fallback_lines,
            "",
            "## Palette",
            f"- Palette mode: `{result['palette']['palette_mode']}`",
            f"- Colors: {palette_colors}",
            f"- Usage: {result['palette']['usage']}",
            "",
            "## Dependencies",
            f"- Python packages: {dependencies}",
            "",
            "## Python code",
            "```python",
            result["python_code"].rstrip(),
            "```",
            "",
            "## Adaptation notes",
            adaptation_notes,
        ]
    )


def build_result(brief: dict[str, Any]) -> dict[str, Any]:
    charts, palettes = load_registries()
    primary_chart = choose_primary_chart(brief, charts)
    code_chart, fallback_chart = resolve_code_chart(primary_chart, charts)
    palette = choose_palette(brief, code_chart, palettes)
    python_code = render_template(code_chart, brief, palette)
    result = {
        "sections": [
            "Primary figure",
            "Optional fallback",
            "Palette",
            "Dependencies",
            "Python code",
            "Adaptation notes",
        ],
        "brief_id": brief["id"],
        "primary_chart": primary_chart,
        "fallback_chart": fallback_chart,
        "code_chart": code_chart,
        "palette": palette,
        "dependencies": code_chart["backend"],
        "python_code": python_code,
        "adaptation_notes": build_adaptation_notes(primary_chart, code_chart, fallback_chart),
    }
    result["markdown"] = build_markdown_response(result)
    return result


def main() -> None:
    args = parse_args()
    brief = load_brief(args)
    result = build_result(brief)
    if args.output == "json":
      serializable = {key: value for key, value in result.items() if key != "markdown"}
      print(json.dumps(serializable, indent=2, ensure_ascii=False))
      return
    print(result["markdown"])


if __name__ == "__main__":
    main()
