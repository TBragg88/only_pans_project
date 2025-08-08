"""
Integration Tests for OnlyPans Recipe App
End-to-end testing of user workflows and system interactions
"""

from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from recipes.models import Recipe, Tag, Rating, Comment


class RecipeWorkflowTest(TestCase):
    """Test complete recipe creation and management workflow"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_complete_recipe_lifecycle(self):
        """Test complete recipe creation, viewing, editing, deletion"""
        # Step 1: User logs in
        login_success = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_success)

        # Step 2: Create a new recipe
        recipe_data = {
            'title': 'Integration Test Recipe',
            'description': 'A recipe created during integration testing',
            # Instructions captured via step formset
            'prep_time': 15,
            'cook_time': 30,
            'servings': 4,
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-0-ingredient_name': 'Test Ingredient',
            'ingredients-0-quantity': '2',
            'ingredients-0-unit': 'cups',
            'steps-TOTAL_FORMS': '1',
            'steps-INITIAL_FORMS': '0',
            'steps-0-instruction': 'Follow the instructions above',
            'steps-0-order': '1'
        }

        create_response = self.client.post(
            reverse('recipes:recipe_create'),
            recipe_data
        )
        
        # Should redirect after successful creation
        self.assertEqual(create_response.status_code, 302)

        # Verify recipe was created
    recipe = Recipe.objects.get(title='Integration Test Recipe')
    self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.prep_time, 15)

        # Step 3: View the recipe
        view_response = self.client.get(
            reverse('recipes:recipe_detail', args=[recipe.slug])
        )
        self.assertEqual(view_response.status_code, 200)
        self.assertContains(view_response, 'Integration Test Recipe')

        # Step 4: Edit the recipe
        edit_data = recipe_data.copy()
        edit_data['title'] = 'Updated Integration Test Recipe'
        edit_data['description'] = 'Updated description'

        edit_response = self.client.post(
            reverse('recipes:recipe_edit', args=[recipe.slug]),
            edit_data
        )
        self.assertEqual(edit_response.status_code, 302)

        # Verify recipe was updated
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, 'Updated Integration Test Recipe')

        # Step 5: Delete the recipe
        delete_response = self.client.post(
            reverse('recipes:recipe_delete', args=[recipe.slug])
        )
        self.assertEqual(delete_response.status_code, 302)

        # Verify recipe was deleted
        self.assertFalse(
            Recipe.objects.filter(
                title='Updated Integration Test Recipe'
            ).exists()
        )


class UserInteractionTest(TestCase):
    """Test user interactions like rating and commenting"""

    def setUp(self):
        self.client = Client()
        
        # Create two users
        self.author = User.objects.create_user(
            username='author',
            password='authorpass123'
        )
        
        self.reviewer = User.objects.create_user(
            username='reviewer',
            password='reviewerpass123'
        )

        # Create a recipe
        self.recipe = Recipe.objects.create(
            title='Test Recipe for Interaction',
            description='A recipe to test interactions',
            user=self.author,
            prep_time=5,
            cook_time=10,
            servings=2,
        )
        from recipes.models import RecipeStep
        RecipeStep.objects.create(recipe=self.recipe, step_number=1, instruction='Cook it well')

    def test_rating_and_comment_workflow(self):
        """Test user rating and commenting on recipes"""
        # Login as reviewer
        self.client.login(username='reviewer', password='reviewerpass123')

        # Add a rating
        rating_response = self.client.post(
            reverse('recipes:recipe_detail', args=[self.recipe.slug]),
            {
                'rating': 5,
                'rating_submit': '1'
            }
        )
        
        # Check if rating was created
        self.assertTrue(
            Rating.objects.filter(
                recipe=self.recipe,
                user=self.reviewer,
                rating=5
            ).exists()
        )

        # Add a comment
        comment_response = self.client.post(
            reverse('recipes:recipe_detail', args=[self.recipe.slug]),
            {
                'content': 'This recipe is amazing! Thanks for sharing.',
                'comment_submit': '1'
            }
        )

        # Check if comment was created
        self.assertTrue(
            Comment.objects.filter(
                recipe=self.recipe,
                user=self.reviewer
            ).exists()
        )

        # Verify recipe page shows rating and comment
        recipe_response = self.client.get(
            reverse('recipes:recipe_detail', args=[self.recipe.slug])
        )
        self.assertContains(recipe_response, 'Excellent recipe!')
        self.assertContains(recipe_response, 'This recipe is amazing!')

    def test_user_cannot_rate_own_recipe(self):
        """Test that users cannot rate their own recipes"""
        # Login as recipe author
        self.client.login(username='author', password='authorpass123')

        # Try to rate own recipe
        rating_response = self.client.post(
            reverse('recipes:recipe_detail', args=[self.recipe.slug]),
            {
                'rating': 5,
                'rating_submit': '1'
            }
        )

        # Should not create a rating
        self.assertFalse(
            Rating.objects.filter(
                recipe=self.recipe,
                user=self.author
            ).exists()
        )


class SearchIntegrationTest(TestCase):
    """Test search functionality across the application"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create various recipes for search testing
        self.italian_recipe = Recipe.objects.create(
            title='Classic Italian Pasta',
            description='Traditional Italian pasta with tomato sauce',
            user=self.user,
            prep_time=10,
            cook_time=20,
            servings=2,
        )
        RecipeStep.objects.create(recipe=self.italian_recipe, step_number=1, instruction='Cook pasta, add sauce')

        self.mexican_recipe = Recipe.objects.create(
            title='Spicy Mexican Tacos',
            description='Authentic Mexican tacos with fresh ingredients',
            user=self.user,
            prep_time=10,
            cook_time=10,
            servings=2,
        )
        RecipeStep.objects.create(recipe=self.mexican_recipe, step_number=1, instruction='Prepare fillings, assemble tacos')

        self.dessert_recipe = Recipe.objects.create(
            title='Chocolate Cake',
            description='Rich and moist chocolate cake',
            user=self.user,
            prep_time=10,
            cook_time=30,
            servings=8,
        )
        RecipeStep.objects.create(recipe=self.dessert_recipe, step_number=1, instruction='Mix ingredients, bake')

        # Create tags
        self.italian_tag = Tag.objects.create(
            name='Italian',
            tag_type='cuisine'
        )
        self.mexican_tag = Tag.objects.create(
            name='Mexican',
            tag_type='cuisine'
        )
        self.dessert_tag = Tag.objects.create(
            name='Dessert',
            tag_type='course'
        )

        # Associate tags with recipes
        self.italian_recipe.tags.add(self.italian_tag)
        self.mexican_recipe.tags.add(self.mexican_tag)
        self.dessert_recipe.tags.add(self.dessert_tag)

    def test_search_by_title(self):
        """Test searching recipes by title"""
        response = self.client.get(
            reverse('recipes:recipe_list') + '?search=pasta'
        )
        self.assertContains(response, 'Classic Italian Pasta')
        self.assertNotContains(response, 'Spicy Mexican Tacos')

    def test_search_by_description(self):
        """Test searching recipes by description"""
        response = self.client.get(
            reverse('recipes:recipe_list') + '?search=authentic'
        )
        self.assertContains(response, 'Spicy Mexican Tacos')
        self.assertNotContains(response, 'Classic Italian Pasta')

    def test_search_no_results(self):
        """Test search with no matching results"""
        response = self.client.get(
            reverse('recipes:recipe_list') + '?search=nonexistent'
        )
        self.assertContains(response, 'No recipes found')

    def test_filter_by_tag(self):
        """Test filtering recipes by tag"""
        response = self.client.get(
            reverse('recipes:recipe_list') + f'?tags={self.dessert_tag.id}'
        )
        self.assertContains(response, 'Chocolate Cake')
        self.assertNotContains(response, 'Classic Italian Pasta')

    def test_combined_search_and_filter(self):
        """Test combining search text with tag filtering"""
        response = self.client.get(
            reverse('recipes:recipe_list') +
            f'?search=italian&tags={self.italian_tag.id}'
        )
        self.assertContains(response, 'Classic Italian Pasta')
        self.assertNotContains(response, 'Chocolate Cake')


