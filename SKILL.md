---
name: ppt-create
description: Use when creating Chinese classroom courseware, image-based PDF decks, slide-image courseware, PDF课件, direct slide image generation, polished non-editable decks, or cleaning labels from existing image-based PPT/PDF files.
---

# PPT Create

## Overview

Create a complete image-based Chinese classroom courseware PDF. The workflow is image-first: generate one finished 16:9 slide image per page with an image model, then package the same ordered images into PDF.

Use this when visual polish matters more than object-level editability. If the user explicitly asks for editable-object slides, use an editable PPT workflow instead. If the user explicitly asks for PPTX in addition to PDF, create PPTX as an extra deliverable; otherwise do not create PPTX.

## Defaults

- Teacher name: `小余老师`.
- Canvas: 16:9 landscape.
- Deliverables: PDF, `slides/`, `slides_pack/`, and a montage preview.
- Page images: `slide-01.png`, `slide-02.png`, etc.
- Always keep PNG originals in `slides/`; always package from a compressed `slides_pack/` folder by default. Do not ask whether to compress.
- Default packaging images: JPG, fit within `1920x1080`, quality `90`.
- Final PDF: `<课件名称>_小余老师.pdf`.
- If the deck has 30 pages or fewer, output only the single final PDF.
- If the deck has more than 30 pages, output both the single final PDF and 30-page chunk PDFs named like `<课件名称>_小余老师_part-01.pdf`, `<课件名称>_小余老师_part-02.pdf`, etc.
- Correction suffix example: `_去标签版`.

## Required Tools

**REQUIRED IMAGE TOOL:** Use the `image_gen` / image generation tool for newly created slide images.

For packaging, prefer scripts in this skill's `scripts/` directory. If this workflow already uses `xhs-ppt-recreation`, its image-PPT packaging and montage scripts are acceptable.

## Mandatory Image Model Generation

Every newly created deck must call the image generation tool to render one complete final slide image per page.

Each generated slide image must already contain the complete slide: title, body copy, visual scene, illustrations, cards, decorative elements, and background. PDF packaging must place those final images as full-page pages. Create PPTX only if the user explicitly asks for it.

Do not replace image model generation with:

- shape-only PPT construction,
- code-drawn layouts,
- manually assembled backgrounds plus text overlays,
- SVG-only mockups,
- template-only decks,
- or an editable-object PPT workflow.

Only skip image generation when the user explicitly asks for an editable-object PPT, a text-only outline, or a non-image draft.

If the user says "直接生图", "根据先前流程", "制作PPT", "制作课件", "输出PDF", "输出PPT/PDF", or invokes this skill for final delivery, treat image generation as required. Even when the user says PPT, the default final deliverable is PDF unless they explicitly ask for PPTX output.

## Workflow

1. Read the user's outline, style prompt, and reference images.
2. Extract the course title, page count, page titles, page copy, audience, visual style, fixed text, and negative constraints.
3. Build the full page list before generating images. Include cover,目录/路线页, transition pages if useful, content pages, activities, summary, and closing pages.
4. Write one shared style brief for the whole deck: palette, illustration style, typography, classroom tone, teacher name, and negative constraints.
5. Draft one image prompt per slide using the shared style brief.
6. Generate one complete slide image per page with the image generation tool.
7. Save final images in order as `slide-01.png`, `slide-02.png`, etc. Never leave project-bound final images only under the image generation default folder.
8. Create a montage preview for visual review.
9. Regenerate or repair pages with visible defects.
10. Create the compressed packaging image set in `slides_pack/` from the approved PNG originals using JPG, max `1920x1080`, quality `90`. Do this by default without asking.
11. Package PDF from `slides_pack/`; use `slides/` only when compression makes text visibly worse.
12. If the page count is greater than 30, also output chunk PDFs in 30-page batches. Always keep the single complete PDF too.
13. Create PPTX only when the user explicitly asks for PPTX output.
14. Verify image count, PDF page count, chunk PDF page ranges when applicable, and the montage or representative rendered pages before claiming completion. If PPTX was explicitly requested, also verify PPT slide count.

## Parallelization Strategy

Use parallel work where it improves speed without breaking style consistency.

Safe to parallelize:

- Drafting prompts for independent slides after the page list and shared style brief are fixed.
- Generating multiple slide images in separate image generation calls when tool/runtime limits allow it.
- QA checks on different page ranges, such as text readability, label removal, ordering, and style consistency.
- Regenerating independent defective pages while unaffected pages remain fixed.
- Packaging scripts and file-count inspection after all final images exist.

Keep sequential:

- Requirement extraction and page list approval.
- Shared style brief creation.
- Final slide ordering.
- Final PDF packaging from the approved ordered `slides_pack/` folder, after it is derived from `slides/`.
- Final verification and delivery notes.

Parallel generation rule: every parallel slide prompt must reference the same shared style brief, exact page title, exact body text, and the same negative constraints. If parallel outputs drift in style, stop batching and regenerate affected pages with a tighter shared style brief.

## Output Folder

Create one folder per deck:

