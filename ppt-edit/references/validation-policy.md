# Validation Policy

## Page Validation

Every page must have `validation.json` with top-level:

```json
{
  "passed": true
}
```

A page can be recorded only when:

- `validation.json.passed` is `true`
- `manifest.json` can independently build the page
- `page.pptx` is openable
- `preview.png` exists
- `split_assets_contact.png` exists
- all text, shapes, and images have valid coordinates
- all image assets have provenance
- there are no page contract violations

If a page fails, keep `passed=false`, record the concrete reason, and fix the root cause before resetting and redispatching. Never falsify validation.

## Final Validation

After all pages are recorded, run:

```powershell
editppt run finalize <run>
```

Final validation must confirm:

- the PPTX package is valid
- slide count equals `2 * source_page_count`
- even slides are hidden editable reconstruction pages
- odd slides are visible original-image pages
- all page manifests exist
- all page validations passed
- media relationships are complete
- notes mapping is correct when notes exist
- no warnings remain
- `fonts/` exists when fonts can be located locally

Do not deliver before finalize succeeds.

