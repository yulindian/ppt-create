# Parallel Dispatch

## Rule

Process multi-page runs in parallel whenever possible. Each page is independent; each worker owns exactly one `pages/page_NNN/` directory.

The parent agent owns shared run state and user communication. Page workers own page-local reconstruction artifacts only.

## Parent Flow

Call:

```powershell
editppt run next <run> --json
```

When `stage=dispatch_pages`, for each suggested page:

```powershell
python <image-to-editable-ppt-skill-root>/scripts/build-page-worker-prompt.py <run> --page page_NNN --out <absolute-page-dir>/worker-prompt.md
```

Spawn one page worker per page up to `page_jobs.json.max_concurrent_pages`, then record the dispatch:

```powershell
editppt run dispatch <run> --page page_NNN --agent-id <worker-id> --prompt-file <absolute-page-dir>/worker-prompt.md
```

When a worker completes, record the page:

```powershell
editppt run record <run> --page page_NNN --agent-id <worker-id>
```

## Worker Requirements

Each worker must read its generated `worker-prompt.md` and produce:

```text
manifest.json
imagegen-jobs.json
page.pptx
preview.png
split_assets_contact.png
validation.json
page_result.json
```

Each worker must use `editppt page build`, `editppt page contact-sheet`, and `editppt page validate`.

## Concurrency Rules

- Use `page_jobs.json.max_concurrent_pages` as the concurrency limit.
- Default concurrency is acceptable unless pages are very complex or image backend load is high.
- Do not reset or replace an active worker because it is slow.
- Do not dispatch the same page twice while an active lease exists.
- Do not let different workers write the same page directory.
- Do not have the parent agent rebuild multiple pages locally to bypass workers.

