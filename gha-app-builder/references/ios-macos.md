# iOS & macOS — Build on GitHub's Real Apple Hardware

This is the case where GitHub Actions is most valuable to an agent: Apple's tooling and
license terms mean iOS/macOS apps can only be legitimately built on real Apple hardware.
`macos-latest` (or a pinned version, e.g. `macos-14`) gives that hardware on demand,
without the user owning a Mac. It costs noticeably more per minute than Linux (see
SKILL.md §8), so keep the macOS job itself lean — do dependency installs, linting, etc.
on `ubuntu-latest` in a separate job where possible.

## What you need before this can be signed

1. An Apple Developer Program membership (for anything beyond a personal free-provisioning
   build).
2. A **signing certificate** (`.p12`, exported from Keychain Access, password-protected).
3. A **provisioning profile** matching the app's bundle ID and the certificate.
4. Both stored as base64-encoded secrets (see `secrets-and-signing.md`).

Managing certificates/profiles by hand gets painful fast; most real projects use
[fastlane match](https://docs.fastlane.tools/actions/match/) to sync them from a private
git repo or cloud storage instead of juggling raw `.p12`/`.mobileprovision` files. Both
approaches are shown below — start with the raw approach for a simple one-off, move to
`match` once there's more than one app/target.

## Unsigned build / simulator build (no Apple account needed)

Useful for CI checks or handing back a simulator build:

```yaml
name: iOS Simulator Build

on: [push, workflow_dispatch]

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Select Xcode version
        run: sudo xcode-select -s /Applications/Xcode.app
      - name: Build for simulator
        run: |
          xcodebuild build \
            -project MyApp.xcodeproj \
            -scheme MyApp \
            -sdk iphonesimulator \
            -destination "generic/platform=iOS Simulator"
```

## Signed IPA build (raw certificate approach)

```yaml
name: iOS Release

on:
  push:
    tags: ["v*"]
  workflow_dispatch: {}

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Import signing certificate
        env:
          CERT_BASE64: ${{ secrets.IOS_CERT_BASE64 }}
          CERT_PASSWORD: ${{ secrets.IOS_CERT_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.IOS_KEYCHAIN_PASSWORD }}
        run: |
          echo "$CERT_BASE64" | base64 -d > cert.p12
          security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security import cert.p12 -k build.keychain -P "$CERT_PASSWORD" -A
          security set-key-partition-list -S apple-tool:,apple: -s -k "$KEYCHAIN_PASSWORD" build.keychain
          rm cert.p12

      - name: Install provisioning profile
        env:
          PROFILE_BASE64: ${{ secrets.IOS_PROFILE_BASE64 }}
        run: |
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          echo "$PROFILE_BASE64" | base64 -d > \
            ~/Library/MobileDevice/Provisioning\ Profiles/profile.mobileprovision

      - name: Archive and export IPA
        run: |
          xcodebuild archive \
            -project MyApp.xcodeproj \
            -scheme MyApp \
            -archivePath build/MyApp.xcarchive
          xcodebuild -exportArchive \
            -archivePath build/MyApp.xcarchive \
            -exportPath build/ipa \
            -exportOptionsPlist ExportOptions.plist

      - uses: actions/upload-artifact@v4
        with:
          name: MyApp-ipa
          path: build/ipa/*.ipa
```

`ExportOptions.plist` is a small file checked into the repo describing the export method
(`app-store`, `ad-hoc`, `development`) and team ID — it isn't a secret.

## Signed build with fastlane match + fastlane gym (scales better)

```yaml
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: "3.3"
    bundler-cache: true

- name: Fetch certificates via match
  env:
    MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
    MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_TOKEN }}
  run: bundle exec fastlane match appstore --readonly

- name: Build and upload to TestFlight
  env:
    APP_STORE_CONNECT_API_KEY: ${{ secrets.ASC_API_KEY_JSON }}
  run: bundle exec fastlane gym && bundle exec fastlane pilot upload
```

## macOS desktop apps (.dmg / .app), including notarization

Same `macos-latest` runner, `xcodebuild` (or your Mac build tool of choice), then Apple's
notarization service so Gatekeeper trusts the binary on other people's Macs:

```yaml
- name: Build .app
  run: xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Release build

- name: Codesign
  env:
    CERT_BASE64: ${{ secrets.MACOS_CERT_BASE64 }}
    CERT_PASSWORD: ${{ secrets.MACOS_CERT_PASSWORD }}
  run: |
    echo "$CERT_BASE64" | base64 -d > cert.p12
    security import cert.p12 -k build.keychain -P "$CERT_PASSWORD" -A
    codesign --deep --force --sign "Developer ID Application: Your Name" MyApp.app

- name: Notarize
  env:
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APPLE_APP_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
    TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
  run: |
    ditto -c -k --keepParent MyApp.app MyApp.zip
    xcrun notarytool submit MyApp.zip \
      --apple-id "$APPLE_ID" --password "$APPLE_APP_SPECIFIC_PASSWORD" \
      --team-id "$TEAM_ID" --wait
    xcrun stapler staple MyApp.app
```

## Gotchas

- Pin the Xcode version (`macos-14` + `xcode-select`) rather than trusting whatever
  `macos-latest` currently defaults to — Apple SDK changes can silently break a build.
  Check GitHub's `actions/runner-images` repo for exactly which Xcode versions a given
  macOS image includes.
- Always delete the temporary keychain/`.p12`/`.mobileprovision` files at the end of the
  job (`if: always()`), even though the runner is ephemeral and destroyed afterward —
  it's cheap insurance and good hygiene if a later step in the same job reuses the
  workspace.
- Bundle ID, team ID, and provisioning profile must all match exactly, or `xcodebuild`
  fails with a signing error that often doesn't clearly say which of the three is wrong.
