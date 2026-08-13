#!/usr/bin/env python
"""Copy finalized ppt-edit artifacts into a delivery directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("final_pptx")
    parser.add_argument("delivery_dir")
    parser.add_argument("--name", help="Output PPTX filename")
    args = parser.parse_args()

    final_pptx = Path(args.final_pptx).resolve()
    delivery_dir = Path(args.delivery_dir).resolve()
    if not final_pptx.is_file():
        raise SystemExit(f"missing PPTX: {final_pptx}")

    delivery_dir.mkdir(parents=True, exist_ok=True)
    out_name = args.name or final_pptx.name
    out_pptx = delivery_dir / out_name
    shutil.copy2(final_pptx, out_pptx)

    final_dir = final_pptx.parent
    validation = final_dir / "validation.json"
    if validation.is_file():
        shutil.copy2(validation, delivery_dir / "validation.json")

    fonts = final_dir / "fonts"
    if fonts.is_dir():
        dest = delivery_dir / "fonts"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(fonts, dest)

    print(out_pptx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

