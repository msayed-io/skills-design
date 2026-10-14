# Contributing to `skills-design`

> Conventions, contracts, and the review checklist for adding or editing a skill.
> Read [`AGENTS.md`](../AGENTS.md) first — it explains how the skills are actually consumed at runtime,
> which is what these conventions protect.

---

## 1. What this repository is for

A **library of independent, self-contained agent skills** for design, brand, frontend, and delivery work.
Two consequences drive every rule below:

1. **A skill must work when copied alone** into `.claude/skills/`, `~/.claude/skills/`, a plugin cache, or a
   non-Claude runtime. No repo-root imports, no shared build, no monorepo assumptions.
2. **A skill's cost is context.** Every word competes with the user's project. Prefer progressive disclosure
   (thin `SKILL.md` + on-demand `references/`) over one giant file, and prefer a searchable CSV over prose
   when the content is factual.

---

## 2. Skill anatomy

```
my-skill/
├── SKILL.md              # REQUIRED — the only mandatory file
├── references/*.md       # optional deep docs, loaded on demand
├── scripts/*.py|*.cjs    # optional tools (stdlib / Node built-ins only)
│   └── tests/            # optional pytest suites
├── data/*.csv            # optional knowledge base (header row + rows)
├── templates/            # optional starter artifacts
├── canvas-fonts/*.ttf    # only if the skill genuinely needs bundled fonts
└── LICENSE.txt           # only when required by the upstream source
```

### The frontmatter contract

```yaml
---
name: my-skill                      # REQUIRED — the activation identifier
description: >-                     # REQUIRED — the matcher text
  One dense paragraph: what it does, when to activate (actions, keywords,
  platforms, formats), and what it explicitly does NOT do.
argument-hint: "[subcommand] [args]" # optional — slash-command argument shape
license: MIT                         # optional — or "Complete terms in LICENSE.txt"
metadata:                            # optional
  author: someone
  version: "1.0.0"
---
```

**`description:` is the API.** An agent runtime decides activation from this string alone, so it must:

- start with the capability, then the triggers ("Use this when users request …");
- enumerate concrete keywords, platforms, formats, and numbers (`55 styles`, `1080×1080`, `22 stacks`) —
  specific tokens are what make matching reliable;
- state exclusions when the skill is narrow (`This skill generates images only. It does not write code.`);
- fit one paragraph. Compare `ui-ux-pro-max` and `imagegen-frontend-web` for good dense examples.

