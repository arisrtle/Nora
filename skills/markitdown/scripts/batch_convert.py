#!/usr/bin/env python3
"""
Batch conversion script for MarkItDown skill.
Converts all supported files in a directory to Markdown.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Supported file extensions
SUPPORTED_EXTENSIONS: Set[str] = {
    # Documents
    '.pdf', '.docx', '.pptx', '.xlsx', '.xls',
    # Data
    '.csv', '.json', '.xml',
    # Web
    '.html', '.htm',
    # Images (basic, without OCR)
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
    # Text
    '.txt', '.md',
    # Archives
    '.zip',
    # E-books
    '.epub',
}


def is_supported_file(file_path: Path) -> bool:
    """Check if file extension is supported."""
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def convert_single_file(
    input_path: Path,
    output_dir: Path,
    relative_root: Path,
    use_ocr: bool = False,
    api_key: str = None
) -> tuple[Path, bool, str]:
    """
    Convert a single file, maintaining directory structure.
    
    Returns:
        Tuple of (input_path, success, error_message)
    """
    try:
        # Import convert function
        sys.path.insert(0, str(Path(__file__).parent))
        from convert import convert_file
        
        # Calculate output path maintaining relative structure
        rel_path = input_path.relative_to(relative_root)
        output_path = output_dir / rel_path.with_suffix('.md')
        
        # Create output directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert file
        convert_file(
            input_path=str(input_path),
            output_path=str(output_path),
            use_ocr=use_ocr,
            api_key=api_key
        )
        
        return (input_path, True, "")
        
    except Exception as e:
        return (input_path, False, str(e))


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert documents in a directory to Markdown"
    )
    
    parser.add_argument(
        "input_dir",
        help="Input directory containing documents"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for markdown files"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process subdirectories recursively"
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="Enable OCR for images (requires API key)"
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )
    parser.add_argument(
        "-j", "--jobs",
        type=int,
        default=4,
        help="Number of parallel conversions (default: 4)"
    )
    
    args = parser.parse_args()
    
    import os
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    
    if args.ocr and not api_key:
        print(
            "Warning: OCR requested but no API key provided.",
            file=sys.stderr
        )
    
    # Collect files
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find all supported files
    files_to_convert: List[Path] = []
    
    if args.recursive:
        for ext in SUPPORTED_EXTENSIONS:
            files_to_convert.extend(input_dir.rglob(f"*{ext}"))
    else:
        for ext in SUPPORTED_EXTENSIONS:
            files_to_convert.extend(input_dir.glob(f"*{ext}"))
    
    # Remove duplicates and sort
    files_to_convert = sorted(set(files_to_convert))
    
    if not files_to_convert:
        print("No supported files found.", file=sys.stderr)
        sys.exit(0)
    
    print(f"Found {len(files_to_convert)} files to convert", file=sys.stderr)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert files in parallel
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                convert_single_file,
                file_path,
                output_dir,
                input_dir,
                args.ocr,
                api_key
            ): file_path
            for file_path in files_to_convert
        }
        
        for future in as_completed(futures):
            input_path, success, error = future.result()
            if success:
                successful += 1
                print(f"✓ {input_path}", file=sys.stderr)
            else:
                failed += 1
                print(f"✗ {input_path}: {error}", file=sys.stderr)
    
    elapsed = time.time() - start_time
    
    # Summary
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Conversion complete!", file=sys.stderr)
    print(f"  Successful: {successful}", file=sys.stderr)
    print(f"  Failed: {failed}", file=sys.stderr)
    print(f"  Time: {elapsed:.2f}s", file=sys.stderr)
    print(f"  Output directory: {output_dir}", file=sys.stderr)
    
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()