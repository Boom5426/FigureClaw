# FigureClaw Executable-First Rearchitecture Design

## Goal

Refactor FigureClaw so first-time users can install it quickly, get a runnable
figure recommendation immediately, and grow into stricter control only when
they need it. The default product behavior should be executable-first: the
primary figure is the best chart that ships runnable code, while stricter
runtime validation and clearer installation/docs reduce ambiguity for advanced
users and maintainers.

## Scope

- Reframe the product around executable-first figure recommendation
- Add a Phase 0 audit of notebook sources under `Figures/`
- Split user-facing input flow from strict runtime validation
- Replace the current hardcoded primary-chart selection with ranked candidate
  selection
- Tighten error semantics for briefs, palettes, and chart compatibility
- Reorganize examples, packaging, and install flows around a minimal
  success-first path
- Introduce a unified remote `setup.md` entrypoint for agent-driven setup
- Expand tests to cover negative cases, selection policy, and package
  consistency

## Non-Goals

- No attempt to support every notebook in `Figures/` in this pass
- No natural-language parsing inside the strict CLI runtime
- No generalized plugin system for arbitrary external chart registries
- No full UI or web app; this remains a skill package plus local helper tooling
- No promise that every current chart id survives unchanged if the audit shows a
  semantic mismatch

## Product Model

The current repository mixes two different products:

- an agent-facing skill that should feel easy to use from natural language or
  partial structure
- a maintainer-facing CLI/runtime that must be deterministic, strict, and easy
  to test

The redesign separates those concerns.

### User-Facing Layer

This layer is intentionally forgiving. Users should be able to:

- install the skill from one setup entrypoint
- run one minimal example immediately
- describe a figure in natural language or partial structure through an agent
- see a primary figure that matches the code they actually receive

This layer is where assumptions may be inferred and stated.

### Runtime Layer

This layer is intentionally strict. Once input reaches the runtime, it should:

- accept exactly one brief object
- normalize it into one canonical internal representation
- validate all enums and chart compatibility rules
- choose charts deterministically
- render code or fail with a precise contract error

The runtime should never silently rewrite invalid input in a way that hides user
mistakes.

## Default Behavior

### Executable-First Primary Figure

The default `primary_chart` must be the chart that the system can actually turn
into runnable code now. Unsupported or style-heavy charts may still be exposed,
but they should not be the default primary recommendation unless the user
explicitly asks for them.

This fixes the current confusion where the response can recommend one chart but
emit code for another chart.

### Unsupported Charts

Tier 2 and Tier 3 charts remain useful, but they move out of the default path:

- if the user does not explicitly request them, they should influence guidance
  only when useful in notes or alternatives
- if the user explicitly requests them through `candidate_chart_types`, the
  response may return both:
  - a conceptual chart the user asked for
  - an executable primary chart used for code generation

### Fallback Semantics

`fallback_chart` should mean a real alternate executable path, not "the chart we
actually used because the primary chart was never executable."

For common success cases, the response should stay simple:

- `primary_chart`
- optional `fallback_chart`
- optional `conceptual_chart` only when the user explicitly asked for a more
  complex unsupported chart

## Phase 0: Notebook Source Audit

Before changing selection logic, audit the notebook sources in `Figures/`
against the current registry and templates.

### Audit Scope

Audit only the notebooks directly referenced by the current registry, plus the
palette notebook used to reason about color guidance. Do not expand to all 23
notebooks in this phase.

### Audit Outputs

Produce two outputs:

- exported `.py` snapshots of audited notebooks in a dedicated audit directory
- a chart audit matrix recording, per chart:
  - source notebook
  - current chart id
  - actual visual grammar
  - actual backend dependencies
  - actual data shape
  - whether the current template is semantically equivalent
  - conclusion: `keep`, `rename`, `demote`, or `drop`

### Audit Decision Rules

- `keep`: the shipped template is a faithful simplified version of the source
- `rename`: the template is close, but the current name or brief contract is
  misleading
- `demote`: the source is too style-heavy or too bespoke to promise as a normal
  executable-first chart
- `drop`: the current template is no longer the same chart in practical terms

This audit is required because some current mappings appear semantically
misaligned.

## Input Contract

### External Draft Brief

Users and agents should be allowed to start from a lightweight draft object:

- required:
  - `story_goal`
  - `field_mapping`
- optional:
  - `id`
  - `data_shape`
  - `figure_role`
  - `style_mode`
  - `palette_mode`
  - `candidate_chart_types`
  - `notes`

Defaults:

- `figure_role = paper-main`
- `style_mode = readable`
- `palette_mode = auto`
- `id = generated if omitted`

### Canonical Runtime Brief

The runtime should operate only on a canonical normalized brief. By the time the
renderer runs, the brief must have:

- resolved defaults
- validated enum values
- resolved or validated `data_shape`
- known chart compatibility
- explicit `palette_mode`
- a stable `id`

### Runtime Rules

- `--brief-json` and `--brief-file` accept exactly one object, never an array
- unknown enum values fail immediately
- unknown chart ids in `candidate_chart_types` fail immediately
- if `data_shape` is omitted and cannot be inferred unambiguously, fail
- after `code_chart` is selected, validate its required fields before rendering

## Error Model

Errors should be contract-level and actionable.

Examples:

