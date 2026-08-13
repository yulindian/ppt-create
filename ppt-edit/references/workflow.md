# Workflow

## Input Selection

Support `.pptx`, `.pdf`, single images, multiple images, and screenshots.

Prefer inputs in this order:

1. Use the original PPTX when available.
2. Use a same-name PDF if PPTX extraction, rendering, or page selection is unstable.
3. Use ordered images when no document source exists.

For trial conversions, extract the requested page range, usually the first 3 or 5 pages, and never modify the source file.

## Working Directory

Use a stable ASCII working directory when file paths contain Chinese characters, punctuation, or spaces that could break Python, PowerShell, or CLI tools.

Recommended layout:

```text
D:/codex/ppt_edit_work/project_name/
  input/
    source_full.pptx
    source_first3.pptx
  run/
```

Copy final artifacts back to the user's project delivery directory after validation.

## Prepare

Run:

```powershell
editppt prepare <input> --job-dir <run> --image-backend builtin-imagegen
```

Use `--image-backend builtin-imagegen` when the current agent runtime can call the built-in image tool. If not, use the lower-level CLI fallback contract.

After prepare, confirm these files exist:

```text
deck_manifest.json
page_jobs.json
notes_manifest.json
pages/page_NNN/source.png
pages/page_NNN/text_hints.json
pages/page_NNN/text_hints.png
pages/page_NNN/page_request.json
```

## OCR and Text Hints

OCR/image backends are allowed for user-requested conversions unless the user explicitly requests local-only or confidential processing.

Use PaddleOCR text hints when a token is configured. If no PaddleOCR token exists, continue with offline `builtin-ink`; do not stop unless the user requires OCR-grade text precision.

Offline hints provide text geometry and approximate size, not reliable text content. Page reconstructors must still read the source image and reconstruct visible text.

Mention offline OCR in the final reply.

