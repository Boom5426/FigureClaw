# Set Up FigureClaw

Read this file and set up FigureClaw for me in the current environment.

## What this installs

FigureClaw installs the `figure-recommender` skill package for executable-first
scientific figure recommendation and Python code generation.

## Primary path

If you are in Codex, start here first.

1. Fetch and follow `.codex/INSTALL.md`
2. Verify the skill exists at `~/.codex/skills/figure-recommender`
3. Run the shared smoke test from the cloned repository root

## Other supported environments

- Claude Code
- Dr. Claw

### Claude Code

1. Follow instructions in `.claude/INSTALL.md`
2. Verify the skill exists at `~/.claude/skills/figure-recommender`

### Dr. Claw

1. Run `python3 skills/figure-recommender/scripts/package_skill.py`
2. Upload `dist/figure-recommender.zip`

## Shared smoke test

Run:

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

Confirm the response contains:

- `"primary_chart"`
- `"contrast_dot"`
- `"python_code"`

## First use

- Ask for the skill with a natural-language plotting goal and let the agent infer the draft brief.
- For strict CLI usage, start from `skills/figure-recommender/examples/briefs/`.
- Prefer executable-first defaults unless you explicitly request a conceptual unsupported chart.
