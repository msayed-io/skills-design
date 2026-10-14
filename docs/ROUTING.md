# Routing Guide — task → skill → sequence

> How to pick the right skill (and the right *combination*) for a request, with end-to-end playbooks.
> Selection algorithm: [`AGENTS.md §3`](../AGENTS.md) · per-skill detail: [`CATALOG.md`](CATALOG.md) ·
> exact commands: [`CLI.md`](CLI.md).

---

## 1. Master decision tree

```
What is the user actually asking for?
│
├─ CODE that runs (site, app, component, artifact)
│   │
│   ├─ Existing project to improve ──────────────► redesign-existing-projects
│   │                                              (+ ui-ux-pro-max for the audit data)
│   │
│   ├─ New frontend, taste matters ──────────────► design-taste-frontend  [pick ONE taste skill]
│   │       │                                      + ui-ux-pro-max (data first)
│   │       ├─ GPT-family agent, motion-heavy ───► gpt-taste
│   │       ├─ "make it feel expensive" ─────────► high-end-visual-design
│   │       ├─ explicitly minimal/warm ──────────► minimalist-ui
│   │       ├─ explicitly brutalist/terminal ────► industrial-brutalist-ui
│   │       └─ output truncated / huge build ────► + full-output-enforcement
│   │
│   ├─ Component/styling implementation ─────────► ui-styling  (shadcn/ui + Tailwind + a11y)
│   │
│   ├─ Multi-component claude.ai artifact ───────► web-artifacts-builder
│   │
│   └─ Build / sign / release ───────────────────► gha-app-builder
│
├─ IMAGES (not code)
│   │
│   ├─ Website section references ───────────────► imagegen-frontend-web  (1 image per section)
│   ├─ App screens / flows ──────────────────────► imagegen-frontend-mobile
│   ├─ Brand boards / logo systems / identity ───► brandkit
│   ├─ Poster / static art ──────────────────────► canvas-design
│   ├─ Generative / code art ────────────────────► algorithmic-art
│   └─ …then implement the images ───────────────► image-to-code
│
├─ BRAND SYSTEM (identity, tokens, governance)
│   │
│   ├─ Deliverables: logo, CIP, icons, banners,
│   │  social photos, decks ─────────────────────► design   (the router)
│   ├─ Voice / messaging / asset governance ─────► brand
│   ├─ Tokens / component specs / CSS vars ──────► design-system
│   ├─ Pipeline: brand → tokens → code ──────────► brand ➜ design-system ➜ ui-styling
│   └─ Anthropic's own look ─────────────────────► brand-guidelines
│
├─ DECISIONS / DATA ("which style? colors? fonts? UX rule? chart? stack pattern?")
│   └────────────────────────────────────────────► ui-ux-pro-max   (search, then decide)
│
├─ PRESENTATIONS
│   ├─ Tokens exist / brand-compliant ───────────► design-system (slide system + validators)
│   ├─ Strategy & copy only ─────────────────────► slides
│   └─ Re-theme an existing artifact ────────────► theme-factory
│
├─ MARKETING ASSETS
│   ├─ Banners / covers / heroes / ads ──────────► banner-design  (or design's built-in)
│   └─ Social images at exact px ────────────────► design (social photos module)
│
└─ DESIGN SYSTEM DOCUMENT for Google Stitch ─────► stitch-design-taste  (emits DESIGN.md)
```

---

## 2. Playbooks

Each playbook lists the sequence, the skills, and the verification step. Commands assume
`SKILLS=/path/to/skills-design` and cwd = **your project root**.

### P1 · Brand-new product identity, end to end

```
design (brief) ➜ design (logo) ➜ brand (guidelines) ➜ design-system (tokens) ➜ ui-styling (code)
```

```bash
python3 $SKILLS/design/scripts/logo/search.py "fintech trust modern" --design-brief -p "Acme"
export GEMINI_API_KEY="..."
python3 $SKILLS/design/scripts/logo/generate.py --brand "Acme" --industry finance --batch 4 --output-dir assets/logo
cp $SKILLS/brand/templates/brand-guidelines-starter.md docs/brand-guidelines.md   # then fill it in
node    $SKILLS/brand/scripts/sync-brand-to-tokens.cjs --dry-run
node    $SKILLS/brand/scripts/sync-brand-to-tokens.cjs
node    $SKILLS/design-system/scripts/validate-tokens.cjs
python3 $SKILLS/ui-styling/scripts/tailwind_config_gen.py --framework react --validate-only
```
**Verify:** tokens validator passes · `assets/design-tokens.{json,css}` exist · no hardcoded hex in `src/`.

