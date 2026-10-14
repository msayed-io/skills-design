# CLI Reference — every executable in the repo

> Exact flags, environment variables, and verified invocations for all 50 scripts across 8 skills.
> Path rules: [`AGENTS.md §4`](../AGENTS.md) · when to use which tool: [`ROUTING.md`](ROUTING.md).

**Verified environment:** CPython 3.11.2, Node.js v22.22.3, Linux. Every command marked ✅ was executed
against this checkout with no packages installed.

```bash
export SKILLS=/path/to/skills-design     # used below; substitute your real path
cd /path/to/YOUR-project                 # cwd stays at the project root
```

---

## 0. Invocation rules

1. **Absolute path + cwd = project root** works for every script here (they resolve their own data via
   `__file__` / `require.main`). ✅ verified.
2. Some scripts also do bare sibling imports (`from core import …`); if you ever hit
   `ModuleNotFoundError: core`, `cd` into the script's own directory and re-run. ✅ verified working both ways.
3. Windows: use `python` instead of `python3`; `py -3` as a last resort.
4. **There is no root `scripts/` directory.** Never run `python3 scripts/x.py` from the repo root.
5. Outputs belong to the **project** (`docs/`, `assets/`, `src/`, `plans/reports/`), never to a skill directory.

**Dependency tiers**

| Tier | Scripts | Needs |
|---|---|---|
| **T0 — pure stdlib, offline** | all `search.py`, `search-slides.py`, `validate_data.py`, validators, `generate-tokens/embed-tokens/validate-tokens.cjs`, all `brand` scripts, `tailwind_config_gen.py`, `gha_mvp.py inspect/validate` | Python 3.10+ or Node 18+ only |
| **T1 — network, no packages** | `fetch-background.py`, `gha_mvp.py dispatch/watch/run-report`, `logo/generate.py` (MuAPI/Atlas providers) | network + a token/API key |
| **T2 — third-party packages** | `logo/generate.py` (Gemini), `cip/generate.py`, `icon/generate.py` | `pip install google-genai pillow` + API key |
| **T3 — external toolchain** | `shadcn_add.py`, `init-artifact.sh`, `bundle-artifact.sh` | Node + npm + network (shadcn CLI, Vite, Parcel) |

---

## 1. `ui-ux-pro-max` — 5 scripts

### `scripts/search.py` ✅

```bash
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "<query>" [options]
```

| Flag | Values | Purpose |
|---|---|---|
| `query` (positional) | — | 2–5 meaningful terms, one dominant intent |
| `--domain`, `-d` | `style` `color` `chart` `landing` `product` `ux` `typography` `google-fonts` `icons` `gsap` `react` `web` `app-interface` | Restrict the corpus (auto-detected if omitted; the output reports `auto-detected` and the runner-up) |
| `--stack`, `-s` | `react` `nextjs` `vue` `svelte` `astro` `swiftui` `react-native` `flutter` `nuxtjs` `nuxt-ui` `html-tailwind` `shadcn` `jetpack-compose` `threejs` `angular` `laravel` `wpf` `winui` `uwp` `avalonia` `javafx` `uno` | Stack-specific implementation guidance |
| `--max-results`, `-n` | 1–20 (default 3) | Result count |
| `--json` | — | Machine-readable output |
| `--full` | — | Do not truncate long fields (default truncates at 300 chars) |
| `--design-system`, `-ds` | — | Generate a complete design-system recommendation |
| `--project-name`, `-p` | text | Project name in the design-system output |
| `--format`, `-f` | `ascii` (default) \| `markdown` | Design-system output format (ignored with `--json`) |
| `--variance` | 1–10 | `DESIGN_VARIANCE` dial (design-system mode only) |
| `--motion` | 1–10 | `MOTION_INTENSITY` dial; attaches a GSAP snippet from `motion.csv` |
| `--density` | 1–10 | `VISUAL_DENSITY` dial; overrides the spacing scale |
| `--persist` | — | Write `design-system/<slug>/MASTER.md` |
| `--output-dir`, `-o` | path | Where `design-system/` is created — **always pass the project root explicitly** (defaults to cwd) |
| `--page` | name | Also create a page-specific override file under `pages/` |
| `--force` | — | Overwrite an existing `MASTER.md` (without it, persistence is **skipped** so prior decisions survive) |

