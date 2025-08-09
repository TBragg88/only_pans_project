"""
Form Tests for OnlyPans Recipe App
Tests for form validation, custom fields, and user input handling
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from recipes.forms import (
    RecipeForm, RecipeIngredientFormSet, RecipeStepFormSet
)
from recipes.models import Tag, Ingredient, Unit


class RecipeFormTest(TestCase):
    """Test RecipeForm validation and functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_recipe_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Test Recipe',
            'description': 'A delicious test recipe',
            'instructions': 'Mix ingredients and cook',
            'prep_time': 15,
            'cook_time': 30,
            'servings': 4,
            'difficulty': 'medium'
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_missing_required_fields(self):
        """Test form with missing required fields"""
        form_data = {
            'description': 'Missing title and other required fields'
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('prep_time', form.errors)
        self.assertIn('cook_time', form.errors)

    def test_recipe_form_invalid_time_values(self):
        """Test form with invalid time values"""
        form_data = {
            'title': 'Test Recipe',
            'instructions': 'Test instructions',
            'prep_time': -5,  # Negative time
            'cook_time': 0,   # Zero cook time
            'servings': 4
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prep_time', form.errors)

    def test_recipe_form_long_title(self):
        """Test form with excessively long title"""
        long_title = 'A' * 201  # Assuming 200 char limit
        form_data = {
            'title': long_title,
            'instructions': 'Test instructions',
            'servings': 4
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_recipe_form_with_tags(self):
        """Test form with tag selection"""
        tag1 = Tag.objects.create(name='Italian', tag_type='cuisine')
        tag2 = Tag.objects.create(name='Vegetarian', tag_type='dietary')
        
        form_data = {
            'title': 'Tagged Recipe',
            'prep_time': 10,
            'cook_time': 20,
            'servings': 4,
            'tags': [tag1.id, tag2.id]
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_image_upload(self):
        """Test form with image upload"""
        # Create a simple test image
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        form_data = {
            'title': 'Recipe with Image',
            'prep_time': 10,
            'cook_time': 20,
            'servings': 4
        }
        form = RecipeForm(data=form_data, files={'image': image})
        self.assertTrue(form.is_valid())


class RecipeIngredientFormSetTest(TestCase):
    """Test RecipeIngredientFormSet validation"""

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.unit = Unit.objects.create(name='cup', abbreviation='c')

    def test_ingredient_formset_valid(self):
        """Test valid ingredient formset"""
        formset_data = {
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '1',
            'ingredients-MAX_NUM_FORMS': '20',
            'ingredients-0-ingredient': self.ingredient.id,
            'ingredients-0-quantity': '2',
            'ingredients-0-unit': self.unit.id,
            'ingredients-1-ingredient': '',
            'ingredients-1-quantity': '',
            'ingredients-1-unit': ''
        }
        formset = RecipeIngredientFormSet(data=formset_data)
        self.assertTrue(formset.is_valid())

    def test_ingredient_formset_missing_quantity(self):
        """Test ingredient formset with missing quantity"""
        formset_data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-ingredient': self.ingredient.id,
            'ingredients-0-quantity': '',  # Missing quantity
            'ingredients-0-unit': self.unit.id
        }
        formset = RecipeIngredientFormSet(data=formset_data)
        self.assertFalse(formset.is_valid())

    def test_ingredient_formset_negative_quantity(self):
        """Test ingredient formset with negative quantity - should be valid at form level"""
        formset_data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-ingredient': self.ingredient.id,
            'ingredients-0-quantity': '-1',  # Negative quantity
            'ingredients-0-unit': self.unit.id
        }
        formset = RecipeIngredientFormSet(data=formset_data)
        # The formset allows negative quantities at the form level
        self.assertTrue(formset.is_valid())

    def test_ingredient_formset_duplicate_ingredients(self):
        """Test ingredient formset with duplicate ingredients"""
        formset_data = {
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-ingredient': self.ingredient.id,
            'ingredients-0-quantity': '1',
            'ingredients-0-unit': self.unit.id,
            'ingredients-1-ingredient': self.ingredient.id,  # Duplicate
            'ingredients-1-quantity': '2',
            'ingredients-1-unit': self.unit.id
        }
        formset = RecipeIngredientFormSet(data=formset_data)
        # This might be valid depending on business logic
        # You can allow duplicates or add custom validation
        self.assertTrue(formset.is_valid())


class RecipeStepFormSetTest(TestCase):
    """Test RecipeStepFormSet validation"""

    def test_step_formset_valid(self):
        """Test valid step formset"""
        formset_data = {
            'steps-TOTAL_FORMS': '3',
            'steps-INITIAL_FORMS': '0',
            'steps-0-instruction': 'Prepare ingredients',
            'steps-0-order': '1',
            'steps-1-instruction': 'Mix ingredients',
            'steps-1-order': '2',
            'steps-2-instruction': 'Cook until done',
            'steps-2-order': '3'
        }
        formset = RecipeStepFormSet(data=formset_data)
        self.assertTrue(formset.is_valid())

    def test_step_formset_empty_instruction(self):
        """Test step formset with empty instruction"""
        formset_data = {
            'steps-TOTAL_FORMS': '1',
            'steps-INITIAL_FORMS': '0',
            'steps-0-instruction': '',  # Empty instruction
            'steps-0-order': '1'
        }
        formset = RecipeStepFormSet(data=formset_data)
        self.assertFalse(formset.is_valid())

    def test_step_formset_valid_steps(self):
        """Test step formset with valid steps"""
        formset_data = {
            'steps-TOTAL_FORMS': '2',
            'steps-INITIAL_FORMS': '0',
            'steps-0-instruction': 'First step',
            'steps-1-instruction': 'Second step'
        }
        formset = RecipeStepFormSet(data=formset_data)
        self.assertTrue(formset.is_valid())


class FormIntegrationTest(TestCase):
    """Test form integration and complex scenarios"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.ingredient = Ingredient.objects.create(name='Flour')
        self.unit = Unit.objects.create(name='cup', abbreviation='c')
        self.tag = Tag.objects.create(name='Dessert', tag_type='meal_type')

    def test_complete_recipe_form_submission(self):
        """Test complete recipe creation with all formsets"""
        # Main recipe form data
        recipe_data = {
            'title': 'Complete Test Recipe',
            'description': 'A complete test recipe with all components',
            'instructions': 'Follow the steps below',
            'prep_time': 20,
            'cook_time': 45,
            'servings': 6,
            'tags': [self.tag.id]
        }
        
        # Ingredient formset data
        ingredient_data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-ingredient': self.ingredient.id,
            'ingredients-0-quantity': '2',
            'ingredients-0-unit': self.unit.id
        }
        
        # Step formset data
        step_data = {
            'steps-TOTAL_FORMS': '2',
            'steps-INITIAL_FORMS': '0',
            'steps-0-instruction': 'Mix dry ingredients',
            'steps-0-order': '1',
            'steps-1-instruction': 'Add wet ingredients and stir',
            'steps-1-order': '2'
        }
        
        # Combine all form data
        combined_data = {**recipe_data, **ingredient_data, **step_data}
        
        # Test main form
        recipe_form = RecipeForm(data=combined_data)
        self.assertTrue(recipe_form.is_valid(), f"Recipe form errors: {recipe_form.errors}")
        
        # Test formsets
        ingredient_formset = RecipeIngredientFormSet(data=combined_data)
        self.assertTrue(ingredient_formset.is_valid(), 
                       f"Ingredient formset errors: {ingredient_formset.errors}")
        
        step_formset = RecipeStepFormSet(data=combined_data)
        self.assertTrue(step_formset.is_valid(), 
                       f"Step formset errors: {step_formset.errors}")

    def test_form_validation_with_missing_components(self):
        """Test form validation when some components are missing"""
        # Recipe with no ingredients or steps
        recipe_data = {
            'title': 'Incomplete Recipe',
            'prep_time': 5,
            'cook_time': 10,
            'servings': 2
        }
        
        empty_ingredient_data = {
            'ingredients-TOTAL_FORMS': '0',
            'ingredients-INITIAL_FORMS': '0'
        }
        
        empty_step_data = {
            'steps-TOTAL_FORMS': '0',
            'steps-INITIAL_FORMS': '0'
        }
        
        combined_data = {**recipe_data, **empty_ingredient_data, **empty_step_data}
        
        # Main form should still be valid
        recipe_form = RecipeForm(data=combined_data)
        self.assertTrue(recipe_form.is_valid())
        
        # Empty formsets might be valid depending on your requirements
        ingredient_formset = RecipeIngredientFormSet(data=combined_data)
        step_formset = RecipeStepFormSet(data=combined_data)
        
        # These assertions depend on your business logic
        # You might want to require at least one ingredient or step
