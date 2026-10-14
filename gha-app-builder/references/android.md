# Android — Securely build, sign, test, and deliver APK/AAB

## Important distinction

- **APK** can be installed on an emulator or connected Android device with `adb install`.
- **AAB** is a publishing bundle for Google Play. It is not directly installable with `adb`.
  Use an APK for direct installation, or use `bundletool` to generate device-specific APKs from
  an AAB for testing.
- GitHub-hosted runners cannot install an APK on the user's physical phone. They can install it
  on a CI emulator or connected hardware that the runner can access. The normal output for a user
  is an uploaded Artifact or a Release asset.

## Secret contract

For a signed build, store these as GitHub **Environment secrets** when possible, under a protected
`production` or `android-release` Environment:

```text
ANDROID_KEYSTORE_BASE64
ANDROID_KEYSTORE_PASSWORD
ANDROID_KEY_ALIAS
ANDROID_KEY_PASSWORD
```

Do not commit the keystore, a `.b64` file, `keystore.properties`, passwords, or a service-account
JSON key. Use repository secrets only for non-production testing, and use branch/tag restrictions
and required reviewers for production signing.

Create the Base64 value without wrapping lines and send it through stdin to GitHub CLI so it does
not appear in shell history or command arguments:

```bash
base64 -w0 app-release.jks | gh secret set ANDROID_KEYSTORE_BASE64 --repo OWNER/REPO --env android-release
printf '%s' "$KEYSTORE_PASSWORD" | gh secret set ANDROID_KEYSTORE_PASSWORD --repo OWNER/REPO --env android-release
printf '%s' "$KEY_ALIAS" | gh secret set ANDROID_KEY_ALIAS --repo OWNER/REPO --env android-release
printf '%s' "$KEY_PASSWORD" | gh secret set ANDROID_KEY_PASSWORD --repo OWNER/REPO --env android-release
```

The agent must never read back or print secret values. Before using these commands, verify the
repository, Environment name, and intended branch/tag. If the local shell has no secure secret
source, stop and ask the user to configure the secrets through GitHub or a secret manager.

## Gradle signing configuration

Prefer letting the Android project consume environment variables. In `app/build.gradle`:

```groovy
android {
    signingConfigs {
        release {
            def ks = System.getenv("ANDROID_KEYSTORE_PATH")
            if (ks != null) {
                storeFile file(ks)
                storePassword System.getenv("ANDROID_KEYSTORE_PASSWORD")
                keyAlias System.getenv("ANDROID_KEY_ALIAS")
                keyPassword System.getenv("ANDROID_KEY_PASSWORD")
            }
        }
    }
    buildTypes {
        release { signingConfig signingConfigs.release }
    }
}
```

For Kotlin DSL use the equivalent `System.getenv` values and `file(ks)`. Keep this configuration
conditional so a pull-request debug/test build does not require release secrets. Fail clearly in a
release job when a required value is missing; do not substitute a debug key silently.

## Secure signed APK/AAB workflow

The following is a working pattern. For production, review each third-party action and pin it to
a verified full commit SHA; the readable major tags below are intentionally easier to adapt.

```yaml
name: Android Signed Build

on:
  pull_request:
  push:
    tags: ["v*"]
  workflow_dispatch:
    inputs:
      output:
        description: "Release output"
        type: choice
        options: [apk, aab, both]
        default: both
        required: true

permissions:
  contents: read

concurrency:
  group: android-release-${{ github.ref }}
  cancel-in-progress: false

jobs:
  debug-check:
    # No signing secrets are available in this job.
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"
          cache: gradle
      - name: Build and test debug variant
        run: |
          chmod +x ./gradlew
          ./gradlew testDebugUnitTest assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: android-debug-${{ github.sha }}
          path: app/build/outputs/apk/debug/*.apk
          if-no-files-found: error
          retention-days: 14

  signed-release:
    if: github.event_name == 'workflow_dispatch' || startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-24.04
    environment: android-release
    permissions:
      contents: read
    env:
      ANDROID_KEYSTORE_PASSWORD: ${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
      ANDROID_KEY_ALIAS: ${{ secrets.ANDROID_KEY_ALIAS }}
      ANDROID_KEY_PASSWORD: ${{ secrets.ANDROID_KEY_PASSWORD }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"
          cache: gradle
      - name: Materialize keystore in temporary workspace
        env:
          KEYSTORE_BASE64: ${{ secrets.ANDROID_KEYSTORE_BASE64 }}
        run: |
          set -euo pipefail
          test -n "$KEYSTORE_BASE64"
          umask 077
          printf '%s' "$KEYSTORE_BASE64" | base64 --decode > "$RUNNER_TEMP/release.keystore"
          test -s "$RUNNER_TEMP/release.keystore"
          keytool -list -keystore "$RUNNER_TEMP/release.keystore" \
            -storepass "$ANDROID_KEYSTORE_PASSWORD" >/dev/null
      - name: Build signed outputs
        env:
          ANDROID_KEYSTORE_PATH: ${{ runner.temp }}/release.keystore
        run: |
          set -euo pipefail
          chmod +x ./gradlew
          ./gradlew --no-daemon clean
          ./gradlew --no-daemon assembleRelease bundleRelease
      - name: Verify signed APK and AAB exist
        run: |
          set -euo pipefail
          test -n "$(find app/build/outputs/apk/release -type f -name '*.apk' -print -quit)"
          test -n "$(find app/build/outputs/bundle/release -type f -name '*.aab' -print -quit)"
      - uses: actions/upload-artifact@v4
        with:
          name: android-release-${{ github.ref_name }}-${{ github.sha }}
          path: |
            app/build/outputs/apk/release/*.apk
            app/build/outputs/bundle/release/*.aab
          if-no-files-found: error
          retention-days: 30
      - name: Remove signing material
        if: always()
        run: rm -f "$RUNNER_TEMP/release.keystore"
```

The Environment should be configured in GitHub repository settings with required reviewers for
production. The `debug-check` job is intentionally secret-free. The signed job only runs for an
explicit dispatch or version tag; change that policy only after reviewing the release threat model.

## Direct APK installation in CI

To install an APK on an Android emulator, add a separate job or steps after starting an emulator:

```yaml
- name: Install APK on CI emulator
  uses: reactivecircus/android-emulator-runner@v2
  with:
    api-level: 35
    arch: x86_64
    target: google_apis
    script: |
      adb install -r app/build/outputs/apk/release/app-release.apk
      adb shell am force-stop com.example.app
      adb shell monkey -p com.example.app 1
```

Use this only for test verification. It does not install the app on the user's phone. For an AAB,
first generate APKs with the official `bundletool` matching the app's signing and device setup, or
use Google Play internal testing; do not claim that `adb install app-release.aab` works.

## Optional Google Play upload

Uploading an AAB to Google Play is a separate privileged operation. Use a protected Environment,
a narrowly scoped Play service account, and a reviewed official/maintained action or Play API.
Only publish after the signed Artifact has been verified. Keep the upload job separate from the
build job and do not grant Play credentials to pull-request workflows.

## Verification checklist

Before reporting success, verify the exact run and commit SHA, confirm the release Environment was
approved, verify the APK/AAB files and their sizes, inspect signing metadata without printing
secrets, calculate or retain SHA-256 hashes, and report whether the output is an installable APK,
a Play-upload AAB, or both. If a key alias/password/profile is wrong, report the missing or
mismatched prerequisite instead of falling back to a debug signature.
