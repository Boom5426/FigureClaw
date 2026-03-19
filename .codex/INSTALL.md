# Install FigureClaw For Codex

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

4. Verify with:

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

## Notes

- This repository ships a self-contained `figure-recommender` skill.
- Runtime assets live under `skills/figure-recommender/` and do not depend on external notebooks.
- If the symlink already exists, replace it with `ln -sfn`.
- The repository root `setup.md` is the preferred agent-readable entrypoint.
