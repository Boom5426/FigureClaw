#!/usr/bin/env python3
from __future__ import annotations

import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
DIST_DIR = REPO_ROOT / "dist"
ZIP_PATH = DIST_DIR / "figure-recommender.zip"
INCLUDE_PATHS = [
    "SKILL.md",
    "README.md",
    "references/chart-registry.json",
    "references/figure-recommender.md",
    "references/palette-registry.json",
    "examples/figure_briefs.json",
    "scripts/generate_figure_response.py",
    "scripts/package_skill.py",
    "templates/contrast_dot.py.tmpl",
    "templates/stacked_bar.py.tmpl",
    "templates/raincloud.py.tmpl",
    "templates/line.py.tmpl",
    "templates/multi_trend.py.tmpl",
    "templates/heatmap.py.tmpl",
    "templates/benchmark_scatter_error.py.tmpl",
    "templates/correlation_network.py.tmpl"
]


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
      for relative_path in INCLUDE_PATHS:
        full_path = SKILL_ROOT / relative_path
        archive.write(full_path, arcname=Path("figure-recommender") / relative_path)
    print(ZIP_PATH)


if __name__ == "__main__":
    main()
