---
name: ppt-edit
description: "Convert image-based, scanned, visual-design, or insufficiently editable PPT/PDF/image slide sources into editable PowerPoint decks using a paired delivery structure: visible original-image slides plus hidden editable reconstruction slides. Use when the user asks to 转可编辑PPT, 图片PPT转可编辑, 扫描PPT重建, PPT视觉稿还原, 保留原图页并生成隐藏可编辑页, or wants reusable editable PowerPoint output with validation and bundled fonts."
---

# ppt-edit

## Overview

Use this skill to turn visual slide sources into editable PowerPoint decks. The required delivery format is paired slides: each source page becomes one visible original-image slide followed by one hidden editable reconstruction slide.

This skill is a stricter orchestration layer over the `editppt` workflow. It adds project conventions for trial conversions, parallel page workers, font strategy, validation, and delivery packaging.

## Required References

Read only the references needed for the current step:

- `references/workflow.md`: read before starting any conversion.
- `references/parallel-dispatch.md`: read before handling multi-page runs or page workers.
- `references/font-policy.md`: read before choosing or auditing fonts.
- `references/validation-policy.md`: read before recording pages or finalizing.
- `references/delivery-format.md`: read before copying final artifacts or replying to the user.

If the lower-level `image-to-editable-ppt` skill is available, also use it for its `editppt` command contracts, page-worker prompt builder, manifest schema, and page decision rules. This skill does not replace those contracts; it narrows the business workflow and delivery rules for editable PPT production.

## Core Workflow

1. Confirm the input file exists and choose the source route: PPTX first, same-name PDF fallback, then ordered images.
2. Use a stable ASCII working directory for tool execution when source paths contain Chinese characters or spaces.
3. Run `editppt --help`; if unavailable, install the existing editable-PPT CLI before continuing.
4. Run `editppt prepare <input> --job-dir <run> --image-backend builtin-imagegen` when the built-in image tool is callable; otherwise use the CLI fallback contract.
5. Use `editppt run next <run> --json` to advance state.
6. For a single-page run, claim local execution with `editppt run dispatch --local` before writing page artifacts.
7. For multi-page runs, dispatch page workers in parallel according to `references/parallel-dispatch.md`.
8. Record each completed page only with `editppt run record`.
9. Finalize only after all pages are recorded with `editppt run finalize`.
10. Copy the final PPTX, `validation.json`, and `fonts/` folder to the delivery directory.

## Hard Rules

- Do not skip `editppt prepare`.
- Do not hand-edit `deck_manifest.json`, `page_jobs.json`, or other run state files.
- Do not use a full-page screenshot as the editable reconstruction page.
- Do not record a page unless `validation.json` has top-level `"passed": true`.
- Do not set `"passed": true` manually to bypass validation.
- Do not rebuild all pages locally in a multi-page run; use page workers.
- Do not let multiple workers write the same page directory.
- Do not replace source-specific title, sticker, slogan, or decorative fonts with default UI fonts.
- Do not deliver without running finalize validation.
- Do not deliver without the final `fonts/` folder when fonts can be located locally.

## Final Reply

Report:

- final PPTX path
- source page count and output slide count
- hidden slide rule
- validation result
- OCR mode, especially if offline hints were used
- whether font optimization was applied
- fonts folder path
