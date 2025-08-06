# OnlyPans Testing Suite

This directory contains all test files for the OnlyPans project.

## Structure

```
tests/
├── __init__.py                 # Makes tests a Python package
├── test_models.py              # Model testing (Recipe, User, etc.)
├── test_views.py               # View testing (authentication, CRUD)
├── test_forms.py               # Form validation testing
├── test_utils.py               # Utility function testing
├── test_integration.py         # Integration testing
├── test_selenium.py            # End-to-end browser testing
└── fixtures/                   # Test data fixtures
    └── test_data.json
```

## Running Tests

```bash
# Run all tests
python manage.py test tests

# Run specific test file
python manage.py test tests.test_models

# Run with coverage
coverage run --source='.' manage.py test tests
coverage report
coverage html

# Run with verbose output
python manage.py test tests --verbosity=2
```

## Test Categories

-   **Unit Tests**: Individual component testing
-   **Integration Tests**: Component interaction testing
-   **Functional Tests**: User workflow testing
-   **Selenium Tests**: Browser automation testing
