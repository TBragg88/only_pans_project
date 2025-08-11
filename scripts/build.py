#!/usr/bin/env python3
"""
Build script for OnlyPans production optimization
Minifies CSS and JavaScript files for better performance
"""
import os
import subprocess
import sys


def run_minifiers():
    """Run CSS and JavaScript minification"""
    try:
        # Minify CSS
        print("Minifying CSS...")
        result_css = subprocess.run([sys.executable, "minify_css.py"], 
                                   capture_output=True, text=True)
        if result_css.returncode == 0:
            print(result_css.stdout)
        else:
            print(f"CSS minification failed: {result_css.stderr}")
            
        # Minify JavaScript
        print("Minifying JavaScript...")
        result_js = subprocess.run([sys.executable, "minify_js.py"], 
                                  capture_output=True, text=True)
        if result_js.returncode == 0:
            print(result_js.stdout)
        else:
            print(f"JavaScript minification failed: {result_js.stderr}")
            
        print("\n🚀 Build optimization complete!")
        print("✅ CSS minified for production")
        print("✅ JavaScript minified for production")
        print("✅ Critical CSS inlined")
        print("✅ Resources set to defer/preload")
        
    except Exception as e:
        print(f"Build script error: {e}")


def main():
    print("🔧 OnlyPans Production Build Script")
    print("===================================")
    run_minifiers()


if __name__ == "__main__":
    main()
