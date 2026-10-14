# Skill Catalog — all 27 skills in depth

> Reference for agents and humans: what each skill is, exactly when to activate it, what it needs,
> what it produces, and where it stops.
> Companion docs: [`ROUTING.md`](ROUTING.md) (task → skill) · [`CLI.md`](CLI.md) (every script) ·
> [`CONTRIBUTING.md`](CONTRIBUTING.md) (conventions).

**Legend** — Type: 📄 prompt-only · 🔧 tool-backed (ships scripts/data/templates/fonts).
Word counts are for `SKILL.md` only; use them to budget context.

---

## Directory ↔ activation name map

The runtime registers a skill by its frontmatter `name:`, **not** its folder name. 10 of 27 differ.

| # | Directory | Activation `name:` | Family | Type | Words |
|---|---|---|---|---|---|
| 1 | `algorithmic-art/` | `algorithmic-art` | E · Art & artifacts | 🔧 | 2,746 |
| 2 | `banner-design/` | `banner-design` | A · Brand & identity | 📄 | 1,037 |
| 3 | `brand/` | `brand` | A · Brand & identity | 🔧 | 484 |
| 4 | `brand-guidelines/` | `brand-guidelines` | A · Brand & identity | 📄 | 329 |
| 5 | `brandkit/` | `brandkit` | A · Brand & identity | 📄 | 2,586 |
| 6 | `brutalist-skill/` | **`industrial-brutalist-ui`** | C · Frontend taste | 📄 | 1,074 |
| 7 | `canvas-design/` | `canvas-design` | E · Art & artifacts | 🔧 | 1,749 |
| 8 | `design/` | `design` | A · Brand & identity | 🔧 | 1,835 |
| 9 | `design-system/` | `design-system` | A · Brand & identity | 🔧 | 906 |
| 10 | `frontend-design/` | `frontend-design` | C · Frontend taste | 📄 | 1,505 |
| 11 | `gha-app-builder/` | `gha-app-builder` | F · Delivery & build | 🔧 | 1,104 |
| 12 | `gpt-tasteskill/` | **`gpt-taste`** | C · Frontend taste | 📄 | 1,134 |
| 13 | `image-to-code-skill/` | **`image-to-code`** | D · Image direction | 📄 | 5,806 |
| 14 | `imagegen-frontend-mobile/` | `imagegen-frontend-mobile` | D · Image direction | 📄 | 6,532 |
| 15 | `imagegen-frontend-web/` | `imagegen-frontend-web` | D · Image direction | 📄 | 5,790 |
| 16 | `minimalist-skill/` | **`minimalist-ui`** | C · Frontend taste | 📄 | 1,087 |
| 17 | `output-skill/` | **`full-output-enforcement`** | C · Behavior modifier | 📄 | 407 |
| 18 | `redesign-skill/` | **`redesign-existing-projects`** | C · Frontend taste | 📄 | 2,196 |
| 19 | `slides/` | `slides` | A · Brand & identity | 📄 | 221 |
| 20 | `soft-skill/` | **`high-end-visual-design`** | C · Frontend taste | 📄 | 1,449 |
| 21 | `stitch-skill/` | **`stitch-design-taste`** | C · Frontend taste | 📄 | 1,613 |
| 22 | `taste-skill/` | **`design-taste-frontend`** | C · Frontend taste | 📄 | 12,793 |
| 23 | `taste-skill-v1/` | **`design-taste-frontend-v1`** | C · Frontend taste | 📄 | 2,937 |
| 24 | `theme-factory/` | `theme-factory` | E · Art & artifacts | 🔧 | 486 |
| 25 | `ui-styling/` | `ui-styling` | A · Brand & identity | 🔧 | 1,276 |
| 26 | `ui-ux-pro-max/` | `ui-ux-pro-max` | B · Design intelligence | 🔧 | 2,102 |
| 27 | `web-artifacts-builder/` | `web-artifacts-builder` | E · Art & artifacts | 🔧 | 439 |

---

# A · Brand & identity systems

---

## 1. `design` — unified design router

| | |
|---|---|
| Directory | [`design/`](../design/) |
| Type | 🔧 tool-backed · **largest surface in the repo** |
| License / version | MIT · `claudekit` v2.1.0 |
| `SKILL.md` | 1,835 words (333 lines) |
| `argument-hint` | `[design-type] [context]` |
| Assets | 18 `references/` · 9 scripts in 3 sub-trees · 8 CSVs (~290 rows) |

**Activate when:** the request is a *brand deliverable* — logo, corporate identity program, mockups,
pitch deck, banner, icon set, or social media images.

**Do not use for:** UI/frontend implementation (use `ui-styling` / a taste skill), pure design decisions
(use `ui-ux-pro-max`), or CI/build work.

**Built-in modules** (each has its own references + data):

