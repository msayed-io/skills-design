#!/usr/bin/env python3
"""Small, dependency-free MVP helper for GitHub Actions.

It deliberately separates local static inspection from remote side effects. It does not
create releases, mutate secrets, or execute the project's production build locally.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")
SECRET_RE = re.compile(r"\$\{\{\s*secrets\.([A-Za-z_][A-Za-z0-9_]*)")


def emit(value, code=0):
    print(json.dumps(value, indent=2, ensure_ascii=False))
    raise SystemExit(code)


def token():
    value = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not value:
        emit({"ok": False, "error": "Set GH_TOKEN or GITHUB_TOKEN for GitHub API operations."}, 2)
    return value


def api(path, method="GET", body=None):
    base = "https://api.github.com"
    headers = {"Authorization": f"Bearer {token()}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    req = Request(base + path, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:4000]
        emit({"ok": False, "http_status": exc.code, "error": detail}, 1)
    except URLError as exc:
        emit({"ok": False, "error": f"GitHub API connection failed: {exc.reason}"}, 1)


def workflow_files(repo):
    root = Path(repo).resolve()
    folder = root / ".github" / "workflows"
    return root, sorted([p for p in folder.glob("*") if p.suffix in (".yml", ".yaml")]) if folder.exists() else []


def text_keys(text):
    # Conservative structural checks that work without PyYAML. They intentionally do not
    # pretend to be a YAML parser; GitHub-side validation remains authoritative.
    keys = set()
    for line in text.splitlines():
        if not line.startswith((" ", "\t", "-", "#")):
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):", line)
            if m: keys.add(m.group(1))
    return keys


def validate(path):
    p = Path(path)
    if not p.is_file(): return {"ok": False, "errors": [f"Workflow not found: {path}"]}
    text = p.read_text(encoding="utf-8", errors="replace")
    errors, warnings, actions, secrets = [], [], [], sorted(set(SECRET_RE.findall(text)))
    if p.suffix not in (".yml", ".yaml"): errors.append("Workflow must use .yml or .yaml")
    if not re.search(r"(?m)^\s*on\s*:", text): errors.append("Missing top-level on trigger block")
    if not re.search(r"(?m)^\s*jobs\s*:", text): errors.append("Missing top-level jobs block")
    if not re.search(r"(?m)^\s+[A-Za-z0-9_-]+:\s*$", text): warnings.append("Could not identify job IDs; use a YAML parser for complex syntax")
    if "workflow_dispatch" not in text: warnings.append("No workflow_dispatch trigger; an agent cannot manually dispatch this workflow")
    if "pull_request_target" in text: warnings.append("High risk: review pull_request_target before executing any fork-controlled code")
    if re.search(r"(?m)^\s*permissions:\s*\n", text) is None: warnings.append("No explicit permissions baseline found")
    for line_no, line in enumerate(text.splitlines(), 1):
        m = USES_RE.match(line)
        if m:
            ref = m.group(1).rsplit("@", 1)[-1] if "@" in m.group(1) else ""
            actions.append({"line": line_no, "uses": m.group(1), "pinned_sha": bool(SHA_RE.fullmatch(ref))})
            if not SHA_RE.fullmatch(ref): warnings.append(f"Line {line_no}: action is not pinned to a full commit SHA: {m.group(1)}")
        if "${{ secrets." in line and "run:" in line: warnings.append(f"Line {line_no}: secret interpolation in run; prefer env and avoid shell exposure")
    if "actions/upload-artifact@v3" in text or "actions/download-artifact@v3" in text: warnings.append("Artifact v3 is obsolete for new workflows; review v4 compatibility")
    return {"ok": not errors, "file": str(p), "errors": errors, "warnings": warnings, "actions": actions, "secret_names_only": secrets}


def inspect(repo):
    root, files = workflow_files(repo)
    markers = {
        "android": any((root / x).exists() for x in ["gradlew", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"]),
        "flutter": (root / "pubspec.yaml").exists(),
        "node": (root / "package.json").exists(),
        "dotnet": any(root.glob("*.sln")) or any(root.glob("*.csproj")),
        "xcode": any(root.glob("*.xcodeproj")) or any(root.glob("*.xcworkspace")),
        "docker": (root / "Dockerfile").exists(),
    }
    remote = ""
    try:
        remote = subprocess.check_output(["git", "-C", str(root), "remote", "get-url", "origin"], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError): pass
    return {"ok": True, "repo_path": str(root), "github_remote": remote, "project_markers": markers, "workflow_files": [str(x.relative_to(root)) for x in files], "workflow_validation": [validate(x) for x in files]}


def dispatch(args):
    inputs = json.loads(args.inputs) if args.inputs else {}
    if not isinstance(inputs, dict): emit({"ok": False, "error": "--inputs must be a JSON object"}, 2)
    status, result = api(f"/repos/{args.repo}/actions/workflows/{args.workflow}/dispatches", "POST", {"ref": args.ref, "inputs": inputs})
    emit({"ok": status in (200, 201, 204), "dispatch_http_status": status, "repo": args.repo, "workflow": args.workflow, "ref": args.ref, "inputs": sorted(inputs), "note": "Dispatch often returns 204 without a run ID; correlate the run by workflow/ref/event/head SHA before monitoring.", "response": result})


def run_report(args):
    _, run = api(f"/repos/{args.repo}/actions/runs/{args.run_id}")
    _, jobs = api(f"/repos/{args.repo}/actions/runs/{args.run_id}/jobs?per_page=100")
    _, artifacts = api(f"/repos/{args.repo}/actions/runs/{args.run_id}/artifacts?per_page=100")
    emit({"ok": True, "run": {k: run.get(k) for k in ["id", "name", "workflow_id", "path", "event", "status", "conclusion", "head_branch", "head_sha", "run_number", "html_url", "created_at", "updated_at"]}, "jobs": jobs.get("jobs", []) if jobs else [], "artifacts": artifacts.get("artifacts", []) if artifacts else []})


def watch(args):
    deadline = time.monotonic() + args.timeout
    while True:
        _, run = api(f"/repos/{args.repo}/actions/runs/{args.run_id}")
        state = {k: run.get(k) for k in ["id", "status", "conclusion", "html_url", "head_sha", "head_branch"]}
        if run.get("status") == "completed":
            state["ok"] = run.get("conclusion") == "success"
            emit(state, 0 if state["ok"] else 1)
        if time.monotonic() >= deadline:
            emit({"ok": False, "error": "Timed out while waiting for workflow run", "last": state}, 2)
        time.sleep(args.interval)


def main():
    parser = argparse.ArgumentParser(description="GitHub Actions App Builder MVP helper")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inspect"); p.add_argument("--repo", default=".")
    p = sub.add_parser("validate"); p.add_argument("--workflow", required=True)
    p = sub.add_parser("dispatch"); p.add_argument("--repo", required=True); p.add_argument("--workflow", required=True); p.add_argument("--ref", required=True); p.add_argument("--inputs")
    p = sub.add_parser("watch"); p.add_argument("--repo", required=True); p.add_argument("--run-id", required=True, type=int); p.add_argument("--interval", type=int, default=10); p.add_argument("--timeout", type=int, default=3600)
    p = sub.add_parser("run-report"); p.add_argument("--repo", required=True); p.add_argument("--run-id", required=True, type=int)
    args = parser.parse_args()
    if args.command == "inspect": emit(inspect(args.repo))
    if args.command == "validate": emit(validate(args.workflow), 0 if validate(args.workflow)["ok"] else 1)
    if args.command == "dispatch": dispatch(args)
    if args.command == "watch": watch(args)
    if args.command == "run-report": run_report(args)

if __name__ == "__main__": main()
