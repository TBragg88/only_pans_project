#!/usr/bin/env python3
"""
Simple CSS minifier to reduce file size for performance optimization
"""
import re
import os

def minify_css(css_content):
    """Basic CSS minification"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove extra whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Remove space around certain characters
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    
    # Remove trailing semicolons before closing braces
    css_content = re.sub(r';\s*}', '}', css_content)
    
    # Remove leading/trailing whitespace
    css_content = css_content.strip()
    
    return css_content

def main():
    css_file = 'static/css/styles.css'
    minified_file = 'static/css/styles.min.css'
    
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            original_css = f.read()
        
        minified_css = minify_css(original_css)
        
        with open(minified_file, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        original_size = len(original_css)
        minified_size = len(minified_css)
        reduction = ((original_size - minified_size) / original_size) * 100
        
        print(f"CSS minification complete!")
        print(f"Original size: {original_size:,} bytes")
        print(f"Minified size: {minified_size:,} bytes")
        print(f"Reduction: {reduction:.1f}%")
    else:
        print(f"CSS file not found: {css_file}")

if __name__ == "__main__":
    main()
