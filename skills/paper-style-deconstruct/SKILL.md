---
name: paper-style-deconstruct
description: Analyze the writing style and argument structure of an English engineering research-paper PDF and produce a detailed Chinese Markdown writing blueprint. Use when a user asks to deconstruct a paper, analyze its writing style, study its rhetoric, formulas, figures, tables, or section organization, or imitate its academic writing style. Intended for CS, EE, automation, and related engineering papers.
---

# Paper Style Deconstruct

Analyze an English engineering research paper into a Chinese, evidence-based writing blueprint. The purpose is to learn transferable rhetorical and structural choices, not to reproduce the paper.

## Scope and prerequisites

- Apply to English research-paper PDFs in computer science, electrical engineering, automation, and related fields.
- Require a readable local PDF. Scanned PDFs without an OCR text layer can be inspected visually, but sentence-level coverage is not reliable; state this limitation before continuing.
- Install extraction dependencies before use:

  ```bash
  python -m pip install -r skills/paper-style-deconstruct/requirements.txt
  ```

- Extract the paper before analysis:

  ```bash
  python skills/paper-style-deconstruct/scripts/extract_pdf.py <pdf_path>
  ```

## Workflow

### 1. Inspect the extracted paper

Read `content.json`, its text blocks, tables, embedded-image index, and page renderings. Page renderings are the source for vector figures, composite figures, and other graphics that are not embedded as raster images. Use the page number and bounding boxes to connect evidence to the original PDF.

If extraction reports warnings, explain their effect on the analysis. Do not claim that an unreadable figure, table, formula, or scanned sentence was fully analyzed.

### 2. Analyze the full body text

Default to sentence-level coverage of all readable body text. Exclude references, page headers and footers, acknowledgments, and boilerplate. For every analyzed sentence, record:

- Original short excerpt and page/section location
- Rhetorical function
- Sentence pattern, tense, voice, and stance or hedging
- A transferable writing observation

For long papers, this produces a large report and can take substantial time. Tell the user that full coverage is expensive before beginning; only reduce scope when the user explicitly requests a focused analysis.

### 3. Analyze non-textual evidence

- For each formula or algorithm block, explain its introduction, numbering, post-explanation, and position in the argument.
- For every figure and table that can be read, identify its claim, caption style, in-text references, surrounding explanation, and argumentative role.
- Separate observations directly supported by the paper from interpretation. Mark uncertain visual readings as limitations.

### 4. Produce the report

Read `references/analysis-framework.md` and follow `references/report-template.md`. Write Chinese except for brief English excerpts. Save the report beside the PDF as `<paper_name>_deconstruction.md`.

The report must include a concrete writing blueprint: section-level sentence counts, rhetorical sequences, generalized sentence patterns, tense and voice conventions, and transition-word guidance. Tailor it to the analyzed paper; do not invent statistics or evidence.

## Copyright and privacy

- Use only the excerpts needed to support an analysis. Include page and section locations instead of reproducing full paragraphs or a full-paper appendix.
- Do not redistribute the source PDF, its extracted assets, or its complete text unless the user has permission to do so.
- Treat uploaded unpublished manuscripts as confidential and do not place their contents in public examples, evaluations, or repositories.

## Resources

- `references/analysis-framework.md`: evidence standards and analysis dimensions
- `references/report-template.md`: required report layout
- `scripts/extract_pdf.py`: PDF text, table, image, and page-render extraction
