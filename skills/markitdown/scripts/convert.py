#!/usr/bin/env python3
"""
MarkItDown conversion script for agent use.
Converts various document formats to Markdown.

This script is designed to be called by Nora agent, which manages the LLM client.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, Any


def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    docintel_endpoint: Optional[str] = None,
    llm_client: Any = None,      # 由 agent 传入，已初始化
    llm_model: Optional[str] = None  # 由 agent 传入模型名称
) -> str:
    """
    Convert a file to Markdown using MarkItDown.
    
    Args:
        input_path: Path to input file or URL
        output_path: Path to output markdown file (optional)
        docintel_endpoint: Azure Document Intelligence endpoint
        llm_client: 由 Agent 传入的 OpenAI 兼容客户端（已初始化，包含 API key）
        llm_model: 由 Agent 传入的模型名称（如 qwen-vl-plus, gpt-4o 等）
    
    Returns:
        Converted markdown content as string
    """
    try:
        from markitdown import MarkItDown
    except ImportError:
        raise ImportError(
            "MarkItDown not installed. Run: pip install 'markitdown[all]'"
        )
    
    kwargs = {}
    
    if docintel_endpoint:
        kwargs["docintel_endpoint"] = docintel_endpoint
    
    # 如果 agent 传入了 llm_client，启用 OCR/图片描述
    if llm_client is not None:
        kwargs["enable_plugins"] = True
        kwargs["llm_client"] = llm_client
        # 只有当 llm_model 不为 None 时才传入，否则让 markitdown 自己决定
        if llm_model is not None:
            kwargs["llm_model"] = llm_model
    
    # Create converter
    md = MarkItDown(**kwargs)
    
    # Convert
    if input_path.startswith(("http://", "https://")):
        result = md.convert(input_path)
    else:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")
        result = md.convert(str(path))
    
    # Save to file if output path provided
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        print(f"Converted: {input_path} -> {output_path}", file=sys.stderr)
    
    return result.text_content


def main():
    """命令行入口（独立使用，不依赖 agent）"""
    parser = argparse.ArgumentParser(
        description="Convert documents to Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf
  %(prog)s presentation.pptx --output summary.md
  %(prog)s https://youtube.com/watch?v=... --output transcript.md

注意：OCR 功能需要在 agent 中调用，命令行版本不支持 OCR。
        """
    )
    
    parser.add_argument("input", help="Input file path or URL")
    parser.add_argument("-o", "--output", help="Output markdown file path (optional)")
    parser.add_argument("-d", "--docintel-endpoint", help="Azure Document Intelligence endpoint")
    
    args = parser.parse_args()
    
    try:
        content = convert_file(
            input_path=args.input,
            output_path=args.output,
            docintel_endpoint=args.docintel_endpoint,
            llm_client=None,  # 命令行模式不启用 OCR
        )
        
        if not args.output:
            print(content)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()