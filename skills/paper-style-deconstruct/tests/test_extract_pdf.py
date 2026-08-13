from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import fitz


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))
import extract_pdf  # noqa: E402


def create_pdf(path: Path, include_image: bool = False, repeated_image: bool = False) -> None:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "A readable body sentence. Another sentence follows.")
    page.draw_rect(fitz.Rect(72, 100, 230, 180), color=(0, 0, 0), fill=(0.8, 0.8, 0.8))
    if include_image:
        image = fitz.Pixmap(fitz.csRGB, fitz.Rect(0, 0, 8, 8), 0)
        image.clear_with(0x336699)
        image_path = path.with_suffix(".png")
        image.save(image_path)
        page.insert_image(fitz.Rect(72, 210, 130, 268), filename=image_path)
        if repeated_image:
            page.insert_image(fitz.Rect(150, 210, 208, 268), filename=image_path)
        image_path.unlink()
    document.save(path)
    document.close()


class ExtractPdfTests(unittest.TestCase):
    def test_extracts_text_renders_and_deduplicates_repeated_images(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            source = temporary_path / "paper.pdf"
            output = temporary_path / "output"
            create_pdf(source, include_image=True, repeated_image=True)

            result = extract_pdf.extract_pdf(source, output)

            self.assertEqual(result["format_version"], "1.0")
            self.assertEqual(result["page_count"], 1)
            page = result["pages"][0]
            self.assertTrue((output / page["render"]).is_file())
            self.assertIn("readable body sentence", page["text_blocks"][0]["full_text"].lower())
            self.assertEqual(len(page["images"]), 2)
            self.assertEqual(page["images"][0]["asset"], page["images"][1]["asset"])
            self.assertEqual(len(result["assets"]["embedded_images"]), 1)
            self.assertTrue((output / page["images"][0]["asset"]).is_file())

    def test_vector_content_has_a_page_render_without_embedded_images(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            source = temporary_path / "vector.pdf"
            output = temporary_path / "output"
            create_pdf(source)

            result = extract_pdf.extract_pdf(source, output)

            page = result["pages"][0]
            self.assertEqual(page["images"], [])
            self.assertGreater((output / page["render"]).stat().st_size, 0)

    def test_table_extraction_failure_is_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            source = temporary_path / "paper.pdf"
            output = temporary_path / "output"
            create_pdf(source)

            with mock.patch("pdfplumber.open", side_effect=RuntimeError("table reader failed")):
                result = extract_pdf.extract_pdf(source, output)

            self.assertEqual(result["pages"][0]["tables"], [])
            self.assertTrue(any("Table extraction failed" in warning for warning in result["warnings"]))

    def test_invalid_source_and_dpi_raise_clear_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            with self.assertRaisesRegex(FileNotFoundError, "does not exist"):
                extract_pdf.extract_pdf(temporary_path / "missing.pdf", temporary_path / "output")

            text_file = temporary_path / "paper.txt"
            text_file.write_text("not a PDF", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Expected a .pdf"):
                extract_pdf.extract_pdf(text_file, temporary_path / "output")

            source = temporary_path / "paper.pdf"
            create_pdf(source)
            with self.assertRaisesRegex(ValueError, "render_dpi"):
                extract_pdf.extract_pdf(source, temporary_path / "output", render_dpi=0)

    def test_cli_writes_content_json_to_explicit_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            source = temporary_path / "paper.pdf"
            output = temporary_path / "custom-output"
            create_pdf(source)

            completed = subprocess.run(
                [sys.executable, str(PACKAGE_ROOT / "scripts" / "extract_pdf.py"), str(source), "-o", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            content_path = output / "content.json"
            self.assertTrue(content_path.is_file())
            self.assertEqual(json.loads(content_path.read_text(encoding="utf-8"))["file"], "paper.pdf")


if __name__ == "__main__":
    unittest.main()
