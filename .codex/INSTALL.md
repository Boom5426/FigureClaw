# Install FigureClaw For Codex

The preferred top-level entrypoint is `setup.md`, but this file is the concrete
Codex install runbook.

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

4. Verify the link and run the shared smoke test:

```bash
test -L ~/.codex/skills/figure-recommender
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
