# Workflow Fundamentals — Full Reference

## File location and naming

- Every workflow lives at `.github/workflows/<anything>.yml` (or `.yaml`).
- One repo can have many workflow files; each is independent unless you explicitly chain
  them (`workflow_call`, `workflow_run`).
- `name:` at the top is just the display name shown in the Actions tab; the filename is
  what you reference from `gh workflow run <filename>`.

## Full annotated skeleton

```yaml
name: Build and Release

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        type: choice
        options: [staging, production]
        default: staging

permissions:
  contents: write        # needed to create Releases; default should be `read`

env:
  NODE_ENV: production   # available to every job/step below

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm test

  build:
    needs: test                       # waits for `test` to succeed first
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: echo "building on ${{ matrix.os }}"
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.os }}
          path: dist/
          retention-days: 14

  release:
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - uses: softprops/action-gh-release@v2
        with:
          files: build-*/**
```

## Key contexts (the `${{ ... }}` variables)

| Context | Examples |
|---|---|
| `github.*` | `github.ref`, `github.sha`, `github.event_name`, `github.actor`, `github.repository` |
| `secrets.*` | `secrets.MY_TOKEN` — only resolvable server-side, never printed |
| `vars.*` | Non-secret repo/org variables, same UI as secrets but plaintext |
| `matrix.*` | Current combination inside a `strategy.matrix` job |
| `needs.<job>.outputs.*` | Values a previous job explicitly exposed via `outputs:` |
| `inputs.*` | Values passed to `workflow_dispatch` or `workflow_call` |
| `steps.<id>.outputs.*` | Output of a specific earlier step (needs `id:` on that step) |

Conditional execution:

```yaml
- name: Deploy only on main
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh
```

## Passing data between steps and jobs

```yaml
# Step -> later step in the SAME job
- id: version
  run: echo "value=1.2.3" >> "$GITHUB_OUTPUT"
- run: echo "Building ${{ steps.version.outputs.value }}"

# Job -> a DIFFERENT job needs an explicit `outputs:` map
jobs:
  a:
    outputs:
      version: ${{ steps.version.outputs.value }}
    steps: [ ... ]
  b:
    needs: a
    steps:
      - run: echo "${{ needs.a.outputs.version }}"
```

## Caching

Most `setup-*` actions have a built-in `cache:` option (shown above for
`setup-node`). For anything else, use the generic cache action:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.gradle/caches
    key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle*') }}
    restore-keys: gradle-${{ runner.os }}-
```

## Reusable workflows and composite actions

When the same build steps are needed from several workflows (e.g. "build Android" shared
between a PR-check pipeline and a nightly pipeline), factor it out:

```yaml
# .github/workflows/build-android.yml
on:
  workflow_call:
    outputs:
      apk-path:
        value: ${{ jobs.build.outputs.apk-path }}
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      apk-path: ${{ steps.build.outputs.path }}
    steps: [ ... ]
```

```yaml
# caller workflow
jobs:
  android:
    uses: ./.github/workflows/build-android.yml
```

## Environments (approval gates, per-stage secrets)

Define an "environment" (e.g. `production`) in repo Settings, optionally requiring manual
approval or restricting which branches can deploy to it, then:

```yaml
jobs:
  deploy:
    environment: production   # pauses for reviewer approval if configured
    runs-on: ubuntu-latest
    steps: [ ... ]
```

Secrets/variables scoped to that environment are only visible to jobs that declare it.

## Status badge

```markdown
![build](https://github.com/OWNER/REPO/actions/workflows/build.yml/badge.svg)
```
