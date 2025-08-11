#!/usr/bin/env python3
"""
Maintenance script for OnlyPans Recipe App
Run this script to perform routine maintenance tasks
"""
import os


def minify_css():
    """Minify CSS files for production"""
    print("🔧 Minifying CSS...")
    # Minify CSS using Python
    minify_cmd = """
    python -c "
import re
with open('static/css/styles.css', 'r') as f:
    css = f.read()
css = re.sub(r'/\\*.*?\\*/', '', css, flags=re.DOTALL)
css = re.sub(r'\\s+', ' ', css)
css = re.sub(r';\\s*}', '}', css)
css = re.sub(r'{\\s*', '{', css)
css = re.sub(r';\\s*', ';', css)
with open('static/css/styles.min.css', 'w') as f:
    f.write(css.strip())
"
    """
    os.system(minify_cmd.strip())
    print("✅ CSS minified successfully")


def collect_static():
    """Collect static files for production"""
    print("📦 Collecting static files...")
    os.system("python manage.py collectstatic --noinput")
    print("✅ Static files collected")


def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    result = os.system("python manage.py test")
    if result == 0:
        print("✅ All tests passed")
    else:
        print("❌ Some tests failed")
    return result == 0


def check_migrations():
    """Check for pending migrations"""
    print("🔍 Checking migrations...")
    os.system("python manage.py makemigrations --dry-run --verbosity=1")
    os.system("python manage.py showmigrations")


def main():
    """Run maintenance tasks"""
    print("🚀 OnlyPans Maintenance Script")
    print("==============================")
    
    tasks = [
        ("Minify CSS", minify_css),
        ("Collect Static Files", collect_static),
        ("Run Tests", run_tests),
        ("Check Migrations", check_migrations),
    ]
    
    for task_name, task_func in tasks:
        print(f"\n📋 {task_name}")
        try:
            task_func()
        except Exception as e:
            print(f"❌ Error in {task_name}: {e}")
    
    print("\n🎉 Maintenance complete!")


if __name__ == "__main__":
    main()
