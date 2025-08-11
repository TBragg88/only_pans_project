#!/usr/bin/env python3
"""
Simple JavaScript minifier to reduce file size for performance optimization
"""
import re
import os


def minify_js(js_content):
    """Basic JavaScript minification"""
    # Remove single-line comments (but preserve URLs)
    js_content = re.sub(r'//(?![^\n]*:)[^\n]*\n', '\n', js_content)
    
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # Remove extra whitespace but preserve line breaks for better debugging
    js_content = re.sub(r'[ \t]+', ' ', js_content)
    
    # Remove blank lines
    js_content = re.sub(r'\n\s*\n', '\n', js_content)
    
    # Remove leading/trailing whitespace from lines
    lines = [line.strip() for line in js_content.split('\n')]
    js_content = '\n'.join(lines)
    
    return js_content


def main():
    js_file = 'static/js/app.js'
    minified_file = 'static/js/app.min.js'
    
    if os.path.exists(js_file):
        with open(js_file, 'r', encoding='utf-8') as f:
            original_js = f.read()
        
        minified_js = minify_js(original_js)
        
        with open(minified_file, 'w', encoding='utf-8') as f:
            f.write(minified_js)
        
        original_size = len(original_js)
        minified_size = len(minified_js)
        reduction = ((original_size - minified_size) / original_size) * 100
        
        print(f"JavaScript minification complete!")
        print(f"Original size: {original_size:,} bytes")
        print(f"Minified size: {minified_size:,} bytes")
        print(f"Reduction: {reduction:.1f}%")
    else:
        print(f"JavaScript file not found: {js_file}")


if __name__ == "__main__":
    main()
