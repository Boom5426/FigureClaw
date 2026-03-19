#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[3]
CHART_REGISTRY_PATH = REPO_ROOT / "skills" / "figure-recommender" / "references" / "chart-registry.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "source-audits"

AUDIT_METADATA: dict[str, dict[str, Any]] = {
    "contrast_dot": {
        "decision": "rename",
        "actual_visual_grammar": "labeled two-metric comparison scatter",
        "actual_backend": ["matplotlib"],
        "actual_data_shape": "benchmark points with x/y metrics and labels",
        "notes": (
            "The notebook called 对比点图 behaves like a labeled benchmark scatter, "
            "not a grouped category contrast-dot chart with mean and SEM overlays."
        ),
    },
    "stacked_bar": {
        "decision": "keep",
        "actual_visual_grammar": "stacked categorical bar chart",
        "actual_backend": ["matplotlib", "pandas", "numpy"],
        "actual_data_shape": "category + subgroup + value table",
        "notes": "The current template is a reasonable simplified version of the notebook.",
    },
    "raincloud": {
        "decision": "keep",
        "actual_visual_grammar": "distribution plot combining density and points",
        "actual_backend": ["matplotlib", "pandas", "numpy"],
        "actual_data_shape": "grouped samples by category",
        "notes": "The current raincloud template preserves the core distribution-comparison semantics.",
    },
    "line": {
        "decision": "keep",
        "actual_visual_grammar": "ordered line chart",
        "actual_backend": ["matplotlib"],
        "actual_data_shape": "ordered x/y series",
        "notes": "The template matches the source chart family closely.",
    },
    "multi_trend": {
        "decision": "keep",
        "actual_visual_grammar": "multi-series time trend comparison",
        "actual_backend": ["matplotlib", "pandas"],
        "actual_data_shape": "multiple named series over time",
        "notes": (
            "The notebook uses heavier styling than the template, but the simplified "
            "template preserves the same broad multi-series trend story."
        ),
    },
    "heatmap": {
        "decision": "keep",
        "actual_visual_grammar": "matrix heatmap",
        "actual_backend": ["seaborn", "matplotlib", "pandas"],
        "actual_data_shape": "row/column/value matrix table",
        "notes": "The shipped heatmap template is semantically aligned with the source notebook.",
    },
    "benchmark_scatter_error": {
        "decision": "keep",
        "actual_visual_grammar": "two-metric scatter with x/y error bars",
        "actual_backend": ["matplotlib", "numpy", "pandas"],
        "actual_data_shape": "label + x/y means with x/y uncertainty",
        "notes": "The template preserves the notebook's core benchmark comparison structure.",
    },
    "correlation_network": {
        "decision": "keep",
        "actual_visual_grammar": "network-like relation map for weighted pairwise associations",
        "actual_backend": ["matplotlib", "numpy"],
        "actual_data_shape": "edge table with source, target, and weight",
        "notes": (
            "The notebook is heavily styled, but the template still represents the same "
            "weighted relationship story."
        ),
    },
    "sunburst": {
        "decision": "demote",
        "actual_visual_grammar": "hierarchical radial partition chart",
        "actual_backend": ["plotly", "pandas"],
        "actual_data_shape": "hierarchical parent/child/value structure",
        "notes": "The chart is conceptually valid but should remain non-default because it is not executable in the Tier 1 path.",
    },
    "chord": {
        "decision": "demote",
        "actual_visual_grammar": "circular flow/relation chord diagram",
        "actual_backend": ["pycirclize", "pandas", "numpy", "matplotlib"],
        "actual_data_shape": "source/target/weight flow table",
        "notes": "The chart is too style-heavy and backend-specific for the default executable-first path.",
    },
}

