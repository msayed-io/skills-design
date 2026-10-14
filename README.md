<div align="center">

<img src=".github/assets/logo.png" alt="skills-design logo" width="120" />

# skills-design

**A curated library of 27 installable agent skills for design, brand, and frontend work.**

Prompt-engineered playbooks + searchable local datasets + zero-dependency CLIs that make an AI agent
produce *deliberate* visual work instead of templated defaults.

[![Skills](https://img.shields.io/badge/skills-27-2f6feb)](#the-catalog)
[![Curated data rows](https://img.shields.io/badge/data_rows-4%2C757-2f6feb)](#data-driven-skills)
[![Python](https://img.shields.io/badge/python-3.9%2B__stdlib_only-3572A5)](#runtime-requirements)
[![Node](https://img.shields.io/badge/node-18%2B__builtins_only-339933)](#runtime-requirements)
[![Tests](https://img.shields.io/badge/tests-230_passing-success)](#tests)
[![Docs](https://img.shields.io/badge/agent_docs-AGENTS.md-8250df)](AGENTS.md)

</div>

---

## What this repository is

`skills-design` is a **skill library**, not an application. Every top-level directory is one
self-contained *Agent Skill* — the format used by Claude Code, Claude plugins, Codex, and similar
agent runtimes: a `SKILL.md` file whose YAML frontmatter (`name` + `description`) tells the agent
*when* to activate it, and whose body tells the agent *how* to execute the work.

The skills here cover the full design-to-delivery path:

```
brand identity → design tokens → UI implementation → marketing assets → build & release
```

Some skills are pure **prompt engineering** (they reshape the agent's taste and block its default
biases). Others are **tool-backed**: they ship curated CSV knowledge bases, BM25 search CLIs, token
generators, validators, and image-generation wrappers, so the agent retrieves verified data instead
of hallucinating hex codes and font pairings.

### What this repository is *not*

- **Not a runnable app.** There is no build step, no `package.json`, no server. Nothing to `npm install` at the root.
- **Not a single coherent design system.** It is 27 independent skills with deliberate overlaps; see [Choosing a skill](#choosing-a-skill) and [`docs/ROUTING.md`](docs/ROUTING.md).
- **Not original third-party-free work.** Skills are aggregated from several upstream sources with different licenses. See [License & attribution](#license--attribution).

---

## For agents: the 60-second contract

If you are an AI agent reading this repository, follow these rules before anything else. The full
operating manual is [`AGENTS.md`](AGENTS.md).

1. **Never load all 27 skills.** They total ~62,000 words of `SKILL.md` alone. Read frontmatter descriptions, pick **one** skill per task, then read only that skill's `SKILL.md`, and pull in `references/*` on demand.
2. **The activation name is the frontmatter `name:`, not the directory name.** 10 of 27 differ (e.g. `taste-skill/` activates as `design-taste-frontend`). Full mapping in [`docs/CATALOG.md`](docs/CATALOG.md#directory--activation-name-map).
3. **Script paths are skill-relative, the working directory is the project root.** `scripts/foo.py` means *that skill's own* `scripts/`; `../other-skill/scripts/foo.py` means a sibling skill installed next to it. Scripts read/write project files (`docs/brand-guidelines.md`, `assets/design-tokens.json`, `src/`) relative to the cwd.
4. **Only 7 skills ship executable CLIs** (`brand`, `design`, `design-system`, `ui-styling`, `ui-ux-pro-max`, `gha-app-builder`, `web-artifacts-builder`). Three more ship assets instead of tools (`canvas-design`, `algorithmic-art`, `theme-factory`); the other **17 are instructions only**. Do not go looking for a CLI that does not exist — full inventory in [`docs/CLI.md`](docs/CLI.md).
5. **No secrets in the repo.** Image-generation scripts read API keys from the environment / `.env` (`GEMINI_API_KEY`, `ATLASCLOUD_API_KEY`, `MUAPI_API_KEY`); `gha-app-builder` reads `GH_TOKEN` / `GITHUB_TOKEN`. Never echo them.
6. **Verify before claiming success.** Search CLIs print explicit "no match" text — a zero-result answer is data, not an error to hide. Token/slide validators exist for a reason; run them.

---

## The catalog

27 skills, grouped by job. **Type:** 📄 = prompt-only instructions · 🔧 = ships scripts/data/templates.

### A · Brand & identity systems

| Skill | Directory | Type | What it does |
|---|---|---|---|
| `design` | [`design/`](design/) | 🔧 | **Unified design router** (v2.1.0): logo generation (55 styles × 30 palettes × 25 industries), corporate identity program (50 deliverables), slides, banners (22 styles), SVG icons (15 styles), social photos. Wraps `brand`, `design-system`, `ui-styling` as siblings. |
| `brand` | [`brand/`](brand/) | 🔧 | Brand voice, visual identity, messaging frameworks, asset management, consistency audits. Syncs `docs/brand-guidelines.md` → `design-tokens.json` → `.css`. |
| `design-system` | [`design-system/`](design-system/) | 🔧 | Three-layer token architecture (primitive → semantic → component), component specs, Tailwind integration, and a full slide-decision system (8 CSVs, BM25 search, validators). |
| `ui-styling` | [`ui-styling/`](ui-styling/) | 🔧 | shadcn/ui + Radix + Tailwind implementation layer, accessibility patterns, theming/dark mode, plus a canvas visual-design layer with 54 bundled fonts. |
| `slides` | [`slides/`](slides/) | 📄 | Strategic HTML presentations: layout patterns, copywriting formulas, deck strategies, Chart.js integration. |
| `banner-design` | [`banner-design/`](banner-design/) | 📄 | Multi-format banners for social, ads, web heroes, and print — sizes, styles, export workflow. |
| `brandkit` | [`brandkit/`](brandkit/) | 📄 | Premium brand-kit **image** generation: logo concepting methods, 3×3 board system, visual modes (dark-tech, luxury, editorial, security, gaming…). |
| `brand-guidelines` | [`brand-guidelines/`](brand-guidelines/) | 📄 | Anthropic's official brand colors/typography, applied to any artifact. **Anthropic-specific.** |

### B · Design intelligence (searchable data)

| Skill | Directory | Type | What it does |
|---|---|---|---|
| `ui-ux-pro-max` | [`ui-ux-pro-max/`](ui-ux-pro-max/) | 🔧 | BM25 search engine over **4,000+ curated rows**: 79 searchable styles (50 active), 192 product palettes + reasoning profiles, 74 font pairings, 1,934 Google Fonts, 105 curated icons, 119 UX guidelines, 17 GSAP presets, 25 chart types, 22 stack guides (1,271 rows). Can generate + persist a full design system (`MASTER.md` + page overrides). |

### C · Frontend taste (anti-generic prompt skills)

| Skill | Directory | Type | What it does |
|---|---|---|---|
| `design-taste-frontend` | [`taste-skill/`](taste-skill/) | 📄 | **The default taste authority (v2).** Brief inference → three dials (`DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`) → official design-system selection → hard layout discipline → pre-flight check. 12,793 words. |
| `design-taste-frontend-v1` | [`taste-skill-v1/`](taste-skill-v1/) | 📄 | The original v1, frozen for backward compatibility. Only install when a project depends on its exact behavior. |
| `gpt-taste` | [`gpt-tasteskill/`](gpt-tasteskill/) | 📄 | Awwwards-level engineering for GPT-style agents: simulated Python randomization for layout variance, strict AIDA structure, gapless bento grids, GSAP ScrollTrigger paradigms. |
| `high-end-visual-design` | [`soft-skill/`](soft-skill/) | 📄 | "Expensive agency" feel: exact fonts, spacing, shadows, card architecture, motion choreography, performance guardrails. |
| `minimalist-ui` | [`minimalist-skill/`](minimalist-skill/) | 📄 | Premium utilitarian minimalism: warm monochrome, spot pastels, flat bento, banned elements list. |
| `industrial-brutalist-ui` | [`brutalist-skill/`](brutalist-skill/) | 📄 | Swiss industrial print **or** tactical CRT telemetry — rigid grids, extreme type scale, analog degradation. |
| `redesign-existing-projects` | [`redesign-skill/`](redesign-skill/) | 📄 | Audit-first upgrades of existing sites/apps: 10 audit dimensions, upgrade techniques, fix priority, no functional breakage. |
| `frontend-design` | [`frontend-design/`](frontend-design/) | 📄 | Anthropic's guidance for distinctive, intentional UI: grounding in subject matter, typographic restraint, plan→build→critique. |
| `stitch-design-taste` | [`stitch-skill/`](stitch-skill/) | 📄 | Emits an agent-friendly `DESIGN.md` semantic design system for **Google Stitch** (ships a reference `DESIGN.md`). |
| `full-output-enforcement` | [`output-skill/`](output-skill/) | 📄 | Behavior modifier: bans truncation and placeholder patterns, enforces complete code output, handles token-limit splits. |

### D · Image direction (generation-first)

| Skill | Directory | Type | What it does |
|---|---|---|---|
| `imagegen-frontend-web` | [`imagegen-frontend-web/`](imagegen-frontend-web/) | 📄 | **One horizontal image per section** (hard rule), combinatorial variation engine, hero minimalism, palette consistency. Images only. |
| `imagegen-frontend-mobile` | [`imagegen-frontend-mobile/`](imagegen-frontend-mobile/) | 📄 | Premium app-native screen/flow images: platform modes (iOS/Android/cross), device mockup framing, safe areas, anti-AI-tells. Images only. |
| `image-to-code` | [`image-to-code-skill/`](image-to-code-skill/) | 📄 | Image-first website workflow for Codex: generate → deeply analyze → implement to match. 19 numbered rules. |

### E · Static art, themes & artifacts

| Skill | Directory | Type | What it does |
|---|---|---|---|
| `canvas-design` | [`canvas-design/`](canvas-design/) | 🔧 | Museum/magazine-quality posters and art as `.png`/`.pdf` via a written design philosophy. Ships 54 fonts (OFL). |
| `algorithmic-art` | [`algorithmic-art/`](algorithmic-art/) | 🔧 | Generative art with p5.js: seeded randomness, parameter systems, interactive viewer templates (`.html` + `.js`). |
| `theme-factory` | [`theme-factory/`](theme-factory/) | 🔧 | 10 pre-set themes (colors + fonts) for slides/docs/landing pages, or generate one on the fly. Ships `theme-showcase.pdf`. |
| `web-artifacts-builder` | [`web-artifacts-builder/`](web-artifacts-builder/) | 🔧 | Complex multi-component claude.ai HTML artifacts: React 18 + TS + Vite + Tailwind + shadcn/ui, bundled to a single HTML file. Ships `init-artifact.sh`, `bundle-artifact.sh`, pre-packed components. |

### F · Delivery & build

| Skill | Directory | Type | What it does |
|---|---|---|---|
| `gha-app-builder` | [`gha-app-builder/`](gha-app-builder/) | 🔧 | Makes **GitHub Actions** the authoritative build environment: inspect/validate workflows, dispatch, watch runs, verify artifacts and signing gates. Android · iOS/macOS · Windows · Docker/web · CLI. Ships an Arabic `SYSTEM_PROMPT.md`. |

---

## Choosing a skill

The fastest correct path (full decision trees in [`docs/ROUTING.md`](docs/ROUTING.md)):

| The task is… | Use | Then |
|---|---|---|
| "Design a logo / brand kit / CIP mockups" | `design` | `design` → `brandkit` if you need presentation boards as images |
| "Build a design system / tokens" | `brand` | → `design-system` → `ui-styling` |
| "Design or review a UI, pick colors/fonts/stack patterns" | `ui-ux-pro-max` (search first) | → `design-taste-frontend` for taste enforcement |
| "Build me a landing page / portfolio that doesn't look AI-generated" | `design-taste-frontend` | + `full-output-enforcement` if output gets truncated |
| "Upgrade this existing ugly site" | `redesign-existing-projects` | audit before touching code |
| "Generate design mockup images for a site/app" | `imagegen-frontend-web` / `imagegen-frontend-mobile` | → `image-to-code` to implement |
| "Make a pitch deck" | `design-system` (slide system) or `slides` | → `theme-factory` to theme it |
| "Poster / art / generative visual" | `canvas-design` or `algorithmic-art` | — |
| "Build, sign and release the app" | `gha-app-builder` | never claim success before the remote run is terminal |

### Precedence rules (the overlaps are intentional)

- **One aesthetic authority per project.** `design-taste-frontend`, `gpt-taste`, `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`, and `stitch-design-taste` all dictate visual taste. Loading two produces contradictory rules. Pick one; `design-taste-frontend` is the default.
- **`design` supersedes `slides` and `banner-design`.** `design/references/slides-*.md` are byte-identical copies of `slides/references/*.md`, and `design/references/banner-sizes-and-styles.md` is identical to `banner-design/references/`. Install the standalone versions only when you want the narrow skill without the router.
- **`ui-ux-pro-max` is the data layer; taste skills are the opinion layer.** Query the data first, then apply taste. They are complementary, not competing.
- **`brand-guidelines` is Anthropic-branded.** Use it only when Anthropic's look-and-feel is actually wanted.
- **`design-taste-frontend-v1` is frozen.** New work uses v2.
- **`ui-styling` and `canvas-design` both ship the same 54 fonts** (identical files). Use whichever skill is active; don't copy the font tree twice.

---

## Install

Skills are directories. "Installing" means placing a skill directory where your agent runtime discovers skills.

### Claude Code — per project

```bash
# from the root of YOUR project
mkdir -p .claude/skills
cp -r /path/to/skills-design/ui-ux-pro-max .claude/skills/
cp -r /path/to/skills-design/taste-skill   .claude/skills/design-taste-frontend
```

> Rename the directory to the frontmatter `name:` when they differ — see the
> [mapping table](docs/CATALOG.md#directory--activation-name-map).

### Claude Code — globally

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/skills-design/<skill-dir> ~/.claude/skills/
```

### Install the `design` bundle correctly

`design` routes to `brand`, `design-system`, and `ui-styling` as **siblings** (`../brand/scripts/…`).
Install all four side by side or the routing paths break:

```bash
for s in design brand design-system ui-styling ui-ux-pro-max; do
  cp -r /path/to/skills-design/$s .claude/skills/
done
```

### Codex / other runtimes

Point the agent at the skill directory and have it read `SKILL.md` as a system/context document.
Prompt-only skills (📄) work with no setup at all. Tool-backed skills (🔧) need the runtime
requirements below.

### Verify an install

```bash
# from the installed skill directory
python3 scripts/search.py "saas dashboard" --domain style -n 1   # ui-ux-pro-max
node scripts/inject-brand-context.cjs --json                     # brand (needs docs/brand-guidelines.md)
```

---

## Runtime requirements

| Requirement | Needed by | Notes |
|---|---|---|
| **Python 3.10+** | `ui-ux-pro-max`, `design`, `design-system`, `ui-styling`, `gha-app-builder` | **Standard library only.** No `pip install` required for search, briefs, validators, or generators. `ui-styling` documents 3.10+ as its floor; verified here on CPython 3.11. |
| **Node.js 18+** | `brand`, `design-system` | `.cjs` scripts use only `fs`, `path`, `child_process` — no npm install. |
| **Bash + npm** | `web-artifacts-builder` | `init-artifact.sh` scaffolds React/Vite/Tailwind and needs network access to npm. |
| `pillow`, `google-genai` | `design` (logo/CIP **generation** only) | `pip install google-genai pillow`. Search/brief commands do **not** need these. |
| Chrome headless / Playwright / Puppeteer | `design` social photos | Screenshot export at exact pixel sizes. |
| p5.js (CDN) | `algorithmic-art` | Referenced by the generated viewer HTML. |

### Environment variables

| Variable | Skill | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | `design` | Default image provider (Nano Banana). [Get a key](https://aistudio.google.com/apikey) |
| `GOOGLE_API_KEY` | `design` | Fallback key name accepted by the generators |
| `ATLASCLOUD_API_KEY` | `design` | `--provider atlas` |
| `MUAPI_API_KEY` | `design` | `--provider muapi` |
| `GH_TOKEN` / `GITHUB_TOKEN` | `gha-app-builder` | Dispatch and watch workflow runs |
| `DESIGN_SYSTEM_PROJECT_ROOT` | `design-system` | Overrides the cwd for validators/fetchers |

Keys are read from the environment or from `.env` files (skill dir → `~/.claude/skills/.env` → `~/.claude/.env`).
**No key is ever committed here, and none is required to browse or search the datasets.**

---

## Verified commands

All of these were executed against this checkout (Python 3.11, Node 22) and work with no installs:

```bash
# Search the UI/UX knowledge base (auto-detects domain)
python3 ui-ux-pro-max/scripts/search.py "saas dashboard dark" --domain style -n 1

# Generate a full, persistable design system with the three dials
python3 ui-ux-pro-max/scripts/search.py "fintech dashboard" --design-system \
  --variance 7 --motion 5 --density 6 --persist --output-dir /path/to/project

# Logo design brief (no API key needed — brief only)
python3 design/scripts/logo/search.py "tech startup modern" --design-brief -p "Acme"

# Slide strategy / layout / copy / chart search
python3 design-system/scripts/search-slides.py "investor pitch" -n 1
python3 design-system/scripts/search-slides.py "cta" --context --position 9 --total 10

# Inspect a repo's GitHub Actions state (no side effects)
python3 gha-app-builder/scripts/gha_mvp.py inspect --repo .

# Tailwind config generation (dry, offline)
python3 ui-styling/scripts/tailwind_config_gen.py --framework react --validate-only
```

Image **generation** (as opposed to briefs/search) requires an API key:

```bash
export GEMINI_API_KEY="..."
python3 design/scripts/logo/generate.py --brand "Acme" --industry tech --style minimalist --pro
python3 design/scripts/logo/generate.py --brand "Acme" --batch 9 --output-dir ./logos
python3 design/scripts/cip/generate.py --brand "Acme" --logo ./logos/acme.png
python3 design/scripts/icon/generate.py --prompt "settings gear" --style outlined --sizes "16,24,32,48"
```

Full CLI reference for all 50 scripts: [`docs/CLI.md`](docs/CLI.md).

---

## Data-driven skills

Three skills replace model guesswork with retrievable facts:

| Skill | Rows | Contents |
|---|---|---|
| `ui-ux-pro-max` | 4,325 | styles, product palettes + reasoning profiles, typography pairings, Google Fonts catalog, icons, UX guidelines, motion/GSAP presets, chart selection, landing patterns, React performance, 22 stack guides |
| `design` | 290 | 55 logo styles, 30 color psychologies, 25 industries, 49 CIP deliverables, CIP styles/industries/mockup contexts, 15 icon styles |
| `design-system` | 142 | 15 deck strategies, 25 layouts, layout logic, typography logic, color logic, backgrounds, 25 copy formulas, 25 chart configs |

Search is **BM25** over CSV, implemented from scratch in each skill's `core.py` / `slide_search_core.py`.
No index files, no services, no network. Provenance and SHA-256 snapshots for the upstream-derived
catalogs live in [`ui-ux-pro-max/data/data-provenance.json`](ui-ux-pro-max/data/data-provenance.json)
and [`ui-ux-pro-max/data/catalog-summary.json`](ui-ux-pro-max/data/catalog-summary.json).

---

## Tests

Five skills ship pytest suites (18 test files):

```bash
python3 -m venv .venv && .venv/bin/pip install pytest

(cd ui-ux-pro-max/scripts && ../../.venv/bin/python -m pytest tests -q)
(cd design/scripts/logo   && ../../../.venv/bin/python -m pytest tests -q)
(cd design-system/scripts && ../../.venv/bin/python -m pytest tests -q)
(cd ui-styling/scripts    && ../../.venv/bin/python -m pytest tests -q)
(cd brand/scripts         && ../../.venv/bin/python -m pytest tests -q)
```

Current status on this checkout: **230 tests passing** (137 + 8,236 subtests in `ui-ux-pro-max`,
64 in `ui-styling`, 15 in `brand`, 12 in `design/logo`, 2 in `design-system`).

> **Known limitation:** 4 files in `ui-ux-pro-max/scripts/tests/` (`test_catalog_refresh.py`,
> `test_catalog_summary_line_endings.py`, `test_relevance_evaluator.py`, `test_skill_script_paths.py`)
> fail at *collection* here because they locate an upstream monorepo root by searching for scripts
> (`generate-catalog-summary.py`, `refresh-google-fonts.py`, `evaluate-relevance.py`) and skill trees
> (`cli/assets/skills`, `.claude/skills`) that are **not part of this distribution**. Exclude them, or
> run the suite in the upstream repo. The remaining 11 files pass.

---

## Repository layout

```
skills-design/
├── README.md               ← you are here (project profile)
├── AGENTS.md               ← operating manual for AI agents  ← READ THIS FIRST
├── .github/assets/         ← logo, banner, social preview
├── docs/
│   ├── CATALOG.md          ← all 27 skills in depth: triggers, I/O, assets, limits
│   ├── ROUTING.md          ← task → skill decision trees + conflict resolution
│   ├── CLI.md              ← every script: flags, env, verified examples
│   └── CONTRIBUTING.md     ← conventions, frontmatter contract, licensing rules
└── <skill-directory>/      ← 27 of these, one per skill
    ├── SKILL.md            ← REQUIRED: frontmatter (name, description) + instructions
    ├── LICENSE.txt         ← present for 7 upstream-derived skills (Apache-2.0)
    ├── references/*.md     ← deep docs, loaded on demand (59 files)
    ├── scripts/*.py|.cjs   ← executable tools (40 py · 7 cjs · 2 sh · 1 js)
    ├── data/*.csv          ← searchable knowledge bases (53 CSVs, 4,757 rows)
    ├── templates/          ← starter files and scaffolds
    └── canvas-fonts/*.ttf  ← 108 bundled font files (SIL OFL)
```

**Totals:** 394 tracked files · 99 markdown documents (~104,900 words) · 53 CSVs (4,757 rows) · 50 scripts · 108 bundled font files.

---

## Conventions & gotchas

Read [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) before changing anything. The short version:

1. **Directory name ≠ activation name** for 10 skills. Tools key off frontmatter `name:`.
2. **270 files use CRLF line endings**, 17 use LF (all of `gha-app-builder` is LF). Match the file you are editing; do not mass-normalize.
3. **No root `LICENSE` on purpose.** Seven skills are Apache-2.0 (Anthropic-derived), four are MIT (`claudekit`-authored: `banner-design`, `brand`, `design`, `design-system`, `slides`, `ui-styling`), the rest carry no declared license. A blanket root license would mis-license upstream work.
4. **Frontmatter is the API.** `description:` is what an agent matcher reads to decide activation — it must state triggers, actions, and scope in one dense string. `argument-hint:`, `license:`, and `metadata:` are optional.
5. **Intentional duplication exists.** `design/references/` mirrors `slides/` and `banner-design/`; `ui-styling/canvas-fonts/` mirrors `canvas-design/canvas-fonts/`. Keep copies byte-identical when you update one.
6. **`gha-app-builder/SYSTEM_PROMPT.md` is written in Arabic.** That is intentional — do not translate it in place.

---

## License & attribution

| License | Skills | Source |
|---|---|---|
| **Apache-2.0** (`LICENSE.txt`) | `algorithmic-art`, `brand-guidelines`, `canvas-design`, `frontend-design`, `theme-factory`, `ui-styling`, `web-artifacts-builder` | Anthropic skills collection |
| **MIT** (declared in frontmatter) | `banner-design`, `brand`, `design`, `design-system`, `slides` | `claudekit` (author metadata in frontmatter) |
| **SIL OFL 1.1** | 54 font families in `canvas-design/canvas-fonts/` and `ui-styling/canvas-fonts/` | Each family ships its own `*-OFL.txt` |
| **Undeclared** | `brandkit`, `brutalist-skill`, `gpt-tasteskill`, `image-to-code-skill`, `imagegen-frontend-mobile`, `imagegen-frontend-web`, `minimalist-skill`, `output-skill`, `redesign-skill`, `soft-skill`, `stitch-skill`, `taste-skill`, `taste-skill-v1`, `ui-ux-pro-max`, `gha-app-builder` | Community / repo-authored — treat as "all rights reserved" until the owner declares otherwise |

Font license snapshots: [`ui-ux-pro-max/data/google-font-licenses.json`](ui-ux-pro-max/data/google-font-licenses.json).

---

## Documentation index

| Document | Read it when… |
|---|---|
| [`AGENTS.md`](AGENTS.md) | You are an agent about to work in this repo — selection algorithm, path contract, safety rules, verification checklists |
| [`docs/CATALOG.md`](docs/CATALOG.md) | You need per-skill detail: activation triggers, inputs/outputs, bundled assets, script inventory, hard limits |
| [`docs/ROUTING.md`](docs/ROUTING.md) | You have a task and need to pick (and combine) the right skills |
| [`docs/CLI.md`](docs/CLI.md) | You are about to run a script and need exact flags, env vars, and expected output |
| [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) | You are adding or editing a skill |

---

## Contributing

New skill? Follow the contract:

```
my-skill/
├── SKILL.md          # frontmatter: name, description (+ optional argument-hint, license, metadata)
├── references/       # optional deep docs, loaded on demand
├── scripts/          # optional, stdlib-only Python or builtin-only Node
└── data/             # optional CSVs with a header row
```

Then: add it to the right family table above, add an entry in `docs/CATALOG.md`, wire it into
`docs/ROUTING.md` if it overlaps an existing skill, and run the test suites if you touched scripts.
Details and the review checklist: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

---

<div align="center">

**27 skills · 4,757 rows of curated design data · 50 scripts · 230 passing tests**

Built for agents that need to make *decisions*, not defaults.

</div>
