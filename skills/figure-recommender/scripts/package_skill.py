#!/usr/bin/env python3
from __future__ import annotations

import json
import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
DIST_DIR = REPO_ROOT / "dist"
ZIP_PATH = DIST_DIR / "figure-recommender.zip"
MANIFEST_PATH = SKILL_ROOT / "package-manifest.json"


def load_manifest() -> list[str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    include_paths = manifest.get("include", [])
    if not include_paths:
        raise ValueError("package-manifest.json must define a non-empty include list.")
    return include_paths


def validate_include_paths(include_paths: list[str]) -> None:
    missing = [relative_path for relative_path in include_paths if not (SKILL_ROOT / relative_path).exists()]
    if missing:
        raise FileNotFoundError("Missing package files: " + ", ".join(missing))


def main() -> None:
    include_paths = load_manifest()
    validate_include_paths(include_paths)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative_path in include_paths:
            full_path = SKILL_ROOT / relative_path
            archive.write(full_path, arcname=Path("figure-recommender") / relative_path)
    print(ZIP_PATH)


if __name__ == "__main__":
    main()