| Module | Capability | Data | Scripts |
|---|---|---|---|
| Logo | 55 styles, 30 color psychologies, 25 industry guides; brief → generate → batch variants | `data/logo/{styles,colors,industries}.csv` | `scripts/logo/{search,generate,core}.py` |
| CIP | ~49 corporate-identity deliverables, 19 styles, 19 industries, 19 mockup contexts; HTML presentation rendering | `data/cip/*.csv` | `scripts/cip/{search,generate,render-html,core}.py` |
| Icon | 15 styles, SVG output, multi-size export (16/24/32/48), batch variations | `data/icon/styles.csv` | `scripts/icon/generate.py` |
| Slides | Strategies, layouts, HTML template, copywriting formulas | *(references only)* | — |
| Banner | 22 art styles, social/ads/web/print sizes | *(references only)* | — |
| Social photos | HTML/CSS → screenshot at exact px, 8 platform sizes | *(references only)* | — |

**Sibling routing:** `brand` (identity/voice), `design-system` (tokens), `ui-styling` (code) are expected
as sibling installs; the skill also works standalone through its own references.

**Requires:** nothing for briefs/search. For generation: `GEMINI_API_KEY` (default, Nano Banana) or
`ATLASCLOUD_API_KEY` / `MUAPI_API_KEY`, plus `pip install google-genai pillow`. Screenshot export needs
Chrome headless, Playwright, or Puppeteer.

**Notes:** `references/slides-*.md` are byte-identical copies of `slides/references/*.md`, and
`references/banner-sizes-and-styles.md` is identical to `banner-design/references/`. `scripts/logo/tests/`
ships 12 passing tests.

---

## 2. `brand` — brand voice, identity & asset governance

| | |
|---|---|
| Directory | [`brand/`](../brand/) |
| Type | 🔧 tool-backed |
| License / version | MIT · `claudekit` v1.0.0 |
| `SKILL.md` | 484 words (108 lines) — deliberately thin; the knowledge lives in `references/` |
| `argument-hint` | `[update\|review\|create] [args]` |
| Assets | 11 `references/` · 4 Node scripts + 1 pytest suite (15 tests) · 1 template |

**Activate when:** brand voice/tone, visual identity standards, messaging frameworks, brand consistency
audits, asset naming/approval, palette management, typography specs.

**The pipeline it owns:**

```
docs/brand-guidelines.md   ← single source of truth (start from templates/brand-guidelines-starter.md)
        ↓ node scripts/sync-brand-to-tokens.cjs
assets/design-tokens.json  → assets/design-tokens.css  → CSS entry points in src/
```

**Scripts:** `inject-brand-context.cjs` (extract brand context for prompt injection, `--json`),
`sync-brand-to-tokens.cjs` (`--dry-run`, `--force`), `validate-asset.cjs <asset-path>`,
`extract-colors.cjs` (`--palette` or `<image-path>`).

**Guardrail:** the sync **stops** when it detects pre-existing token files, `:root` custom properties,
Tailwind v4 `@theme` variables, or Tailwind theme colors/presets, and reports the offending source.
Use `--force` only when overwriting the managed `assets/design-tokens.*` outputs is intentional.

**Subcommands:** `update` → `references/update.md`. Routing: parse the first word of `$ARGUMENTS`, load
`references/{subcommand}.md`, execute with the rest.

**Requires:** Node 18+ (built-ins only). No API keys.

---

## 3. `design-system` — tokens, component specs & the slide decision system

| | |
|---|---|
| Directory | [`design-system/`](../design-system/) |
| Type | 🔧 tool-backed |
| License / version | MIT · `claudekit` v1.0.0 |
| `SKILL.md` | 906 words (248 lines) |
| `argument-hint` | `[component or token]` |
| Assets | 7 `references/` · 9 scripts (4 `.cjs`, 5 `.py`) + 2 tests · 8 CSVs (142 rows) · 1 template |

**Activate when:** design tokens (primitive → semantic → component), CSS variables, spacing/typography
scales, component specifications and states/variants, Tailwind integration, or **brand-compliant
presentations**.

**Two distinct capabilities in one skill:**

1. **Token system** — `templates/design-tokens-starter.json`, `generate-tokens.cjs`, `embed-tokens.cjs`,
   `validate-tokens.cjs`, references for token architecture / primitive / semantic / component tokens /
   states & variants / Tailwind integration.
2. **Slide system** — a contextual decision engine over 8 CSVs:

| CSV | Rows | Maps |
|---|---|---|
| `slide-strategies.csv` | 15 | deck structures + emotion arcs + sparkline beats |
| `slide-layouts.csv` | 25 | layouts + component variants + animations |
| `slide-layout-logic.csv` | 15 | goal → layout + `break_pattern` flag |
| `slide-typography.csv` | 14 | content type → type scale |
| `slide-color-logic.csv` | 13 | emotion → color treatment |
| `slide-backgrounds.csv` | 10 | slide type → image category (Pexels/Unsplash) |
| `slide-copy.csv` | 25 | copywriting formulas (PAS, AIDA, FAB…) |
| `slide-charts.csv` | 25 | chart types with Chart.js config |

