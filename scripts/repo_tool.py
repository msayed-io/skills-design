#!/usr/bin/env python3
"""Repository tooling for skills-design.

No third-party dependencies. Run from any working directory:
  python3 scripts/repo_tool.py validate
  python3 scripts/repo_tool.py catalog --output catalog/skills.json
  python3 scripts/repo_tool.py install ui-ux-pro-max --target .claude/skills
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".github", "catalog", "scripts"}
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Runtime-sensitive sibling installs. Keep this small and explicit: these are the
# only documented cross-skill paths in the repository today.
BUNDLES = {
    "design": ["design", "brand", "design-system", "ui-styling"],
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter delimited by ---")
    values: dict[str, str] = {}
    pending: str | None = None
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")) and pending:
            values[pending] += " " + raw.strip()
            continue
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if value in {">", "|-", ">-", "|"}:
            values[key] = ""
            pending = key
        else:
            values[key] = value.strip("'\"")
            pending = None
    return values


def skill_dirs() -> list[Path]:
    return sorted(
        p for p in ROOT.iterdir()
        if p.is_dir() and p.name not in SKIP_DIRS and not p.name.startswith(".")
        and (p / "SKILL.md").is_file()
    )


def skill_record(path: Path) -> dict[str, Any]:
    skill = parse_frontmatter(path / "SKILL.md")
    files = [p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()]
    body = (path / "SKILL.md").read_text(encoding="utf-8")
    return {
        "directory": path.name,
        "name": skill.get("name", ""),
        "description": skill.get("description", ""),
        "argumentHint": skill.get("argument-hint", ""),
        "lineCount": len(body.splitlines()),
        "wordCount": len(re.findall(r"\S+", body)),
        "kind": "tool-backed" if any((path / d).is_dir() for d in ("scripts", "data", "templates", "canvas-fonts")) else "prompt-only",
        "has": {d: (path / d).is_dir() for d in ("references", "scripts", "data", "templates", "canvas-fonts")},
        "files": files,
    }


def catalog() -> dict[str, Any]:
    records = [skill_record(p) for p in skill_dirs()]
    return {
        "schemaVersion": 1,
        "repository": "msayed-io/skills-design",
        "generatedBy": "scripts/repo_tool.py catalog",
        "skillCount": len(records),
        "installBundles": BUNDLES,
        "skills": records,
    }


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[str, Path] = {}
    for path in skill_dirs():
        try:
            record = skill_record(path)
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", path.name):
            errors.append(f"{path.name}: directory must be kebab-case")
        for key in ("name", "description"):
            if not record[key]:
                errors.append(f"{path.name}: frontmatter {key!r} is required")
        name = record["name"]
        if name in seen:
            errors.append(f"duplicate activation name {name!r}: {seen[name]} and {path}")
        else:
            seen[name] = path
        if record["lineCount"] > 500:
            warnings.append(f"{path.name}: SKILL.md has {record['lineCount']} lines; move deep material to references/")
        text = (path / "SKILL.md").read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.name}: broken local link {target}")
    for bundle, members in BUNDLES.items():
        for member in members:
            if not (ROOT / member / "SKILL.md").is_file():
                errors.append(f"bundle {bundle!r}: missing member {member!r}")
    return errors, warnings


def install(names: list[str], target: Path, bundle: str | None, overwrite: bool) -> None:
    requested = list(names)
    if bundle:
        if bundle not in BUNDLES:
            raise SystemExit(f"Unknown bundle {bundle!r}. Available: {', '.join(sorted(BUNDLES))}")
        requested.extend(BUNDLES[bundle])
    by_key: dict[str, Path] = {}
    for path in skill_dirs():
        record = skill_record(path)
        by_key[path.name] = path
        by_key[record["name"]] = path
    target.mkdir(parents=True, exist_ok=True)
    for key in requested:
        if key not in by_key:
            raise SystemExit(f"Unknown skill {key!r}. Run: python3 scripts/repo_tool.py catalog")
        source = by_key[key]
        record = skill_record(source)
        destination = target / record["name"]
        if destination.exists():
            if not overwrite:
                raise SystemExit(f"Refusing to overwrite {destination}; pass --overwrite")
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        print(f"installed {record['name']} <- {source.name} -> {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate, index, and install skills-design skills.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate every skill contract and local link")
    cat = sub.add_parser("catalog", help="write the machine-readable skill catalog")
    cat.add_argument("--output", type=Path, default=ROOT / "catalog" / "skills.json")
    ins = sub.add_parser("install", help="install skills by directory or activation name")
    ins.add_argument("skills", nargs="*", help="directory names or frontmatter activation names")
    ins.add_argument("--bundle", choices=sorted(BUNDLES), help="install a documented skill bundle")
    ins.add_argument("--target", type=Path, required=True, help="skill discovery directory, e.g. .claude/skills")
    ins.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.command == "validate":
        errors, warnings = validate()
        for message in warnings:
            print(f"WARN: {message}")
        for message in errors:
            print(f"ERROR: {message}")
        if errors:
            print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
            return 1
        print(f"OK: validated {len(skill_dirs())} skills ({len(warnings)} warning(s))")
        return 0
    if args.command == "catalog":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(catalog(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"WROTE: {args.output} ({len(skill_dirs())} skills)")
        return 0
    if not args.skills and not args.bundle:
        raise SystemExit("Provide at least one skill or --bundle design")
    install(args.skills, args.target, args.bundle, args.overwrite)
    return 0


if __name__ == "__main__":
    sys.exit(main())
