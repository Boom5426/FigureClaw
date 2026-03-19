from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .contracts import FIELD_ALIASES, resolve_field_name
from .errors import FigureContractError


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


def build_placeholder_map(brief: dict[str, Any], palette: dict[str, Any], chart_id: str) -> dict[str, str]:
    mapping = brief["field_mapping"]
    title = TITLE_BY_CHART.get(chart_id, "Scientific figure")

    def resolve_field(*names: str) -> str | None:
        for name in names:
            for alias in FIELD_ALIASES.get(name, [name]):
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
        replacements[f"__{key.upper()}_COL__"] = json.dumps(value, ensure_ascii=False)

    semantic_tokens = {
        "__CATEGORY_COL__": resolve_field_name(mapping, "category"),
        "__SUBGROUP_COL__": resolve_field_name(mapping, "subgroup"),
        "__VALUE_COL__": resolve_field_name(mapping, "value"),
        "__X_COL__": resolve_field_name(mapping, "x"),
        "__Y_COL__": resolve_field_name(mapping, "y"),
        "__SERIES_COL__": resolve_field_name(mapping, "series"),
        "__ROW_COL__": resolve_field_name(mapping, "row"),
        "__COLUMN_COL__": resolve_field_name(mapping, "column"),
        "__LABEL_COL__": resolve_field_name(mapping, "label"),
        "__SOURCE_COL__": resolve_field_name(mapping, "source"),
        "__TARGET_COL__": resolve_field_name(mapping, "target"),
        "__WEIGHT_COL__": resolve_field_name(mapping, "weight"),
    }
    for token, value in semantic_tokens.items():
        if value is not None:
            replacements[token] = json.dumps(value, ensure_ascii=False)

    x_error = resolve_field_name(mapping, "x_error")
    y_error = resolve_field_name(mapping, "y_error")
    if x_error is not None:
        replacements["__XERR_COL__"] = json.dumps(x_error, ensure_ascii=False)
    if y_error is not None:
        replacements["__YERR_COL__"] = json.dumps(y_error, ensure_ascii=False)

    significance = resolve_field_name(mapping, "significance")
    replacements["__SIGNIFICANCE_COL__"] = json.dumps(significance, ensure_ascii=False) if significance else "None"
    return replacements


def render_template(skill_root: Path, code_chart: dict[str, Any], brief: dict[str, Any], palette: dict[str, Any]) -> str:
    template_path = skill_root / code_chart["template_file"]
    template = template_path.read_text(encoding="utf-8")
    rendered = template
    for placeholder, value in build_placeholder_map(brief, palette, code_chart["chart_id"]).items():
        rendered = rendered.replace(placeholder, value)
    unresolved = sorted(set(re.findall(r"__[A-Z0-9_]+__", rendered)))
    if unresolved:
        raise FigureContractError(
            f"Template rendering failed for chart '{code_chart['chart_id']}'. Unresolved placeholders: {unresolved}"
        )
    return rendered
