# FigureClaw

FigureClaw is a portable scientific figure skill package centered on
`figure-recommender`: a structured figure recommendation and Python codegen
skill for paper figures, supplementary figures, and analysis plots.

## Fastest Setup

Ask your agent to read the unified setup guide:

`Read https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/setup.md and set up FigureClaw for me.`

## What It Ships

- `skills/figure-recommender`
  - Structured `figure_brief -> chart selection -> palette -> Python plotting code`
  - Tier 1 template-driven code generation
  - Tier 2 and Tier 3 recommendation plus fallback behavior
  - Self-contained references, templates, examples, and packaging scripts

## Why This Repo Exists

The goal is to make one scientific plotting skill installable in multiple agent
environments without changing the runtime logic:

- Codex can install it from a raw `INSTALL.md`
- Claude Code can install it from a Claude-specific `INSTALL.md`
- Dr. Claw can import the packaged zip directly
- Users who prefer manual setup can copy or symlink the skill folder themselves

## Core Workflow

1. Accept a structured `figure_brief`
2. Select the best supported figure type
3. Choose a palette mode
4. Return a fixed six-section response
5. Emit runnable Tier 1 Python plotting code from local templates

## Tier 1 Charts

These chart families currently ship direct code generation support:

- Contrast dot plot
- Stacked bar chart
- Raincloud plot
- Line chart
- Multi-series trend chart
- Heatmap
- Benchmark scatter plot with error bars
- Correlation network heatmap

## Palette Modes

- `paper-neutral`
- `paper-emphasis`
- `sequential`
- `diverging`
- `presentation-bold`

## Quick Start

Run the generator directly:

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

Build the Dr. Claw import package:

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```

## Install With Codex

Paste this into Codex:

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md`

Manual path target:

`~/.codex/skills/figure-recommender`

## Install With Claude

Paste this into Claude Code:

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md`

Manual path target:

`~/.claude/skills/figure-recommender`

## Install With Dr. Claw

1. Run `python3 skills/figure-recommender/scripts/package_skill.py`
2. Upload the generated `dist/figure-recommender.zip` in the Dr. Claw Skills UI
3. Let Dr. Claw discover the packaged `SKILL.md`, templates, and references

## Skill Contract

Input brief fields:

- `story_goal`
- `field_mapping`
- `id`
- `data_shape`
- `figure_role`
- `style_mode`
- `palette_mode`

Defaults:

- `figure_role = paper-main`
- `style_mode = readable`
- `palette_mode = auto`

Output sections:

- `Primary figure`
- `Optional fallback`
- `Palette`
- `Dependencies`
- `Python code`
- `Adaptation notes`

## Repository Layout

- `skills/figure-recommender/`: skill package
- `.codex/INSTALL.md`: Codex installation entrypoint
- `.claude/INSTALL.md`: Claude Code installation entrypoint
- `setup.md`: unified agent-readable setup entrypoint
- `tests/`: fixture and packaging tests
- `docs/`: plans, specs, and project notes

## Development

Run the full test suite:

```bash
python3 -m pytest tests -q
```

Rebuild the zip package:

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```
