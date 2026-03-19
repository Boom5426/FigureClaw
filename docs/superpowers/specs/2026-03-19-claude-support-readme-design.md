# FigureClaw Claude Support and README Design

## Goal

Add first-class Claude installation guidance to FigureClaw without changing the
`figure-recommender` skill runtime. The skill should remain a single portable
package, while the repository adds platform-specific install entrypoints and
clearer documentation for Codex, Claude, and Dr. Claw users.

## Scope

- Add a Claude-specific install entrypoint at `.claude/INSTALL.md`
- Keep `.codex/INSTALL.md` as the Codex entrypoint
- Expand the root `README.md` into a publishable project overview with:
  - project summary
  - capability summary
  - installation sections for Codex, Claude, and Dr. Claw
  - quick usage example
  - repository layout
  - development and verification commands
- Expand `skills/figure-recommender/README.md` so the packaged skill docs also
  explain platform-specific installation paths

## Non-Goals

- No changes to the figure selection or code generation logic
- No new chart templates or palette modes
- No new runtime dependencies
- No automatic installer script beyond platform-specific markdown instructions

## Design

### Install Entry Strategy

The repository keeps platform-specific install entrypoints in hidden
top-level directories:

- `.codex/INSTALL.md` for Codex
- `.claude/INSTALL.md` for Claude Code

Both entrypoints use the same repository and skill directory, but differ in the
final symlink target:

- Codex uses `~/.codex/skills/figure-recommender`
- Claude uses `~/.claude/skills/figure-recommender`

### Documentation Strategy

The root README becomes the primary landing page for the repository. It should
explain what FigureClaw is, how the `figure-recommender` skill works, and how a
user installs it in each target environment. The README should avoid branch-only
URLs and document the stable `main` install paths.

The skill README remains focused on the `figure-recommender` package itself:
inputs, outputs, build steps, direct CLI usage, and manual installation paths.

### Verification

Because the change is documentation and entrypoint oriented, the test surface is
lightweight and file-based:

- assert `.claude/INSTALL.md` exists and contains the Claude skill path
- assert `.codex/INSTALL.md` still points to the Codex skill path
- assert the root README covers Codex, Claude, and Dr. Claw install flows
- assert the skill README documents Codex and Claude local install paths

## Risks

- README drift between root docs and skill docs
- platform path mistakes in install snippets
- documenting a `main` raw URL before merge; acceptable for repo docs, but local
  verification should remain file-based until the branch is merged
