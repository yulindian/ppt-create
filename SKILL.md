---
name: ppt-create
description: Create Chinese classroom courseware as image-based PPTX and PDF from a user-provided outline, style prompt, and optional reference images. Use when the user asks to make PPT/PDF课件, directly generate slide images, synthesize a PPT, output a PDF made from slide images, remove page labels from image-based PPTs, or follow the established workflow with fixed teacher name 小余老师, no page-number/page-type labels, and final PPT plus PDF delivery.
---

# PPT Create

## Overview

Create a complete image-based courseware deck: generate one finished 16:9 slide image per page, then output both a PPTX and a PDF from the same ordered images. Prefer this workflow for Chinese primary-school courseware where visual polish matters more than object-level editability.

## Defaults

- Teacher name: `小余老师`.
- Canvas: 16:9 landscape.
- Deliverables: PPTX, PDF, `slides/`, and a montage preview.
- Page images: `slide-01.png`, `slide-02.png`, etc.
- Final files: `<课件名称>_小余老师.pptx` and `<课件名称>_小余老师.pdf`.
- If producing a correction, use suffixes such as `_去标签版`.

## Triggered Dependencies

Use the built-in image generation tool for slide images. For packaging, use the bundled scripts in this skill or the existing `xhs-ppt-recreation` packaging scripts when they are already available.

## Workflow

1. Read the user's outline, style prompt, and reference images.
2. Extract the course title, page count, page titles, page copy, visual style, fixed text, and negative constraints.
3. Build a page list before generating images. Include cover,目录/路线页, transition pages if useful, content pages, activities, summary, and closing pages.
4. Generate one complete slide image per page with title, body text, illustrations, decorative elements, and background already integrated.
5. Save final images in order as `slide-01.png`, `slide-02.png`, etc. Never leave project-bound final images only under the image generation default folder.
6. Create a montage preview for visual review.
7. Regenerate or repair pages with visible defects.
8. Package the same final images into PPTX and PDF.
9. Verify image count, PPT slide count, PDF page count, and at least the montage or representative rendered pages before claiming completion.

## Output Folder

Create one folder per deck:

```text
<workspace>/<课件名称>_图片PPT/
├─ <课件名称>_小余老师.pptx
├─ <课件名称>_小余老师.pdf
├─ montage-preview.png
└─ slides/
   ├─ slide-01.png
   ├─ slide-02.png
   └─ ...
```

For cleaned/corrected versions:

```text
<课件名称>_小余老师_去标签版.pptx
<课件名称>_小余老师_去标签版.pdf
montage-preview-no-labels.png
slides_no_labels/
```

## Slide Image Prompt Rules

For every slide prompt, include:

- Course theme and audience.
- Exact slide title.
- Exact body text when known.
- Layout goal: e.g. middle whitespace, illustration plus text, rounded card, cloud panel, four-card grid.
- Visual style from the user's style prompt.
- Required fixed teacher name when needed: `小余老师`.
- Negative constraints.

Always include this constraint unless the user explicitly asks for labels:

```text
Do not include any page number, page label, page type tag, corner tag, or text such as "第几页", "第01页", "知识页", "礼仪页", "互动页", "总结页", "过渡页", "导入页", "练习页". No watermark, QR code, account name, or platform mark.
```

For low-grade classroom courseware:

- Use large, readable rounded Chinese text.
- Keep sentences short and projection-friendly.
- Use clear cards, cloud panels, book pages, blackboards, tickets, badges, or simple charts.
- Keep decorations around the edges when the middle needs content space.
- Avoid dense text and tiny labels.

## Visual QA

Check before packaging:

- Page count matches the outline.
- No blank, duplicated, or wrongly ordered pages.
- No watermark, QR code, account, or platform identity.
- No page-number/page-type labels unless requested.
- Titles and body text are readable.
- Text does not overflow or collide with illustrations.
- Style is consistent.
- PDF and PPT use the same final slide images.

## Packaging

Prefer scripts in `scripts/`:

```powershell
python scripts/images_to_pptx.py --slides-dir <slides> --out <deck.pptx>
python scripts/images_to_pdf.py --slides-dir <slides> --out <deck.pdf>
```

If `xhs-ppt-recreation` is available and already used in the workflow, its `pack_image_ppt.mjs` and `make_slide_montage.mjs` scripts are also acceptable.

## Existing Image-Based PPT Cleanup

When the user asks to remove `第几页`, `知识页`, `互动页`, `礼仪页`, `总结页`, `过渡页`, or similar labels from an existing image-based PPT:

1. Locate the source slide images if available. If not, extract or render slides first.
2. Generate a montage and identify pages with labels.
3. Prefer writing cleaned images to `slides_no_labels/`; do not overwrite the original `slides/`.
4. If labels are embedded in the image, either regenerate the affected slide or locally patch only the label area.
5. Make the removal complete. A small neutral patch is acceptable when the alternative is visible label text; disclose it in final notes.
6. Rebuild both PPTX and PDF from the cleaned images.
7. Verify PPT slide count and PDF page count.

## Final Response

Return concise paths to:

- PPTX
- PDF
- montage preview
- output folder if useful

State verification results: page count, PPT/PDF consistency, and label/watermark status. For PDF files, include the required Codex PDF file citation when appropriate.
