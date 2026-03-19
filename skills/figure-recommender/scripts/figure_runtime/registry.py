from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registries(references_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    charts = {item["chart_id"]: item for item in load_json(references_dir / "chart-registry.json")["charts"]}
    palettes = {item["palette_mode"]: item for item in load_json(references_dir / "palette-registry.json")["palettes"]}
    return charts, palettes


def supported_story_goals(charts: dict[str, dict[str, Any]]) -> set[str]:
    goals: set[str] = set()
    for chart in charts.values():
        goals.update(chart.get("story_goals", []))
    return goals

