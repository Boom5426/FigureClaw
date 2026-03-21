# Install FigureClaw For Codex

The preferred top-level entrypoint is `setup.md`, but this file is the concrete
Codex install runbook.

## Goal

By the end of this guide, you should have:

- FigureClaw linked into `~/.codex/skills/figure-recommender`
- one built-in example run successfully
- a basic understanding of what `primary_chart` and `python_code` mean

## Manual install

1. Clone the repository:

```bash
git clone https://github.com/Boom5426/FigureClaw.git ~/.codex/FigureClaw
```

2. Link the skill into your Codex skill directory:

```bash
mkdir -p ~/.codex/skills
ln -s ~/.codex/FigureClaw/skills/figure-recommender ~/.codex/skills/figure-recommender
```

3. Restart Codex.

4. Verify the link:

```bash
test -L ~/.codex/skills/figure-recommender
```

No output is normal. An exit code of `0` means the skill is linked where Codex expects it.

5. Run the shared smoke test:

```bash
cd ~/.codex/FigureClaw
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

Success looks like:

- the symlink check exits with code `0`
- the JSON output includes `"primary_chart"`
- the grouped comparison example resolves to `"contrast_dot"`
- the JSON output includes `"python_code"`

## What the smoke test means

When that JSON prints successfully, FigureClaw has already completed the real
v1 workflow:

1. read a structured `figure_brief`
2. choose an executable `primary_chart`
3. choose a palette
4. generate runnable Python plotting code

For your first read, only care about these fields:

- `primary_chart`: the chart FigureClaw recommends you actually draw
- `palette`: the colors chosen for that chart
- `python_code`: the generated plotting script

If you see `"contrast_dot"` in the built-in grouped comparison example, the
selection pipeline is working as expected.

## First real use

After the smoke test passes, try one minimal inline brief:

```bash
cd ~/.codex/FigureClaw
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-json '{"story_goal":"compare_group_difference","field_mapping":{"category":"condition","value":"score"}}' \
  --output json
```

That is the fastest way to move from “install verified” to “I am actually using
FigureClaw on my own request”.

After restarting Codex, you can also ask directly:

`Use the figure-recommender skill. I want to compare scores across treatment groups and generate runnable Python plotting code.`

If Codex does not infer a structured input yet, FigureClaw can start from your
natural-language request and infer a minimal brief first.

## If it does not show up in Codex

1. Confirm the link target:

```bash
test -L ~/.codex/skills/figure-recommender
readlink ~/.codex/skills/figure-recommender
```

2. If the link points somewhere stale, replace it:

```bash
ln -sfn ~/.codex/FigureClaw/skills/figure-recommender ~/.codex/skills/figure-recommender
```

3. Make sure you restarted Codex after linking.

4. Re-run the smoke test from `~/.codex/FigureClaw`.

## Notes

- This repository ships a self-contained `figure-recommender` skill.
- Runtime assets live under `skills/figure-recommender/` and do not depend on external notebooks.
- If the symlink already exists, use `ln -sfn`.
- The repository root `setup.md` is the preferred agent-readable entrypoint.
