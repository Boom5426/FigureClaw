from __future__ import annotations

import re
import subprocess
import zipfile
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SCRIPT = REPO_ROOT / "skills" / "figure-recommender" / "scripts" / "package_skill.py"
PACKAGE_MANIFEST = REPO_ROOT / "skills" / "figure-recommender" / "package-manifest.json"


def test_package_skill_builds_dr_claw_compatible_zip(tmp_path: Path) -> None:
    manifest = json.loads(PACKAGE_MANIFEST.read_text(encoding="utf-8"))
    completed = subprocess.run(
        ["python3", str(PACKAGE_SCRIPT)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    zip_path = Path(completed.stdout.strip())
    assert zip_path.exists()

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        assert "figure-recommender/SKILL.md" in names
        assert "figure-recommender/README.md" in names
        assert "figure-recommender/references/chart-registry.json" in names
        assert "figure-recommender/references/palette-registry.json" in names
        assert "figure-recommender/templates/contrast_dot.py.tmpl" in names
        assert "figure-recommender/scripts/generate_figure_response.py" in names
        for relative_path in manifest["include"]:
            assert f"figure-recommender/{relative_path}" in names
        skill_md = archive.read("figure-recommender/SKILL.md").decode("utf-8")
        skill_readme = archive.read("figure-recommender/README.md").decode("utf-8")

    assert all(not name.startswith("figure-recommender/tests/") for name in names)
    assert all(not name.startswith("figure-recommender/docs/source-audits/") for name in names)
    assert all(not name.startswith("figure-recommender/Figures/") for name in names)
    assert all(not name.endswith("FigureClaw.png") for name in names)

    assert re.search(r"^name:\s*figure-recommender\s*$", skill_md, re.MULTILINE)
    assert "This README documents the packaged skill boundary." in skill_readme
