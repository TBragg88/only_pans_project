"""
Run all tests for OnlyPans Recipe App
Usage: python manage.py test tests.run_all_tests
"""

import sys
from django.test.runner import DiscoverRunner
from django.core.management import execute_from_command_line


class OnlyPansTestRunner(DiscoverRunner):
    """Custom test runner for OnlyPans with additional reporting"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = {
            'models': [],
            'views': [],
            'forms': [],
            'integration': []
        }
    
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """Run tests with custom reporting"""
        print("🧪 Starting OnlyPans Recipe App Test Suite")
        print("=" * 50)
        
        result = super().run_tests(test_labels, extra_tests, **kwargs)
        
        print("\n" + "=" * 50)
        print("✅ Test Suite Complete")
        
        return result


def run_all_tests():
    """Run all tests with coverage reporting"""
    
    test_commands = [
        ['test', 'tests.test_models', '--verbosity=2'],
        ['test', 'tests.test_views', '--verbosity=2'],
        ['test', 'tests.test_forms', '--verbosity=2'],
        ['test', 'tests.test_integration', '--verbosity=2'],
    ]
    
    print("🚀 Running OnlyPans Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    for i, cmd in enumerate(test_commands, 1):
        test_type = cmd[1].split('.')[-1].replace('test_', '').title()
        print(f"\n📋 Running {test_type} Tests ({i}/{len(test_commands)})")
        print("-" * 30)
        
        try:
            execute_from_command_line(['manage.py'] + cmd)
        except SystemExit as e:
            if e.code != 0:
                all_passed = False
                print(f"❌ {test_type} tests failed")
            else:
                print(f"✅ {test_type} tests passed")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed successfully!")
    else:
        print("⚠️  Some tests failed. Check output above.")
    print("=" * 50)
    
    return all_passed


def run_quick_tests():
    """Run a quick subset of tests for rapid development"""
    
    quick_tests = [
        'tests.test_models.RecipeModelTest.test_recipe_creation',
        'tests.test_views.RecipeViewTest.test_recipe_list_view',
        'tests.test_forms.RecipeFormTest.test_recipe_form_valid_data',
    ]
    
    print("⚡ Running Quick Test Suite")
    print("=" * 30)
    
    for test in quick_tests:
        try:
            execute_from_command_line(['manage.py', 'test', test, '--verbosity=1'])
            print(f"✅ {test.split('.')[-1]} passed")
        except SystemExit as e:
            if e.code != 0:
                print(f"❌ {test.split('.')[-1]} failed")
                return False
    
    print("🎉 Quick tests completed successfully!")
    return True


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'quick':
        run_quick_tests()
    else:
        run_all_tests()
