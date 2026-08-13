"""Extract text, tables, raster-image locations, and page renders from a PDF.

Usage: python scripts/extract_pdf.py <pdf_path> [--output-dir <dir>]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CONTENT_FORMAT_VERSION = "1.0"


def _relative_path(path: Path, output_dir: Path) -> str:
    return path.relative_to(output_dir).as_posix()


def _extract_text_blocks(page: Any) -> list[dict[str, Any]]:
    import fitz

    text_blocks: list[dict[str, Any]] = []
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])
    for block in blocks:
        if block.get("type") != 0:
            continue
        lines: list[dict[str, Any]] = []
        full_lines: list[str] = []
        for line in block.get("lines", []):
            spans = [
                {
                    "text": span["text"],
                    "font": span["font"],
                    "size": span["size"],
                    "flags": span["flags"],
                    "bbox": list(span["bbox"]),
                }
                for span in line.get("spans", [])
            ]
            line_text = "".join(span["text"] for span in spans)
            lines.append({"text": line_text, "spans": spans, "bbox": list(line["bbox"])})
            full_lines.append(line_text)
        text_blocks.append(
            {"bbox": list(block["bbox"]), "lines": lines, "full_text": "\n".join(full_lines)}
        )
    return text_blocks


def _image_occurrences(page: Any) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    seen_xrefs: set[int] = set()
    for image in page.get_images(full=True):
        xref = image[0]
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)
        for bbox in page.get_image_rects(xref, transform=False):
            occurrences.append({"xref": xref, "bbox": list(bbox)})
    return occurrences


def _extract_raster_assets(document: Any, output_dir: Path) -> dict[int, str]:
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    assets: dict[int, str] = {}
    for page in document:
        for image in page.get_images(full=True):
            xref = image[0]
            if xref in assets:
                continue
            extracted = document.extract_image(xref)
            if not extracted or not extracted.get("image"):
                continue
            extension = extracted.get("ext", "bin")
            asset_path = images_dir / f"xref_{xref}.{extension}"
            asset_path.write_bytes(extracted["image"])
            assets[xref] = _relative_path(asset_path, output_dir)
    return assets


def _extract_tables(pdf_path: Path, page_count: int, warnings: list[str]) -> list[list[dict[str, Any]]]:
    tables_by_page: list[list[dict[str, Any]]] = [[] for _ in range(page_count)]
    try:
        import pdfplumber

        with pdfplumber.open(pdf_path) as plumber_document:
            for page_number, plumber_page in enumerate(plumber_document.pages):
                for index, table in enumerate(plumber_page.extract_tables()):
                    if table and any(any(cell is not None for cell in row) for row in table):
                        tables_by_page[page_number].append({"index": index, "rows": table})
    except Exception as error:  # Table extraction is explicitly best effort.
        warnings.append(f"Table extraction failed: {error}")
    return tables_by_page


def extract_pdf(pdf_path: str | Path, output_dir: str | Path, render_dpi: int = 160) -> dict[str, Any]:
    """Extract PDF content and write binary assets into *output_dir*."""
    import fitz

    source = Path(pdf_path).expanduser().resolve()
    destination = Path(output_dir).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"PDF file does not exist: {source}")
    if source.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, received: {source.name}")
    if render_dpi <= 0:
        raise ValueError("render_dpi must be greater than zero")

    destination.mkdir(parents=True, exist_ok=True)
    renders_dir = destination / "pages"
    renders_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []

    try:
        document = fitz.open(source)
    except Exception as error:
        raise ValueError(f"Unable to open PDF '{source}': {error}") from error

    try:
        raster_assets = _extract_raster_assets(document, destination)
        tables_by_page = _extract_tables(source, len(document), warnings)
        scale = render_dpi / 72
        pages: list[dict[str, Any]] = []

        for page_index, page in enumerate(document):
            render_path = renders_dir / f"page_{page_index + 1:03d}.png"
            page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False).save(render_path)
            embedded_images = []
            for occurrence in _image_occurrences(page):
                asset_path = raster_assets.get(occurrence["xref"])
                if asset_path is None:
                    warnings.append(
                        f"Could not extract raster asset xref {occurrence['xref']} on page {page_index + 1}."
                    )
                    continue
                embedded_images.append({**occurrence, "asset": asset_path})

            pages.append(
                {
                    "page_number": page_index + 1,
                    "width": page.rect.width,
                    "height": page.rect.height,
                    "render": _relative_path(render_path, destination),
                    "text_blocks": _extract_text_blocks(page),
                    "images": embedded_images,
                    "tables": tables_by_page[page_index],
                }
            )
    finally:
        document.close()

    return {
        "format_version": CONTENT_FORMAT_VERSION,
        "file": source.name,
        "page_count": len(pages),
        "assets": {
            "page_renders_directory": "pages",
            "embedded_images_directory": "images",
            "embedded_images": [{"xref": xref, "asset": asset} for xref, asset in sorted(raster_assets.items())],
        },
        "warnings": warnings,
        "pages": pages,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract structured content from a research-paper PDF")
    parser.add_argument("pdf_path", help="Path to the source PDF")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: <pdf>_extracted)")
    parser.add_argument("--render-dpi", type=int, default=160, help="DPI for complete-page PNG renders")
    args = parser.parse_args()

    source = Path(args.pdf_path).expanduser()
    output_dir = Path(args.output_dir).expanduser() if args.output_dir else source.with_name(f"{source.stem}_extracted")
    try:
        result = extract_pdf(source, output_dir, args.render_dpi)
    except (FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    content_path = output_dir.resolve() / "content.json"
    content_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for warning in result["warnings"]:
        print(f"warning: {warning}", file=sys.stderr)
    print(content_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
