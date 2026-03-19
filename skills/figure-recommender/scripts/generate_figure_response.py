#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from figure_runtime.contracts import ensure_brief_object, normalize_brief
from figure_runtime.errors import FigureContractError
from figure_runtime.registry import load_json, load_registries, supported_story_goals
from figure_runtime.render import render_template
from figure_runtime.selection import select_charts
from figure_runtime.validation import choose_palette_or_error, validate_known_values, validate_required_fields

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_ROOT / "references"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate structured figure recommendations and plotting code.")
    parser.add_argument("--brief-file", type=Path, help="Path to a JSON file containing a figure_brief object.")
    parser.add_argument("--brief-json", help="Inline JSON string containing a figure_brief object.")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def load_brief(args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.brief_file) == bool(args.brief_json):
        raise FigureContractError("Provide exactly one of --brief-file or --brief-json.")
    raw_brief = load_json(args.brief_file) if args.brief_file else json.loads(args.brief_json)
    return normalize_brief(ensure_brief_object(raw_brief))


def build_adaptation_notes(
    primary_chart: dict[str, Any],
    code_chart: dict[str, Any],
    fallback_chart: dict[str, Any] | None,
    conceptual_chart: dict[str, Any] | None,
) -> list[str]:
    notes = []
    if conceptual_chart is not None:
        notes.append(
            f"Requested conceptual chart `{conceptual_chart['chart_id']}` does not ship direct codegen in v1."
        )
        notes.append(f"Python code is generated from executable chart `{code_chart['chart_id']}`.")
    elif primary_chart["support_level"] != "tier1":
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
    charts, palettes = load_registries(REFERENCES_DIR)
    validate_known_values(
        brief,
        supported_story_goals=supported_story_goals(charts),
        known_palettes=set(palettes),
        known_charts=set(charts),
    )
    primary_chart, code_chart, fallback_chart, conceptual_chart = select_charts(brief, charts)
    validate_required_fields(brief, code_chart)
    palette = choose_palette_or_error(brief, code_chart, palettes)
    python_code = render_template(SKILL_ROOT, code_chart, brief, palette)
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
        "conceptual_chart": conceptual_chart,
        "palette": palette,
        "dependencies": code_chart["backend"],
        "python_code": python_code,
        "adaptation_notes": build_adaptation_notes(primary_chart, code_chart, fallback_chart, conceptual_chart),
    }
    result["markdown"] = build_markdown_response(result)
    return result


def main() -> None:
    try:
        args = parse_args()
        brief = load_brief(args)
        result = build_result(brief)
        if args.output == "json":
            serializable = {key: value for key, value in result.items() if key != "markdown"}
            print(json.dumps(serializable, indent=2, ensure_ascii=False))
            return
        print(result["markdown"])
    except FigureContractError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