```bash
# ✅ verified
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "saas dashboard dark" --domain style -n 1
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "portfolio" -n 1        # prints an explicit "No matches" block
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "fintech dashboard" --design-system --variance 7 --motion 5 --density 6
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "chip badge overflow nowrap" --stack html-tailwind
```

**Zero-result contract:** the script prints *"No matches. This is not a match with an empty value — the query
did not hit the database. Retry with broader/different keywords before falling back to general defaults, and
say explicitly that no database match was found if you do fall back."* Surface that to the user; never hide it.

### Other files

| File | Role |
|---|---|
| `scripts/core.py` | BM25 engine + `CSV_CONFIG` (domain → file, search columns, output columns) + `AVAILABLE_STACKS`. Imported by `search.py`; not a CLI. |
| `scripts/design_system.py` | `generate_design_system()` — builds the MASTER design system from search results and the dials. Library. |
| `scripts/reasoning_contract.py` | Reasoning-profile contract used by design-system generation. Library. |
| `scripts/validate_data.py` ✅ | **Data integrity check.** Run it after editing any CSV: `python3 $SKILLS/ui-ux-pro-max/scripts/validate_data.py` → `OK: validated 12 domain files, 22 stack files, and ui-reasoning.csv`. Ignores `--help`; it just validates. |

---

## 2. `design` — 9 scripts in 3 sub-trees

### Logo · `scripts/logo/`

**`search.py`** ✅ — domains `style`, `color`, `industry` (auto-detected if omitted).

| Flag | Purpose |
|---|---|
| `--domain`, `-d` | `style` \| `color` \| `industry` |
| `--max-results`, `-n` | default 3 |
| `--json` | JSON output |
| `--design-brief`, `-db` | Full brief: industry analysis, recommended styles, colors, typography, symbols |
| `--brand-name`, `-p` | Brand name for the brief |

```bash
# ✅ verified — no API key, no packages
python3 $SKILLS/design/scripts/logo/search.py "tech startup modern" --design-brief -p "Acme"
python3 $SKILLS/design/scripts/logo/search.py "minimalist clean" --domain style
```

**`generate.py`** (T2 — needs `GEMINI_API_KEY` + `google-genai`, `pillow`)

| Flag | Values / purpose |
|---|---|
| `--prompt`, `-p` | Free-form logo description |
| `--brand`, `-b` | Brand name |
| `--style`, `-s` | **18 CLI choices:** `minimalist` `vintage` `modern` `luxury` `playful` `corporate` `organic` `geometric` `hand-drawn` `3d` `abstract` `lettermark` `wordmark` `emblem` `mascot` `gradient` `lineart` `negative-space` |
| `--industry`, `-i` | **10 CLI choices:** `tech` `healthcare` `finance` `food` `fashion` `fitness` `eco` `education` `real-estate` `creative` |
| `--output`, `-o` / `--output-dir` | Single file / batch directory |
| `--batch` | Number of variants |
| `--brand-context` | Extra context injected into the prompt |
| `--pro` | `gemini-3-pro-image-preview` instead of the default `gemini-2.5-flash-image` |
| `--provider` | `gemini` (default) \| `atlas` \| `muapi` |
| `--atlas-model` / `--muapi-model` | Provider model slug (`nano-banana`, `nano-banana-pro`) |
| `--aspect-ratio` | `1:1` `16:9` `9:16` `4:3` `3:4` |
| `--list-styles` / `--list-industries` | Print the enums |

> **Note:** the CLI `--style` enum has 18 values while `data/logo/styles.csv` holds 55 style rows. The CSV is
> the *knowledge base* used by `search.py --design-brief`; the enum is what the generator accepts directly.
> Search first, then map the recommendation onto a supported `--style`.

