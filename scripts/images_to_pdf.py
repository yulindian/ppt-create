#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def main():
    parser = argparse.ArgumentParser(description="Create a PDF from ordered slide-*.png images.")
    parser.add_argument("--slides-dir", required=True, help="Directory containing slide-01.png, slide-02.png, ...")
    parser.add_argument("--out", required=True, help="Output PDF path")
    parser.add_argument("--expected-count", type=int, default=None, help="Fail if the image count differs")
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    out_pdf = Path(args.out)
    files = sorted(slides_dir.glob("slide-*.png"))
    if not files:
        raise SystemExit(f"No slide-*.png files found in {slides_dir}")
    if args.expected_count is not None and len(files) != args.expected_count:
        raise SystemExit(f"Expected {args.expected_count} images, got {len(files)}")

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(files[0]) as first:
        width, height = first.size

    deck = canvas.Canvas(str(out_pdf), pagesize=(width, height))
    for file in files:
        with Image.open(file) as image:
            if image.size != (width, height):
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            deck.drawImage(ImageReader(image.convert("RGB")), 0, 0, width=width, height=height)
        deck.showPage()
    deck.save()

    print({
        "output": str(out_pdf),
        "pages": len(files),
        "page_size": f"{width}x{height}",
        "size_mb": round(out_pdf.stat().st_size / 1024 / 1024, 2),
    })


if __name__ == "__main__":
    main()
