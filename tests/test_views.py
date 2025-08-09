"""
View Tests for OnlyPans Recipe App
Tests for authentication, recipe CRUD, user interactions
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from recipes.models import Recipe, Tag, Ingredient


class AuthenticationViewTest(TestCase):
    """Test user authentication views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_view_get(self):
        """Test login page loads correctly"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_login_view_post_valid(self):
        """Test valid login submission"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        """Test invalid login submission"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')

    def test_register_view_get(self):
        """Test registration page loads correctly"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_view_post_valid(self):
        """Test valid registration submission"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after register
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_view(self):
        """Test user logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)


class RecipeViewTest(TestCase):
    """Test recipe-related views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='A test recipe',
            user=self.user,
            prep_time=15,
            cook_time=30,
            servings=4
        )
        # Minimal step so detail page shows instructions
        from recipes.models import RecipeStep
        RecipeStep.objects.create(recipe=self.recipe, step_number=1, instruction='Test instructions')

    def test_recipe_list_view(self):
        """Test recipe list page"""
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_recipe_detail_view(self):
        """Test recipe detail page"""
        response = self.client.get(
            reverse('recipes:recipe_detail', args=[self.recipe.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')
        self.assertContains(response, 'Test instructions')

    def test_recipe_create_view_authenticated(self):
        """Test recipe creation by authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipes:recipe_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Recipe')

    def test_recipe_create_view_unauthenticated(self):
        """Test recipe creation redirects for unauthenticated user"""
        response = self.client.get(reverse('recipes:recipe_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_recipe_create_post(self):
        """Test recipe creation form submission"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create test ingredients and tags
        ingredient = Ingredient.objects.create(name='Test Ingredient')
        tag = Tag.objects.create(name='Test Tag', tag_type='cuisine')
        
        response = self.client.post(reverse('recipes:recipe_create'), {
            'title': 'New Test Recipe',
            'description': 'A new test recipe',
            # Steps provided via formset
            'prep_time': 20,
            'cook_time': 40,
            'servings': 6,
            'tags': [tag.id],
            'ingredients-0-ingredient': ingredient.id,
            'ingredients-0-quantity': '1',
            'ingredients-0-unit': '',
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'steps-0-instruction': 'Step 1',
            'steps-TOTAL_FORMS': '1',
            'steps-INITIAL_FORMS': '0'
        })
        
        self.assertTrue(
            Recipe.objects.filter(title='New Test Recipe').exists()
        )

    def test_recipe_edit_view_owner(self):
        """Test recipe editing by owner"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('recipes:recipe_edit', args=[self.recipe.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Recipe')

    def test_recipe_edit_view_non_owner(self):
        """Test recipe editing by non-owner returns 403"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(
            reverse('recipes:recipe_edit', args=[self.recipe.slug])
        )
        self.assertEqual(response.status_code, 403)

    def test_recipe_delete_view(self):
        """Test recipe deletion by owner"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('recipes:recipe_delete', args=[self.recipe.slug])
        )
        self.assertEqual(response.status_code, 302)  # Redirect after delete
        self.assertFalse(
            Recipe.objects.filter(slug=self.recipe.slug).exists()
        )


class SearchAndFilterTest(TestCase):
    """Test search and filtering functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test recipes with different attributes
        self.pasta_recipe = Recipe.objects.create(
            title='Italian Pasta',
            description='Delicious pasta dish',
            user=self.user,
            prep_time=5,
            cook_time=10,
            servings=2,
        )
        from recipes.models import RecipeStep
        RecipeStep.objects.create(recipe=self.pasta_recipe, step_number=1, instruction='Cook pasta')
        
        self.salad_recipe = Recipe.objects.create(
            title='Fresh Salad',
            description='Healthy green salad',
            user=self.user,
            prep_time=5,
            cook_time=0,
            servings=2,
        )
        RecipeStep.objects.create(recipe=self.salad_recipe, step_number=1, instruction='Mix vegetables')

    def test_recipe_search(self):
        """Test recipe search functionality"""
        response = self.client.get(
            reverse('recipes:recipe_list') + '?search=pasta'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Italian Pasta')
        self.assertNotContains(response, 'Fresh Salad')

    def test_recipe_filter_empty_results(self):
        """Test search with no results"""
        response = self.client.get(
            reverse('recipes:recipe_list') + '?search=nonexistent'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')


class ProfileViewTest(TestCase):
    """Test user profile views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = self.user.profile

    def test_profile_view(self):
        """Test user profile page"""
        response = self.client.get(
            reverse('accounts:profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_profile_edit_view_owner(self):
        """Test profile editing by owner"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')

    def test_profile_edit_view_unauthenticated(self):
        """Test profile edit redirects for unauthenticated user"""
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