```bash
export GEMINI_API_KEY="..."
python3 $SKILLS/design/scripts/logo/generate.py --brand "Acme" --industry finance --style minimalist --pro
python3 $SKILLS/design/scripts/logo/generate.py --brand "Acme" --batch 9 --output-dir assets/logo
python3 $SKILLS/design/scripts/logo/generate.py --brand "Acme" --provider muapi --muapi-model nano-banana-pro
```

**`core.py`** — BM25 engine for the logo CSVs (library, not a CLI).
**`tests/test_generate.py`** — 12 tests ✅ passing.

### CIP · `scripts/cip/`

**`search.py`** ✅ — `--domain {deliverable,style,industry,mockup}`, `--max`, `--all`, `--cip-brief`,
`--brand`, `--style`, `--json`.

**`generate.py`** (T2) — `--brand/-b` (**required**), `--logo/-l` (enables image-editing mode with the real
logo), `--deliverable/-d`, `--deliverables` (comma-separated), `--industry/-i`, `--style/-s`,
`--mockup/-m`, `--set` (full CIP set), `--output/-o`, `--model {flash,pro}` (`pro` = 4K text rendering),
`--ratio`, `--prompt-only` (print the prompt, generate nothing — **use this to review before spending**),
`--json`, `--no-logo-prompt`.

**`render-html.py`** ✅ help — `--brand/-b` (**required**), `--images` (**required**, directory of mockups),
`--industry/-i`, `--style/-s`, `--output`.

**`core.py`** — BM25 engine for the CIP CSVs.

```bash
python3 $SKILLS/design/scripts/cip/search.py "consultancy premium" --domain style
python3 $SKILLS/design/scripts/cip/generate.py --brand "Acme" --set --prompt-only      # dry review
python3 $SKILLS/design/scripts/cip/generate.py --brand "Acme" --logo assets/logo/acme.png --model pro
python3 $SKILLS/design/scripts/cip/render-html.py --brand "Acme" --images assets/cip --output assets/cip/index.html
```

### Icon · `scripts/icon/`

**`generate.py`** (T2) — `--prompt`, `--name`, `--style`, `--category`, `--color`, `--size`, `--viewbox`,
`--output`, `--output-dir`, `--batch`, `--sizes "16,24,32,48"`, `--list-styles`, `--list-categories`.
Model: `gemini-3.1-pro-preview`; output is SVG text.

> ⚠️ **Gotcha (verified):** this script imports `google-genai` eagerly, so even `--help` fails without it:
> `Error: google-genai package not installed.` Install first (`pip install google-genai`), then read `--help`.
> Use `data/icon/styles.csv` (15 styles) if you only need the style list offline.

---

## 3. `design-system` — 9 scripts

### Python

| Script | Flags | Notes |
|---|---|---|
| `search-slides.py` ✅ | `query` · `-d/--domain {strategy,layout,copy,chart}` · `-n/--max-results` · `--all` · `--json` · `--context` · `--position` (default 1) · `--total` (default 9) · `--prev-emotion` | `--context` runs the premium contextual flow (layout + typography + color + background for that slide position) |
| `generate-slide.py` ✅ | `--json/-j <file>` · `--output/-o <file>` · `--demo` | Emits HTML that **must** use CSS variables from `design-tokens.css`; escapes user values and rejects non-`http(s)`/`#`/`/` URLs (CWE-79 guard) |
| `fetch-background.py` | `[slide_type]` · `--list` · `--css` · `--json` · `--colors` · `--all` | T1 — curated Pexels/Unsplash lookups from `data/slide-backgrounds.csv`; honors `DESIGN_SYSTEM_PROJECT_ROOT` |
| `html-token-validator.py` ✅ | `[files …]` · `-t/--type {slides,infographics,all}` · `-v/--verbose` · `--colors` · `--fix` (experimental) | Source of truth: `assets/design-tokens.css`. Finds hardcoded colors/fonts/spacing |
| `slide-token-validator.py` | *same interface* | **Legacy 35-line wrapper** that delegates to `html-token-validator.py`. Prefer `html-token-validator.py --type slides` |
| `tests/test_validate_tokens.py` | — | 2 tests ✅ passing |