Decision flow: parse goal → strategy → per slide: layout logic → typography → color logic → background →
animation class → generate HTML with tokens → validate. Pattern breaking follows the Duarte sparkline
(alternate "what is / what could be" emotions).

**Requires:** Node 18+ and Python 3.10+ (stdlib). `fetch-background.py` performs network image lookups;
`DESIGN_SYSTEM_PROJECT_ROOT` overrides the project root for validators/fetchers.

---

## 4. `ui-styling` — shadcn/ui + Tailwind implementation layer

| | |
|---|---|
| Directory | [`ui-styling/`](../ui-styling/) |
| Type | 🔧 tool-backed · **largest by bytes** (6.0 MB, 106 files) |
| License | frontmatter `license: MIT` (`claudekit` v1.0.0) **and** an Apache-2.0 `LICENSE.txt` (inherited with the bundled canvas fonts) — dual-declared, see [`CONTRIBUTING.md`](CONTRIBUTING.md#7-licensing) |
| `SKILL.md` | 1,276 words (336 lines) |
| `argument-hint` | `[component or layout]` |
| Assets | 7 `references/` · 2 scripts + 2 test files (64 tests) · 54 fonts (identical to `canvas-design`) · `requirements.txt` |

**Activate when:** building UIs with shadcn/ui (Radix + Tailwind), implementing a design system in code,
responsive layouts, accessible components (dialogs, dropdowns, forms, tables), theming/dark mode,
consistent styling patterns — and for the canvas-based visual design layer.

**Three layers:** component (`shadcn/ui` over Radix primitives, copy-paste into your codebase,
TypeScript-first) → styling (Tailwind utility-first, build-time, dead-code elimination) → visual design
(canvas: museum-quality compositions, philosophy-driven).

**Scripts:** `shadcn_add.py` (component installer wrapping the shadcn CLI; `--list`, `--dry-run`,
`--all`, `--overwrite`, `--project-root`) and `tailwind_config_gen.py` (`--framework react|vue|svelte|nextjs`,
`--js`, `--colors`, `--fonts`, `--spacing`, `--breakpoints`, `--plugins`, `--validate-only`, `--force`).

**References:** `shadcn-components.md`, `shadcn-theming.md`, `shadcn-accessibility.md`,
`tailwind-utilities.md`, `tailwind-responsive.md`, `tailwind-customization.md`, `canvas-design-system.md`.

**Requires:** Python 3.10+ (stdlib only — `requirements.txt` lists pytest/pytest-cov/pytest-mock as dev
deps), Node 18+ and npm for the shadcn CLI. Network access for component installation.

---

## 5. `slides` — strategic HTML presentations

| | |
|---|---|
| Directory | [`slides/`](../slides/) |
| Type | 📄 prompt-only |
| License / version | MIT · `claudekit` v1.0.0 |
| `SKILL.md` | 221 words (44 lines) — a pure router |
| `argument-hint` | `[topic] [slide-count]` |
| Assets | 5 `references/` |

**Activate when:** marketing presentations, pitch decks, data-driven slides with Chart.js,
copywriting-optimized decks.

**Subcommand:** `create` → `references/create.md`. Knowledge base: `layout-patterns.md`,
`html-template.md`, `copywriting-formulas.md`, `slide-strategies.md`.

**Prefer `design-system` instead when** design tokens exist — its slide system is the same strategy
knowledge plus token enforcement and validators. All five references here are byte-identical to
`design/references/slides-*.md`.

**Requires:** nothing. No scripts, no keys.

---

## 6. `banner-design` — multi-format banners

| | |
|---|---|
| Directory | [`banner-design/`](../banner-design/) |
| Type | 📄 prompt-only |
| License / version | MIT · `claudekit` v1.0.0 |
| `SKILL.md` | 1,037 words (145 lines) |
| `argument-hint` | `[platform] [style] [dimensions]` |
| Assets | 1 `references/` (`banner-sizes-and-styles.md`) |

**Activate when:** banners, covers, headers — social (Facebook, X, LinkedIn, YouTube, Instagram),
Google Display ads, website heroes, event/print.

**Explicit scope limit (from the skill):** *banner design only* — not video editing, not full website
design, not print production.

**Workflow:** 1) gather requirements (`AskUserQuestion`) → 2) research & art direction → 3) design and
generate options → 4) export to images → 5) present and iterate. Styles covered: minimalist, gradient,
bold typography, photo-based, illustrated, geometric, retro, glassmorphism, 3D, neon, duotone, editorial,
collage. Includes a size quick-reference and a security section.

**Requires:** an export path (headless browser / image tool) for step 4; otherwise nothing.

---

## 7. `brandkit` — premium brand-kit image generation

| | |
|---|---|
| Directory | [`brandkit/`](../brandkit/) |
| Type | 📄 prompt-only (2,586 words / 798 lines of art-direction doctrine) |
| License | none declared |

