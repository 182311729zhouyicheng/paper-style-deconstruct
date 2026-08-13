# Human Evaluation Rubric

Download the PDF from the public source URL in `evals.json`; do not commit it. Run the extractor, enable the skill, and request a full deconstruction. Score each criterion as pass, partial, or fail, with page-specific notes.

## Extraction checks

| Criterion | Pass condition |
| --- | --- |
| Page coverage | Every PDF page has a nonempty render in `pages/`. |
| Raster assets | Every extractable embedded raster occurrence is listed with a page bounding box; repeated assets are stored once. |
| Vector support | At least one vector/composite figure can be inspected from the page render. |
| Graceful degradation | Any table-extraction issue is shown as a warning without losing page renders or body text. |

## Report checks

| Criterion | Pass condition |
| --- | --- |
| Sentence coverage | Every readable body sentence is represented once, excluding references and page furniture. |
| Evidence discipline | Each material conclusion gives a short excerpt or a stable page/section/artifact location. |
| Fact vs interpretation | Visual and rhetorical inferences are explicitly framed as analysis, and uncertainty is stated. |
| Non-textual analysis | Present formulas, figures, and tables are tied to their in-text introduction and argumentative role. |
| Writing blueprint | Each major existing section has a usable function sequence, sentence-count guidance, generalized patterns, and language conventions. |
| Copyright boundary | No full-paper transcript, full-paper appendix, or copied source figures appear in the report. |

The package is ready for public contribution only when both evaluation papers pass all extraction checks and all report checks, with no unresolved critical limitation.
