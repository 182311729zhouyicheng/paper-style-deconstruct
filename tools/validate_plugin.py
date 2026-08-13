"""Validate the local skill-only plugin manifest without Codex tooling."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"invalid plugin manifest: {error}")

    required = ("name", "version", "description", "author", "license", "skills", "interface")
    for field in required:
        if field not in manifest:
            fail(f"missing manifest field: {field}")
    if manifest["name"] != "paper-style-deconstruct":
        fail("manifest name must match the repository name")
    if re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]) is None:
        fail("manifest version must use semantic versioning")
    if manifest["skills"] != "./skills/":
        fail("manifest skills path must be ./skills/")
    if not isinstance(manifest["author"], dict) or not manifest["author"].get("name"):
        fail("manifest author.name is required")

    interface = manifest["interface"]
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
        if not interface.get(field):
            fail(f"missing interface field: {field}")
    if len(interface["defaultPrompt"]) > 3:
        fail("interface.defaultPrompt supports at most three prompts")

    skill_path = ROOT / "skills" / "paper-style-deconstruct" / "SKILL.md"
    contents = skill_path.read_text(encoding="utf-8")
    if not contents.startswith("---\n"):
        fail("SKILL.md must begin with YAML frontmatter")
    closing = contents.find("\n---", 4)
    if closing == -1:
        fail("SKILL.md frontmatter is not closed")
    frontmatter = yaml.safe_load(contents[4:closing])
    if frontmatter.get("name") != manifest["name"] or not frontmatter.get("description"):
        fail("SKILL.md metadata must match the manifest name and include a description")

    print("PASS: Codex plugin manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