**Activate when:** you need **images** of brand systems — brand-guideline boards, logo systems, identity
decks, visual-world presentations. Trained for minimalist, cinematic, editorial, dark-tech, luxury,
cultural, security, gaming, developer-tool, and consumer-app brand systems.

**Contents:** reference style DNA · core principle · default output · brand-strategy-first rule ·
logo generation standard · **5 logo concept methods** (monogram + meaning, product action, metaphor
fusion, negative space, construction geometry) · board composition DNA · **default 3×3 panel system**
(logo cover, construction, digital application, brand essence, color system, typography, physical
application, image direction, system detail) · 2×3 reference layout · **9 visual modes** (dark
developer/builder, dark product/operator, dark nature/calm, dark security/threat, light
editorial/compliance, luxury/beauty/fashion, voice/communication, cultural/experimental, + reference
usage) · premium detail language · text rules · tagline style · image & mockup direction · color
discipline · anti-generic rules · prompt template · final output standard.

**Explicitly forbids:** generic logos, random mockups, messy AI moodboards.

**Requires:** an image-generation capability in the host agent. Produces images, **not** source files —
chain into `design` or a taste skill when code or vectors are needed.

---

## 8. `brand-guidelines` — Anthropic brand styling

| | |
|---|---|
| Directory | [`brand-guidelines/`](../brand-guidelines/) |
| Type | 📄 prompt-only |
| License | Apache-2.0 (`LICENSE.txt`) |
| `SKILL.md` | 329 words (73 lines) |

**Activate when:** an artifact should carry **Anthropic's** look and feel. This is a specific company
identity, not a generic branding tool.

**The system:** dark `#141413`, light `#faf9f5`, mid gray `#b0aea5`, light gray `#e8e6dc`, green
`#788c5d`; headings in **Poppins** (Arial fallback, applied at 24pt+), body in **Lora** (Georgia
fallback); non-text shapes cycle orange/blue/green accents; smart background-aware text color.

**Do not combine with** `brand` (which builds *your* identity) inside one artifact.

**Requires:** fonts pre-installed in the environment for best results; falls back gracefully.

---

# B · Design intelligence

---

## 9. `ui-ux-pro-max` — searchable UI/UX knowledge base

| | |
|---|---|
| Directory | [`ui-ux-pro-max/`](../ui-ux-pro-max/) |
| Type | 🔧 tool-backed · **the data layer of this repo** |
| License | none declared |
| `SKILL.md` | 2,102 words (214 lines) |
| Assets | 2 `references/` · 5 scripts · 15 test files (137 tests + 8,236 subtests) · 39 data files (**4,325 rows**) |

**Activate when:** anything about UI structure, visual design decisions, interaction patterns, or UX
quality control — new pages, component creation/refactor, color/typography/spacing/layout systems, UX or
accessibility review, navigation/animation/responsive behavior, perceived quality.

**Skip for:** pure backend logic, API/database design, non-visual performance work, infra/DevOps — unless
the task changes how something *looks, feels, moves, or is interacted with*.

**Datasets** (verified against `data/catalog-summary.json`, `verifiedAt: 2026-08-26`):

| Domain flag | File | Rows | Contents |
|---|---|---|---|
| `style` | `styles.csv` | 88 | 79 searchable / 50 active / 29 supplemental / 9 deprecated |
| `product`, `color` | `products.csv`, `colors.csv` | 192 + 192 | product types → full 17-role palettes |
| *(reasoning)* | `ui-reasoning.csv` | 192 | exact reasoning profiles per product type |
| `typography` | `typography.csv` | 74 | font pairings |
| `google-fonts` | `google-fonts.csv` | 1,934 | licensed Google Font families (+ license snapshots) |
| `icons` | `icons.csv` | 105 | curated icons (+1,512 upstream Phosphor refs) |
| `ux` | `ux-guidelines.csv` | 119 | guidelines with rationale |
| `gsap` | `motion.csv` | 17 | motion presets with snippets |
| `chart` | `charts.csv` | 25 | chart selection + accessibility grading |
| `landing` | `landing.csv` | 34 | landing patterns |
| `react` | `react-performance.csv` | 44 | React performance rules |
| `app-interface` | `app-interface.csv` | 32 | app UI polish rules |
| `web` / `--stack` | `stacks/*.csv` | 1,271 | 22 stacks: react, nextjs, vue, nuxtjs, nuxt-ui, svelte, astro, angular, laravel, html-tailwind, shadcn, uno, threejs, swiftui, react-native, flutter, jetpack-compose, wpf, winui, uwp, avalonia, javafx |

**Priority model:** the skill ranks 10 rule categories 1→10 (accessibility and touch/interaction are
CRITICAL; charts/data LOW) — see the table in its `SKILL.md`. Full rule text lives in
`references/quick-reference.md` (3,496 words) and app polish in `references/pro-rules.md`; **load them on
demand**.

**Design-system mode:** `--design-system` generates a complete recommendation; the three dials
(`--variance`, `--motion`, `--density`, each 1–10) tune it; `--persist --output-dir <project-root>`
writes `design-system/<slug>/MASTER.md` (+ `pages/` overrides with `--page`). Persistence is skipped if
`MASTER.md` exists unless `--force`.