### P2 · Corporate identity program (CIP) with real logo

```
design (logo) ➜ design (CIP) ➜ design (render HTML deck)
```

```bash
python3 $SKILLS/design/scripts/cip/search.py "consultancy premium" --domain style
python3 $SKILLS/design/scripts/cip/generate.py --brand "Acme" --logo assets/logo/acme.png --output-dir assets/cip
python3 $SKILLS/design/scripts/cip/generate.py --brand "Acme" --all --pro          # full deliverable set, 4K text
python3 $SKILLS/design/scripts/cip/render-html.py --input assets/cip --output assets/cip/index.html
```
**Verify:** every generated mockup opens; the real logo (not an invented one) appears in the deliverables.

### P3 · Landing page that does not look AI-generated

```
ui-ux-pro-max (data) ➜ design-taste-frontend (taste) ➜ [build] ➜ pre-flight check
```

```bash
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "saas analytics landing" --design-system \
        --variance 8 --motion 6 --density 4 --persist --output-dir .
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "editorial hero serif" --domain style -n 2
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "landing page conversion" --domain landing -n 2
```
**Verify:** one-line Design Read emitted · dials named exactly · official DS installed if the brief named one ·
skill's pre-flight checklist run · no AI tells from `AGENTS.md §8.1`.

### P4 · Redesign an existing site without breaking it

```
redesign-existing-projects (audit) ➜ ui-ux-pro-max (evidence) ➜ fix by priority ➜ full-output-enforcement
```

Audit all 10 dimensions first, write the findings down, then fix in the skill's priority order.
**Verify:** functionality unchanged (routes, forms, states) · audit items closed · diff reviewed.

### P5 · Design references as images, then implement

```
imagegen-frontend-web (N sections = N images) ➜ image-to-code ➜ design-taste-frontend
```

For mobile: `imagegen-frontend-mobile` instead.
**Verify:** image count == section count · consistent palette across the set · text legible · hero clean on a
small laptop · implementation matches the analyzed images.

### P6 · Investor deck, brand-compliant

```
design-system (strategy search) ➜ design-system (generate slides) ➜ validators ➜ theme-factory (optional)
```

```bash
python3 $SKILLS/design-system/scripts/search-slides.py "investor pitch" -d strategy -n 1
python3 $SKILLS/design-system/scripts/search-slides.py "problem slide" --context --position 2 --total 10
python3 $SKILLS/design-system/scripts/search-slides.py "cta" --context --position 10 --prev-emotion frustration
python3 $SKILLS/design-system/scripts/generate-slide.py --json slide.json --output deck/slide-02.html
python3 $SKILLS/design-system/scripts/slide-token-validator.py deck/slide-02.html
```
**Verify:** token validator passes on every slide · pattern-breaking beats present · charts from
`slide-charts.csv`.

### P7 · Icon set

```bash
python3 $SKILLS/design/scripts/icon/generate.py --prompt "dashboard navigation" --style duotone --batch 6 --output-dir assets/icons
python3 $SKILLS/design/scripts/icon/generate.py --prompt "user profile" --sizes "16,24,32,48"
```
**Verify:** SVGs are valid XML · all requested sizes exported · no emoji used as icons.

### P8 · Social campaign images at exact pixel sizes

```
brand (context) ➜ design-system (tokens) ➜ ui-ux-pro-max (patterns) ➜ HTML/CSS ➜ screenshot export
```

```bash
node $SKILLS/brand/scripts/inject-brand-context.cjs --json      # feed this into the prompt
```
Sizes: IG post 1080×1080 · IG story 1080×1920 · IG carousel 1080×1350 · FB post 1200×630 ·
X post 1200×675 · LinkedIn 1200×627 · YT thumb 1280×720 · Pinterest 1000×1500.
**Verify:** exported PNGs opened and inspected at exact px; layout issues fixed and re-exported.

### P9 · Accessibility / UX review

```bash
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "error summary validation" --domain ux
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "focus not obscured" --domain ux
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "icon button accessible label" --domain icons
python3 $SKILLS/ui-ux-pro-max/scripts/search.py "chip badge overflow nowrap" --stack html-tailwind
```
Order: **semantic outcome → component domain → stack**. Read `references/pro-rules.md` for the
pre-delivery checklist.
**Verify:** contrast ≥ 4.5:1 · targets ≥ 44×44 · keyboard paths · labels · reduced-motion.

### P10 · Poster / generative art

