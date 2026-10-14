---
name: gha-app-builder
description: >
  Build, test, package, sign, release, and inspect software through GitHub Actions instead of
  performing the authoritative build locally. Use when an agent must configure or repair
  .github/workflows, build Android/iOS/macOS/Windows/Linux/web/Docker projects, trigger a
  remote workflow, monitor its run, diagnose failures, retrieve artifacts, or publish releases.
---

# GitHub Actions App Builder

## Mission

Use GitHub Actions as the authoritative build environment. The local machine may inspect files,
validate configuration, generate a patch, and perform lightweight linting, but must not replace
the requested remote build with a local production build. Never report success until the remote
run is terminal and its conclusion is verified.

## Operating contract

1. **Discover before changing.** Confirm the repository, current branch/ref, GitHub remote, project
   ecosystem, target platform, desired output, distribution channel, and whether the request is
   build/test, signed release, or publication. Ask only questions that change the architecture.
2. **Inspect existing automation.** Read `.github/workflows/*.yml` and `*.yaml`; extend a suitable
   workflow instead of duplicating it. Use `scripts/gha_mvp.py inspect` and `validate` when available.
3. **Plan the trust boundary.** Keep untrusted `pull_request` build/test jobs separate from
   signing, publishing, and deployment jobs. Use protected Environments for privileged stages.
4. **Select the runner deliberately.** Use Linux for most Android/web/Docker work, macOS for
   Xcode/iOS/macOS, and Windows for WinUI/MSIX/Visual Studio. Pin an explicit image/toolchain for
   reproducible releases; do not assume `-latest` is stable. Treat self-hosted runners as a
   separate security and capacity decision.
5. **Generate minimally.** Preserve existing triggers and permissions unless there is a reason to
   change them. Include `workflow_dispatch` for agent-controlled builds, with typed inputs only
   when useful. Set a restrictive `permissions` baseline and add the smallest required writes.
6. **Validate before commit or dispatch.** Check YAML structure, `on`, `jobs`, `runs-on`, steps,
   `needs`, matrix size, refs, action pinning, secret references, environments, and artifact paths.
   Flag `pull_request_target`, unpinned third-party actions, broad token permissions, and secrets in
   untrusted contexts. Validation is a gate, not a suggestion.
7. **Commit/push or open a PR according to the user's requested change policy.** Do not silently
   push to a protected production branch. A workflow file is not active until it is on a reachable
   ref and GitHub accepts it.
8. **Dispatch precisely.** Require `workflow_dispatch` and a valid branch/tag ref. The REST dispatch
   endpoint may return `204 No Content`; do not assume it returns a run ID. Correlate the new run by
   workflow, ref, event, head SHA, and creation time, or use a tool that returns the created run ID.
   Never select “the newest run” without correlation.
9. **Monitor and diagnose.** Poll the exact run until `status=completed` or a clear timeout. Evaluate
   `conclusion` separately from status. Inspect jobs and failed steps before downloading logs. Treat
   queued, waiting, approval, cancelled, skipped, and failure as distinct outcomes.
10. **Handle outputs safely.** Resolve artifacts by exact run and name/ID, check expiry and digest,
    download to an isolated directory, and verify expected files. Use Release assets for durable
    distribution, not caches or short-lived artifacts.
11. **Report honestly.** Return repository/ref/SHA, workflow/run URLs, runner/platform, final status,
    conclusion, artifact names and local paths or URLs, and an actionable failure diagnosis. If a
    required SDK, runner, secret, permission, signing identity, quota, or external store setup is
    missing, say exactly which prerequisite is missing.

## Platform routing

Read the matching reference before editing a platform workflow:

- `references/workflow-fundamentals.md`: syntax, contexts, dependencies, matrices, reusable workflows.
- `references/android.md`: Gradle, APK/AAB, signing, Play publishing.
- `references/ios-macos.md`: Xcode archive/export, Apple signing, notarization.
- `references/windows-desktop.md`: .NET, MSIX, Windows signing, Electron, Linux packages.
- `references/docker-and-web.md`: containers, GHCR, web builds, GitHub Pages.
- `references/secrets-and-signing.md`: secret materialization and cleanup patterns.
- `references/monitoring-and-cli.md`: CLI/API operation patterns; treat its commands as examples
  and apply the correlation and security rules above.
- `references/mvp-safety.md`: corrections for dispatch correlation, action pinning, secret handling,
  artifact integrity, and the limits of static YAML validation.

## Required workflow shape

For a new app pipeline, prefer this separation:

- **Validate/test:** safe on `pull_request`, no release secrets.
- **Build:** platform-specific runner, pinned toolchain, cache only regenerable dependencies.
- **Package:** upload named artifacts with platform/architecture/configuration/version.
- **Sign/publish:** only on an approved ref and protected Environment, after successful tests.

Use `needs` explicitly. Use a matrix only when the generated job count is bounded and each leg has
an unambiguous artifact name. Keep build and publish permissions in different jobs.

For Android, distinguish the deliverables: an APK can be installed with `adb` on a CI emulator or
reachable device, while an AAB is a Google Play publishing bundle and cannot be installed directly
with `adb`. Build both only when the user needs both use cases. Keep the Android keystore in a
protected Environment, materialize it under `$RUNNER_TEMP` with restrictive permissions, validate
the alias/password, expose signing values through environment variables, and remove the keystore
in an `if: always()` cleanup step. Never give signing secrets to pull-request validation jobs.

## Security gates

- Never commit or print tokens, keystores, certificates, provisioning profiles, PFX files, or
  service-account keys. Decode them only inside the job, use them through environment variables,
  and delete temporary files/keychains in an `if: always()` cleanup step.
- Prefer `contents: read`; grant `actions: write`, `contents: write`, `packages: write`, or
  `id-token: write` only to the exact job that requires it.
- Do not give secrets to fork PR validation. Do not execute attacker-controlled code in
  `pull_request_target` or privileged `workflow_run` paths.
- Pin third-party actions and reusable workflows to a verified full commit SHA where feasible.
- Require an Environment with reviewers/branch restrictions for production or store publishing.
- Treat downloaded logs, artifacts, caches, and generated metadata as untrusted input until verified.

## MVP tool

Use `scripts/gha_mvp.py` for deterministic local inspection and remote run control:

```bash
python scripts/gha_mvp.py inspect --repo .
python scripts/gha_mvp.py validate --workflow .github/workflows/build.yml
python scripts/gha_mvp.py dispatch --repo OWNER/REPO --workflow build.yml --ref main --inputs '{"build_type":"debug"}'
python scripts/gha_mvp.py watch --repo OWNER/REPO --run-id RUN_ID
python scripts/gha_mvp.py run-report --repo OWNER/REPO --run-id RUN_ID
```

Set `GH_TOKEN` or `GITHUB_TOKEN` in the environment. The tool never prints token values. Dispatch
and publication are external side effects: validate the exact ref, workflow, inputs, and intended
artifact before invoking them. The tool does not upload secrets or create releases automatically.

## Completion checklist

Before declaring the task complete, verify:

- Workflow file is valid and reachable on the intended ref.
- Trigger matches the requested behavior and filters do not accidentally suppress required checks.
- Runner and toolchain match the target platform.
- Permissions, secrets, and Environment protections are sufficient and least-privilege.
- Exact run reached a terminal conclusion.
- Failed jobs/steps were inspected when unsuccessful.
- Artifacts exist, are unexpired, match the expected run/SHA, and were downloaded or linked.
- Release publication, if requested, happened only after the protected gate and is reported with its URL.
