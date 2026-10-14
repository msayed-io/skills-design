# Triggering, Watching and Debugging a Run

An agent using this skill needs to do four things beyond just writing the YAML: fire a
run on demand, wait for it, pull the result down, and read the logs when it fails. The
`gh` CLI is the fastest path when available; raw REST calls work anywhere with an HTTP
client and a token.

## Setup (once per environment)

```bash
gh auth login                 # interactive, or:
gh auth login --with-token < token.txt
gh repo set-default owner/repo
```

## Discover workflows

```bash
gh workflow list
gh workflow view build.yml
```

## Trigger a run manually (no new commit needed)

```bash
gh workflow run build.yml --ref main
gh workflow run build.yml --ref main -f environment=production -f build_type=release
```

The workflow must declare `workflow_dispatch:` (with matching `inputs:` if you pass `-f`
flags) for this to work — see `workflow-fundamentals.md`.

## Find and watch the run you just triggered

```bash
gh run list --workflow=build.yml --limit 1 --json databaseId,status,conclusion
gh run watch <run-id> --exit-status     # blocks, streams progress, exits non-zero on failure
```

`gh run watch --exit-status` is the key command for an agent: it turns "did the build
succeed" into a simple process exit code instead of requiring a manual polling loop.

## Pull the built artifact down

```bash
gh run download <run-id>                       # all artifacts from that run
gh run download <run-id> -n app-release         # just the one named artifact
```

## Read logs on failure

```bash
gh run view <run-id> --log                      # full log, every step
gh run view <run-id> --log-failed               # only the failed step(s) — start here
```

## Create a Release and attach a build to it

```bash
gh release create v1.2.0 ./app-release.apk \
  --title "v1.2.0" --notes "Automated build from CI"
```

## Equivalent REST calls (no `gh` CLI available)

```
POST  /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches
      body: {"ref": "main", "inputs": {"environment": "production"}}

GET   /repos/{owner}/{repo}/actions/runs?branch=main&per_page=1
      -> read .workflow_runs[0].id, .status, .conclusion

GET   /repos/{owner}/{repo}/actions/runs/{run_id}
      -> poll until .status == "completed"

GET   /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
      -> per-job/per-step detail when something fails

GET   /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts
      -> list artifact ids and names

GET   /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip
      -> download (redirects to a short-lived URL)
```

All calls need `Authorization: Bearer <token>` and
`Accept: application/vnd.github+json` headers.

## Polling loop pattern (pseudocode, for any agent/language)

```
run_id = dispatch_workflow_and_get_new_run_id()
loop:
    run = get_run(run_id)
    if run.status == "completed":
        break
    sleep(10s)
if run.conclusion != "success":
    logs = get_failed_step_logs(run_id)
    report_failure(logs)
else:
    artifact = find_artifact(run_id, expected_name)
    download(artifact)
    report_success(artifact.path)
```

Always dispatch-then-poll-by-id rather than "list runs and grab the latest," when
possible — two runs can be triggered close together and the "latest" one might not be
yours. `gh workflow run` doesn't return an id directly, so the reliable pattern is:
note the timestamp right before dispatching, then `gh run list --created ">=<timestamp>"`
to find the exact run that command created.