```
canvas-design: philosophy (.md) ➜ canvas (.png/.pdf) ➜ refinement pass
algorithmic-art: philosophy (.md) ➜ read templates/ ➜ generator (.js) + viewer (.html)
```
**Verify:** nothing overlaps or leaves the canvas · fonts pulled from `canvas-fonts/` · seeded randomness
reproducible · the mandatory second refinement pass actually happened.

### P11 · Ship a build through GitHub Actions

```bash
python3 $SKILLS/gha-app-builder/scripts/gha_mvp.py inspect --repo .
python3 $SKILLS/gha-app-builder/scripts/gha_mvp.py validate --workflow .github/workflows/release.yml
python3 $SKILLS/gha-app-builder/scripts/gha_mvp.py dispatch --repo owner/name --workflow release.yml --ref main
python3 $SKILLS/gha-app-builder/scripts/gha_mvp.py watch --repo owner/name --run-id 123456
python3 $SKILLS/gha-app-builder/scripts/gha_mvp.py run-report --repo owner/name --run-id 123456
```
**Verify:** all five success criteria in [`CATALOG.md §27`](CATALOG.md#27-gha-app-builder--github-actions-as-the-build-environment).
Never report success from a written workflow or a 200 response to a dispatch.

### P12 · Complex claude.ai artifact

```bash
bash $SKILLS/web-artifacts-builder/scripts/init-artifact.sh my-artifact
cd my-artifact && …develop…
bash $SKILLS/web-artifacts-builder/scripts/bundle-artifact.sh
```
**Verify:** single bundled HTML file opens standalone · no AI-slop styling · state/routing work.

---

## 3. Combination matrix

**Stacks safely** (different jobs):

| Base | Add | Why it works |
|---|---|---|
| `ui-ux-pro-max` | any taste skill | data layer + opinion layer |
| any taste skill | `full-output-enforcement` | taste + output discipline, no overlap |
| `brand` | `design-system` → `ui-styling` | the documented pipeline |
| `design` | `brandkit` | deliverables + presentation boards |
| `redesign-existing-projects` | `ui-ux-pro-max` | audit dimensions need evidence |
| `imagegen-frontend-web` | `image-to-code` | images → implementation |
| `design-system` (slides) | `theme-factory` | structure → theme |
| `canvas-design` | `algorithmic-art` | only if the brief wants both static and generative output |

**Never combine** (same job, contradictory rules):

| ❌ | ❌ | Conflict |
|---|---|---|
| `design-taste-frontend` | `gpt-taste` / `high-end-visual-design` / `minimalist-ui` / `industrial-brutalist-ui` / `stitch-design-taste` / `frontend-design` | Two taste authorities → contradictory typography, layout, and motion rules |
| `design-taste-frontend` | `design-taste-frontend-v1` | Two versions of the same skill |
| `minimalist-ui` | `industrial-brutalist-ui` | Opposite aesthetics (and brutalist's two archetypes are themselves exclusive) |
| `brand` | `brand-guidelines` | Your identity vs. Anthropic's |
| `design` (slides/banner built-ins) | `slides` / `banner-design` | Identical content, duplicate loading |
| `imagegen-frontend-web` | `image-to-code` *at the same time* | Sequence them: images first, then implementation |

---

## 4. Ambiguity handling

| If the request says… | Ask / assume |
|---|---|
| "make a website" with no other detail | `design-taste-frontend` §0 requires a one-line Design Read; if still ambiguous, ask **one** question (product + audience) |
| "design a logo" with no industry | Run `logo/search.py --design-brief` — it infers industry from the query; confirm before generating |
| "slides" with no count | `design-system` contextual search needs `--position` and `--total`; ask for the deck length or default to a strategy from `slide-strategies.csv` |
| "landing page images" with no section count | `imagegen-frontend-web` defaults: "landing page" → 6 sections, "full website template" → 8 |
| "make it accessible" | Query observable outcomes one at a time (`AGENTS.md §5.1`), never a generic result |
| "build the app" locally | `gha-app-builder` forbids substituting a local production build — confirm the remote workflow |
| "use our brand" with no brand file | Create `docs/brand-guidelines.md` from `brand/templates/brand-guidelines-starter.md` first |

---

## 5. When *nothing* here fits

This library is design/brand/frontend + one build skill. It has **no** skill for: backend architecture,
database design, API contracts, non-visual performance work, infrastructure/DevOps (beyond GitHub Actions
builds), test strategy, or security review. Say so explicitly rather than forcing a design skill onto a
non-design problem — `ui-ux-pro-max` states this exclusion itself.