**Requires:** Python 3.10+, **standard library only**, no network. `data/data-provenance.json` and
`catalog-summary.json` record upstream sources and SHA-256 snapshots; a promotion policy gates font
families (licensed families only, relevance gate required).

**Known limitation:** 4 test files need the upstream monorepo (see [`CONTRIBUTING.md`](CONTRIBUTING.md#8-tests)).

---

# C · Frontend taste & behavior

---

## 10. `design-taste-frontend` — the default taste authority (v2)

| | |
|---|---|
| Directory | [`taste-skill/`](../taste-skill/) |
| Type | 📄 prompt-only · **12,793 words — the biggest document in the repo** |
| License | none declared |

**Activate when:** landing pages, portfolios, redesigns — any frontend work where "does not look
templated" is the acceptance criterion.

**How it works:** `§0` brief inference (read the signals, output a one-line **Design Read**, ask *one*
question if ambiguous) → `§1` three dials `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`
(baseline **8 / 6 / 4**, with an inference table and use-case presets) → `§2` brief → design-system map
(when to install an **official** package vs. build an aesthetic) → `§3` default architecture (stack,
state, icons, emoji policy, responsiveness, mandatory dependency verification) → `§4` engineering
directives (typography, color calibration, layout diversification, materiality/shadows, interactive
states, data & forms, hard layout discipline, image strategy, content density) → pre-flight check.

**Official-system honesty rule:** if the brief reads as Fluent, Material 3, Carbon, Polaris, Atlaskit,
Primer, GOV.UK Frontend, USWDS, Bootstrap 5.3, Radix Themes, shadcn/ui, or Tailwind v4 — **install the
official package**; never hand-recreate its CSS, never import its tokens and override 90% of them.
**One system per project.** For aesthetics with no official package (glassmorphism, bento, brutalism,
editorial, dark tech, aurora gradients, kinetic type, "liquid glass") it prescribes honest native
implementations and requires labelling approximations.

**Budget note:** read the section matching your sub-task; do not ingest all 12,793 words.

---

## 11. `design-taste-frontend-v1` — frozen v1

| Directory [`taste-skill-v1/`](../taste-skill-v1/) · 📄 · 2,937 words · license undeclared |
|---|

The original taste skill, preserved for projects depending on its exact behavior. Contains the same three
dials with level definitions, AI-tell lists (visual/CSS, typography, layout, content — the "Jane Doe
effect"), a creative arsenal (hero paradigms, navigation, grids, cards, scroll animations, galleries,
micro-interactions), and the "motion-engine bento" paradigm with 5 card archetypes.

**Use only for backward compatibility.** New work → `design-taste-frontend`.

---

## 12. `gpt-taste` — Awwwards-level engineering for GPT-family agents

| Directory [`gpt-tasteskill/`](../gpt-tasteskill/) · 📄 · 1,134 words · license undeclared |
|---|

**Activate when:** the executing agent is GPT-family and the brief is motion-rich and editorial.

**Mechanism:** forces a simulated Python `random.choice()` inside a mandatory `<design_plan>` block
(deterministic seed from the prompt) to select 1 hero architecture, 1 typography stack (Satoshi, Cabinet
Grotesk, Outfit, or Geist — **never Inter**), 3 component architectures, and 2 GSAP paradigms. Enforces
AIDA page structure, the "2-line iron rule" for headings (bans 6-line wraps), gapless bento grids, strict
GSAP ScrollTrigger usage (pinning, stacking, scrubbing), inline micro-images, and massive section spacing.
**No emojis anywhere** in code, comments, or output.

---

## 13. `high-end-visual-design` — the "expensive agency" spec

| Directory [`soft-skill/`](../soft-skill/) · 📄 · 1,449 words · license undeclared |
|---|

Principal UI/UX architect + motion choreographer. Defines the exact fonts, spacing, shadows, card
structures, and animations that make a site feel expensive, with an "Absolute Zero" anti-pattern list, a
creative variance engine (vibe/texture archetypes × layout archetypes), haptic micro-aesthetics
(double-bezel nesting, island button architecture, spatial rhythm), motion choreography (fluid-island nav,
magnetic button hover physics, scroll interpolation), performance guardrails, an execution protocol, and a
pre-output checklist.

---

## 14. `minimalist-ui` — premium utilitarian minimalism

| Directory [`minimalist-skill/`](../minimalist-skill/) · 📄 · 1,087 words · license undeclared |
|---|

Clean editorial interfaces: warm monochrome palette with spot pastels, typographic contrast, flat bento
grids, **no gradients, no heavy shadows**. Ships an absolute negative-constraints list (banned elements),
typographic architecture, the color palette, component specifications, iconography/imagery directives,
subtle motion rules, and an execution protocol.

---

## 15. `industrial-brutalist-ui` — Swiss print or tactical telemetry

| Directory [`brutalist-skill/`](../brutalist-skill/) · 📄 · 1,074 words · license undeclared |
|---|

Fuses mid-century Swiss typographic print with military/aerospace terminal aesthetics for data-heavy
dashboards, portfolios, and editorial sites that should feel like declassified blueprints.

**Two mutually exclusive archetypes — pick one per project, never mix:**
- **2.1 Swiss Industrial Print** (light): newsprint substrates, monolithic heavy sans, visible grid lines,
  asymmetric negative space, viewport-bleeding numerals, primary red as alert accent.
- **2.2 Tactical Telemetry & CRT** (dark-only): dense tabular data, monospace dominance, ASCII brackets and
  crosshairs, phosphor glow, scanlines, low bit-depth dithering.

Also covers macro/micro/textural typography, color systems for both modes, spatial engineering,
components & symbology, post-processing effects, and web engineering directives.

---

## 16. `redesign-existing-projects` — audit-first upgrades

| Directory [`redesign-skill/`](../redesign-skill/) · 📄 · 2,196 words · license undeclared |
|---|

**Activate when:** an existing site or app must be upgraded to premium quality **without breaking
functionality**. Works with any CSS framework or vanilla CSS.

**Audit dimensions (10):** typography · color and surfaces · layout · interactivity and states · content ·
component patterns · iconography · code quality · **strategic omissions** (what AI typically forgets) —
each with concrete checks. Then upgrade techniques (typography, layout, motion, surfaces), a fix-priority
order, and hard rules.

**Pairs well with:** `ui-ux-pro-max` (data for the audit) and `full-output-enforcement` (large refactors).

---

## 17. `frontend-design` — Anthropic's design guidance

| Directory [`frontend-design/`](../frontend-design/) · 📄 · 1,505 words · Apache-2.0 |
|---|

Guidance for distinctive, intentional visual design when building new UI or reshaping existing UI.
Core moves: **ground the design in the subject matter** (identify product, audience, and the design's
primary job; a toy for girls 8–11 ≠ a dashboard for financial analysts) · design principles (hero opens
with the most characteristic thing in the subject's world; typography carries personality; deliberate
typefaces and a real type scale; line lengths < 80 chars) · an explicit list of default typographic
treatments to avoid because they read as generated · a plan → review-against-brief → build → critique
process · restraint and self-critique · writing in design.

---

## 18. `stitch-design-taste` — semantic design system for Google Stitch

| Directory [`stitch-skill/`](../stitch-skill/) · 📄 · 1,613 words · license undeclared · ships a sample `DESIGN.md` |
|---|

**Activate when:** the output target is **Google Stitch**, or you need a machine-readable design system
document rather than code.

**What it does:** analyzes the brief and synthesizes a `DESIGN.md` with 9 sections — visual theme &
atmosphere, color palette & roles, typography rules, hero section, component stylings, layout principles,
responsive rules, motion philosophy, and **anti-patterns (AI tells)** — gated by four configurable dials
(Creativity `8`, Density `4`, Variance `8`, Motion Intent `6`). The bundled `DESIGN.md` is a worked
example ("Taste Standard") with exact hex roles and spring-physics motion notes.

---

## 19. `full-output-enforcement` — behavior modifier

| Directory [`output-skill/`](../output-skill/) · 📄 · 407 words (the shortest skill) · license undeclared |
|---|

Overrides default LLM truncation behavior: enforces complete code generation, bans placeholder patterns
(`// rest of code`, `...`, `<!-- omitted -->`, TODO stubs), defines an execution process, and specifies how
to split work cleanly across token limits plus a quick check.

**Carries no visual taste**, so it stacks safely with any taste skill — useful for large redesigns and
multi-file builds.

---

# D · Image direction

---

## 20. `imagegen-frontend-web` — website design references as images

| | |
|---|---|
| Directory | [`imagegen-frontend-web/`](../imagegen-frontend-web/) |
| Type | 📄 prompt-only · 5,790 words (987 lines) · license undeclared |

**Hard output rule (read first):** **one separate horizontal image per section.** 1 section → 1 image;
8 sections → 8 images. "Landing page" with no count defaults to 6 sections; "full website template" to 8.
Never a single tall composite. Announce each ("Section 3 of 8: Trust bar").

**Also enforces:** hero composition bias · brief-to-direction mapping · a **combinatorial variation
engine** (theme paradigm, background character, typography character, hero architecture, section system,
signature component set, motion-implied language, per-section composition anchor and background mode, CTA
variation, hero scale, narrative/concept spine, second-read moment) · frontend reference rules · hero
minimalism (absolute hero rules, headline rule, typography execution, graphic restraint) · image count and
page slicing · a single consistent palette across the set.

**Produces images only.** Hand off to `image-to-code` or a taste skill for implementation.

---

## 21. `imagegen-frontend-mobile` — app screen & flow images

| | |
|---|---|
| Directory | [`imagegen-frontend-mobile/`](../imagegen-frontend-mobile/) |
| Type | 📄 prompt-only · 6,532 words (1,465 lines) · license undeclared |

Premium, app-native screen concepts and flows for iOS, Android, and cross-platform products: onboarding,
auth, dashboards, profile, settings, chat, ecommerce, fintech, health/fitness, productivity, social,
utilities.

**Rule set (22 numbered sections):** platform mode (iOS-native / Android-native / cross-platform neutral) ·
mandatory screen-first · generate enough screens · never crop old images · app design bible ·
multi-screen consistency · logical flow · default mockup presence and device frame rules · onboarding flow ·
first-screen cleanliness · safe area and system regions · navigation · clean layout · creative image
direction · background texture and surfaces · image-behind-text · creative assets · iconography ·
**anti-AI-tells** (visual, layout, copy, UI clutter) · style variation engine.

**Generates images only — it does not write code.**

---

## 22. `image-to-code` — image-first website implementation

| | |
|---|---|
| Directory | [`image-to-code-skill/`](../image-to-code-skill/) |
| Type | 📄 prompt-only · 5,806 words (1,228 lines) · license undeclared |

**Activate when:** a visually important web task where the agent should generate the design image(s)
itself, analyze them deeply, then implement the site to match as closely as possible. Tuned for Codex.

**19 numbered rules** covering: baseline configuration · mandatory image-first · generate enough images ·
Codex-specific section images (large, readable, section-specific — not tiny compressed boards) · never crop
old images · fresh re-generation · optional detail/extraction images · clean analysis standard · deep image
analysis requirement · the image-first workflow · when to trigger generation · combinatorial variation
engine · website reference rule · hero minimalism (absolute rules, cleanliness, headline) · responsive
first-view · **anti-nested-box rule** (no cards-inside-cards-inside-cards) · reduce micro-UI clutter ·
section image generation · website image system.

---

# E · Art, themes & artifacts

---

## 23. `canvas-design` — museum-quality static art

| | |
|---|---|
| Directory | [`canvas-design/`](../canvas-design/) |
| Type | 🔧 (fonts + workflow) · 1,749 words · Apache-2.0 |
| Assets | `canvas-fonts/` — 54 families (108 files with OFL licenses) |

**Activate when:** a poster, piece of art, design, or other **static** work is requested. Creates original
visual designs; never copies existing artists' work.

**Two-step process:** 1) write a **design philosophy** (an aesthetic movement, `.md`) interpreted through
form, space, color, composition, pattern, and minimal text as visual accent; 2) express it on a canvas as a
single-page, design-forward `.pdf` or `.png`. Systematic-observation language (dense accumulation of marks,
repetition, layered patterns), sparse clinical typography, limited intentional palette, nothing overlapping
or off-page. Then a mandatory **refinement pass**: improve cohesion rather than adding more graphics.
Multi-page output is optional.

