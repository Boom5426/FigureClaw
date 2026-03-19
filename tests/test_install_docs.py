from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_platform_install_guides_exist_and_use_expected_skill_paths() -> None:
    setup_doc = read_text("setup.md")
    codex_install = read_text(".codex/INSTALL.md")
    claude_install_path = REPO_ROOT / ".claude" / "INSTALL.md"

    assert "set up FigureClaw for me" in setup_doc
    assert "Codex" in setup_doc
    assert "Claude Code" in setup_doc
    assert "Dr. Claw" in setup_doc
    assert "If you are in Codex, start here first." in setup_doc
    assert "\"primary_chart\"" in setup_doc
    assert "\"contrast_dot\"" in setup_doc
    assert "\"python_code\"" in setup_doc

    assert "git clone https://github.com/Boom5426/FigureClaw.git" in codex_install
    assert "mkdir -p ~/.codex/skills" in codex_install
    assert "~/.codex/skills/figure-recommender" in codex_install
    assert "cd ~/.codex/FigureClaw" in codex_install
    assert "If it does not show up in Codex" in codex_install
    assert "test -L ~/.codex/skills/figure-recommender" in codex_install

    assert claude_install_path.exists()
    claude_install = claude_install_path.read_text(encoding="utf-8")
    assert "git clone https://github.com/Boom5426/FigureClaw.git" in claude_install
    assert "mkdir -p ~/.claude/skills" in claude_install
    assert "~/.claude/skills/figure-recommender" in claude_install


def test_readmes_cover_codex_claude_and_dr_claw_install_flows() -> None:
    root_readme = read_text("README.md")
    zh_readme_path = REPO_ROOT / "README_CN.md"
    skill_readme = read_text("skills/figure-recommender/README.md")
    skill_md = read_text("skills/figure-recommender/SKILL.md")

    assert zh_readme_path.exists()
    zh_readme = zh_readme_path.read_text(encoding="utf-8")

    assert "[简体中文](README_CN.md)" in root_readme
    assert "[English](README.md)" in zh_readme
    assert "FigureClaw.png" in root_readme
    assert "FigureClaw.png" in zh_readme
    assert "60-Second Quick Start" in root_readme
    assert "60 秒快速上手" in zh_readme
    assert "<details>" in root_readme
    assert "Manual install" in root_readme
    assert "<details>" in zh_readme
    assert "手动安装" in zh_readme

    assert "setup.md" in root_readme
    assert "Codex-first" in root_readme
    assert "## Install With Codex" in root_readme
    assert "## Install With Claude" in root_readme
    assert "## Install With Dr. Claw" in root_readme
    assert "https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md" in root_readme
    assert "https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md" in root_readme

    assert "~/.codex/skills/" in skill_readme
    assert "~/.claude/skills/" in skill_readme
    assert "Dr. Claw" in skill_readme
    assert "examples/briefs/" in skill_readme
    assert "This README documents the packaged skill boundary." in skill_readme
    assert "The zip package intentionally excludes `tests/`, `docs/source-audits/`, and `Figures/`." in skill_readme

    assert "infer the minimal brief" in skill_md
    assert "Do not answer with handcrafted plotting code when the local helper can be run." in skill_md
    assert "Never fabricate direct code for a chart that is not shipped with a local template." in skill_md


def test_user_examples_are_single_brief_json_files() -> None:
    brief_dir = REPO_ROOT / "skills" / "figure-recommender" / "examples" / "briefs"
    assert brief_dir.exists()

    brief_files = sorted(brief_dir.glob("*.json"))
    assert brief_files

    for brief_file in brief_files:
        payload = read_text(str(brief_file.relative_to(REPO_ROOT)))
        data = __import__("json").loads(payload)
        assert isinstance(data, dict), brief_file.name
        assert "story_goal" in data, brief_file.name
        assert "field_mapping" in data, brief_file.name


def test_codex_style_install_layout_runs_the_documented_smoke_test(tmp_path: Path) -> None:
    codex_root = tmp_path / ".codex"
    repo_link = codex_root / "FigureClaw"
    skill_link = codex_root / "skills" / "figure-recommender"

    repo_link.parent.mkdir(parents=True, exist_ok=True)
    skill_link.parent.mkdir(parents=True, exist_ok=True)
    repo_link.symlink_to(REPO_ROOT, target_is_directory=True)
    skill_link.symlink_to(repo_link / "skills" / "figure-recommender", target_is_directory=True)

    completed = subprocess.run(
        [
            "python3",
            "skills/figure-recommender/scripts/generate_figure_response.py",
            "--brief-file",
            "skills/figure-recommender/examples/briefs/grouped-comparison.json",
            "--output",
            "json",
        ],
        cwd=repo_link,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "\"primary_chart\"" in completed.stdout
    assert "\"contrast_dot\"" in completed.stdout
    assert "\"python_code\"" in completed.stdout
