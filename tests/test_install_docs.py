from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_platform_install_guides_exist_and_use_expected_skill_paths() -> None:
    codex_install = read_text(".codex/INSTALL.md")
    claude_install_path = REPO_ROOT / ".claude" / "INSTALL.md"

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
    skill_readme = read_text("skills/figure-recommender/README.md")

    assert "## Install With Codex" in root_readme
    assert "## Install With Claude" in root_readme
    assert "## Install With Dr. Claw" in root_readme
    assert "https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md" in root_readme
    assert "https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md" in root_readme

    assert "~/.codex/skills/" in skill_readme
    assert "~/.claude/skills/" in skill_readme
    assert "Dr. Claw" in skill_readme
