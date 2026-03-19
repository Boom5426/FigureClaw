from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import pandas as pd


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
    )
    return json.loads(completed.stdout)


def build_dummy_dataframe(field_mapping: dict, chart_id: str) -> pd.DataFrame:
    def field(*keys: str) -> str:
        for key in keys:
            if key in field_mapping:
                return field_mapping[key]
        raise KeyError(keys[0])

    if chart_id in {"contrast_dot", "raincloud"}:
        return pd.DataFrame(
            {
                field("category"): ["A", "A", "B", "B", "C", "C"],
                field("value"): [1.2, 1.4, 2.1, 2.2, 1.8, 1.7],
            }
        )
    if chart_id == "stacked_bar":
        return pd.DataFrame(
            {
                field("category", "parent"): ["G1", "G1", "G2", "G2", "G3", "G3"],
                field("subgroup", "child"): ["T1", "T2", "T1", "T2", "T1", "T2"],
                field("value"): [0.4, 0.6, 0.55, 0.45, 0.3, 0.7],
            }
        )
    if chart_id in {"line", "multi_trend"}:
        return pd.DataFrame(
            {
                field("x"): [0, 1, 2, 0, 1, 2],
                field("y"): [0.1, 0.15, 0.25, 0.08, 0.12, 0.2],
                field("series"): ["S1", "S1", "S1", "S2", "S2", "S2"],
            }
        )
    if chart_id == "heatmap":
        return pd.DataFrame(
            {
                field("row"): ["R1", "R1", "R2", "R2"],
                field("column"): ["C1", "C2", "C1", "C2"],
                field("value"): [0.5, -0.2, 0.3, 0.9],
            }
        )
    if chart_id == "benchmark_scatter_error":
        return pd.DataFrame(
            {
                field("x"): [0.82, 0.79, 0.85],
                field("y"): [12.0, 8.0, 16.0],
                field("x_error"): [0.01, 0.015, 0.008],
                field("y_error"): [1.0, 0.7, 1.2],
                field("label"): ["M1", "M2", "M3"],
            }
        )
    if chart_id == "correlation_network":
        data = {
            field("source", "sender"): ["A", "A", "B", "C"],
            field("target", "receiver"): ["B", "C", "C", "D"],
            field("weight", "interaction_score"): [0.8, -0.4, 0.6, -0.7],
        }
        significance = field_mapping.get("significance") or field_mapping.get("p_value")
        if significance:
            data[significance] = [0.001, 0.02, 0.03, 0.2]
        return pd.DataFrame(data)
    raise AssertionError(f"Unhandled chart_id in test fixture builder: {chart_id}")


def test_cli_outputs_expected_chart_selection_for_fixtures() -> None:
    for fixture in load_fixtures():
        result = run_cli(fixture["brief"])
        expected = fixture["expected"]
        assert result["primary_chart"]["chart_id"] == expected["primary_chart_id"], fixture["name"]
        assert result["code_chart"]["chart_id"] == expected["code_chart_id"], fixture["name"]
        fallback = result["fallback_chart"]["chart_id"] if result["fallback_chart"] else None
        assert fallback == expected["fallback_chart_id"], fixture["name"]
        conceptual = result["conceptual_chart"]["chart_id"] if result.get("conceptual_chart") else None
        assert conceptual == expected.get("conceptual_chart_id"), fixture["name"]
        assert result["palette"]["palette_mode"] == expected["palette_mode"], fixture["name"]
        assert result["sections"] == [
            "Primary figure",
            "Optional fallback",
            "Palette",
            "Dependencies",
            "Python code",
            "Adaptation notes",
        ]


def test_generated_python_code_compiles_for_every_fixture() -> None:
    for fixture in load_fixtures():
        result = run_cli(fixture["brief"])
        code = result["python_code"]
        ast.parse(code)
        assert "{{" not in code and "}}" not in code, fixture["name"]


def test_generated_python_code_runs_with_dummy_dataframe() -> None:
    for fixture in load_fixtures():
        result = run_cli(fixture["brief"])
        namespace: dict = {}
        exec(result["python_code"], namespace)
        df = build_dummy_dataframe(fixture["brief"]["field_mapping"], result["code_chart"]["chart_id"])
        fig = namespace["build_figure"](df)
        assert fig is not None, fixture["name"]
        fig.clf()
