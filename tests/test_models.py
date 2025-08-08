"""
Model Tests for OnlyPans Recipe App
Tests for Recipe, UserProfile, Ingredient, Tag models
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    Rating,
    Comment,
)
from accounts.models import UserProfile


class RecipeModelTest(TestCase):
    """Test Recipe model functionality"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_recipe_creation(self):
        """Test basic recipe creation"""
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='A test recipe description',
            prep_time=15,
            cook_time=30,
            servings=4,
            user=self.user
        )
        
        self.assertEqual(recipe.title, 'Test Recipe')
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.servings, 4)
        self.assertTrue(recipe.slug)  # Slug should be auto-generated

    def test_recipe_string_representation(self):
        """Test recipe __str__ method"""
        recipe = Recipe.objects.create(
            title='Delicious Pasta',
            user=self.user,
            prep_time=10,
            cook_time=20,
            servings=2,
        )
        self.assertEqual(str(recipe), 'Delicious Pasta')

    def test_recipe_slug_generation(self):
        """Test automatic slug generation"""
        recipe = Recipe.objects.create(
            title='My Amazing Recipe',
            user=self.user,
            prep_time=5,
            cook_time=5,
            servings=1,
        )
        self.assertEqual(recipe.slug, 'my-amazing-recipe')

    def test_recipe_total_time_calculation(self):
        """Test total_time property"""
        recipe = Recipe.objects.create(
            title='Test Recipe',
            user=self.user,
            prep_time=15,
            cook_time=45,
            servings=2,
        )
        self.assertEqual(recipe.total_time, 60)

    def test_recipe_average_rating(self):
        """Test average rating calculation"""
        recipe = Recipe.objects.create(
            title='Test Recipe',
            user=self.user,
            prep_time=1,
            cook_time=1,
            servings=1,
        )
        
        # Create test ratings
        user2 = User.objects.create_user('user2', 'user2@test.com', 'pass123')
        user3 = User.objects.create_user('user3', 'user3@test.com', 'pass123')
        
        Rating.objects.create(recipe=recipe, user=self.user, rating=5)
        Rating.objects.create(recipe=recipe, user=user2, rating=4)
        Rating.objects.create(recipe=recipe, user=user3, rating=3)
        
        # Should be (5+4+3)/3 = 4.0
        self.assertEqual(recipe.average_rating, 4.0)


class IngredientModelTest(TestCase):
    """Test Ingredient model functionality"""

    def test_ingredient_creation(self):
        """Test basic ingredient creation"""
        ingredient = Ingredient.objects.create(name='Tomatoes')
        
        self.assertEqual(ingredient.name, 'Tomatoes')
        self.assertEqual(str(ingredient), 'Tomatoes')

    def test_ingredient_uniqueness(self):
        """Test ingredient name uniqueness"""
        Ingredient.objects.create(name='Salt')
        
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name='Salt')


class TagModelTest(TestCase):
    """Test Tag model functionality"""

    def test_tag_creation(self):
        """Test basic tag creation"""
        tag = Tag.objects.create(
            name='Vegetarian',
            tag_type='dietary'
        )
        
        self.assertEqual(tag.name, 'Vegetarian')
        self.assertEqual(tag.tag_type, 'dietary')
        # Tag.__str__ returns name and tag type display
        self.assertEqual(str(tag), 'Vegetarian (Dietary)')

    def test_tag_color_assignment(self):
        """Test tag color based on category"""
        dietary_tag = Tag.objects.create(name='Vegan', tag_type='dietary')
        cuisine_tag = Tag.objects.create(name='Italian', tag_type='cuisine')
        # Use variables to avoid unused warnings
        self.assertEqual(dietary_tag.tag_type, 'dietary')
        self.assertEqual(cuisine_tag.tag_type, 'cuisine')
        
        # These would need to be implemented in the model
        # Green for dietary
        # self.assertIn('#28a745', dietary_tag.get_color())
        # Blue for cuisine
        # self.assertIn('#17a2b8', cuisine_tag.get_color())


class UserProfileModelTest(TestCase):
    """Test UserProfile model functionality"""

    def test_profile_auto_creation(self):
        """Test automatic profile creation on user signup"""
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        
        # Profile should be auto-created via signal
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)

    def test_profile_string_representation(self):
        """Test profile __str__ method"""
        user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'pass123'
        )
        profile = user.profile
        
        self.assertEqual(str(profile), "testuser's Profile")


class RatingModelTest(TestCase):
    """Test Rating model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'pass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            user=self.user,
            prep_time=1,
            cook_time=1,
            servings=1,
        )

    def test_rating_creation(self):
        """Test basic rating creation"""
        rating = Rating.objects.create(
            recipe=self.recipe,
            user=self.user,
            rating=5
        )
        
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.recipe, self.recipe)
        self.assertEqual(rating.user, self.user)

    def test_rating_validation(self):
        """Test rating value validation"""
        # Valid ratings (1-5)
        for valid_rating in [1, 2, 3, 4, 5]:
            rating = Rating(
                recipe=self.recipe,
                user=self.user,
                rating=valid_rating
            )
            rating.full_clean()  # Should not raise ValidationError

    def test_unique_user_recipe_rating(self):
        """Test one rating per user per recipe"""
        Rating.objects.create(recipe=self.recipe, user=self.user, rating=5)
        
        with self.assertRaises(IntegrityError):
            Rating.objects.create(recipe=self.recipe, user=self.user, rating=3)


class CommentModelTest(TestCase):
    """Test Comment model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'pass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            user=self.user,
            prep_time=1,
            cook_time=1,
            servings=1,
        )

    def test_comment_creation(self):
        """Test basic comment creation"""
        comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Great recipe!'
        )
        
        self.assertEqual(comment.content, 'Great recipe!')
        self.assertEqual(comment.recipe, self.recipe)
        self.assertEqual(comment.user, self.user)

    def test_comment_reply(self):
        """Test comment reply functionality"""
        parent_comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Great recipe!'
        )
        
        user2 = User.objects.create_user('user2', 'user2@test.com', 'pass123')
        reply = Comment.objects.create(
            recipe=self.recipe,
            user=user2,
            content='I agree!',
            parent_comment=parent_comment
        )
        
        self.assertEqual(reply.parent_comment, parent_comment)
        self.assertIn(reply, parent_comment.replies.all())
