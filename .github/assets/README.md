# Repository brand assets

Visual identity for `skills-design` itself — used by `README.md` and GitHub's social preview.

| File | Size | Used for |
|---|---|---|
| `logo.png` | 512×512 | README hero, favicon-scale mark |
| `logo-dark.png` | 512×512 | Dark-mode variant (GitHub `picture` element) |
| `banner.png` | 1280×640 | Repository social preview |
| `logo.svg` | vector | Source of truth for the mark; scales cleanly |

## Rules

- The mark is derived **only** from the project's declared brand identity (colors, typography, personality).
  Do not restyle it from a generic template.
- Keep `logo.png` legible at 32×32 — it appears next to the repo name in GitHub UI and in agent tool output.
- Keep the background transparent (or provide both light and dark variants) so it works on GitHub's
  light and dark themes.
- Reference images from the README with a relative path: `.github/assets/logo.png`.
- Binary assets live here, not inside a skill directory — skills must stay portable and self-contained.
