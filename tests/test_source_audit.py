from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHART_REGISTRY_PATH = REPO_ROOT / "skills" / "figure-recommender" / "references" / "chart-registry.json"
AUDIT_JSON_PATH = REPO_ROOT / "docs" / "source-audits" / "chart-source-audit.json"
AUDIT_MARKDOWN_PATH = REPO_ROOT / "docs" / "source-audits" / "2026-03-19-chart-source-audit.md"
AUDIT_NOTEBOOK_DIR = REPO_ROOT / "docs" / "source-audits" / "notebooks"

ALLOWED_DECISIONS = {"keep", "rename", "demote", "drop"}


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def audited_chart_entries() -> list[dict]:
    chart_registry = load_json(CHART_REGISTRY_PATH)
    assert isinstance(chart_registry, dict)
    charts = chart_registry["charts"]
    return [chart for chart in charts if chart.get("source_notebook")]


def notebook_stub(source_notebook: str) -> str:
    return Path(source_notebook).stem


def test_source_audit_artifacts_exist() -> None:
    assert AUDIT_JSON_PATH.exists()
    assert AUDIT_MARKDOWN_PATH.exists()
    assert AUDIT_NOTEBOOK_DIR.exists()


def test_source_audit_covers_every_registry_backed_chart() -> None:
    audit = load_json(AUDIT_JSON_PATH)
    assert isinstance(audit, dict)
    audited_charts = audit["charts"]

    expected_chart_ids = {chart["chart_id"] for chart in audited_chart_entries()}
    actual_chart_ids = {item["chart_id"] for item in audited_charts}
    assert actual_chart_ids == expected_chart_ids


def test_source_audit_records_decision_and_exported_notebook_snapshot() -> None:
    audit = load_json(AUDIT_JSON_PATH)
    assert isinstance(audit, dict)
    audited_by_chart_id = {item["chart_id"]: item for item in audit["charts"]}

    for chart in audited_chart_entries():
        audited = audited_by_chart_id[chart["chart_id"]]
        assert audited["decision"] in ALLOWED_DECISIONS

        exported_notebook = AUDIT_NOTEBOOK_DIR / f"{notebook_stub(chart['source_notebook'])}.py"
        assert exported_notebook.exists(), chart["chart_id"]