```bash
# ✅ verified
python3 $SKILLS/design-system/scripts/search-slides.py "investor pitch" -n 1
python3 $SKILLS/design-system/scripts/search-slides.py "problem agitation" -d copy
python3 $SKILLS/design-system/scripts/search-slides.py "cta" --context --position 9 --total 10 --prev-emotion frustration
python3 $SKILLS/design-system/scripts/html-token-validator.py --type slides -v
python3 $SKILLS/design-system/scripts/generate-slide.py --demo -o /tmp/demo.html
```

### Node (`.cjs`, built-ins only)

| Script | Usage | Purpose |
|---|---|---|
| `generate-tokens.cjs` | `node generate-tokens.cjs --config tokens.json -o tokens.css` · `--format tailwind` | CSS variables (or Tailwind config) from a tokens JSON |
| `embed-tokens.cjs` | `node embed-tokens.cjs` · `--minimal` · `--style` | Inline CSS for standalone HTML (slides, infographics); `--style` wraps in `<style>` |
| `validate-tokens.cjs` | `node validate-tokens.cjs --dir src/` · `--fix` | Find hardcoded values that should be tokens |

---

## 4. `brand` — 4 Node scripts (+15 tests ✅)

| Script | Usage | Purpose |
|---|---|---|
| `inject-brand-context.cjs` | `node inject-brand-context.cjs [path] [--json]` | Extract brand context from markdown guidelines into a prompt-injection block. Default path `docs/brand-guidelines.md` |
| `sync-brand-to-tokens.cjs` | `node sync-brand-to-tokens.cjs [--dry-run] [--force]` | `docs/brand-guidelines.md` → `assets/design-tokens.json` → `assets/design-tokens.css`, then into CSS entry points (`src/index.css`, `src/globals.css`, `src/styles/globals.css`, `src/styles/tokens.css`, …) |
| `validate-asset.cjs` | `node validate-asset.cjs <asset-path> [--json] [--fix]` | Naming, dimensions, file size, metadata vs. brand guidelines |
| `extract-colors.cjs` | `node extract-colors.cjs <image-path> [--brand-file <path>]` · `--palette` | Dominant colors compared against the brand palette. Pure Node — for full extraction, pair with ImageMagick or a multimodal skill |

```bash
# ✅ verified — fails cleanly and tells you what to create when the guidelines are missing
node $SKILLS/brand/scripts/inject-brand-context.cjs --json
#   Error: Brand guidelines not found at <cwd>/docs/brand-guidelines.md
#   Create brand guidelines at docs/brand-guidelines.md or specify a path.

cp $SKILLS/brand/templates/brand-guidelines-starter.md docs/brand-guidelines.md   # then edit
node $SKILLS/brand/scripts/sync-brand-to-tokens.cjs --dry-run
node $SKILLS/brand/scripts/sync-brand-to-tokens.cjs
node $SKILLS/brand/scripts/inject-brand-context.cjs --json | head -20             # verify
```

**Sync guardrail:** it **stops** when it detects existing token files, `:root` custom properties, Tailwind v4
`@theme` variables, or Tailwind theme colors/presets, and reports the offending source. `--force` only when
overwriting the managed `assets/design-tokens.*` outputs is intentional.

---

## 5. `ui-styling` — 2 scripts (+64 tests ✅)

### `scripts/shadcn_add.py` (T3 — shells out to the shadcn CLI)

```bash
python3 $SKILLS/ui-styling/scripts/shadcn_add.py [components …] [options]
```

`--all` · `--overwrite` · `--dry-run` · `--list` · `--project-root <path>`

```bash
python3 $SKILLS/ui-styling/scripts/shadcn_add.py --list
python3 $SKILLS/ui-styling/scripts/shadcn_add.py button card dialog --dry-run     # always dry-run first
```

### `scripts/tailwind_config_gen.py` ✅ (T0 — offline)

