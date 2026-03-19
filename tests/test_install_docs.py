from __future__ import annotations

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

    assert "git clone https://github.com/Boom5426/FigureClaw.git" in codex_install
    assert "mkdir -p ~/.codex/skills" in codex_install
    assert "~/.codex/skills/figure-recommender" in codex_install

    assert claude_install_path.exists()
    claude_install = claude_install_path.read_text(encoding="utf-8")
    assert "git clone https://github.com/Boom5426/FigureClaw.git" in claude_install
    assert "mkdir -p ~/.claude/skills" in claude_install
    assert "~/.claude/skills/figure-recommender" in claude_install


def test_readmes_cover_codex_claude_and_dr_claw_install_flows() -> None:
    root_readme = read_text("README.md")
    zh_readme_path = REPO_ROOT / "README_CN.md"
    skill_readme = read_text("skills/figure-recommender/README.md")

    assert zh_readme_path.exists()
    zh_readme = zh_readme_path.read_text(encoding="utf-8")

    assert "[简体中文](README_CN.md)" in root_readme
    assert "[English](README.md)" in zh_readme
    assert "FigureClaw.png" in root_readme
    assert "FigureClaw.png" in zh_readme
    assert "60-Second Quick Start" in root_readme
    assert "60 秒快速上手" in zh_readme

    assert "setup.md" in root_readme
    assert "## Install With Codex" in root_readme
    assert "## Install With Claude" in root_readme
    assert "## Install With Dr. Claw" in root_readme
    assert "https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md" in root_readme
    assert "https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md" in root_readme

    assert "~/.codex/skills/" in skill_readme
    assert "~/.claude/skills/" in skill_readme
    assert "Dr. Claw" in skill_readme
    assert "examples/briefs/" in skill_readme


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
