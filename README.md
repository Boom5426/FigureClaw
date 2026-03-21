# FigureClaw

English | [简体中文](README_CN.md)

<!-- Hero image slot: add FigureClaw.png to the repository root -->
![FigureClaw](FigureClaw.png)


Make scientific figure creation easy: FigureClaw is designed for high-quality research visualization, automatically recommending the most suitable chart and generating reproducible Python plotting code in one click—helping you create publication-ready figures effortlessly.

## Why FigureClaw

In the era of scientific automation, the biggest pain point is still: it's hard to make beautiful, expressive, and publication-ready figures.

- The difference between top-tier and ordinary journals often lies in the quality and clarity of figures.
- Most researchers and developers struggle to create high-quality, reproducible visualizations, limiting the impact of their work.
- FigureClaw makes "top-journal-level" figures easy, automatic, and reproducible—helping your results stand out.

With FigureClaw, you get:
- One unified setup prompt—no more long manual install guides
- Only charts with ready-to-run local code templates are recommended by default
- Style-heavy or unsupported charts (like sunburst, chord) are exposed as conceptual options, not fake code
- Examples, audits, packaging tools, and local references—all in one portable skill package

## First 5 Minutes In Codex

If this is your first time using FigureClaw in Codex, the goal is not just to install it. The goal is to get one real recommendation running in about five minutes and understand what to do next.

### Step 1: Let Codex install it

Paste this into Codex:

`Read https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/setup.md and set up FigureClaw for me.`

If you do not want the agent to do it for you, expand the manual install block below and run the commands yourself.

<details>
<summary>Manual install for Codex</summary>

```bash
git clone https://github.com/Boom5426/FigureClaw.git ~/.codex/FigureClaw
mkdir -p ~/.codex/skills
ln -sfn ~/.codex/FigureClaw/skills/figure-recommender ~/.codex/skills/figure-recommender
```

Restart Codex after the link is created.

</details>

### Step 2: Confirm Codex can see the skill

Run:

```bash
test -L ~/.codex/skills/figure-recommender
```

No output is normal. If the exit code is `0`, the skill link exists where Codex expects it.

### Step 3: Run the first built-in example

From the repository root, run:

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

This is the first important run in the project. It is not a fake demo. It executes the real FigureClaw path:

1. load a minimal `figure_brief`
2. choose the best executable primary chart
3. choose a palette
4. generate runnable Python plotting code

### Step 4: Only read these 3 fields first

When the JSON shows up, ignore the rest for a moment and only look at:

- `primary_chart`: the chart FigureClaw wants you to actually draw
- `palette`: the color system chosen for that chart
- `python_code`: the generated plotting code

For the built-in grouped comparison example, you should see:

- `"primary_chart"`
- `"contrast_dot"`
- `"python_code"`

That means FigureClaw has already moved past “chart suggestion” and reached “usable code output”.

### Step 5: Replace the example with your own request

Start with the smallest possible brief. You can save this as a json file or run it inline:

```json
{
  "story_goal": "compare_group_difference",
  "field_mapping": {
    "category": "condition",
    "value": "score"
  }
}
```

Then run:

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-json '{"story_goal":"compare_group_difference","field_mapping":{"category":"condition","value":"score"}}' \
  --output json
```

At that point you are no longer just validating the install. You are actually using FigureClaw.

### Step 6: Go back to Codex and ask for a real figure

After restarting Codex, you can say:

`Use the figure-recommender skill. I want to compare scores across treatment groups and generate runnable Python plotting code.`

If you do not have a structured input yet, that is fine. FigureClaw can start from natural language, infer a minimal brief, and continue from there.

## What You Can Generate

FigureClaw currently ships executable templates for:

- group comparison figures
- composition figures
- distribution figures
- line and multi-series trend figures
- matrix heatmaps
- benchmark scatter plots with error bars
- weighted relation and network-style figures

Conceptual requests such as `sunburst` or `chord` are still supported, but they
are exposed as conceptual choices while FigureClaw emits executable code from a
supported chart.

## Install

The preferred entrypoint is [`setup.md`](setup.md), which routes the user to
the right flow for the current environment and includes one shared smoke test.

## Install With Codex

Codex-first users should start here.

If you want the shortest onboarding path, read the “First 5 Minutes In Codex” section above first.

Paste this into Codex:

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md`

Manual path target:

`~/.codex/skills/figure-recommender`

Success looks like:

- the skill exists at `~/.codex/skills/figure-recommender`
- the smoke test prints `"primary_chart"`
- the grouped comparison example resolves to `"contrast_dot"`
- the response contains `"python_code"`
- you understand that `primary_chart` is the recommendation and `python_code` is the generated code

## Install With Claude

Paste this into Claude Code:

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md`

Manual path target:

`~/.claude/skills/figure-recommender`

## Install With Dr. Claw

1. Run `python3 skills/figure-recommender/scripts/package_skill.py`
2. Upload the generated `dist/figure-recommender.zip` in the Dr. Claw Skills UI
3. Let Dr. Claw discover the packaged `SKILL.md`, templates, references, and
   examples

## Verify

Run the shared smoke test from the repository root:

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

Confirm the response includes:

- `"primary_chart"`
- `"contrast_dot"`
- `"python_code"`

## Example Workflow

The default workflow is:

1. describe the figure goal
2. resolve or infer a structured `figure_brief`
3. choose the best executable chart
4. choose a compatible palette
5. emit runnable Python code from local templates

Minimal brief shape:

```json
{
  "story_goal": "compare_group_difference",
  "field_mapping": {
    "category": "condition",
    "value": "score"
  }
}
```

Defaults:

- `figure_role = paper-main`
- `style_mode = readable`
- `palette_mode = auto`

Starter examples live under
[`skills/figure-recommender/examples/briefs/`](skills/figure-recommender/examples/briefs/).

## How It Works

FigureClaw follows an executable-first contract:

1. Normalize and validate one brief object
2. Rank chart candidates
3. Pick the best executable `primary_chart`
4. Optionally expose a `conceptual_chart` when the user explicitly asks for an
   unsupported chart family
5. Render Python code from the shipped local template set

The result always keeps the executable chart and generated code aligned.

## Repository Structure

- `setup.md`: unified agent-readable setup entrypoint
- `skills/figure-recommender/`: runtime package, references, templates, and
  examples
- `.codex/INSTALL.md`: Codex-specific install flow
- `.claude/INSTALL.md`: Claude Code-specific install flow
- `docs/source-audits/`: notebook source audit artifacts
- `tests/`: regression, packaging, validation, and selection tests

## Manual install

Use the collapsed Codex block above for first-time manual setup. Keep
[`setup.md`](setup.md) as the primary entrypoint unless you are debugging a
broken local installation.

## Development

Run the full test suite:

```bash
python3 -m pytest tests -q
```

Rebuild the zip package:

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```

Regenerate notebook audit artifacts:

```bash
python3 skills/figure-recommender/scripts/export_source_notebooks.py \
  --output-dir docs/source-audits
```