```text
<workspace>/<课件名称>_图片PPT/
├─ <课件名称>_小余老师.pdf
├─ <课件名称>_小余老师_part-01.pdf  # only when total pages > 30
├─ <课件名称>_小余老师_part-02.pdf  # only when total pages > 30
├─ preview/
│  └─ montage.png
├─ slides_pack/
│  ├─ slide-01.jpg
│  ├─ slide-02.jpg
│  └─ ...
└─ slides/
   ├─ slide-01.png
   ├─ slide-02.png
   └─ ...
```

For cleaned/corrected versions:

```text
<课件名称>_小余老师_去标签版.pdf
<课件名称>_小余老师_去标签版_part-01.pdf  # only when total pages > 30
preview/montage-no-labels.png
slides_no_labels/
```

## Slide Image Prompt Contract

For every slide prompt, include:

- Course theme and audience.
- Exact slide title.
- Exact body text when known.
- Layout goal, such as middle whitespace, illustration plus text, rounded card, cloud panel, or four-card grid.
- Shared visual style from the deck style brief.
- Fixed teacher name when needed: `小余老师`.
- Negative constraints.
- Decoration-text constraint: do not generate long text, dense paragraphs, pseudo-writing, or incidental words inside illustrations, backgrounds, icons, book covers, posters, road signs, labels, stickers, badges, or decorative elements. Keep decorative areas blank or use simple non-text symbols unless the slide content explicitly requires short readable words there.

Always include this constraint unless the user explicitly asks for labels:

```text
Do not include any page number, page label, page type tag, corner tag, or text such as "第几页", "第1页", "知识页", "礼仪页", "互动页", "总结页", "过渡页", "导入页", or "练习页". No watermark, QR code, account name, or platform mark.
Do not generate long text, dense paragraphs, pseudo-writing, or incidental words inside illustrations, backgrounds, icons, book covers, posters, road signs, stickers, badges, labels, or decorative elements. Keep decorative areas blank or use simple non-text symbols unless explicitly specified as slide content.
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
- No watermark, QR code, account name, or platform identity.
- No page-number/page-type labels unless requested.
- Titles and body text are readable.
- Text does not overflow or collide with illustrations.
- Illustrations, backgrounds, icons, book covers, posters, road signs, labels, stickers, badges, and decorative elements do not contain long text, dense pseudo-writing, or unintended paragraphs.
- Style is consistent across independently generated pages.
- PDF uses the approved final slide images from `slides_pack/`.
- If total pages exceed 30, chunk PDFs cover all pages in order without overlap or missing pages.
- If the user explicitly requested PPTX, PDF and PPTX use the same final slide images.

## Packaging

Prefer scripts in `scripts/`:

```powershell
python scripts/compress_slide_images.py --slides-dir <slides> --out-dir <slides_pack> --quality 90 --max-width 1920 --max-height 1080
python scripts/images_to_pdf.py --slides-dir <slides_pack> --out <deck.pdf> --chunk-size 30
```

Use `slides/` as the source of truth and `slides_pack/` only as the delivery/packaging image set. Do not overwrite PNG originals.

Size-control defaults:

- Always use JPG quality `90`, max `1920x1080`, for ordinary classroom projection unless the user explicitly asks for another setting or preview checks show text degradation.
- Use quality `92-95` for dense text, math formulas, or pages with many thin lines.
- Use quality `85-88` only when the user prioritizes smaller files and preview checks still show readable text.
- Keep the long edge within full-HD `1920x1080` for typical PPT/PDF delivery. Use original dimensions only when the user asks for maximum quality or large-screen printing.
- If a compressed page shows fuzzy text, regenerate only that page in `slides_pack/` at a higher quality or original dimensions.

`images_to_pdf.py` accepts ordered `slide-*.png`, `slide-*.jpg`, and `slide-*.jpeg` files. Keep one image format per packaging folder when possible.

If the user explicitly requests PPTX too, additionally run:

```powershell
python scripts/images_to_pptx.py --slides-dir <slides_pack> --out <deck.pptx>
```

If `xhs-ppt-recreation` is available and already used in the workflow, its `pack_image_ppt.mjs` and `make_slide_montage.mjs` scripts are also acceptable.

## Existing Image-Based PPT Cleanup

When the user asks to remove "第几页", "知识页", "互动页", "礼仪页", "总结页", "过渡页", or similar labels from an existing image-based PPT:

1. Locate the source slide images if available. If not, extract or render slides first.
2. Generate a montage and identify pages with labels.
3. Prefer writing cleaned images to `slides_no_labels/`; do not overwrite the original `slides/`.
4. If labels are embedded in the image, either regenerate the affected slide or locally patch only the label area.
5. Make the removal complete. A small neutral patch is acceptable when the alternative is visible label text; disclose it in final notes.
6. Rebuild the PDF from the cleaned images, including 30-page chunk PDFs when the page count is greater than 30.
7. Rebuild PPTX only if the user explicitly requested PPTX.
8. Verify PDF page count and chunk coverage. If PPTX was explicitly requested, also verify PPT slide count.

## Final Response

Return concise paths to:

- PDF
- Chunk PDFs when total pages > 30
- montage preview
- output folder if useful

State verification results: image count, PDF page count, chunk PDF coverage when applicable, and label/watermark status. Include PPTX only if the user explicitly requested it. For PDF files, include the required Codex PDF file citation when appropriate.
