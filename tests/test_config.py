"""
Test Configuration for OnlyPans Recipe App
Custom test settings and utilities
"""

import os
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings


class OnlyPansTestCase(TestCase):
    """Base test case with common setup for OnlyPans tests"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with common data"""
        super().setUpClass()
        
        # Load test fixtures
        call_command('loaddata', 'users.json', verbosity=0)
        call_command('loaddata', 'ingredients.json', verbosity=0)
        call_command('loaddata', 'tags.json', verbosity=0)
        call_command('loaddata', 'recipes.json', verbosity=0)

    def setUp(self):
        """Set up individual test methods"""
        super().setUp()
        # Any per-test setup can go here


class TestDataMixin:
    """Mixin providing common test data creation methods"""
    
    def create_test_user(self, username='testuser', email='test@example.com'):
        """Create a test user with standard credentials"""
        from django.contrib.auth.models import User
        return User.objects.create_user(
            username=username,
            email=email,
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def create_test_recipe(self, author=None, title='Test Recipe'):
        """Create a test recipe with minimal required fields"""
        from recipes.models import Recipe
        
        if author is None:
            author = self.create_test_user()
        
        return Recipe.objects.create(
            title=title,
            description='A test recipe description',
            instructions='Test recipe instructions',
            author=author,
            prep_time=15,
            cook_time=30,
            servings=4
        )
    
    def create_test_tag(self, name='Test Tag', category='cuisine'):
        """Create a test tag"""
        from recipes.models import Tag
        return Tag.objects.create(name=name, category=category)
    
    def create_test_ingredient(self, name='Test Ingredient'):
        """Create a test ingredient"""
        from recipes.models import Ingredient
        return Ingredient.objects.create(name=name)


# Test settings overrides
if 'test' in os.sys.argv:
    # Use faster password hasher for tests
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    
    # Use in-memory database for faster tests
    if 'DATABASES' in dir(settings):
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    
    # Disable migrations for faster test database setup
    class DisableMigrations:
        def __contains__(self, item):
            return True
        def __getitem__(self, item):
            return None
    
    settings.MIGRATION_MODULES = DisableMigrations()
    
    # Disable static files during testing
    settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


def create_test_image():
    """Create a test image file for upload testing"""
    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image
    import io
    
    # Create a simple test image
    image = Image.new('RGB', (100, 100), color='red')
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=image_io.getvalue(),
        content_type='image/jpeg'
    )
