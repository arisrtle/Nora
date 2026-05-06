---
name: markitdown
description: Convert various document formats (PDF, Word, Excel, PowerPoint, images, audio, HTML, YouTube URLs, EPUB) to Markdown for LLM processing. Use this skill when users need to extract text content from documents for analysis, summarization, or when they ask to convert files to Markdown format.
license: MIT
version: 1.0.0
author: Nora Agent Skills
tags:
  - document-conversion
  - markdown
  - ocr
  - pdf-processing
  - office-conversion
---

# MarkItDown Skill

## Overview

This skill provides document-to-Markdown conversion capabilities using MarkItDown library. It supports converting a wide range of file formats including PDF documents, Microsoft Office files (Word, Excel, PowerPoint), images (with EXIF metadata and OCR), audio files (transcription), web pages (HTML), YouTube videos, EPUB ebooks, and more.

## When to Use This Skill

Use this skill when:
- User asks to read content from PDF, Word, Excel, or PowerPoint files
- User wants to convert documents to Markdown format
- User needs to extract text from images or scanned documents (requires OCR plugin)
- User provides a YouTube URL and wants to get transcript/subtitles
- User mentions extracting text from audio files
- User shares a document and asks for summary or analysis
- User asks "what's in this file?" for supported formats

## Capabilities

### Primary Functions

1. **Single File Conversion**: Convert any supported file to Markdown
2. **Batch Conversion**: Convert multiple files in a directory
3. **OCR Enhancement**: Extract text from images within documents (requires OpenAI API key)

### Supported Formats

| Category | Formats | Notes |
|----------|---------|-------|
| Documents | PDF, DOCX, PPTX, XLSX | Full structure preservation |
| Data | CSV, JSON, XML | Table-to-Markdown conversion |
| Web | HTML | Extracts main content |
| Images | JPG, PNG, GIF, BMP | EXIF metadata + optional LLM OCR |
| Audio | MP3, WAV, M4A | Speech transcription |
| Video | YouTube URLs | Extract video transcripts |
| E-books | EPUB | Chapter structure preserved |
| Archives | ZIP | Iterates over contents |

## Usage

### 在 Agent 中调用此 Skill

Agent 应使用 shell 命令调用此 skill：

```bash
# 基础转换（不需要 API key）
python skills/markitdown/scripts/convert.py <input_file> -o <output_file>

# 需要 OCR 时，Agent 通过环境变量传递 API key
env OPENAI_API_KEY=<agent的api_key> python skills/markitdown/scripts/convert.py <input_file> --ocr -o <output_file>
```

### Batch Conversion

```bash
# Convert all supported files in directory
python scripts/batch_convert.py /path/to/documents --output /path/to/markdown

# Recursive batch conversion
python scripts/batch_convert.py /path/to/documents --recursive --output /path/to/markdown
```

## Security Considerations
⚠️ Important: This skill performs I/O with the privileges of the current process. When processing untrusted documents:

Always validate file paths before conversion

Consider using convert_local() instead of convert() for maximum safety

Sanitize inputs in untrusted environments

Examples
Example 1: Convert PDF to Markdown
User: "Can you read this PDF and tell me what it's about? [UPLOAD document.pdf]"

Action: Agent uses this skill to convert the file

```bash
python scripts/convert.py document.pdf -o document.md
```

Then reads the resulting markdown file to answer.

Example 2: Extract content from Excel
User: "I need to analyze this Excel spreadsheet [UPLOAD data.xlsx]"

Action: Convert Excel to Markdown tables

```bash
python scripts/convert.py data.xlsx -o data.md
```

Then processes the markdown tables for analysis.

Example 3: YouTube transcript extraction
User: "Get me the transcript from this YouTube video: https://youtu.be/..."

Action:

```bash
python scripts/convert.py "https://youtu.com/..." -o transcript.md
```

Example 4: Process scanned document with OCR
User: "This PDF is a scan, can you extract the text? [UPLOAD scan.pdf]"

Action: Enable OCR with OpenAI API

```bash
python scripts/convert.py scan.pdf --ocr --api-key $OPENAI_API_KEY -o extracted.md
```

Then reads extracted.md for the text content.

Dependencies
This skill requires:

markitdown[all] - Complete MarkItDown installation

markitdown-ocr - For OCR capabilities (optional)

openai - For LLM-based OCR (if OCR needed)

Verify installation:

```bash
markitdown --version
pip list | findstr markitdown
```

Configuration
Environment Variables
Variable	Purpose	Required For
OPENAI_API_KEY	LLM-based OCR and image descriptions	OCR features
AZURE_DOCINTEL_ENDPOINT	Azure Document Intelligence endpoint	Enhanced PDF parsing
AZURE_DOCINTEL_KEY	Azure Document Intelligence key	Enhanced PDF parsing
Agent Configuration
Add to config.yaml:

```yaml
skills:
  markitdown:
    enabled: true
    ocr_enabled: false  # Set true if OpenAI API key available
    max_file_size_mb: 100
    temp_dir: uploads/markitdown_temp
```

Error Handling
Common errors and solutions:

Error	Solution
Command not found: markitdown	Install markitdown or add to PATH
No module named 'markitdown'	Run pip install 'markitdown[all]'
OCR requires API key	Set OPENAI_API_KEY environment variable
Unsupported file format	Check formats.md for supported types
Notes
Large files (>50MB) may take significant time to process

Audio transcriptions and OCR features require network connection

Some features (Azure Document Intelligence) require paid service subscription

The skill preserves document structure including headings, lists, and tables as Markdown

Output is optimized for LLM consumption, not for human-readable formatting

References
MarkItDown GitHub Repository

AgentSkills.io Specification

Supported Formats Reference