**Fonts:** search `./canvas-fonts/` and use different families; typography should be part of the art.

---

## 24. `algorithmic-art` — generative art with p5.js

| | |
|---|---|
| Directory | [`algorithmic-art/`](../algorithmic-art/) |
| Type | 🔧 · 2,746 words (404 lines) · Apache-2.0 |
| Assets | `templates/generator_template.js`, `templates/viewer.html` |

**Activate when:** art using code, generative/algorithmic art, flow fields, particle systems.

**Two-step process:** 1) create an **algorithmic philosophy** (`.md`) — computational processes, emergent
behavior, mathematical beauty, seeded randomness, noise fields, organic systems, parametric variation;
2) express it in p5.js (`.html` viewer + `.js` generator).

**Technical requirements:** Art Blocks-style seeded randomness (`randomSeed`/`noiseSeed`), a `params` object
designed around *tunable qualities* (quantities, scales, probabilities, ratios, angles, thresholds) rather
than "pattern types", craftsmanship requirements, and a strict **fixed vs. variable** separation for the
interactive artifact (parameter exploration UI). Includes philosophy examples, a conceptual-seed deduction
step, variation/exploration guidance, and the creative process.

**Read `templates/` before writing code** — the skill marks this as Step 0.

---

## 25. `theme-factory` — 10 preset themes

