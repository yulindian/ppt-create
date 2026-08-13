# Delivery Format

## Paired Slides

For each source page, deliver:

1. Visible original-image slide.
2. Hidden editable reconstruction slide.

For N source pages, the deck must contain `2N` slides. Slides `2, 4, 6, ...` must be hidden.

Speaker notes, when present, belong on the visible original-image slide for the corresponding source page.

## Delivery Directory

Recommended trial directory:

```text
project-name-first3-editable-sample/
  project-name_first3_editable_sample.pptx
  validation.json
  fonts/
```

Recommended full conversion directory:

```text
project-name-editable/
  project-name_editable.pptx
  validation.json
  fonts/
```

If the user works in Chinese project directories, final artifact filenames may use Chinese. Keep temporary run directories ASCII when needed.

## Final Reply Template

Report concise facts:

```text
已完成可编辑 PPT 转换。交付文件采用“原图页 + 隐藏可编辑页”的结构：奇数页为原稿图片，偶数页为对应可编辑重建页并已隐藏。验证通过，输出页数为原稿页数的 2 倍，无页面验证失败。字体文件已随附在最终输出目录的 fonts 文件夹中。
```

Also include:

- final PPTX path
- source page count
- output slide count
- hidden slide rule
- validation result
- OCR mode
- font optimization summary
- fonts folder path

