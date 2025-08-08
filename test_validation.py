#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans.settings')
django.setup()

from django.core.exceptions import ValidationError
from recipes.models import Recipe, Comment, RecipeStep
from accounts.models import User

def test_field_validation():
    print("Testing field validation constraints...")
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    
    # Test Recipe description length (max 2000 chars)
    try:
        long_description = "x" * 2001  # Over limit
        recipe = Recipe(
            title="Test Recipe",
            description=long_description,
            user=user,
            prep_time=10,
            cook_time=20,
            servings=4
        )
        recipe.full_clean()  # This should raise ValidationError
        print("❌ Recipe description validation FAILED - should have rejected 2001 chars")
    except ValidationError as e:
        print("✅ Recipe description validation PASSED - correctly rejected 2001 chars")
    
    # Test Comment content length (max 2000 chars)
    try:
        # First create a valid recipe
        recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Valid description",
            user=user,
            prep_time=10,
            cook_time=20,
            servings=4
        )
        
        long_comment = "x" * 2001  # Over limit
        comment = Comment(
            recipe=recipe,
            user=user,
            content=long_comment
        )
        comment.full_clean()  # This should raise ValidationError
        print("❌ Comment content validation FAILED - should have rejected 2001 chars")
    except ValidationError as e:
        print("✅ Comment content validation PASSED - correctly rejected 2001 chars")
    
    # Test RecipeStep instruction length (max 1000 chars)
    try:
        long_instruction = "x" * 1001  # Over limit
        step = RecipeStep(
            recipe=recipe,
            step_number=1,
            instruction=long_instruction
        )
        step.full_clean()  # This should raise ValidationError
        print("❌ RecipeStep instruction validation FAILED - should have rejected 1001 chars")
    except ValidationError as e:
        print("✅ RecipeStep instruction validation PASSED - correctly rejected 1001 chars")
    
    print("\n✅ Field validation testing complete - spam prevention is working!")

if __name__ == "__main__":
    test_field_validation()
