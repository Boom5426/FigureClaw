# FigureClaw Executable-First Figure Recommender Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework FigureClaw into an executable-first skill package with audited chart sources, strict runtime contracts, ranked chart selection, and a unified setup/onboarding flow.

**Architecture:** Start with a local source audit that converts the notebook sources used by the current registry into committed audit artifacts, then move the runtime from a single permissive script into a small strict module tree. After the runtime behavior is corrected, reorganize examples, setup docs, and packaging so user-facing assets align with the executable-first contract.

**Tech Stack:** Python, pytest, Markdown, JSON, zip packaging, git

---

## Chunk 1: Audit Chart Sources Before Changing Behavior

### Task 1: Add failing tests for committed audit artifacts

**Files:**
- Create: `tests/test_source_audit.py`
- Test: `tests/test_source_audit.py`

- [ ] **Step 1: Write the failing test**

Add assertions that:
- a committed audit index exists
- the audit covers every chart registry entry whose `source_notebook` points into `Figures/`
- committed exported `.py` snapshots exist for the current registry-backed notebooks
- the audit marks each chart with one of `keep`, `rename`, `demote`, or `drop`

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_source_audit.py -q`
Expected: FAIL because the audit index and exported notebook snapshots do not exist yet.

### Task 2: Implement notebook export and audit artifacts

**Files:**
- Create: `skills/figure-recommender/scripts/export_source_notebooks.py`
- Create: `docs/source-audits/2026-03-19-chart-source-audit.md`
- Create: `docs/source-audits/chart-source-audit.json`
- Create: `docs/source-audits/notebooks/对比点图.py`
- Create: `docs/source-audits/notebooks/堆叠柱状图.py`
- Create: `docs/source-audits/notebooks/云雨图.py`
- Create: `docs/source-audits/notebooks/折线图.py`
- Create: `docs/source-audits/notebooks/多变量变化趋势图.py`
- Create: `docs/source-audits/notebooks/热力图.py`
- Create: `docs/source-audits/notebooks/散点图_误差棒组合图.py`
- Create: `docs/source-audits/notebooks/相关性网络热图.py`
- Create: `docs/source-audits/notebooks/旭日图.py`
- Create: `docs/source-audits/notebooks/弦图.py`
- Create: `docs/source-audits/notebooks/配色.py`
- Modify: `skills/figure-recommender/references/chart-registry.json`
- Test: `tests/test_source_audit.py`

- [ ] **Step 1: Write minimal implementation**

Create an exporter that:
- reads local notebook sources from `Figures/`
- emits a plain `.py` snapshot per audited notebook under `docs/source-audits/notebooks/`
- writes a machine-readable `chart-source-audit.json`
- writes a narrative `2026-03-19-chart-source-audit.md`

Use the audit to flag any current chart ids that are semantically misnamed,
over-promoted, or incompatible with their source notebooks.

- [ ] **Step 2: Run the exporter**

Run: `python3 skills/figure-recommender/scripts/export_source_notebooks.py --source-dir Figures --output-dir docs/source-audits`
Expected: PASS and create the audit JSON, audit markdown, and exported notebook `.py` snapshots.

- [ ] **Step 3: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_source_audit.py -q`
Expected: PASS

## Chunk 2: Tighten the Runtime Contract Before Changing Selection

### Task 3: Add failing tests for strict brief validation and error semantics

**Files:**
- Create: `tests/test_brief_validation.py`
- Test: `tests/test_brief_validation.py`

- [ ] **Step 1: Write the failing test**

Cover these behaviors:
- `--brief-file` rejects arrays
- unknown `story_goal` is rejected
- unknown `palette_mode` is rejected
- incompatible explicit palette is rejected
- missing chart-required fields are rejected before template rendering
- error messages mention the concrete missing or invalid keys

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_brief_validation.py -q`
Expected: FAIL because the current runtime silently falls back or errors too late.

### Task 4: Split the runtime into strict internal modules

**Files:**
- Create: `skills/figure-recommender/scripts/figure_runtime/__init__.py`
- Create: `skills/figure-recommender/scripts/figure_runtime/contracts.py`
- Create: `skills/figure-recommender/scripts/figure_runtime/errors.py`
- Create: `skills/figure-recommender/scripts/figure_runtime/registry.py`
- Create: `skills/figure-recommender/scripts/figure_runtime/validation.py`
- Create: `skills/figure-recommender/scripts/figure_runtime/render.py`
- Modify: `skills/figure-recommender/scripts/generate_figure_response.py`
- Modify: `skills/figure-recommender/references/figure-recommender.md`
- Test: `tests/test_brief_validation.py`

- [ ] **Step 1: Write minimal implementation**

Move the runtime into internal modules that:
- parse draft input
- normalize it into a canonical brief
- validate enums and required fields
- raise user-facing contract errors
- render templates only after validation succeeds

Keep `generate_figure_response.py` as the CLI adapter.

- [ ] **Step 2: Run the validation tests to verify they pass**

Run: `python3 -m pytest tests/test_brief_validation.py -q`
Expected: PASS

## Chunk 3: Replace Hardcoded Selection With Executable-First Ranking

### Task 5: Add failing tests for executable-first selection

**Files:**
- Create: `tests/test_chart_selection.py`
- Modify: `tests/test_figure_codegen.py`
- Create: `tests/fixtures/figure_cases.json`
- Test: `tests/test_chart_selection.py`
- Test: `tests/test_figure_codegen.py`

- [ ] **Step 1: Write the failing test**

Cover these behaviors:
- default `paper-main` and `readable` requests choose an executable Tier 1 primary chart
- explicit `candidate_chart_types` may request a non-Tier-1 conceptual chart
- unsupported conceptual requests still emit executable code from a supported chart
- output only includes conceptual chart metadata when the user explicitly asked for a non-executable chart

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_chart_selection.py tests/test_figure_codegen.py -q`
Expected: FAIL because current selection is hardcoded and does not distinguish conceptual vs executable selection.

