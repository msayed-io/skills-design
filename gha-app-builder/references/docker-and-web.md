# Docker Images & Web Apps

## Build and push a multi-arch Docker image to GHCR

```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ["v*"]

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-qemu-action@v3      # enables cross-arch emulation
      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}   # auto-provided, no setup needed for GHCR

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}

      - uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

Swap the `docker/login-action` target/credentials for Docker Hub
(`secrets.DOCKERHUB_USERNAME`/`secrets.DOCKERHUB_TOKEN`) or any other registry if GHCR
isn't the destination.

## Build a static/web app and deploy it

```yaml
name: Web Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3   # if deploying to GitHub Pages
        with:
          path: dist

  deploy:
    needs: build
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

For Vercel/Netlify/AWS Amplify/etc. instead of GitHub Pages, swap the `deploy` job for
that provider's official action (e.g. `amondnet/vercel-action`,
`nwtgck/actions-netlify`), authenticated with that provider's API token stored as a
secret — the `build` job above stays the same.

## Gotchas

- `secrets.GITHUB_TOKEN` is created automatically for every run and is enough to push to
  GHCR under the same repo/org — no manual PAT needed for that specific case.
- Enable Buildx's GitHub Actions cache (`cache-from`/`cache-to: type=gha` above) or
  Docker builds re-download every layer on every run.
- Multi-arch builds via QEMU emulation are noticeably slower than native; for
  performance-sensitive pipelines consider native ARM runners
  (`ubuntu-24.04-arm`) building the arm64 leg in parallel with a native x64 leg instead
  of emulating.
