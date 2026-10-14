# AGENTS.md — Operating Manual for `skills-design`

> **Audience:** AI agents (Claude Code, Codex, plugin runtimes, or any agent with file + shell access)
> working *inside* or *with* this repository.
> **Purpose:** make you use these 27 skills correctly on the first attempt — right skill, right path,
> right command, honest verification.
> **Read time:** ~6 minutes. Skim §1–§4 before doing anything; read the rest on demand.

Human-oriented project profile: [`README.md`](README.md). Per-skill detail: [`docs/CATALOG.md`](docs/CATALOG.md).

---

## 1. Prime directives

1. **Do not bulk-load skills.** `SKILL.md` files total ~62,000 words. Loading more than two at once
   burns context and produces contradictory instructions. Select → read one → act.
2. **One aesthetic authority per task.** Eight skills can act as the taste authority and they contradict
   each other (§3.3, §7). Pick exactly one — `design-taste-frontend` by default.
3. **Skill-relative paths, project-relative cwd.** Every documented command assumes:
   *paths resolve from the skill directory, the working directory stays at the project root* (§4).
4. **Search before you invent.** Three skills ship verified datasets (styles, palettes, fonts, UX rules,
   logo styles, CIP deliverables, slide strategies). Query them instead of generating hex codes,
   font names, or deck structures from memory.
5. **A zero-result search is an answer, not a failure.** Report it as "no verified match in the
   database", then fall back explicitly and label the fallback as general guidance.
6. **Never claim success without evidence.** For generated files: the file exists and opens. For tokens
   and slides: the validator passed. For remote builds: the workflow run reached
   `status=completed` **and** `conclusion=success` (§8.4).
