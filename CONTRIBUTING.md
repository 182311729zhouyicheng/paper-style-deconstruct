# Contributing

Thank you for improving this skill.

## Before opening a pull request

1. Keep source PDFs, extracted assets, and generated reports out of Git.
2. Add or update unit tests for extractor behavior changes.
3. Run the local checks:

   ```bash
   python -m pip install -r skills/paper-style-deconstruct/requirements-dev.txt
   python skills/paper-style-deconstruct/scripts/check_quality.py
   python -m unittest discover -s skills/paper-style-deconstruct/tests -v
   ```

4. If the change affects agent behavior, add a public URL and expected checks to `evals/evals.json`.
5. Do not add long excerpts, source figures, or unpublished manuscripts. Every writing-style conclusion should be traceable to a short excerpt or stable location in the source.

## Pull request expectations

Describe the user problem, explain why the skill instructions or extractor changed, list the commands you ran, and call out any known limitations. Keep changes narrowly focused and avoid unrelated formatting churn.
