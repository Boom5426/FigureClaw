---
name: figure-recommender
description: Use when the user wants a structured scientific figure recommendation, palette selection, and Python plotting code generated from local templates.
---

# Figure Recommender

Select a scientific figure, pick a palette, and generate Tier 1 Python plotting code from self-contained templates shipped with this skill.

## When to Use

Use this skill when the user:
- has a plotting need that can be described as a structured `figure_brief`
- wants a paper figure or supplement figure mapped to a recommended chart type
- wants a plotting script instead of only prose guidance
- needs palette selection bundled with the recommendation

Do not use this skill as the primary workflow when the user:
- already has a plotting script and only needs debugging
- wants a full tutorial on Matplotlib, Seaborn, or Jupyter
- wants non-data illustration generation; use `inno-figure-gen` for that

## Workflow

1. Read `references/figure-recommender.md`.
2. Prefer a structured `figure_brief` with these required fields:
   - `id`
   - `story_goal`
   - `data_shape`
   - `field_mapping`
   - `figure_role`
   - `style_mode`
   - `palette_mode`
   - optional `candidate_chart_types`
   - optional `notes`
3. If the user only gives natural language, infer the brief and state assumptions briefly.
4. Run the local helper:
   - `python3 scripts/generate_figure_response.py --brief-json '<json>'`
   - or `python3 scripts/generate_figure_response.py --brief-file <path>`
5. Use the helper output as the default response. Do not freestyle code if a Tier 1 template exists.
6. If the primary chart is Tier 2 or Tier 3, explain that direct codegen is not shipped for that chart in v1 and use the fallback code the helper returns.
7. If the request is in English, answer in English. Otherwise default to Chinese.

## Output Contract

The response must contain these 6 sections in this order:

```text
Primary figure
Optional fallback
Palette
Dependencies
Python code
Adaptation notes
```

## Quality Rules

- Prefer Tier 1 charts when two options are equally valid.
- Never fabricate code for a chart that is not shipped with a local template.
- Keep notebook source paths exact, for example `Awesome-Scientific-Figures/热力图.ipynb`.
- Keep dependency lists constrained to the local template backend.
- If a high-complexity chart is requested, recommend it only when the data structure clearly warrants it.

## Reference Map

Load these files:

- `references/figure-recommender.md` -> high-level usage, `figure_brief` contract, and chart-selection policy
- `references/chart-registry.json` -> chart metadata, support level, fallback, backend, and template path
- `references/palette-registry.json` -> palette modes and color lists

Use these runtime assets:

- `templates/*.py.tmpl` -> Tier 1 code templates
- `scripts/generate_figure_response.py` -> selector + renderer
