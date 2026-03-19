# Codex-First Skill Hardening Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the FigureClaw skill distribution noticeably easier to install and verify in Codex, while keeping Claude Code and Dr. Claw compatible.

**Architecture:** Keep the executable-first runtime unchanged where possible and harden the distribution surface around it. Concentrate this pass on top-level entry docs, the Codex install guide, the skill contract, and package/install regression tests so the skill can be installed, verified, and debugged with fewer ambiguous steps.

**Tech Stack:** Markdown documentation, Python test suite, zip packaging script, existing figure runtime scripts

---

## Chunk 1: Tighten install and package regression tests

### Task 1: Expand install doc assertions around Codex-first flow

**Files:**
- Modify: `tests/test_install_docs.py`

- [ ] **Step 1: Write the failing test**

Add assertions that require:
- top-level `README.md` to promote `setup.md` as the primary entrypoint
- top-level `README.md` to include a collapsed/manual-install section
- `setup.md` to list Codex first and require a shared smoke test
- `.codex/INSTALL.md` to document success criteria and failure recovery
- a simulated Codex install layout to successfully run the documented smoke test

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_install_docs.py -q`
Expected: FAIL because the current docs do not yet contain the tightened Codex-first wording.

- [ ] **Step 3: Write minimal implementation**

Update the relevant Markdown docs and install verification coverage so the new assertions hold without changing unrelated user-facing behavior.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_install_docs.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_install_docs.py README.md README_CN.md setup.md .codex/INSTALL.md
git commit -m "docs: harden codex-first install flow"
```

### Task 2: Expand package assertions for required and forbidden zip contents

**Files:**
- Modify: `tests/test_skill_package.py`

- [ ] **Step 1: Write the failing test**

Add assertions that the zip package contains the manifest-listed runtime assets and excludes repo-level files and source assets such as `docs/source-audits/`, `tests/`, and `Figures/`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_skill_package.py -q`
Expected: FAIL until the test reflects the intended package contract and the package script/output are validated against it.

- [ ] **Step 3: Write minimal implementation**

If needed, tighten package expectations or supporting docs so the packaged skill matches the intended distribution boundary.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_skill_package.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_skill_package.py skills/figure-recommender/package-manifest.json skills/figure-recommender/scripts/package_skill.py skills/figure-recommender/README.md
git commit -m "test: lock skill package boundary"
```

## Chunk 2: Tighten skill-facing documentation and contract

### Task 3: Tighten the skill contract and package README

**Files:**
- Modify: `skills/figure-recommender/SKILL.md`
- Modify: `skills/figure-recommender/README.md`
- Modify: `README.md`
- Modify: `README_CN.md`
- Modify: `setup.md`
- Modify: `.codex/INSTALL.md`

- [ ] **Step 1: Write the failing test**

Add assertions that require the skill contract to:
- infer a minimal brief before script execution when the user provides only natural language
- forbid fabricating direct code when no Tier 1 template exists
- keep the package README focused on packaged-skill boundaries instead of repo landing-page behavior

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_install_docs.py tests/test_skill_package.py -q`
Expected: FAIL because the current skill/package docs do not yet express all of these constraints.

- [ ] **Step 3: Write minimal implementation**

Update `SKILL.md`, the skill README, and the top-level Codex-facing docs so agent behavior, package responsibilities, and install/onboarding responsibilities are explicit and consistent with the runtime contract.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_install_docs.py tests/test_skill_package.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add README.md README_CN.md setup.md .codex/INSTALL.md skills/figure-recommender/SKILL.md skills/figure-recommender/README.md tests/test_install_docs.py tests/test_skill_package.py
git commit -m "docs: tighten codex-first skill onboarding"
```

## Chunk 3: Full verification

### Task 4: Run end-to-end verification for docs, packaging, and runtime smoke test

**Files:**
- Verify: `tests/test_install_docs.py`
- Verify: `tests/test_skill_package.py`
- Verify: `tests/test_figure_codegen.py`
- Verify: `skills/figure-recommender/scripts/generate_figure_response.py`
- Verify: `skills/figure-recommender/scripts/package_skill.py`

- [ ] **Step 1: Run the targeted regression suite**

Run: `python3 -m pytest tests/test_install_docs.py tests/test_skill_package.py tests/test_figure_codegen.py -q`
Expected: PASS

- [ ] **Step 2: Run the packaged skill build**

Run: `python3 skills/figure-recommender/scripts/package_skill.py`
Expected: prints a zip path under `dist/`

- [ ] **Step 3: Run the shared smoke test**

Run: `python3 skills/figure-recommender/scripts/generate_figure_response.py --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json --output json`
Expected: exit code `0`, output includes `primary_chart`, `python_code`, and `contrast_dot`

- [ ] **Step 4: Run the full test suite**

Run: `python3 -m pytest tests -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/plans/2026-03-19-codex-first-skill-hardening.md
git commit -m "docs: add codex-first skill hardening plan"
```
