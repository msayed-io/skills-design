# Secrets & Signing — Getting Credentials In and Out Safely

Every platform playbook above needs some binary credential (a keystore, a `.p12`
certificate, a `.pfx` file) inside a workflow that only accepts text secrets. The pattern
is always the same: **base64-encode the file locally once, store the resulting text as a
secret, decode it back to a file inside the job.**

## 1. Where secrets live

- **Repo-level**: Settings → Secrets and variables → Actions → "New repository secret."
  Visible to every workflow in that repo.
- **Environment-level**: tied to a named environment (e.g. `production`); only jobs that
  declare `environment: production` can read them, and the environment can require
  manual approval before those jobs run.
- **Org-level**: shared across many repos in an organization.

Anything non-secret but still config-like (a bundle ID, a package name) belongs in
**Variables**, not Secrets — same UI, but stored in plaintext and shown in logs.

## 2. Setting a secret without exposing it in shell arguments

With the GitHub CLI, an agent can set secrets through stdin instead of putting credential values in
shell history or process arguments. Prefer an Environment-scoped secret for signing and publishing:

```bash
base64 -w0 app-release.jks | gh secret set ANDROID_KEYSTORE_BASE64 --repo OWNER/REPO --env android-release
printf '%s' "$KEYSTORE_PASSWORD" | gh secret set ANDROID_KEYSTORE_PASSWORD --repo OWNER/REPO --env android-release
printf '%s' "$KEY_ALIAS" | gh secret set ANDROID_KEY_ALIAS --repo OWNER/REPO --env android-release
printf '%s' "$KEY_PASSWORD" | gh secret set ANDROID_KEY_PASSWORD --repo OWNER/REPO --env android-release
```

Before setting anything, verify the repository and Environment. Never print the values, put them
in command-line arguments, or read them back for confirmation. If the agent does not have a secure
source for the credential, stop and ask the user to configure it through GitHub or a secret manager.

## 3. Encoding a binary file to base64 (do this once, locally)

```bash
# Linux
base64 -w0 keystore.jks > keystore.b64

# macOS
base64 -i keystore.jks -o keystore.b64

# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("keystore.jks")) | Out-File keystore.b64
```

Then `gh secret set NAME < keystore.b64` (or paste the contents into the web UI). Never
commit the `.b64` file or the original binary to the repo — delete both locally once the
secret is set, or keep them only in a secure local secrets manager.

## 4. Decoding it back inside the workflow

```yaml
- name: Decode keystore
  env:
    KEYSTORE_BASE64: ${{ secrets.ANDROID_KEYSTORE_BASE64 }}
  run: |
    set -euo pipefail
    umask 077
    printf '%s' "$KEYSTORE_BASE64" | base64 --decode > "$RUNNER_TEMP/release.keystore"
    test -s "$RUNNER_TEMP/release.keystore"
```

On Windows runners, use PowerShell instead:

```yaml
- run: |
    $bytes = [Convert]::FromBase64String($env:CERT_BASE64)
    [IO.File]::WriteAllBytes("cert.pfx", $bytes)
  env:
    CERT_BASE64: ${{ secrets.WINDOWS_CERT_BASE64 }}
```

Always clean the decoded file up at the end of the job with `if: always()`, even though
the runner VM is destroyed after the job anyway — good hygiene, and essential if a later
step or a debugging session reuses the same workspace.

## 5. Naming convention that scales across platforms

Keep a consistent `<PLATFORM>_<THING>` pattern so an agent (or a human) can guess a
secret's name without hunting through the settings UI:

```
ANDROID_KEYSTORE_BASE64, ANDROID_KEYSTORE_PASSWORD, ANDROID_KEY_ALIAS, ANDROID_KEY_PASSWORD
IOS_CERT_BASE64, IOS_CERT_PASSWORD, IOS_PROFILE_BASE64, IOS_KEYCHAIN_PASSWORD
MACOS_CERT_BASE64, MACOS_CERT_PASSWORD, APPLE_ID, APPLE_APP_SPECIFIC_PASSWORD, APPLE_TEAM_ID
WINDOWS_CERT_BASE64, WINDOWS_CERT_PASSWORD
PLAY_STORE_SERVICE_ACCOUNT_JSON
```

## 6. Prefer short-lived credentials where the platform supports it

For cloud deploy targets (AWS, GCP, Azure), prefer **OIDC** over a long-lived static
access key: the workflow requests a short-lived token at run time, scoped to that one
job, instead of a secret that lives in the store forever.

```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-deploy
      aws-region: us-east-1
```

No `AWS_SECRET_ACCESS_KEY` secret needed at all in this pattern.

## 7. Rotation and least privilege

- Scope each credential as narrowly as possible (a deploy-only Play Store service
  account, not a full-access one; a code-signing cert with no other capability).
- Rotate on any suspected exposure and whenever someone with access leaves the project.
- Restrict *which* workflows/branches can even use a given environment's secrets via
  environment protection rules, so a compromised PR from a fork can't exfiltrate a
  production signing key (public-repo forks never get secrets on `pull_request` runs by
  default — don't switch that trigger to `pull_request_target` without understanding the
  security implications first).
