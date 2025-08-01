"""
Views for the recipes app.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (RecipeForm, RecipeIngredientFormSet, RecipeStepFormSet,
                    CommentForm, RatingForm)
from .models import Recipe, Tag, Comment, Rating


def test_view(request):
    """Simple test view for debugging."""
    return HttpResponse("Test view works!")


def recipe_list(request):
    """Display all recipes with pagination and filtering."""
    recipes = Recipe.objects.all()
    
    # Check if user wants personalized recommendations
    if request.user.is_authenticated and request.GET.get('for_you') == '1':
        # Get personalized recommendations
        recommended_recipes = request.user.profile.get_recommended_recipes(
            limit=50)
        if recommended_recipes:
            recipes = recommended_recipes
    
    # Filter by tag if provided
    tag_filter = request.GET.get('tag')
    if tag_filter:
        recipes = recipes.filter(tags__name=tag_filter)
    
    # Filter by dietary preference if provided
    dietary_filter = request.GET.get('dietary')
    if dietary_filter:
        # Find recipes with tags that match the dietary preference
        recipes = recipes.filter(
            tags__name__icontains=dietary_filter,
            tags__tag_type='dietary'
        )
    
    # Search functionality - search in title, description, and dietary tags
    search_query = request.GET.get('search')
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Apply dietary restrictions for authenticated users
    if (request.user.is_authenticated and
            request.user.profile.dietary_tags.exists() and
            not tag_filter and not dietary_filter and not search_query):
        # Filter out recipes that don't match user's dietary restrictions
        compatible_recipes = []
        for recipe in recipes:
            if request.user.profile.matches_dietary_restrictions(recipe):
                compatible_recipes.append(recipe.id)
        if compatible_recipes:
            recipes = recipes.filter(id__in=compatible_recipes)
    
    # Pagination - 12 recipes per page
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all tags for filtering
    all_tags = Tag.objects.all()
    dietary_tags = Tag.objects.filter(tag_type='dietary')

    context = {
        'page_obj': page_obj,
        'all_tags': all_tags,
        'dietary_tags': dietary_tags,
        'current_tag': tag_filter,
        'current_dietary': dietary_filter,
        'search_query': search_query,
        'for_you': request.GET.get('for_you') == '1',
        'user_has_preferences': (
            request.user.is_authenticated and
            (request.user.profile.dietary_tags.exists() or
             request.user.profile.favorite_cuisines.exists())
        ),
    }
    
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, slug):
    """Display individual recipe details with comments and ratings"""
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Increment view count
    recipe.view_count += 1
    recipe.save()
    
    # Get comments for this recipe (only top-level comments)
    comments = Comment.objects.filter(
        recipe=recipe,
        parent_comment=None
    ).order_by('-created_at')
    
    # Get user's existing rating if logged in
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    # Handle comment form submission
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.user = request.user
                
                # Handle reply to another comment
                parent_comment_id = request.POST.get('parent_comment_id')
                if parent_comment_id:
                    try:
                        parent_comment = Comment.objects.get(
                            id=parent_comment_id,
                            recipe=recipe
                        )
                        comment.parent_comment = parent_comment
                        messages.success(request, "Reply added successfully!")
                    except Comment.DoesNotExist:
                        messages.error(request, "Invalid comment to reply to.")
                        return redirect('recipe_detail', slug=recipe.slug)
                else:
                    messages.success(request, "Comment added successfully!")
                
                comment.save()
                return redirect('recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, "Please log in to comment.")
    
    # Handle rating form submission
    if request.method == 'POST' and 'rating_submit' in request.POST:
        if request.user.is_authenticated:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                # Update or create rating
                rating, created = Rating.objects.update_or_create(
                    recipe=recipe,
                    user=request.user,
                    defaults={'rating': rating_form.cleaned_data['rating']}
                )
                if created:
                    messages.success(request, "Rating added successfully!")
                else:
                    messages.success(request, "Rating updated successfully!")
                return redirect('recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, "Please log in to rate.")
    
    # Initialize forms for GET requests
    comment_form = CommentForm()
    rating_form = RatingForm()
    
    # Get related recipes (same tags)
    related_recipes = Recipe.objects.filter(
        tags__in=recipe.tags.all()
    ).exclude(id=recipe.id).distinct()[:4]
    
    context = {
        'recipe': recipe,
        'related_recipes': related_recipes,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
    }
    
    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def recipe_create(request):
    """Create a new recipe."""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = RecipeIngredientFormSet(
            request.POST,
            prefix='ingredients'
        )
        step_formset = RecipeStepFormSet(
            request.POST,
            request.FILES,
            prefix='steps'
        )
        
        if (form.is_valid() and ingredient_formset.is_valid()
                and step_formset.is_valid()):
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            
            # Save ingredients
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            
            # Save steps
            steps = step_formset.save(commit=False)
            for step in steps:
                step.recipe = recipe
                step.save()
            
            messages.success(
                request,
                'Recipe created successfully!'
            )
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm()
        ingredient_formset = RecipeIngredientFormSet(prefix='ingredients')
        step_formset = RecipeStepFormSet(prefix='steps')
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'title': 'Create New Recipe'
    }
    return render(request, 'recipes/recipe_form.html', context)


@login_required
def recipe_edit(request, slug):
    """Edit an existing recipe"""
    recipe = get_object_or_404(Recipe, slug=slug, user=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(
            request.POST,
            instance=recipe,
            prefix='ingredients'
        )
        step_formset = RecipeStepFormSet(
            request.POST,
            request.FILES,
            instance=recipe,
            prefix='steps'
        )

        if (form.is_valid() and ingredient_formset.is_valid() and
                step_formset.is_valid()):
            recipe = form.save()
            ingredient_formset.save()
            step_formset.save()

            messages.success(
                request,
                'Recipe updated successfully! Your changes have been saved.'
            )
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(
            instance=recipe, prefix='ingredients'
        )
        step_formset = RecipeStepFormSet(instance=recipe, prefix='steps')
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe,
        'title': f'Edit {recipe.title}'
    }
    return render(request, 'recipes/recipe_form.html', context)


@login_required
def recipe_delete(request, slug):
    """Delete a recipe"""
    recipe = get_object_or_404(Recipe, slug=slug, user=request.user)

    if request.method == 'POST':
        recipe.delete()
        messages.success(
            request, 'Recipe deleted successfully!'
        )
        return redirect('recipe_list')

    return render(
        request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe}
    )

