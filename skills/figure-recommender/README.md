# Figure Recommender Skill

Self-contained skill package for structured scientific figure selection, palette recommendation, and Python plotting code generation.

This README documents the packaged skill boundary.

Start from the unified setup guide at repository root `setup.md` when installing through an agent for the first time.

## What It Does

- Accepts a structured `figure_brief`
- Chooses a primary chart and optional fallback
- Selects a palette mode
- Emits Tier 1 Python plotting code from local templates

## Input Contract

Required fields:

- `story_goal`
- `field_mapping`

Optional fields:

- `id`
- `data_shape`
- `figure_role`
- `style_mode`
- `palette_mode`
- `candidate_chart_types`
- `notes`

## Output Contract

The generated response is organized into these sections:

- `Primary figure`
- `Optional fallback`
- `Palette`
- `Dependencies`
- `Python code`
- `Adaptation notes`

## Tier 1 Charts

The packaged templates currently support direct code generation for:

- `contrast_dot`
- `stacked_bar`
- `raincloud`
- `line`
- `multi_trend`
- `heatmap`
- `benchmark_scatter_error`
- `correlation_network`

## Palette Modes

- `paper-neutral`
- `paper-emphasis`
- `sequential`
- `diverging`
- `presentation-bold`

## Package Contents

- `SKILL.md`
- `references/`
- `templates/`
- `examples/`
- `scripts/`

The zip package intentionally excludes `tests/`, `docs/source-audits/`, and `Figures/`.

## Build Zip Package

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```

This writes `dist/figure-recommender.zip`.

## Use the Generator Directly

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

Pass a single `figure_brief` object. Starter examples live under `examples/briefs/`.

## Install With Codex

1. Clone the repository
2. Link `skills/figure-recommender/` into `~/.codex/skills/figure-recommender`
3. Restart Codex
4. Re-run the shared smoke test from the repository root

Or ask Codex to fetch:

`https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md`

## Install With Claude

1. Clone the repository
2. Link `skills/figure-recommender/` into `~/.claude/skills/figure-recommender`
3. Restart Claude Code

Or ask Claude Code to fetch:

`https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md`

## Install With Dr. Claw

Build the zip and upload it in the Skills UI:

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```

## Verify

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json

python3 -m pytest tests -q
python3 skills/figure-recommender/scripts/package_skill.py
```