**`name:` must be a stable identifier.** If it differs from the directory name, that is allowed (10 skills do
it) but you **must** record the mapping in [`CATALOG.md`](CATALOG.md#directory--activation-name-map) and in
the README family table.

### Body structure that works

Observed in the strongest skills here:

1. A one-paragraph statement of the job and the output artifacts.
2. **When to activate / when to skip** — explicit both ways.
3. Numbered workflow steps (or numbered *rules* for prompt-only skills — `image-to-code` has 19,
   `imagegen-frontend-mobile` has 22).
4. Tables for anything enumerable (sizes, styles, flags, priorities, presets).
5. **Hard rules / banned patterns** ("AI tells") — the reason these skills exist.
6. A **pre-flight checklist** the agent must run before delivering.
7. Resource map: which `references/` file to open for which sub-task.

---

## 3. Path rules (non-negotiable)

Documented commands must resolve **from the skill directory**, with the **cwd at the project root**:

- `scripts/<file>` → this skill's own scripts.
- `../<other-skill>/scripts/<file>` → a sibling skill installed alongside it.
- Never `~/…`, never `<project-root>/scripts/…`, never a runtime-specific variable except in the one place
  it is explained (`ui-ux-pro-max` documents `${CLAUDE_PLUGIN_ROOT}` and says what to do when it is absent).

Scripts must locate their own data relative to `__file__` / `require.main` so they work from any cwd, and
must write **project** outputs (`docs/`, `assets/`, `src/`, `plans/reports/`) relative to cwd — never into
the skill directory.

---

## 4. Script conventions

| Rule | Detail |
|---|---|
| **Python: standard library only** | No `requests`, no `pandas`, no `pyyaml`. Third-party imports are allowed only for genuinely external work (image generation: `google-genai`, `pillow`) and must be **lazy** so `--help` and offline modes still work. (`design/scripts/icon/generate.py` currently imports eagerly and fails `--help` without `google-genai` — do not copy that pattern.) |
| **Node: built-ins only** | `fs`, `path`, `child_process`. Use `.cjs` so no `package.json` is needed. |
| **State the floor** | Python 3.10+, Node 18+. If you need more, say so in the skill. |
| **Argparse everywhere** | `--help` must be complete and honest; provide `--json` for machine consumption. |
| **Structured output for side-effecting tools** | `gha_mvp.py` prints JSON with an `ok` flag — follow that for anything that touches a remote system. |
| **Fail loudly and helpfully** | `brand/scripts/inject-brand-context.cjs` prints the exact missing path and what to create. Zero-result searches print an explicit "no match, retry narrower, label any fallback" instruction. |
| **Destructive actions need a guard** | `--dry-run` first-class; refuse to overwrite (`sync-brand-to-tokens.cjs` stops on detected token sources; `search.py --persist` skips an existing `MASTER.md` unless `--force`). |
| **Escape and validate** | `generate-slide.py` HTML-escapes user values and rejects non-`http(s)`/`#`/`/` URLs (CWE-79). Do the same for anything emitting HTML. |
| **Secrets** | Env or `.env` only (`<skill>/.env` → `~/.claude/skills/.env` → `~/.claude/.env`). Never log, never commit, never echo. |
| **UTF-8 on Windows** | Search CLIs re-wrap `sys.stdout`/`stderr` as UTF-8 because they print emoji; copy that guard if yours does. |

---

## 5. Data conventions

- CSV with a **header row**; one fact per row; stable IDs in the first column (`Style ID`, `Product Type`).
- Keep the knowledge base next to the skill (`data/`), and keep the search engine local
  (`core.py` / `slide_search_core.py` — three independent BM25 implementations exist here by design, because
  a skill must not import from a sibling).
- Declare which columns are searched vs. output (see `CSV_CONFIG` in `ui-ux-pro-max/scripts/core.py`).
- Record provenance for anything derived from an upstream catalog:
  `data/data-provenance.json` + `data/catalog-summary.json` (counts, `verifiedAt`, SHA-256 snapshots,
  promotion policy, pending candidates).
- **Validate after editing:** `python3 ui-ux-pro-max/scripts/validate_data.py`.
- Update the counts in `SKILL.md`'s `description:` **and** body whenever the data changes — those numbers are
  the matcher's evidence.

---

## 6. Repository hygiene

| Topic | Rule |
|---|---|
| **Line endings** | 270 files are CRLF, 17 are LF (all of `gha-app-builder`). **Match the file you edit.** Never mass-normalize — it destroys diffability and breaks the upstream-derived skills' expectations. |
| **Intentional duplicates** | `design/references/slides-*.md` ≡ `slides/references/*.md`; `design/references/banner-sizes-and-styles.md` ≡ `banner-design/references/banner-sizes-and-styles.md`; `ui-styling/canvas-fonts/*` ≡ `canvas-design/canvas-fonts/*`. If you change one, change the copy and keep them byte-identical. |
| **Fonts** | Only add a font family with its OFL file. Fonts are large; do not duplicate a font tree into a third skill. |
| **Generated artifacts** | Never commit `.pytest_cache/`, `__pycache__/`, generated logos, exported PNGs, `node_modules/`, or `.env`. |
| **Non-English content** | `gha-app-builder/SYSTEM_PROMPT.md` is Arabic on purpose. Don't translate in place; add a translation as a separate file if needed. |
| **Binary review** | `theme-factory/theme-showcase.pdf` and `web-artifacts-builder/scripts/shadcn-components.tar.gz` are intentional binaries referenced by their skills — don't delete or "optimize" them. |

---

## 7. Licensing

**There is deliberately no root `LICENSE`.** A blanket license would mis-license upstream work. Current map:

| License | Skills |
|---|---|
| Apache-2.0 (`LICENSE.txt` shipped) | `algorithmic-art`, `brand-guidelines`, `canvas-design`, `frontend-design`, `theme-factory`, `ui-styling`, `web-artifacts-builder` |
| MIT (frontmatter, `claudekit` author metadata) | `banner-design`, `brand`, `design`, `design-system`, `slides` |
| SIL OFL 1.1 | 54 font families in `canvas-design/canvas-fonts/` and `ui-styling/canvas-fonts/` (each with its `*-OFL.txt`) |
| Undeclared | `brandkit`, `brutalist-skill`, `gha-app-builder`, `gpt-tasteskill`, `image-to-code-skill`, `imagegen-frontend-mobile`, `imagegen-frontend-web`, `minimalist-skill`, `output-skill`, `redesign-skill`, `soft-skill`, `stitch-skill`, `taste-skill`, `taste-skill-v1`, `ui-ux-pro-max` |

Rules:

1. Copying a skill in from elsewhere? **Bring its license file and attribution**, and declare it in frontmatter.
2. `ui-styling` currently declares `license: MIT` in frontmatter *and* ships an Apache-2.0 `LICENSE.txt`
   (inherited with the canvas-font bundle). If you touch it, keep both and note the dual declaration —
   don't silently drop one.
3. Authoring something new here? Add `license:` to the frontmatter (and a `LICENSE.txt` if it isn't MIT).
4. Never relicense someone else's skill.
5. Treat undeclared skills as "all rights reserved" until the owner states otherwise.

---

## 8. Tests

Five skills ship pytest suites (18 files, **230 passing tests** on this checkout):

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
(cd ui-ux-pro-max/scripts && python -m pytest tests -q)   # 137 + 8,236 subtests (see note)
(cd ui-styling/scripts    && python -m pytest tests -q)   #  64
(cd brand/scripts         && python -m pytest tests -q)   #  15
(cd design/scripts/logo   && python -m pytest tests -q)   #  12
(cd design-system/scripts && python -m pytest tests -q)   #   2
```

**Known limitation:** four `ui-ux-pro-max` test files (`test_catalog_refresh.py`,
`test_catalog_summary_line_endings.py`, `test_relevance_evaluator.py`, `test_skill_script_paths.py`) fail at
*collection* in this distribution. They find the repo root with
`next(parent for parent in Path(__file__).parents if (parent / "scripts/<upstream-tool>").is_file())`,
looking for `generate-catalog-summary.py`, `refresh-google-fonts.py`, `refresh-icon-catalog.py`,
`evaluate-relevance.py`, and the trees `cli/assets/skills` / `.claude/skills` — none of which ship here — so
`next()` raises `StopIteration`. Either run them in the upstream monorepo, or make the anchor resolution
tolerant (fall back to a marker that exists in this distribution) before adding more tests that depend on it.

When adding scripts: add tests next to them in `scripts/tests/`, keep them stdlib + pytest only, and make sure
they pass from the skill's own `scripts/` directory.

---

## 9. Adding a new skill — checklist

- [ ] Directory named in `kebab-case`; frontmatter `name:` decided (and mapping recorded if it differs).
- [ ] `description:` written to the contract in §2 — triggers, keywords, numbers, exclusions.
- [ ] Body follows the structure in §2: when to use / when to skip / workflow / hard rules / pre-flight / resource map.
- [ ] Only stdlib Python or built-in Node; lazy imports for third-party extras.
- [ ] Paths documented skill-relative; cwd documented as the project root.
- [ ] Secrets via env/`.env` only; `--dry-run` for anything destructive; loud, helpful failure messages.
- [ ] Data in CSV with a header row + a validator or provenance record where relevant.
- [ ] License declared (frontmatter and/or `LICENSE.txt`), attribution carried over.
- [ ] Line endings consistent within the new files; nothing mass-normalized.
- [ ] Tests added under `scripts/tests/` if you shipped scripts, and they pass.
- [ ] **Docs updated:** README family table · `docs/CATALOG.md` entry (incl. the name map row) ·
      `docs/ROUTING.md` decision tree + combination matrix (especially if it overlaps an existing skill) ·
      `docs/CLI.md` if you shipped executables.
- [ ] Overlap declared: if your skill competes with an existing one, say which wins and when, in both entries.

## 10. Editing an existing skill — checklist

- [ ] You are not editing a **frozen** skill (`taste-skill-v1` is preserved for backward compatibility).
- [ ] Byte-identical duplicates updated in lockstep (§6).
- [ ] Counts in `description:`/body still match the data (§5).
- [ ] Line endings preserved; diff contains only intentional changes.
- [ ] Test suites still pass; `validate_data.py` still reports OK for data edits.
- [ ] If behavior changed, `docs/CATALOG.md` and `docs/CLI.md` changed with it.

---

## 11. Review lens

Reviewers should ask, in order:

1. **Would an agent activate this at the right time and only at the right time?** (description quality)
2. **Can it be executed correctly on the first try?** (path contract, flags, prerequisites, env vars)
3. **Does it cost less context than it saves?** (progressive disclosure, tables over prose, data over prose)
4. **Does it fail honestly?** (zero-result semantics, guards, verification steps)
5. **Does it conflict with an existing skill — and is that conflict documented and resolved?**
6. **Is the licensing clean and attributed?**