| | |
|---|---|
| Directory | [`theme-factory/`](../theme-factory/) |
| Type | 🔧 · 486 words · Apache-2.0 |
| Assets | `themes/*.md` (10) · `theme-showcase.pdf` |

**Activate when:** an existing artifact (slides, docs, reports, HTML landing page) needs a theme, or a new
theme must be generated on the fly.

**Themes:** Ocean Depths · Sunset Boulevard · Forest Canopy · Modern Minimalist · Golden Hour · Arctic
Frost · Desert Rose · Tech Innovation · Botanical Garden · Midnight Galaxy. Each `themes/<name>.md` holds
complete color and font specifications.

**Process (prescribed):** show `theme-showcase.pdf` **unmodified** → ask which theme → wait for explicit
confirmation → apply colors and fonts to the artifact.

---

## 26. `web-artifacts-builder` — complex claude.ai HTML artifacts

| | |
|---|---|
| Directory | [`web-artifacts-builder/`](../web-artifacts-builder/) |
| Type | 🔧 · 439 words · Apache-2.0 |
| Assets | `scripts/init-artifact.sh`, `scripts/bundle-artifact.sh`, `scripts/shadcn-components.tar.gz` |

**Activate when:** a complex artifact needs state management, routing, or shadcn/ui components.
**Not** for simple single-file HTML/JSX artifacts.

