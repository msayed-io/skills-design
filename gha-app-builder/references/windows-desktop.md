# Windows & Linux Desktop — EXE, MSI, MSIX, AppImage, deb

## .NET app → signed installer on `windows-latest`

```yaml
name: Windows Release

on:
  push:
    tags: ["v*"]
  workflow_dispatch: {}

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: "8.0.x"

      - name: Publish
        run: dotnet publish MyApp.csproj -c Release -r win-x64 --self-contained -o out

      - name: Decode signing certificate
        env:
          CERT_BASE64: ${{ secrets.WINDOWS_CERT_BASE64 }}
        run: |
          $bytes = [Convert]::FromBase64String($env:CERT_BASE64)
          [IO.File]::WriteAllBytes("cert.pfx", $bytes)

      - name: Sign the executable
        env:
          CERT_PASSWORD: ${{ secrets.WINDOWS_CERT_PASSWORD }}
        run: |
          & 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe' sign `
            /f cert.pfx /p $env:CERT_PASSWORD `
            /tr http://timestamp.digicert.com /td sha256 /fd sha256 `
            out\MyApp.exe

      - name: Clean up certificate
        if: always()
        run: Remove-Item -Force cert.pfx -ErrorAction SilentlyContinue

      - uses: actions/upload-artifact@v4
        with:
          name: MyApp-windows
          path: out/MyApp.exe

      - uses: softprops/action-gh-release@v2
        with:
          files: out/MyApp.exe
```

## Packaging as MSIX (Windows Store-style installer)

```yaml
- name: Package MSIX
  run: |
    & "C:\Program Files (x86)\Windows Kits\10\bin\x64\makeappx.exe" pack `
      /d out /p MyApp.msix
- name: Sign MSIX
  run: |
    & 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe' sign `
      /fd SHA256 /a /f cert.pfx /p $env:CERT_PASSWORD MyApp.msix
```

## Electron app → installers for Windows, macOS and Linux from one workflow

`electron-builder` (or `electron-forge`) already knows how to produce a `.exe`/NSIS
installer, a `.dmg`, and an `.AppImage`/`.deb` — run it on the matching OS per matrix leg:

```yaml
name: Electron Release

on:
  push:
    tags: ["v*"]

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - name: Build and publish installers
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CSC_LINK: ${{ secrets.WINDOWS_CERT_BASE64 }}          # electron-builder reads these directly
          CSC_KEY_PASSWORD: ${{ secrets.WINDOWS_CERT_PASSWORD }}
        run: npx electron-builder --publish always
```

`electron-builder --publish always` uploads straight to a GitHub Release matching the
pushed tag, using the automatically-provided `GITHUB_TOKEN` — no separate release step
needed. `CSC_LINK`/`CSC_KEY_PASSWORD` (Windows) and `CSC_LINK`/`CSC_KEY_PASSWORD` again
under macOS-specific env vars handle code signing per platform; see electron-builder's own
docs for the macOS notarization variables (`APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`,
`APPLE_TEAM_ID`) if shipping outside the Mac App Store.

## Linux desktop packaging (AppImage / .deb) on `ubuntu-latest`

```yaml
- name: Build AppImage
  run: |
    npm run build   # or your native build step
    npx electron-builder --linux AppImage deb
- uses: actions/upload-artifact@v4
  with:
    name: MyApp-linux
    path: dist/*.AppImage
```

## Gotchas

- `signtool.exe`'s exact path varies by Windows SDK version installed on the runner
  image — check `actions/runner-images` if the hardcoded path above doesn't exist, or
  search `$env:ProgramFiles(x86)` for `signtool.exe` at runtime instead of hardcoding.
- Self-contained .NET publishes (`--self-contained`) produce large output; only bundle
  the runtime if the target machine isn't guaranteed to have .NET installed.
- electron-builder needs `GH_TOKEN` (not the same as GitHub's `GITHUB_TOKEN` context
  variable name inside `run:` — export it as an env var as shown) to publish releases.
