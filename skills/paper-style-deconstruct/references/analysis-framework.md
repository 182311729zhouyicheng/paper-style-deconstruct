# Evidence-Based Analysis Framework

Use this framework after extraction. Every conclusion must distinguish a directly observable fact from an interpretation, and cite a page number, section label, figure/table/formula label, or a short original excerpt.

## Evidence rules

- Quote only the minimum English text needed to establish a claim.
- Label uncertainty when PDF extraction, OCR, a dense visual, or ambiguous sentence structure prevents a reliable reading.
- Do not infer measurements, intent, or causal claims that the paper does not support.
- Exclude references, page furniture, acknowledgments, and publisher boilerplate from sentence coverage.

## Sentence-level coverage

For each readable body sentence, record its location, short excerpt, rhetorical function, sentence pattern, tense, voice, stance, and transferable technique.

Use these rhetorical labels where relevant: `topic`, `elaboration`, `evidence`, `reasoning`, `transition`, `summary`, `gap`, `contribution`, `justification`, `implication`, `limitation`, and `definition`.

Describe sentence patterns as `simple`, `compound`, `complex`, or `compound-complex`. Identify active/passive voice, observed tense, hedging, boosting, author self-reference, and transition devices without forcing a label where it does not fit.

## Paragraph and section analysis

For every paragraph, state the sentence count, rhetorical sequence, organization pattern, and its link to adjacent paragraphs. Use labels such as MEAL, problem-solution, comparison, sequence, parallel exposition, or another pattern justified by the text.

For each section, report its approximate share of the paper, section purpose, argument progression, transitions, formula/figure/table density, and recurring language choices. Explain the paper's introduction, related work, method, experiments, and conclusion only when those sections exist.

## Formula, algorithm, figure, and table analysis

For each readable artifact, state:

1. Its location and label.
2. Observable properties: caption form, numbering, symbols, data presentation, or visual layout.
3. The text that introduces and follows it.
4. Its role in the argument and why it appears at that point, marked as interpretation.

Use `content.json` for locations and page renderings for vector or composite graphics. Do not claim a visual detail that cannot be read from the render.

## Writing blueprint

Convert observations into a reusable blueprint rather than a summary. For every major section present in the paper, provide a sentence-function sequence, approximate sentence count, generalized sentence patterns, tense/voice conventions, transition choices, and evidence-derived advice for formulas, figures, tables, and citations. Avoid copying extended source text.
