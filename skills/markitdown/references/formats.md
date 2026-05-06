# MarkItDown Supported Formats Reference

## Complete Format Support Matrix

| Category | Format | Extension | Dependencies | Notes |
|----------|--------|-----------|--------------|-------|
| **Documents** |
| | PDF | .pdf | markitdown[pdf] | Preserves text, tables, basic structure |
| | Microsoft Word | .docx | markitdown[docx] | Full document structure (headings, lists, tables) |
| | Microsoft PowerPoint | .pptx | markitdown[pptx] | Slide content with slide breaks |
| | Microsoft Excel | .xlsx, .xls | markitdown[xlsx], markitdown[xls] | Tables converted to Markdown tables |
| | Outlook Email | .msg | markitdown[outlook] | Email body + attachments |
| **Data** |
| | CSV | .csv | Built-in | Table format preserved |
| | JSON | .json | Built-in | Pretty printed with structure |
| | XML | .xml | Built-in | Human-readable format |
| **Web** |
| | HTML | .html, .htm | Built-in | Extracts main content |
| **Images** |
| | JPEG | .jpg, .jpeg | Built-in | EXIF metadata extraction |
| | PNG | .png | Built-in | EXIF metadata extraction |
| | GIF | .gif | Built-in | EXIF metadata extraction |
| | BMP | .bmp | Built-in | Basic metadata |
| | TIFF | .tiff | Built-in | EXIF metadata extraction |
| **Audio** |
| | MP3 | .mp3 | markitdown[audio-transcription] | Speech-to-text transcription |
| | WAV | .wav | markitdown[audio-transcription] | Speech-to-text transcription |
| | M4A | .m4a | markitdown[audio-transcription] | Speech-to-text transcription |
| **Video** |
| | YouTube URLs | youtube.com/* | markitdown[youtube-transcription] | Extracts auto-generated captions |
| **E-books** |
| | EPUB | .epub | Built-in | Chapter structure preserved |
| **Archives** |
| | ZIP | .zip | Built-in | Iterates and converts contents |

## Advanced Features

### OCR (Optical Character Recognition)

Requires: `markitdown-ocr` plugin + OpenAI API key

- Extracts text from images embedded in PDF, DOCX, PPTX, XLSX
- Uses LLM Vision models (GPT-4V, GPT-4o, etc.)
- Best for scanned documents and image-heavy files

### Azure Document Intelligence

Requires: `markitdown[az-doc-intel]` + Azure subscription

- Enhanced PDF parsing with layout understanding
- Better table extraction and form recognition
- Handles complex document structures

### LLM Integration

Image description feature (PPTs, images):
- Requires `llm_client` and `llm_model` parameters
- Supports any OpenAI-compatible API
- Can generate alt-text and image descriptions

## Performance Considerations

| File Type | Typical Size Limit | Processing Time (est.) |
|-----------|-------------------|----------------------|
| Small PDF (<10 pages) | 50 MB | 2-5 seconds |
| Large PDF (100+ pages) | 200 MB | 30-60 seconds |
| Excel with complex tables | 100 MB | 5-15 seconds |
| Audio transcription (1 hour) | 500 MB | Real-time + API latency |
| Image OCR (per image) | 20 MB | 1-3 seconds per image |

## Common Use Cases

### 1. Academic Papers (PDF)
Best for: Extracting text for summarization, Q&A, citation extraction
Output preserves: Headings, paragraphs, basic tables

### 2. Business Reports (PPTX/PDF)
Best for: Converting slide decks to readable text
Output preserves: Slide breaks (as headings), bullet points, speaker notes

### 3. Data Analysis (XLSX/CSV)
Best for: Converting spreadsheets for LLM analysis
Output preserves: Table structures as Markdown tables

### 4. Meeting Transcriptions (MP3/YouTube)
Best for: Converting audio/video to text for analysis
Note: Quality depends on audio clarity and auto-generated captions

### 5. Scanned Documents (PDF with OCR)
Best for: Old books, handwritten notes, scanned forms
Requires: OCR plugin and API key

## Limitations

- Complex layouts (multi-column, sidebars) may not convert perfectly
- Image OCR requires external API and internet connection
- Password-protected files are not supported
- Some proprietary formats (Apple Pages, Keynote) not supported
- Very large files (>200MB) may cause memory issues

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chinese/Japanese characters missing | Ensure fonts are installed, try Azure Document Intelligence |
| Tables not aligning | Use CSV intermediate format |
| Slow PDF conversion | Use --pdf-engine flag with pdfplumber instead of pdfminer |
| Memory errors | Process large files in chunks or use streaming mode |