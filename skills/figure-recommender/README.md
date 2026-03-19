# Figure Recommender Skill

Self-contained skill package for structured scientific figure selection, palette recommendation, and Python plotting code generation.

## What It Does

- Accepts a structured `figure_brief`
- Chooses a primary chart and optional fallback
- Selects a palette mode
- Emits Tier 1 Python plotting code from local templates

## Package Contents

- `SKILL.md`
- `references/`
- `templates/`
- `examples/`
- `scripts/`

## Build Zip Package

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```

This writes `dist/figure-recommender.zip`.

## Use the Generator Directly

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-json '{"id":"fig-01","story_goal":"compare_group_difference","data_shape":"grouped_metric","field_mapping":{"category":"condition","value":"score"},"figure_role":"paper-main","style_mode":"readable","palette_mode":"paper-neutral"}' \
  --output json
```

Pass a single `figure_brief` object, not the whole fixtures array in `examples/figure_briefs.json`.

## Installation Paths

- Dr. Claw: upload the generated zip in the Skills UI
- Local agent setup: copy the `figure-recommender/` folder into `~/.claude/skills/`
