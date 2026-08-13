"""Run lightweight, dependency-free checks for the skill package."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "SKILL.md",
    "requirements.txt",
    "requirements-dev.txt",
    "references/analysis-framework.md",
    "references/report-template.md",
    "scripts/extract_pdf.py",
    "tests/test_extract_pdf.py",
)
FORBIDDEN_GENERATED_NAMES = {"__pycache__", ".pytest_cache"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            fail(f"missing required file: {relative_path}")

    for path in ROOT.rglob("*"):
        if path.name in FORBIDDEN_GENERATED_NAMES:
            fail(f"generated cache must not be committed: {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".pdf":
            fail(f"PDF files must not be committed: {path.relative_to(ROOT)}")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(?P<frontmatter>.*?)\n---\n", skill_text, flags=re.DOTALL)
    if match is None:
        fail("SKILL.md must begin with YAML frontmatter")
    frontmatter = match.group("frontmatter")
    if not re.search(r"^name: paper-style-deconstruct$", frontmatter, re.MULTILINE):
        fail("SKILL.md must define the expected skill name")
    if not re.search(r"^description: .+", frontmatter, re.MULTILINE):
        fail("SKILL.md must define a non-empty description")

    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    for dependency in ("PyMuPDF", "pdfplumber"):
        if dependency not in requirements:
            fail(f"requirements.txt must declare {dependency}")

    template = (ROOT / "references/report-template.md").read_text(encoding="utf-8")
    if "[完整提取的原文文本" in template:
        fail("report template must not request a full-paper appendix")
    for heading in ("逐句修辞分析", "可执行写作配方", "使用限制"):
        if heading not in template:
            fail(f"report template is missing required section: {heading}")

    for script in (ROOT / "scripts").glob("*.py"):
        ast.parse(script.read_text(encoding="utf-8"), filename=str(script))

    print("PASS: skill package quality checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