7. **Never print, log, or commit secrets.** API keys live in env/`.env` only (§6).
8. **Do not "improve" this repository while using it.** You are a consumer here. Edits to skills are a
   separate, deliberate task governed by [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

---

## 2. What a skill is (the contract)

```
<skill-dir>/
├── SKILL.md      # REQUIRED
│   ├── YAML frontmatter  → the activation API
│   │   name:            ← the identifier runtimes register (NOT necessarily the dir name)
│   │   description:     ← the matcher text: when to activate, what it does, what it excludes
│   │   argument-hint:   ← optional slash-command argument shape
│   │   license:         ← optional
│   │   metadata:        ← optional (author, version)
│   └── Markdown body    → the execution instructions
├── references/*.md      # deep docs — load ON DEMAND, never eagerly
├── scripts/*.py|*.cjs   # executable tools (stdlib / builtins only)
├── data/*.csv           # searchable knowledge base (header row + rows)
├── templates/           # starter artifacts to copy and fill
├── canvas-fonts/*.ttf   # bundled fonts (canvas-design, ui-styling)
└── LICENSE.txt          # present for 7 Apache-2.0 skills
```

**Progressive disclosure is the design.** The body of `SKILL.md` tells you which `references/` file to
open for a given sub-task. Open exactly that file. Do not read the whole `references/` tree.

Sizes matter: `taste-skill/SKILL.md` is 12,793 words; `imagegen-frontend-mobile` 6,532;
`image-to-code-skill` 5,806. Budget accordingly — for these, read the numbered rule that matches your
sub-task rather than the whole file.

---

## 3. Skill selection algorithm

Run these five steps in order.

### Step 1 — Classify the request

| Class | Signal words | Go to |
|---|---|---|
| **Data / decisions** | "which style", "colors for", "font pairing", "UX rules", "chart type", "stack guidance" | `ui-ux-pro-max` |
| **Brand asset production** | logo, CIP, brand kit, icon set, mockups | `design` (+ `brandkit` for boards) |
| **System / tokens** | design tokens, component specs, CSS variables, brand sync | `brand` → `design-system` → `ui-styling` |
| **Frontend build** | landing page, portfolio, dashboard UI, "make it look good" | one taste skill (§3.3) |
| **Existing UI upgrade** | redesign, refresh, audit, "it looks dated" | `redesign-existing-projects` |
| **Image generation** | mockup images, design references, app screens as images | `imagegen-frontend-web` / `-mobile` |
| **Image → implementation** | "build this from the mockup" | `image-to-code` |
| **Presentation** | deck, pitch, slides | `design-system` (slide system) or `slides` |
| **Marketing asset** | banner, cover, social post, ad | `banner-design` or `design` (built-in) |
| **Print/poster/art** | poster, artwork, generative, p5.js | `canvas-design` / `algorithmic-art` |
| **Theming** | "apply a theme", palette swap on an artifact | `theme-factory` |
| **Complex HTML artifact** | multi-component React artifact for claude.ai | `web-artifacts-builder` |
| **Build / release** | CI, GitHub Actions, sign, package, artifacts | `gha-app-builder` |

### Step 2 — Resolve the activation name

Use the frontmatter `name:`, not the directory. **10 of 27 differ:**

| Directory | Activation `name:` |
|---|---|
| `brutalist-skill/` | `industrial-brutalist-ui` |
| `gpt-tasteskill/` | `gpt-taste` |
| `image-to-code-skill/` | `image-to-code` |
| `minimalist-skill/` | `minimalist-ui` |
| `output-skill/` | `full-output-enforcement` |
| `redesign-skill/` | `redesign-existing-projects` |
| `soft-skill/` | `high-end-visual-design` |
| `stitch-skill/` | `stitch-design-taste` |
| `taste-skill/` | `design-taste-frontend` |
| `taste-skill-v1/` | `design-taste-frontend-v1` |

The other 17 match their directory name. Full table: [`docs/CATALOG.md`](docs/CATALOG.md#directory--activation-name-map).

### Step 3 — If the task is visual, pick ONE taste authority

| Situation | Skill | Why |
|---|---|---|
| Default / unsure | **`design-taste-frontend`** (`taste-skill/`) | Most complete v2: brief inference → dials → official DS selection → pre-flight |
| Project already pinned to v1 behavior | `design-taste-frontend-v1` | Frozen compatibility only |
| Agent is GPT-family, motion-heavy brief | `gpt-taste` | GSAP ScrollTrigger paradigms, AIDA, randomization protocol |
| "Make it feel expensive" | `high-end-visual-design` | Agency-grade component/motion specs |
| Explicitly minimal, warm, editorial | `minimalist-ui` | Banned-elements list, warm monochrome |
| Explicitly brutalist / terminal / data-dense | `industrial-brutalist-ui` | Two mutually exclusive archetypes — pick one |
| Output target is **Google Stitch** | `stitch-design-taste` | Emits a `DESIGN.md` semantic system |
| Anthropic guidance flavor wanted | `frontend-design` | Subject-grounding + restraint |

Then optionally stack a **behavior modifier** (these do not carry taste, so they combine safely):
`full-output-enforcement` (no truncation, no placeholders).

### Step 4 — Check whether the skill needs a sibling

`design` routes to `brand`, `design-system`, `ui-styling` via `../<skill>/scripts/…`. If those
directories are not installed side by side, either install them or fall back to `design`'s built-in
references (`references/logo-*.md`, `references/cip-*.md`, `references/slides-*.md`, …), which are
self-contained.

### Step 5 — State the choice before executing

Emit one line, e.g.:

```
Skill: ui-ux-pro-max (data) + design-taste-frontend (taste). Not loading: brandkit, slides, canvas-design.
```

This makes the decision auditable and prevents mid-task skill creep.

---

## 4. Path resolution contract (the #1 source of agent errors)

Rules, verbatim from the skills themselves:

- `scripts/<file>` = **this skill's own** `scripts/` folder.
- `../<other-skill>/scripts/<file>` = a **sibling** skill installed alongside it.
- Build the absolute path from the skill's base directory (the runtime reports it when the skill loads).
- **Keep the working directory at the project root** — scripts read/write project files relative to cwd:
  `docs/brand-guidelines.md`, `assets/design-tokens.json`, `assets/design-tokens.css`, `src/`, `plans/reports/`.

### Two invocation styles that both work

**A. Absolute path, cwd = project root (preferred):**

```bash
python3 /path/to/skills/ui-ux-pro-max/scripts/search.py "fintech dashboard" --domain product
node    /path/to/skills/brand/scripts/inject-brand-context.cjs --json
```

These scripts resolve their own data directories relative to `__file__` / `require.main`, so they work
from any cwd. Verified in this checkout.

**B. cwd = the skill's `scripts/` directory** — required only if a script does a bare sibling import
(`from core import …`). Also verified working:

```bash
cd /path/to/skills/design/scripts/logo && python3 search.py "tech" --domain style
```

### Plugin-runtime form

`ui-ux-pro-max/SKILL.md` documents:

```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --domain <domain>
```

`${CLAUDE_PLUGIN_ROOT}` exists **only** under a Claude plugin install. Under a plain directory copy or a
non-Claude runtime, substitute the real path. If `python` is missing, try `python3`, then `py -3`
(Windows).

### What never works

- ❌ `python3 scripts/search.py` from the **repository root** — there is no root `scripts/`.
- ❌ Assuming `~/.claude/skills/<name>` when the skill was installed per-project.
- ❌ Writing generated tokens to the skill directory. Outputs belong to the **project**: `assets/`, `docs/`, `src/`.

---

## 5. Execution rules by skill family

### 5.1 Data skills — `ui-ux-pro-max`, `design/*/search.py`, `design-system/search-slides.py`

1. **Choose the smallest search mode that fits** (`ui-ux-pro-max` query contract):
   - new project/page or system-wide direction → `--design-system`
   - targeted concern or component bug → one explicit `--domain`
   - known implementation stack → `--stack`
2. **One dominant intent per query, 2–5 meaningful terms**, plus one constraint (product, platform, interaction).
3. **Verify the result** — check the returned domain, the top result's identity, and its fit for the
   user's product/platform *before* applying it.
4. **Retry once** with a narrower rewrite or an explicit `--domain` / `--stack` if the output is empty or off-topic.
5. **Do not persist unverified output.**
6. Accessibility work: query the **observable outcome** first (`"error summary validation" --domain ux`,
   `"focus not obscured" --domain ux`), then component-specific (`--domain icons`), then the stack.
   Never accept a generic accessibility result for a specific WCAG criterion.
7. Text-layout/compact-component bugs: semantic UX outcome first, then `--stack <stack>` for implementation.
8. Persisting a design system: always pass `--output-dir <project-root>` explicitly. Persistence is
   **skipped if `MASTER.md` exists** unless `--force` — that guard protects prior design decisions.

### 5.2 Generation skills — `design` (logo / CIP / icon), image-direction skills

- **Brief first, pixels second.** `search.py --design-brief` / `--brief` costs nothing and needs no key.
  Generate only after the brief is agreed.
- Requires an API key + `pip install google-genai pillow` for logo/CIP; `icon/generate.py` writes SVG text.
- Prefer `--logo <path>` on `cip/generate.py` so real brand marks are used instead of invented ones.
- `imagegen-frontend-web`: **one image per section** — 8 sections = 8 images. Never one tall composite.
  Announce each ("Section 3 of 8: …").
- `imagegen-frontend-mobile`: screens inside a subtle device frame by default; multi-screen consistency
  and safe areas are hard rules. **Images only — it does not write code.**
- `image-to-code`: generate → analyze deeply → implement to match. Do not crop old images; regenerate
  fresh ones for detail views.
- `brandkit` and the imagegen skills produce **images**, not source files. If the user needs code,
  chain into a taste skill afterwards.

### 5.3 System skills — `brand`, `design-system`, `ui-styling`

Order of operations for a new brand → system → UI pipeline:

```
1. brand        → docs/brand-guidelines.md           (source of truth)
2. design-system→ assets/design-tokens.json + .css   (primitive → semantic → component)
3. ui-styling   → tailwind config, shadcn/ui setup, component code
4. validators   → node scripts/validate-tokens.cjs, python3 scripts/html-token-validator.py
```

- `brand/scripts/sync-brand-to-tokens.cjs` **stops** when it detects existing token files, `:root`
  custom properties, Tailwind v4 `@theme` variables, or Tailwind theme colors/presets. Read the
  reported source before proceeding. Re-run with `--force` **only** when overwriting the managed
  `assets/design-tokens.*` outputs is intentional.
- Slides produced by `design-system` must use CSS variables from `design-tokens.css`. **No hardcoded
  colors, fonts, or spacing.** Validate with `slide-token-validator.py`.
- `ui-styling/scripts/shadcn_add.py` shells out to the shadcn CLI: use `--dry-run` first, and
  `--list` to see available components.

### 5.4 Taste skills (prompt-only)

- Apply their **dials** as named globals: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`
  (baseline `8 / 6 / 4` in `design-taste-frontend`). Never invent aliases like `LAYOUT_VARIANCE`.
- Do the **brief inference / design read** first and output the one-line read before generating.
- If the brief is ambiguous, **ask one question** — do not guess.
- Run the skill's **pre-flight checklist** before delivering. These checklists are the point of the skill.
- When the brief names a real design system (Fluent, Material, Carbon, Polaris, Atlaskit, Primer,
  GOV.UK, USWDS, Bootstrap, Radix Themes, shadcn/ui, Tailwind v4), **install the official package**.
  Do not hand-recreate its CSS. One system per project.

### 5.5 Build skill — `gha-app-builder`

- GitHub Actions is the **authoritative** build environment. Locally you may inspect, validate config,
  generate a patch, lint — but do **not** substitute a local production build for the requested remote one.
- Inspect `.github/workflows/*.yml|yaml` first; extend an existing workflow instead of duplicating it.
- Use `scripts/gha_mvp.py inspect` / `validate` / `dispatch` / `watch` / `run-report`.
- Success = run terminal **and** `conclusion=success` **and** repo/ref/head_sha/workflow match **and**
  the expected artifact exists and is unexpired. Anything less: report the failure with a diagnosis.
- `SYSTEM_PROMPT.md` in that skill is written in Arabic on purpose.

---

## 6. Environment & secrets

| Variable | Skill | Required for |
|---|---|---|
| `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) | `design` | logo/CIP/icon **generation** |
| `ATLASCLOUD_API_KEY` | `design` | `--provider atlas` |
| `MUAPI_API_KEY` | `design` | `--provider muapi` |
| `GH_TOKEN` / `GITHUB_TOKEN` | `gha-app-builder` | dispatch, watch, run reports |
| `DESIGN_SYSTEM_PROJECT_ROOT` | `design-system` | override cwd for validators/fetchers |

`.env` lookup order used by the generators: skill root `.env` → `~/.claude/skills/.env` → `~/.claude/.env`.

**Hard rules:** search/brief/validate commands need **no keys**. If a key is missing, do the offline part
of the job (brief, data, structure) and tell the user exactly which variable to set for the generation
step. Never hardcode a key into a file, a prompt, a workflow, or your output. Never echo `$GEMINI_API_KEY`.

Optional installs, and only when the task needs them:

```bash
pip install google-genai pillow      # design generation
npm i -D playwright                  # or use Chrome headless / Puppeteer for screenshot export
```

---

## 7. Conflict resolution

Overlaps in this library are intentional. Resolve them like this:

| Conflict | Resolution |
|---|---|
| Two taste skills loaded | Keep one (§3.3). `design-taste-frontend` wins by default. |
| `design` vs `slides` | `design/references/slides-*.md` are byte-identical copies of `slides/references/*.md`. Use `design`'s built-in path when `design` is active; use standalone `slides` when you want the narrow skill. |
| `design` vs `banner-design` | Same: `banner-sizes-and-styles.md` is identical in both. |
| `design-system` slides vs `slides` | `design-system` is token-driven and validator-backed (brand-compliant decks). `slides` is reference-only strategy. Prefer `design-system` when tokens exist. |
| `ui-ux-pro-max` vs a taste skill | Not a conflict: `ui-ux-pro-max` supplies **data** (palettes, fonts, UX rules, stack guidance), the taste skill supplies **opinion and discipline**. Data first, then taste. |
| `canvas-design` vs `ui-styling` canvas layer | `canvas-design` = standalone art/poster output. `ui-styling` = canvas inside a UI project. They ship identical font trees; don't duplicate the fonts. |
| `brand-guidelines` vs `brand` | `brand-guidelines` = Anthropic's specific identity. `brand` = *your* brand system. Don't mix them in one artifact. |
| `design-taste-frontend` vs `-v1` | v2 unless the project explicitly depends on v1 behavior. |
| `minimalist-ui` vs `industrial-brutalist-ui` | Mutually exclusive aesthetics. Also: `industrial-brutalist-ui` itself has two archetypes (Swiss light / CRT dark) — pick one and never mix inside a single interface. |
| `imagegen-*` vs `image-to-code` | `imagegen-*` stops at images. `image-to-code` continues into implementation. |

---

## 8. Verification checklists

### 8.1 Any UI/frontend output
- [ ] No AI tells: centered-hero-with-purple-gradient, Inter everywhere, uniform rounded corners, emoji as icons, `Jane Doe` placeholder content, cards-inside-cards.
- [ ] Contrast ≥ 4.5:1, focus rings visible, keyboard reachable, icon-only buttons labeled.
- [ ] Touch targets ≥ 44×44px, spacing ≥ 8px, loading feedback present.
- [ ] No horizontal scroll; mobile-first breakpoints; `prefers-reduced-motion` honored.
- [ ] Colors/spacing/typography come from tokens or a searched palette — not raw hex scattered in components.
- [ ] Dependencies verified to exist at the stated versions before import.

### 8.2 Brand / token output
- [ ] `docs/brand-guidelines.md` exists and is the single source of truth.
- [ ] `assets/design-tokens.json` + `assets/design-tokens.css` generated, three layers intact.
- [ ] `node <design-system>/scripts/validate-tokens.cjs` passes.
- [ ] No hardcoded color/font/spacing in generated slides or components.

### 8.3 Slides / decks
- [ ] Strategy chosen from `slide-strategies.csv` (not invented).
- [ ] Layout, typography, color, and background each resolved via the decision CSVs.
- [ ] `python3 <design-system>/scripts/slide-token-validator.py` passes on every slide.
- [ ] Charts use the Chart.js config from `slide-charts.csv`; legends + tooltips + accessible colors.
- [ ] Pattern-breaking beats present (no 10 identical slides).

### 8.4 Remote builds (`gha-app-builder`)
- [ ] Workflow inspected/validated before dispatch (`gha_mvp.py inspect|validate`).
- [ ] Run reached `status=completed` and `conclusion=success`.
- [ ] `repository`, `ref`, `head_sha`, and workflow name match the request.
- [ ] Artifact present, unexpired, name/digest verified.
- [ ] Signing/publish gates passed where required.
- [ ] Report includes the run URL and conclusion — not "should be fine".

### 8.5 Generated images
- [ ] Count matches the request (one per section for `imagegen-frontend-web`).
- [ ] Text legible at delivery size; nothing cropped or overlapping.
- [ ] Single consistent palette across the set.
- [ ] Actually opened/inspected, not assumed correct.

---

## 9. Anti-patterns (do not do these)

- ❌ `cat`-ing every `SKILL.md` "to understand the repo". Read this file + `docs/CATALOG.md` instead.
- ❌ Loading `references/` wholesale. Load the one file the body points to.
- ❌ Running `python3 scripts/...` from the repo root (§4).
- ❌ Writing outputs into a skill directory. Outputs go to the **project**.
- ❌ Inventing hex codes, font pairings, logo styles, deck structures, or CIP deliverables when a
      searchable dataset exists.
- ❌ Persisting a design system with `--force` over someone's `MASTER.md` without asking.
- ❌ Reporting a search miss as a success, or silently substituting generic advice for a missing match.
- ❌ Declaring a build successful because a workflow file was written or a dispatch returned 200.
- ❌ Mixing two design systems or two taste skills in one tree.
- ❌ Translating `gha-app-builder/SYSTEM_PROMPT.md`, normalizing line endings repo-wide, or adding a
      blanket root `LICENSE`.
- ❌ Committing `.env`, API keys, generated logos, or `node_modules` into this repo.

---

## 10. Reporting back to the user

End every task with:

```
Skill(s) used      : <activation names> (+ which you deliberately did NOT load)
Commands run       : <exact invocations>
Data consulted     : <domain/rows/results, or "no verified match">
Files created      : <project-relative paths>
Verification       : <validators run + results / run URL + conclusion / images inspected>
Open items         : <missing API key, unanswered question, known limitation>
```

If a limitation is structural (e.g. the 4 upstream-only tests in `ui-ux-pro-max`, or a missing API key),
say so plainly instead of working around it silently.

---

## 11. Quick reference card

```
REPO          27 skills · 394 files · 99 md (~104.9k words) · 53 CSV (4,757 rows) · 50 scripts
RUNTIME       Python 3.9+ stdlib only · Node 18+ builtins only · bash for web-artifacts-builder
NO INSTALL    search, briefs, validators, token generation, config generation
KEYS NEEDED   only for design logo/CIP/icon generation + gha dispatch
TESTS         230 passing across 5 suites (4 ui-ux-pro-max files need the upstream monorepo)
LINE ENDINGS  270 CRLF · 17 LF (gha-app-builder) — match, don't normalize
NAME ≠ DIR    10 skills — see §3.2
DEFAULT TASTE design-taste-frontend (dials 8/6/4)
DEFAULT DATA  ui-ux-pro-max/scripts/search.py
DOCS          README.md · docs/CATALOG.md · docs/ROUTING.md · docs/CLI.md · docs/CONTRIBUTING.md
```
