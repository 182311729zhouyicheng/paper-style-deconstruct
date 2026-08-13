# Paper Style Deconstruct | 论文写作风格拆解

Turn an English engineering research-paper PDF into a Chinese, evidence-backed writing blueprint. The skill makes academic writing choices inspectable: sentence rhetoric, argument progression, formulas, figures, tables, citations, and section patterns.

[English](#why-this-skill) | [中文](#中文简介) | [Quick start](#quick-start) | [Demo](#demo) | [Contributing](#contributing)

`paper-style-deconstruct` is an Agent Skill for turning an English engineering research-paper PDF into a detailed Chinese writing-style analysis and a reusable writing blueprint.

It is intended for computer science, electrical engineering, automation, and closely related papers. It analyzes sentence-level rhetoric, paragraph and section organization, formula placement, figures, tables, citations, and the paper's argument progression.

## Why this skill

- **More than a summary:** traces how each readable sentence advances an academic argument.
- **Visual-aware:** renders every page so vector diagrams and composite figures remain available to an agent with vision.
- **Reusable output:** produces a section-by-section writing recipe rather than copying a paper's prose.
- **Responsible by design:** requires short evidence excerpts and location references, not a full-paper transcript.

## Quick start

```bash
git clone https://github.com/jackz121000/paper-style-deconstruct.git
cd paper-style-deconstruct
python -m pip install -r skills/paper-style-deconstruct/requirements.txt
python skills/paper-style-deconstruct/scripts/extract_pdf.py path/to/paper.pdf
```

Install the repository as a Codex plugin or copy `skills/paper-style-deconstruct/` into a compatible Agent Skills location. Then ask: `请完整拆解这篇英文工程论文的写作风格。`

## Demo

The repository includes two reproducible public-paper cases in `evals/evals.json`:

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762): formulas, tables, and raster assets.
- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385): vector/composite architecture figures and experimental tables.

See [`examples/attention-is-all-you-need-excerpt.md`](examples/attention-is-all-you-need-excerpt.md) for a compact, non-infringing illustration of the analysis format. Download evaluation PDFs yourself; never commit them.

## What is included

- `.codex-plugin/plugin.json`: Codex skill-only plugin manifest
- `skills/paper-style-deconstruct/`: instructions, extractor, references, tests, and dependencies
- `evals/`: public-paper evaluation cases and an editorial review rubric
- `examples/`: short, evidence-based report excerpts with no source PDF assets

## Installation

Copy this directory into your Agent Skills directory, or add it to an Agent Skills-compatible repository. For local Python dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r skills/paper-style-deconstruct/requirements.txt
```

On macOS or Linux, activate the virtual environment with `source .venv/bin/activate`.

## Usage

Extract a paper before asking an agent to analyze it:

```bash
python skills/paper-style-deconstruct/scripts/extract_pdf.py path/to/paper.pdf
```

The default output directory is `path/to/paper_extracted/` and contains:

```text
content.json          Structured text, tables, image locations, and asset index
images/               Deduplicated embedded raster assets
pages/page_001.png    Render of every PDF page, including vector graphics
```

Then ask an agent with this skill enabled to deconstruct the paper. The final report is written beside the source PDF as `<paper_name>_deconstruction.md`.

## Input and output boundaries

- Supports readable, English-language engineering PDFs. Scanned PDFs require OCR for reliable sentence-level analysis.
- Page PNGs preserve vector and composite graphics for visual inspection. The script does not claim to automatically identify the exact bounding box of every vector figure.
- Table extraction is best effort. A table-extraction warning does not stop text and page-render extraction.
- The generated report is in Chinese, with only short English excerpts needed as evidence.

## Copyright and privacy

Do not commit PDFs, extracted paper text, generated paper images, or reports derived from unpublished manuscripts. Link public evaluation documents instead of distributing them. The skill teaches analytical methods; it should not be used to reproduce a paper's full text or figures.

## Development and checks

Install development dependencies and run all checks:

```bash
python -m pip install -r skills/paper-style-deconstruct/requirements-dev.txt
python skills/paper-style-deconstruct/scripts/check_quality.py
python -m unittest discover -s skills/paper-style-deconstruct/tests -v
```

The quality script validates required package files, YAML frontmatter, dependency declarations, report-template constraints, and accidental generated artifacts. Evaluation cases and the human review rubric are in `evals/`.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). Keep `SKILL.md` concise and move detailed, optional guidance into `references/`. Add tests for every extractor behavior change, and do not add copyrighted paper files. New evaluation cases must point to public URLs and state what a reviewer should verify.

## License

Apache-2.0. See `LICENSE.txt`.

## 中文简介

这是一个面向英文工程论文的 Agent Skill。它将论文转换为中文、可追溯证据的写作风格拆解报告：逐句修辞功能、段落和章节论证链、公式放置、图表叙事、引用策略，以及可直接使用的写作配方。

它不输出论文全文，不打包测试论文 PDF，并要求将观察事实与分析推断分开。适用于计算机、电子、电气、自动化及相近工程领域。
