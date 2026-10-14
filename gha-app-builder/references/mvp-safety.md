# MVP Safety Notes and Corrections

The platform playbooks are starting templates, not copy-paste authorization. Before using any example in a real repository, apply these corrections.

## Dispatch identity

`gh workflow run` starts a dispatch but does not reliably provide the created run ID. The REST dispatch endpoint can return `204 No Content`. Correlate the run by workflow filename/ID, event, ref, head SHA, and a narrow creation-time window. Never monitor the newest run without correlation because concurrent runs can be mistaken for the requested build.

## Action pinning

Examples that use `actions/checkout@v4`, `actions/setup-java@v4`, `softprops/action-gh-release@v2`, or another tag are readable templates. For production or privileged workflows, resolve and review the action repository and pin the reference to a verified full commit SHA. Apply the same rule to reusable workflows.

## Secret handling

Do not put a secret expression directly inside a shell command when an environment variable is possible. Prefer:

```yaml
- name: Use credential
  env:
    CREDENTIAL: ${{ secrets.CREDENTIAL }}
  run: ./tool --credential "$CREDENTIAL"
```

Decode binary credentials only inside the job, use a temporary path, and remove the file or keychain with `if: always()`. Never use `gh secret set --body "..."` with a credential in shell history or process arguments; use stdin or a connected secrets manager.

## Build versus publication

Unsigned CI artifacts and signed distribution artifacts have different trust requirements. Keep pull-request validation secret-free. Put signing and publication in separate jobs guarded by `needs`, a protected Environment, an approved ref, and narrow permissions. A successful compilation is not evidence that the app is ready for a Store or public release.

## Artifact integrity

Use unique artifact names per matrix leg. Resolve an artifact from the exact run, check `expired`, `expires_at`, `head_sha`, expected file names, and SHA-256 digest where available. Do not treat cache data as a release artifact. Download into an isolated directory and do not execute a downloaded file merely because the workflow succeeded.

## YAML and platform validation

Static checks are useful but are not a complete YAML parser or GitHub validator. Validate with a YAML parser and, where available, GitHub's own workflow validation. Confirm that the workflow exists on the intended branch, that filters do not suppress required checks, and that the selected Runner has the expected OS, architecture, SDK, and licensing prerequisites.
