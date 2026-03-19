from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "skills" / "figure-recommender" / "scripts" / "generate_figure_response.py"


def run_cli_with_json(brief: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            str(CLI_PATH),
            "--brief-json",
            json.dumps(brief, ensure_ascii=False),
            "--output",
            "json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def run_cli_with_file(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            str(CLI_PATH),
            "--brief-file",
            str(path),
            "--output",
            "json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def minimal_brief() -> dict:
    return {
        "id": "fig-01",
        "story_goal": "compare_group_difference",
        "data_shape": "grouped_metric",
        "field_mapping": {
            "category": "condition",
            "value": "score",
        },
        "figure_role": "paper-main",
        "style_mode": "readable",
        "palette_mode": "paper-neutral",
    }


def test_brief_file_rejects_array_input_with_contract_error(tmp_path: Path) -> None:
    brief_file = tmp_path / "array.json"
    brief_file.write_text(json.dumps([minimal_brief()], ensure_ascii=False), encoding="utf-8")

    completed = run_cli_with_file(brief_file)

    assert completed.returncode != 0
    assert "single brief object" in completed.stderr


def test_unknown_story_goal_is_rejected() -> None:
    brief = minimal_brief()
    brief["story_goal"] = "made_up_story_goal"
    brief["data_shape"] = "made_up_shape"

    completed = run_cli_with_json(brief)

    assert completed.returncode != 0
    assert "Unknown story_goal" in completed.stderr


def test_unknown_palette_mode_is_rejected() -> None:
    brief = minimal_brief()
    brief["palette_mode"] = "typo-bad"

    completed = run_cli_with_json(brief)

    assert completed.returncode != 0
    assert "Unknown palette_mode" in completed.stderr


def test_incompatible_explicit_palette_is_rejected() -> None:
    brief = minimal_brief()
    brief["palette_mode"] = "diverging"

    completed = run_cli_with_json(brief)

    assert completed.returncode != 0
    assert "not allowed for chart" in completed.stderr
    assert "contrast_dot" in completed.stderr


def test_missing_chart_required_fields_fail_before_template_render() -> None:
    brief = {
        "id": "fig-heatmap",
        "story_goal": "show_matrix_pattern",
        "data_shape": "matrix",
        "field_mapping": {
            "value": "z_score",
        },
        "figure_role": "paper-main",
        "style_mode": "readable",
        "palette_mode": "diverging",
    }

    completed = run_cli_with_json(brief)

    assert completed.returncode != 0
    assert "requires field_mapping keys" in completed.stderr
    assert "row" in completed.stderr
    assert "column" in completed.stderr
    assert "Unresolved placeholders" not in completed.stderr