class PerformanceTest(TransactionTestCase):
    """Test application performance with larger datasets"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_recipe_list_performance(self):
        """Test recipe list page performance with many recipes"""
        # Create multiple recipes
        recipes = []
        for i in range(50):
            recipes.append(Recipe(
                title=f'Recipe {i}',
                description=f'Description for recipe {i}',
                user=self.user,
                prep_time=5,
                cook_time=5,
                servings=2,
            ))
        
        Recipe.objects.bulk_create(recipes)

        # Test that the page loads efficiently
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check pagination is working
        self.assertContains(response, 'Recipe 0')
        
        # Note: In a real scenario, you might use tools like
        # django-debug-toolbar to measure actual query counts
        # and response times

    def test_search_performance(self):
        """Test search performance with large dataset"""
        # Create recipes with varied content
        recipes = []
        for i in range(100):
            recipes.append(Recipe(
                title=f'Recipe {i} with varied content',
                description=f'This is recipe number {i} for testing',
                user=self.user,
                prep_time=5,
                cook_time=5,
                servings=2,
            ))
        
        Recipe.objects.bulk_create(recipes)

        # Test search performance
        response = self.client.get(
            reverse('recipes:recipe_list') + '?search=recipe'
        )
        self.assertEqual(response.status_code, 200)
        
        # Should handle the search efficiently
        # In production, you might want to implement search indexing
        # for better performance


class SecurityTest(TestCase):
    """Test security aspects of the application"""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='user1pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='user2pass123'
        )
        
        self.user1_recipe = Recipe.objects.create(
            title='User 1 Recipe',
            user=self.user1,
            prep_time=5,
            cook_time=5,
            servings=1,
        )

    def test_unauthorized_recipe_edit_attempt(self):
        """Test that users cannot edit other users' recipes"""
        # Login as user2
        self.client.login(username='user2', password='user2pass123')
        
        # Try to access user1's recipe edit page
        response = self.client.get(
            reverse('recipes:recipe_edit', args=[self.user1_recipe.slug])
        )
        
        # Should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_recipe_delete_attempt(self):
        """Test that users cannot delete other users' recipes"""
        # Login as user2
        self.client.login(username='user2', password='user2pass123')
        
        # Try to delete user1's recipe
        response = self.client.post(
            reverse('recipes:recipe_delete', args=[self.user1_recipe.slug])
        )
        
        # Should be forbidden and recipe should still exist
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Recipe.objects.filter(slug=self.user1_recipe.slug).exists()
        )
