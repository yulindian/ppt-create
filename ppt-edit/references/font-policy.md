# Font Policy

## Principle

Choose fonts from both the user's stated style requirements and the source deck's visual typography. Never hard-code a fixed template font set for all decks.

Priority:

1. User-specified font or style.
2. Source typography personality.
3. Closest locally available font.
4. Cross-page consistency for the same text level.

## Font Style Map

Create or audit a `font_style_map` for:

- main titles
- subtitles
- body text
- labels and stickers
- English text
- special emphasis text

Record the source personality and selected editable PPT treatment in page manifests or quality records.

## Visual Matching Dimensions

Consider:

- rounded
- handwritten
- cartoon
- bold display
- chalkboard or chalk-like
- brush or calligraphy
- serif or sans serif
- rounded English
- business clean
- children's picture-book style

## Substitution

If a user-specified font exists locally, use it. If not, choose the closest local visual substitute and record the substitution in `font_manifest.json` or the page quality record.

Do not replace decorative source typography with `Microsoft YaHei`, `Microsoft YaHei UI`, Arial, or other default UI fonts unless the source level is also plain UI/sans.

## Bundling

The final output folder must include `fonts/`.

Copy every actually used and locally resolvable `.ttf`, `.ttc`, or `.otf` font file. Generate:

```text
fonts/font_manifest.json
fonts/README.txt
```

The final reply must mention the fonts folder.