`--framework {react,vue,svelte,nextjs}` (default `react`) · `--js` (JS instead of TS config) ·
`--output` · `--colors NAME:VALUE …` · `--fonts TYPE:FAMILY …` · `--spacing NAME:VALUE …` ·
`--breakpoints NAME:WIDTH …` · `--plugins` · `--validate-only` · `--force`

```bash
# ✅ verified
python3 $SKILLS/ui-styling/scripts/tailwind_config_gen.py --framework react --validate-only
python3 $SKILLS/ui-styling/scripts/tailwind_config_gen.py --colors brand:#2F6FEB --fonts display:"Instrument Sans" --output tailwind.config.ts
```

`scripts/requirements.txt` documents: **Python 3.10+, no runtime package dependencies**; dev deps are
`pytest>=8`, `pytest-cov>=4.1`, `pytest-mock>=3.12`; Node 18+ and npm for the shadcn CLI
(`npx shadcn-ui@latest init`).

---

## 6. `gha-app-builder` — `scripts/gha_mvp.py`

Dependency-free. Deliberately separates **local static inspection** from **remote side effects**; it does not
create releases, mutate secrets, or run the project's production build locally.

| Subcommand | Flags | Side effects |
|---|---|---|
| `inspect` ✅ | `--repo` (default `.`) | none — prints JSON: remote, project markers (android/flutter/node/dotnet/xcode/docker), workflow files, validation |
| `validate` | `--workflow <file>` (**required**) | none |
| `dispatch` | `--repo` `--workflow` `--ref` (all required) `--inputs` | **triggers a run** |
| `watch` | `--repo` `--run-id` (required) `--interval` (10s) `--timeout` (3600s) | polls until terminal |
| `run-report` | `--repo` `--run-id` (required) | none |

```bash
# ✅ verified
python3 $SKILLS/gha-app-builder/scripts/gha_mvp.py inspect --repo .
# { "ok": true, "github_remote": "https://github.com/msayed-io/skills-design.git",
#   "project_markers": {...}, "workflow_files": [], "workflow_validation": [] }
```

Requires `GH_TOKEN` or `GITHUB_TOKEN` for `dispatch` / `watch` / `run-report`, plus network access to
`api.github.com`. Output is always JSON with an `ok` flag — check it, don't eyeball it.

**Success = all five:** `status=completed` · `conclusion=success` · repo/ref/head_sha/workflow match ·
artifact present, unexpired, digest verified · signing/publish gates passed.

---

## 7. `web-artifacts-builder` — 2 shell scripts (T3)

```bash
bash $SKILLS/web-artifacts-builder/scripts/init-artifact.sh <project-name>
cd <project-name>            # React 18 + TS + Vite + Tailwind 3.4.1 + 40+ shadcn/ui components
…develop…
bash $SKILLS/web-artifacts-builder/scripts/bundle-artifact.sh    # run from the project root
```

`bundle-artifact.sh` fails fast with a clear message if `package.json` or `index.html` is missing, installs
Parcel-based bundling deps, and emits a single HTML artifact. `scripts/shadcn-components.tar.gz` is the
pre-packed component set used by init (keeps installs fast and offline-friendly for components).

Requires bash, Node 18+, npm, and registry access.

---

## 8. `algorithmic-art` — templates, not CLIs

| File | Role |
|---|---|
| `templates/generator_template.js` | The p5.js generative skeleton: seeded randomness (`randomSeed`/`noiseSeed`), the `params` object, draw loop |
| `templates/viewer.html` | Interactive parameter-exploration viewer (fixed vs. variable separation) |

The skill marks **"STEP 0: READ THE TEMPLATE FIRST"** as mandatory before writing any generator code.

---

## 9. Validation & test commands

