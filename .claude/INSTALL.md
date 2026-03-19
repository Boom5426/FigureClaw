# Install FigureClaw For Claude Code

1. Clone the repository:

```bash
git clone https://github.com/Boom5426/FigureClaw.git ~/.claude/FigureClaw
```

2. Link the skill into your Claude skill directory:

```bash
mkdir -p ~/.claude/skills
ln -s ~/.claude/FigureClaw/skills/figure-recommender ~/.claude/skills/figure-recommender
```

3. Restart Claude Code.

## Notes

- This repository ships a self-contained `figure-recommender` skill.
- Runtime assets live under `skills/figure-recommender/` and do not depend on external notebooks.
- If the symlink already exists, replace it with `ln -sfn`.