**Stack:** React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS 3.4.1 + shadcn/ui (40+
components pre-installed from the bundled tarball, all Radix deps included, `@/` path aliases, Node 18+
compatibility with auto-pinned Vite).

**Flow:** `bash scripts/init-artifact.sh <name>` → develop → `bash scripts/bundle-artifact.sh` → single
HTML file → share → optionally test.

**Style directive:** avoid "AI slop" — excessive centered layouts, purple gradients, uniform rounded
corners, Inter font.

**Requires:** bash, Node 18+, npm, and network access to the npm registry.

---

# F · Delivery & build

---

## 27. `gha-app-builder` — GitHub Actions as the build environment

| | |
|---|---|
| Directory | [`gha-app-builder/`](../gha-app-builder/) |
| Type | 🔧 · 1,104 words · license undeclared · **all files LF** (the only LF skill) |
| Assets | `SYSTEM_PROMPT.md` (**Arabic**) · 8 `references/` · `scripts/gha_mvp.py` |

**Activate when:** an agent must configure or repair `.github/workflows`, build Android / iOS / macOS /
Windows / Linux / web / Docker projects, trigger a remote workflow, monitor a run, diagnose failures,
retrieve artifacts, or publish releases.

**Mission:** GitHub Actions is the **authoritative** build environment. Locally you may inspect files,
validate configuration, generate a patch, and lint lightly — but never replace the requested remote build
with a local production build, and never report success until the remote run is terminal and its conclusion
is verified.

**Operating contract:** discover before changing (repo, branch/ref, remote, ecosystem, target platform,
output, channel, request type) → inspect existing automation and extend rather than duplicate → required
workflow shape → security gates → completion checklist.

**`scripts/gha_mvp.py` subcommands:** `inspect --repo .` · `validate --workflow <file>` ·
`dispatch --repo --workflow --ref [--inputs]` · `watch --repo --run-id [--interval --timeout]` ·
`run-report --repo --run-id`. Dependency-free; separates local static inspection from remote side effects;
does **not** create releases, mutate secrets, or run production builds locally.

**References:** `workflow-fundamentals.md`, `android.md`, `ios-macos.md`, `windows-desktop.md`,
`docker-and-web.md`, `monitoring-and-cli.md`, `secrets-and-signing.md`, `mvp-safety.md`.

**Requires:** `GH_TOKEN` or `GITHUB_TOKEN` for anything beyond `inspect`/`validate`; network access to
`api.github.com`.

**Success criteria (all five):** run `status=completed` · `conclusion=success` · repo/ref/head_sha/workflow
match the request · expected artifact present, unexpired, name/digest verified · signing/publish gates
passed where required.

---

# Cross-skill facts worth remembering

| Fact | Detail |
|---|---|
| **Byte-identical duplicates** | `design/references/slides-{create,layout-patterns,html-template,copywriting-formulas,strategies}.md` ≡ `slides/references/{create,layout-patterns,html-template,copywriting-formulas,slide-strategies}.md`; `design/references/banner-sizes-and-styles.md` ≡ `banner-design/references/banner-sizes-and-styles.md`; `ui-styling/canvas-fonts/*` ≡ `canvas-design/canvas-fonts/*` (all 108 files) |
| **Prompt-only vs tool-backed** | 17 skills are instructions only (`SKILL.md` ± `references/`) · 7 ship executable CLIs (`brand`, `design`, `design-system`, `ui-styling`, `ui-ux-pro-max`, `gha-app-builder`, `web-artifacts-builder`) · 3 ship fonts/templates/assets instead of CLIs (`canvas-design`, `algorithmic-art`, `theme-factory`) |
| **Search engines** | Three independent from-scratch BM25 implementations: `ui-ux-pro-max/scripts/core.py`, `design/scripts/{logo,cip}/core.py`, `design-system/scripts/slide_search_core.py` |
| **Line endings** | 270 files CRLF · 17 LF (all of `gha-app-builder`, plus a handful elsewhere) |
| **Licenses** | Apache-2.0 ×7 (`LICENSE.txt`) · MIT ×6 (frontmatter, `claudekit`) · SIL OFL for fonts · undeclared ×14 · `ui-styling` declares both MIT and Apache-2.0 |
| **Non-English content** | `gha-app-builder/SYSTEM_PROMPT.md` is Arabic by design |
| **No root manifest** | No `package.json`, no `pyproject.toml`, no CI workflow, no root `LICENSE`, no `.gitignore` in the upstream tree |