### Task 6: Implement ranked candidate selection and the updated output contract

**Files:**
- Create: `skills/figure-recommender/scripts/figure_runtime/selection.py`
- Modify: `skills/figure-recommender/references/chart-registry.json`
- Modify: `skills/figure-recommender/scripts/generate_figure_response.py`
- Modify: `skills/figure-recommender/scripts/figure_runtime/contracts.py`
- Modify: `skills/figure-recommender/scripts/figure_runtime/registry.py`
- Modify: `skills/figure-recommender/scripts/figure_runtime/validation.py`
- Modify: `skills/figure-recommender/scripts/figure_runtime/render.py`
- Modify: `skills/figure-recommender/references/figure-recommender.md`
- Modify: `tests/test_chart_selection.py`
- Modify: `tests/test_figure_codegen.py`
- Modify: `tests/fixtures/figure_cases.json`
- Test: `tests/test_chart_selection.py`
- Test: `tests/test_figure_codegen.py`

- [ ] **Step 1: Write minimal implementation**

Implement candidate discovery, filtering, and ranking using registry metadata:
- executable charts rank ahead of unsupported charts
- role/style compatibility affects ranking
- lower visual complexity wins when otherwise equivalent
- explicit candidate charts limit the search space

Update the output contract so the normal path returns an executable primary
chart, and unsupported conceptual charts appear only when explicitly requested.

- [ ] **Step 2: Run the selection tests**

Run: `python3 -m pytest tests/test_chart_selection.py tests/test_figure_codegen.py -q`
Expected: PASS

## Chunk 4: Rebuild Examples, Setup, Docs, and Packaging Around the New Contract

### Task 7: Add failing tests for setup docs, examples, and package manifest consistency

**Files:**
- Modify: `tests/test_install_docs.py`
- Modify: `tests/test_skill_package.py`
- Test: `tests/test_install_docs.py`
- Test: `tests/test_skill_package.py`

- [ ] **Step 1: Write the failing test**

Add assertions that:
- a root `setup.md` exists and references Codex, Claude Code, and Dr. Claw
- user-facing examples are stored as single brief JSON files under `skills/figure-recommender/examples/briefs/`
- package manifest contents match the generated zip
- install docs and README point to the new setup and example paths

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_install_docs.py tests/test_skill_package.py -q`
Expected: FAIL because setup docs, examples, and manifest-driven packaging are not implemented yet.

### Task 8: Implement setup entrypoint, example split, and manifest-driven packaging

**Files:**
- Create: `setup.md`
- Create: `skills/figure-recommender/package-manifest.json`
- Create: `skills/figure-recommender/examples/briefs/grouped-comparison.json`
- Create: `skills/figure-recommender/examples/briefs/matrix-pattern.json`
- Create: `skills/figure-recommender/examples/briefs/benchmark-tradeoff.json`
- Create: `skills/figure-recommender/examples/briefs/network-relations.json`
- Create: `skills/figure-recommender/examples/briefs/hierarchy-conceptual-request.json`
- Modify: `skills/figure-recommender/scripts/package_skill.py`
- Modify: `README.md`
- Modify: `skills/figure-recommender/README.md`
- Modify: `.codex/INSTALL.md`
- Modify: `.claude/INSTALL.md`
- Modify: `tests/test_install_docs.py`
- Modify: `tests/test_skill_package.py`
- Modify: `tests/fixtures/figure_cases.json`
- Delete: `skills/figure-recommender/examples/figure_briefs.json`
- Test: `tests/test_install_docs.py`
- Test: `tests/test_skill_package.py`

- [ ] **Step 1: Write minimal implementation**

Implement the user-facing asset reorganization:
- add `setup.md` as the unified remote-readable setup entrypoint
- move user examples to `examples/briefs/*.json`
- move test-only expected fixtures to `tests/fixtures/figure_cases.json`
- switch packaging to a manifest-driven file list with validation
- update all docs to point at the executable-first setup path and the new examples

- [ ] **Step 2: Run docs and packaging tests to verify they pass**

Run: `python3 -m pytest tests/test_install_docs.py tests/test_skill_package.py -q`
Expected: PASS

## Chunk 5: Full Regression and Smoke Verification

### Task 9: Run the complete verification set

**Files:**
- Test: `tests/test_source_audit.py`
- Test: `tests/test_brief_validation.py`
- Test: `tests/test_chart_selection.py`
- Test: `tests/test_figure_codegen.py`
- Test: `tests/test_install_docs.py`
- Test: `tests/test_skill_package.py`

- [ ] **Step 1: Run the full test suite**

Run: `python3 -m pytest tests -q`
Expected: PASS

- [ ] **Step 2: Build the package**

Run: `python3 skills/figure-recommender/scripts/package_skill.py`
Expected: PASS and print a zip path under `dist/`.

- [ ] **Step 3: Run a minimal executable-first smoke test**

Run: `python3 skills/figure-recommender/scripts/generate_figure_response.py --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json --output json`
Expected: PASS and return JSON whose `primary_chart` is executable and whose `python_code` is non-empty.
