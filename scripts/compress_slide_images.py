#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from PIL import Image


SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg"}


def collect_slide_images(slides_dir):
    files = [
        file for file in slides_dir.iterdir()
        if file.is_file()
        and file.name.lower().startswith("slide-")
        and file.suffix.lower() in SUPPORTED_SUFFIXES
    ]
    return sorted(files, key=lambda file: file.name.lower())


def fit_size(width, height, max_width, max_height):
    scale = min(max_width / width, max_height / height, 1)
    return int(round(width * scale)), int(round(height * scale))


def to_rgb(image):
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        background = Image.new("RGB", image.size, "white")
        rgba = image.convert("RGBA")
        background.paste(rgba, mask=rgba.getchannel("A"))
        return background
    return image.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description="Create high-quality JPG packaging images from ordered slide images.")
    parser.add_argument("--slides-dir", required=True, help="Directory containing slide-01.png, slide-02.png, ...")
    parser.add_argument("--out-dir", required=True, help="Output directory for slide-01.jpg, slide-02.jpg, ...")
    parser.add_argument("--quality", type=int, default=90, help="JPG quality, usually 88-92")
    parser.add_argument("--max-width", type=int, default=1920, help="Maximum output width")
    parser.add_argument("--max-height", type=int, default=1080, help="Maximum output height")
    parser.add_argument("--expected-count", type=int, default=None, help="Fail if the image count differs")
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    out_dir = Path(args.out_dir)
    files = collect_slide_images(slides_dir)
    if not files:
        raise SystemExit(f"No slide images found in {slides_dir}")
    if args.expected_count is not None and len(files) != args.expected_count:
        raise SystemExit(f"Expected {args.expected_count} images, got {len(files)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for index, file in enumerate(files, start=1):
        out_file = out_dir / f"slide-{index:02d}.jpg"
        with Image.open(file) as image:
            image = to_rgb(image)
            width, height = fit_size(image.width, image.height, args.max_width, args.max_height)
            if (width, height) != image.size:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            image.save(out_file, quality=args.quality, optimize=True, progressive=True)
        outputs.append(out_file)

    print(json.dumps({
        "output_dir": str(out_dir),
        "images": len(outputs),
        "quality": args.quality,
        "max_size": f"{args.max_width}x{args.max_height}",
        "size_mb": round(sum(file.stat().st_size for file in outputs) / 1024 / 1024, 2),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
