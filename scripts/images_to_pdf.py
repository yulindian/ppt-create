#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg"}


def collect_slide_images(slides_dir):
    files = [
        file for file in slides_dir.iterdir()
        if file.is_file()
        and file.name.lower().startswith("slide-")
        and file.suffix.lower() in SUPPORTED_SUFFIXES
    ]
    return sorted(files, key=lambda file: file.name.lower())


def write_pdf(files, out_pdf):
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(files[0]) as first:
        width, height = first.size

    deck = canvas.Canvas(str(out_pdf), pagesize=(width, height))
    for file in files:
        with Image.open(file) as image:
            if image.size == (width, height) and file.suffix.lower() in {".jpg", ".jpeg"}:
                deck.drawImage(str(file), 0, 0, width=width, height=height)
            elif image.size != (width, height):
                image = image.resize((width, height), Image.Resampling.LANCZOS)
                deck.drawImage(ImageReader(image.convert("RGB")), 0, 0, width=width, height=height)
            else:
                deck.drawImage(ImageReader(image.convert("RGB")), 0, 0, width=width, height=height)
        deck.showPage()
    deck.save()
    return {
        "output": str(out_pdf),
        "pages": len(files),
        "page_size": f"{width}x{height}",
        "size_mb": round(out_pdf.stat().st_size / 1024 / 1024, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Create PDF files from ordered slide images.")
    parser.add_argument("--slides-dir", required=True, help="Directory containing slide-01.png/jpg, slide-02.png/jpg, ...")
    parser.add_argument("--out", required=True, help="Output PDF path")
    parser.add_argument("--expected-count", type=int, default=None, help="Fail if the image count differs")
    parser.add_argument("--chunk-size", type=int, default=0, help="Also write chunked PDFs of this many pages when image count exceeds this value")
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    out_pdf = Path(args.out)
    files = collect_slide_images(slides_dir)
    if not files:
        raise SystemExit(f"No slide images found in {slides_dir}")
    if args.expected_count is not None and len(files) != args.expected_count:
        raise SystemExit(f"Expected {args.expected_count} images, got {len(files)}")

    results = [write_pdf(files, out_pdf)]
    if args.chunk_size and args.chunk_size > 0 and len(files) > args.chunk_size:
        for index, start in enumerate(range(0, len(files), args.chunk_size), start=1):
            chunk_files = files[start:start + args.chunk_size]
            chunk_out = out_pdf.with_name(f"{out_pdf.stem}_part-{index:02d}{out_pdf.suffix}")
            result = write_pdf(chunk_files, chunk_out)
            result["range"] = f"{start + 1}-{start + len(chunk_files)}"
            results.append(result)

    print({
        "outputs": results,
        "total_pages": len(files),
        "chunk_size": args.chunk_size,
    })


if __name__ == "__main__":
    main()
