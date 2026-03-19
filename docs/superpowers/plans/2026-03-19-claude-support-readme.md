# FigureClaw Claude Support and README Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Claude installation support and richer repository documentation for FigureClaw without changing the skill runtime behavior.

**Architecture:** Keep the skill package unchanged and add a Claude-specific install entrypoint alongside the existing Codex entrypoint. Verify the documentation contract with lightweight tests that assert required install sections and platform paths are present.

**Tech Stack:** Markdown, pytest, git

---

## Chunk 1: Add coverage for install docs

### Task 1: Create failing documentation tests

**Files:**
- Create: `tests/test_install_docs.py`
- Test: `tests/test_install_docs.py`

- [ ] **Step 1: Write the failing test**

Add assertions for:
- `.claude/INSTALL.md` existence and `~/.claude/skills/figure-recommender`
- `.codex/INSTALL.md` retaining `~/.codex/skills/figure-recommender`
- root `README.md` mentioning Codex, Claude, and Dr. Claw install sections
- `skills/figure-recommender/README.md` mentioning both local install paths

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_install_docs.py -q`
Expected: FAIL because `.claude/INSTALL.md` does not exist and README coverage is incomplete.

## Chunk 2: Implement documentation and entrypoints

### Task 2: Add Claude install entrypoint

**Files:**
- Create: `.claude/INSTALL.md`
- Modify: `.codex/INSTALL.md`

- [ ] **Step 1: Write minimal implementation**

Add a Claude installation guide mirroring the Codex flow but targeting
`~/.claude/skills/figure-recommender`. Keep the Codex install guide aligned in
tone and notes.

- [ ] **Step 2: Run tests**

Run: `python3 -m pytest tests/test_install_docs.py -q`
Expected: some assertions may still fail until README updates land.

### Task 3: Expand repository README

**Files:**
- Modify: `README.md`
- Modify: `skills/figure-recommender/README.md`

- [ ] **Step 1: Write minimal implementation**

Expand both READMEs to cover:
- what the repository ships
- supported installation targets
- direct CLI usage
- package layout
- verification commands

- [ ] **Step 2: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_install_docs.py -q`
Expected: PASS

## Chunk 3: Full verification

### Task 4: Run full regression checks

**Files:**
- Test: `tests/test_install_docs.py`
- Test: `tests/test_skill_package.py`
- Test: `tests/test_figure_codegen.py`

- [ ] **Step 1: Run the full test suite**

Run: `python3 -m pytest tests -q`
Expected: PASS

- [ ] **Step 2: Rebuild the skill zip**

Run: `python3 skills/figure-recommender/scripts/package_skill.py`
Expected: prints a valid zip path under `dist/`