```bash
# Data integrity (offline, instant)
python3 $SKILLS/ui-ux-pro-max/scripts/validate_data.py            # ✅ OK: 12 domain files, 22 stack files, ui-reasoning.csv

# Design-token compliance in a project
node    $SKILLS/design-system/scripts/validate-tokens.cjs --dir src/
python3 $SKILLS/design-system/scripts/html-token-validator.py --type all -v

# Test suites (230 tests passing on this checkout)
python3 -m venv .venv && .venv/bin/pip install pytest
(cd $SKILLS/ui-ux-pro-max/scripts && python -m pytest tests -q \
   --ignore=tests/test_catalog_refresh.py \
   --ignore=tests/test_catalog_summary_line_endings.py \
   --ignore=tests/test_relevance_evaluator.py \
   --ignore=tests/test_skill_script_paths.py)     # 137 passed + 8,236 subtests
(cd $SKILLS/design/scripts/logo   && python -m pytest tests -q)   # 12 passed
(cd $SKILLS/design-system/scripts && python -m pytest tests -q)   #  2 passed
(cd $SKILLS/ui-styling/scripts    && python -m pytest tests -q)   # 64 passed
(cd $SKILLS/brand/scripts         && python -m pytest tests -q)   # 15 passed
```

> The four ignored `ui-ux-pro-max` files fail at **collection** in this distribution: they locate an upstream
> monorepo root by searching parent directories for `scripts/generate-catalog-summary.py`,
> `scripts/refresh-google-fonts.py`, `scripts/refresh-icon-catalog.py`, `scripts/evaluate-relevance.py`, and
> for skill trees `cli/assets/skills` / `.claude/skills`. None of those ship here, so `next(...)` raises
> `StopIteration`. Run them in the upstream repo, or keep them ignored.

---

## 10. Environment variables

| Variable | Used by | Required for | Notes |
|---|---|---|---|
| `GEMINI_API_KEY` | `design` logo/CIP/icon | Gemini generation | Default provider (Nano Banana). [Key](https://aistudio.google.com/apikey) |
| `GOOGLE_API_KEY` | `design` | — | Accepted fallback name |
| `ATLASCLOUD_API_KEY` | `design` | `--provider atlas` | Async image API |
| `MUAPI_API_KEY` | `design` | `--provider muapi` | Async image API; `--muapi-model nano-banana[-pro]` |
| `GH_TOKEN` / `GITHUB_TOKEN` | `gha-app-builder` | dispatch/watch/run-report | `GH_TOKEN` checked first |
| `DESIGN_SYSTEM_PROJECT_ROOT` | `design-system` | optional | Overrides cwd for `fetch-background.py` and the validators |

**`.env` lookup order** (logo/CIP/icon generators): `<design-skill>/.env` → `~/.claude/skills/.env` →
`~/.claude/.env`. Simple `KEY=VALUE` lines; `#` comments skipped.

**Never** commit a `.env`, echo a key into output, or inline a key in a workflow file.
Every T0 command above works with **no keys at all** — do the offline half of the job (briefs, search,
validation, config generation) and tell the user precisely which variable unlocks the generation step.

---

## 11. Script inventory (50 files)

| Skill | Python | Node `.cjs` | Shell | JS templates | Tests |
|---|---|---|---|---|---|
| `ui-ux-pro-max` | 5 (`core`, `search`, `design_system`, `reasoning_contract`, `validate_data`) | — | — | — | 15 files |
| `design` | 9 (`logo/{search,generate,core}`, `cip/{search,generate,render-html,core}`, `icon/generate`) | — | — | — | 1 file |
| `design-system` | 5 (`search-slides`, `slide_search_core`, `generate-slide`, `fetch-background`, `html-token-validator`) + 1 legacy wrapper | 3 (`generate-tokens`, `embed-tokens`, `validate-tokens`) | — | — | 1 file |
| `brand` | — | 4 (`inject-brand-context`, `sync-brand-to-tokens`, `validate-asset`, `extract-colors`) | — | — | 1 file |
| `ui-styling` | 2 (`shadcn_add`, `tailwind_config_gen`) | — | — | — | 2 files |
| `gha-app-builder` | 1 (`gha_mvp`) | — | — | — | — |
| `web-artifacts-builder` | — | — | 2 (`init-artifact`, `bundle-artifact`) | — | — |
| `algorithmic-art` | — | — | — | 1 (`generator_template.js`) + `viewer.html` | — |
| **Total** | **40** | **7** | **2** | **1** | **18 files · 230 tests** |