- unknown `story_goal`
- unknown `figure_role`
- unknown `style_mode`
- unknown `palette_mode`
- input file contains an array instead of one brief object
- selected chart requires missing field mappings
- palette is incompatible with the selected chart

Errors should avoid leaking internal template mechanics. Messages should point to
the fix and, when possible, to the nearest minimal example brief.

## Selection Architecture

Replace the current hardcoded "story goal maps directly to one chart" logic with
candidate selection plus ranking.

### Candidate Discovery

Candidates should be built from registry data using:

- `story_goal`
- `data_shape`
- explicit `candidate_chart_types` when provided

### Candidate Filtering

Filter candidates by:

- required fields that can be satisfied
- role compatibility
- style compatibility
- whether the chart is allowed to auto-select

### Ranking

Sort candidates by:

1. executable support first
2. better field compatibility
3. role compatibility
4. style compatibility
5. lower visual complexity
6. explicit registry tie-breaker priority

The top ranked executable candidate becomes the default `primary_chart`.

### Registry Extensions

Extend chart registry entries with lightweight metadata:

- `selection_priority`
- `visual_complexity`
- `recommended_roles`
- `allowed_style_modes`
- `auto_selectable`

Keep the registry readable and hand-editable; do not turn it into a general
rules engine.

## Output Contract

For the normal executable-first path, return:

- `primary_chart`
- optional `fallback_chart`
- `palette`
- `dependencies`
- `python_code`
- `adaptation_notes`

Only return `conceptual_chart` when the user explicitly requested a non-Tier-1
chart that cannot be rendered directly.

The default output should minimize cognitive load for first-time users.

## Code Structure

Keep the CLI entrypoint thin and move runtime logic into a small internal module
tree under `skills/figure-recommender/scripts/figure_runtime/`.

Suggested modules:

- `contracts.py`: brief types, enums, normalization helpers
- `errors.py`: user-facing contract errors and exit behavior
- `registry.py`: chart/palette/template loading
- `selection.py`: candidate discovery, filtering, ranking
- `validation.py`: field, palette, and compatibility validation
- `render.py`: placeholder building and template rendering

`generate_figure_response.py` should become an adapter around those modules.

## Examples and Assets

Split examples into two different audiences.

### User Examples

Create `skills/figure-recommender/examples/briefs/*.json` where each file is:

- a single brief object
- directly runnable with the CLI
- named for a real usage goal

These examples should be referenced by README, `setup.md`, and error messages.

### Test Fixtures

Move expected-output fixtures into `tests/fixtures/`. These files may include:

- expected primary chart
- expected conceptual chart
- expected fallback chart
- expected error class or message

User examples must not double as test fixture containers.

## Setup and Installation

Add a unified remote-readable `setup.md` entrypoint.

The intended agent workflow becomes:

`Read <repo>/setup.md and set up FigureClaw for me.`

### setup.md Responsibilities

- detect or ask for target environment: Codex, Claude Code, or Dr. Claw
- route to the correct local install path or package flow
- run a post-install verification step
- run one minimal example
- give the user a small set of next-step prompts

### Platform Install Docs

Keep:

- `.codex/INSTALL.md`
- `.claude/INSTALL.md`

But treat them as subordinate install playbooks referenced by `setup.md`, not as
the only top-level onboarding path.

## Packaging

Replace the static package include list with a manifest-driven approach.

The package build should validate before archiving:

- every referenced template exists
- every referenced runtime file exists
- required examples exist
- registry/template references are internally consistent

The archive contents should reflect the actual runtime contract and docs, not a
manually maintained subset that can drift.

## Documentation Strategy

### Root README

The root README should become the fastest path to first success:

- what FigureClaw is
- the one-line setup prompt using `setup.md`
- a shortest possible example
- links to advanced docs

### Skill README

The skill README should focus on:

- minimal runnable brief
- common story goals
- how to move from natural language to a structured brief
- strict CLI usage for advanced users

### Reference Doc

`references/figure-recommender.md` should become the source of truth for:

- canonical brief contract
- selection rules
- role/style behavior
- error semantics
- chart capability distinctions

## Verification Strategy

Tests must cover both success and failure paths.

### Selection Tests

- executable-first defaults for normal cases
- explicit unsupported chart requests return conceptual metadata correctly
- role/style influence selection as documented

### Validation Tests

- array input rejected
- unknown enum values rejected
- unknown candidate charts rejected
- missing required fields rejected before rendering
- incompatible palette rejected

### Rendering Tests

- generated code parses
- generated code executes with dummy data for supported charts
- unresolved placeholders never escape into output

### Packaging and Docs Tests

- package manifest and archive contents are consistent
- registry references shipped assets correctly
- README, setup docs, and install docs point at valid example and install paths

## Risks

- the audit may reveal that some currently shipped chart ids are wrong and need
  renaming or demotion
- stricter validation is a breaking change for callers who currently rely on
  silent fallback behavior
- adding `conceptual_chart` only for explicit unsupported requests requires
  careful migration in tests and docs
- packaging and docs can drift again unless manifest and tests remain the source
  of truth

## Recommended Rollout Order

1. Audit notebook sources and write the chart audit matrix
2. Reconcile registry entries and chart tiers based on the audit
3. Introduce canonical brief normalization and strict contract errors
4. Replace hardcoded selection with ranked candidate selection
5. Restructure examples, docs, and `setup.md`
6. Move package build to manifest validation
7. Expand the test suite and remove obsolete fixtures
