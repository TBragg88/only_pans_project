"""
Views for the recipes app.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (RecipeForm, RecipeIngredientFormSet, RecipeStepFormSet,
                    CommentForm, RatingForm)
from .models import Recipe, Tag, Comment, Rating, Ingredient


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
    
    # Add liked status for authenticated users
    if request.user.is_authenticated:
        from .models import RecipeLike
        liked_recipe_ids = set(RecipeLike.objects.filter(
            user=request.user
        ).values_list('recipe_id', flat=True))
        
        # Add is_liked attribute to each recipe
        for recipe in page_obj:
            recipe.is_liked = recipe.id in liked_recipe_ids
    else:
        # For anonymous users, no recipes are liked
        for recipe in page_obj:
            recipe.is_liked = False
    
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
    is_liked = False
    is_following = False
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=request.user)
        except Rating.DoesNotExist:
            pass
        
        # Check if user has liked this recipe
        from .models import RecipeLike, Follow
        is_liked = RecipeLike.objects.filter(user=request.user, recipe=recipe).exists()
        
        # Check if user is following the recipe author
        is_following = Follow.objects.filter(follower=request.user, followed=recipe.user).exists()
    
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
        'is_liked': is_liked,
        'is_following': is_following,
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
            
            # Save steps with automatic numbering
            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps, 1):
                step.recipe = recipe
                step.step_number = i
                step.save()
            
            messages.success(
                request,
                'Recipe created successfully!'
            )
            return redirect('recipe_detail', slug=recipe.slug)
        else:
            # Form validation failed - errors will be displayed in template
            messages.error(
                request, 
                'Please correct the errors below and try again.'
            )
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
            
            # Save steps with automatic numbering
            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps, 1):
                if step.recipe_id:  # Only update existing steps
                    step.step_number = i
                    step.save()
            step_formset.save_m2m() if hasattr(step_formset, 'save_m2m') else None

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


def ingredients_api(request):
    """API endpoint to get all ingredients for autocomplete."""
    ingredients = Ingredient.objects.all().order_by('name')
    data = [{'name': ingredient.name} for ingredient in ingredients]
    return JsonResponse(data, safe=False)


@login_required
def toggle_like(request, slug):
    """Toggle like status for a recipe."""
    from django.contrib.auth.models import User
    from .models import RecipeLike
    
    recipe = get_object_or_404(Recipe, slug=slug)
    
    if request.method == 'POST':
        like, created = RecipeLike.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        
        if not created:
            # Unlike the recipe
            like.delete()
            liked = False
            messages.success(request, f'Removed "{recipe.title}" from your liked recipes.')
        else:
            # Like the recipe
            liked = True
            messages.success(request, f'Added "{recipe.title}" to your liked recipes!')
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': liked,
                'like_count': recipe.like_count
            })
    
    return redirect('recipe_detail', slug=slug)


@login_required
def toggle_follow(request, username):
    """Toggle follow status for a user."""
    from django.contrib.auth.models import User
    from .models import Follow
    
    user_to_follow = get_object_or_404(User, username=username)
    
    # Can't follow yourself
    if request.user == user_to_follow:
        messages.error(request, "You can't follow yourself!")
        return redirect('accounts:profile_detail', username=username)
    
    if request.method == 'POST':
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )
        
        if not created:
            # Unfollow the user
            follow.delete()
            following = False
            messages.success(request, f'You are no longer following {user_to_follow.username}.')
        else:
            # Follow the user
            following = True
            messages.success(request, f'You are now following {user_to_follow.username}!')
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'following': following,
                'follower_count': user_to_follow.profile.get_follower_count()
            })
    
    return redirect('accounts:profile_detail', username=username)


@login_required
def liked_recipes(request):
    """Display user's liked recipes."""
    liked_recipe_objects = request.user.profile.get_liked_recipes()
    recipes = [like.recipe for like in liked_recipe_objects]
    
    # Paginate results
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'recipes/liked_recipes.html', {
        'page_obj': page_obj,
        'total_liked': len(recipes)
    })