EXTRA_NOTEBOOKS = {
    "配色": {
        "purpose": "palette reference",
        "notes": "Palette notebook kept for color guidance review and future palette reconciliation.",
    }
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export audited figure notebooks to plain Python and write audit artifacts.")
    parser.add_argument("--source-dir", type=Path, default=None, help="Directory containing the original notebook sources.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory to write audit artifacts.")
    return parser.parse_args()


def find_default_source_dir() -> Path:
    candidates = [
        REPO_ROOT / "Figures",
        REPO_ROOT.parent.parent / "Figures",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not locate a Figures directory. Pass --source-dir explicitly.")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_chart_registry() -> list[dict[str, Any]]:
    registry = load_json(CHART_REGISTRY_PATH)
    return registry["charts"]


def render_notebook_to_python(notebook: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Generated from a source notebook for audit and review purposes.",
        "",
    ]
    for index, cell in enumerate(notebook.get("cells", []), start=1):
        cell_type = cell.get("cell_type", "unknown")
        source_lines = cell.get("source", [])
        lines.append(f"# --- cell {index}: {cell_type} ---")
        if cell_type == "markdown":
            for raw_line in source_lines:
                line = raw_line.rstrip("\n")
                if line:
                    lines.append(f"# {line}")
                else:
                    lines.append("#")
        else:
            if source_lines:
                for raw_line in source_lines:
                    lines.append(raw_line.rstrip("\n"))
            else:
                lines.append("pass")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def notebook_filename(source_notebook: str) -> str:
    return Path(source_notebook).name


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def export_notebook(source_path: Path, output_path: Path) -> None:
    notebook = load_json(source_path)
    rendered = render_notebook_to_python(notebook)
    output_path.write_text(rendered, encoding="utf-8")


def build_chart_audit_entries(charts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for chart in charts:
        metadata = AUDIT_METADATA[chart["chart_id"]]
        source_name = notebook_filename(chart["source_notebook"])
        entries.append(
            {
                "chart_id": chart["chart_id"],
                "source_notebook": chart["source_notebook"],
                "exported_python": f"notebooks/{Path(source_name).stem}.py",
                "decision": metadata["decision"],
                "actual_visual_grammar": metadata["actual_visual_grammar"],
                "actual_backend": metadata["actual_backend"],
                "actual_data_shape": metadata["actual_data_shape"],
                "notes": metadata["notes"],
            }
        )
    return entries


def write_audit_json(output_dir: Path, chart_entries: list[dict[str, Any]]) -> None:
    payload = {
        "scope": "registry-backed chart notebooks plus palette reference",
        "charts": chart_entries,
        "extra_notebooks": [
            {
                "name": notebook_name,
                **metadata,
                "exported_python": f"notebooks/{notebook_name}.py",
            }
            for notebook_name, metadata in EXTRA_NOTEBOOKS.items()
        ],
    }
    (output_dir / "chart-source-audit.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_audit_markdown(output_dir: Path, chart_entries: list[dict[str, Any]]) -> None:
    lines = [
        "# Chart Source Audit",
        "",
        "This audit compares the notebooks backing the current registry against the shipped templates.",
        "",
        "| Chart ID | Decision | Visual Grammar | Notes |",
        "|---|---|---|---|",
    ]
    for entry in chart_entries:
        lines.append(
            f"| `{entry['chart_id']}` | `{entry['decision']}` | {entry['actual_visual_grammar']} | {entry['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Extra Notebook",
            "",
            "- `配色`: retained as a palette reference notebook for future palette reconciliation.",
            "",
        ]
    )
    (output_dir / "2026-03-19-chart-source-audit.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_dir = args.source_dir or find_default_source_dir()
    output_dir = args.output_dir
    notebook_output_dir = output_dir / "notebooks"

    ensure_directory(output_dir)
    ensure_directory(notebook_output_dir)

    charts = load_chart_registry()
    for chart in charts:
        source_name = notebook_filename(chart["source_notebook"])
        source_path = source_dir / source_name
        if not source_path.exists():
            raise FileNotFoundError(f"Missing source notebook: {source_path}")
        export_notebook(source_path, notebook_output_dir / f"{Path(source_name).stem}.py")

    for notebook_name in EXTRA_NOTEBOOKS:
        source_path = source_dir / f"{notebook_name}.ipynb"
        if not source_path.exists():
            raise FileNotFoundError(f"Missing extra audit notebook: {source_path}")
        export_notebook(source_path, notebook_output_dir / f"{notebook_name}.py")

    chart_entries = build_chart_audit_entries(charts)
    write_audit_json(output_dir, chart_entries)
    write_audit_markdown(output_dir, chart_entries)

    print(output_dir)


if __name__ == "__main__":
    main()
