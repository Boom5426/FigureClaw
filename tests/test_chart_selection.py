from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "skills" / "figure-recommender" / "scripts" / "generate_figure_response.py"
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "figure_cases.json"


def load_fixtures() -> list[dict]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def run_cli(brief: dict) -> dict:
    completed = subprocess.run(
        [
            "python3",
            str(CLI_PATH),
            "--brief-json",
            json.dumps(brief, ensure_ascii=False),
            "--output",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return json.loads(completed.stdout)


def test_selection_uses_executable_first_primary_chart() -> None:
    for fixture in load_fixtures():
        result = run_cli(fixture["brief"])
        expected = fixture["expected"]

        assert result["primary_chart"]["chart_id"] == expected["primary_chart_id"], fixture["name"]
        assert result["code_chart"]["chart_id"] == expected["code_chart_id"], fixture["name"]

        expected_conceptual = expected["conceptual_chart_id"]
        actual_conceptual = result.get("conceptual_chart", {})
        actual_conceptual_id = actual_conceptual["chart_id"] if actual_conceptual else None
        assert actual_conceptual_id == expected_conceptual, fixture["name"]
