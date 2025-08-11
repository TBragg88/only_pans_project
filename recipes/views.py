from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (RecipeForm, RecipeIngredientFormSet, RecipeStepFormSet,
                    CommentForm, RatingForm, RecipeSearchForm)
from .models import Recipe, Tag, Comment, Rating, Ingredient
from .notifications import send_comment_notification, send_rating_notification

"""
Views for the recipes app.
"""


@login_required
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Only allow user to delete their own comment
    if comment.user != request.user:
        messages.error(request, "You do not have permission to delete this comment.")
        return redirect('recipes:recipe_detail', slug=comment.recipe.slug)
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('recipes:recipe_detail', slug=comment.recipe.slug)

def test_view(request):
    """Simple test view for debugging."""
    return HttpResponse("Test view works!")

def recipe_list(request):
    """Display all recipes with advanced filtering and pagination."""
    
    # Initialize the search form with GET data
    search_form = RecipeSearchForm(request.GET or None)
    
    # Start with all recipes
    recipes = Recipe.objects.all()
    
    # Apply filters based on form data
    if search_form.is_valid():
        form_data = search_form.cleaned_data
        
        # Text search
        if form_data.get('search'):
            search_query = form_data['search']
            recipes = recipes.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(ingredients__ingredient__name__icontains=search_query)
            ).distinct()
        
        # Tags filter
        if form_data.get('tags'):
            recipes = recipes.filter(tags__in=form_data['tags']).distinct()
            
        # Cuisine filter
        if form_data.get('cuisine'):
            recipes = recipes.filter(tags__in=form_data['cuisine']).distinct()
            
        # Dietary filter
        if form_data.get('dietary'):
            recipes = recipes.filter(tags__in=form_data['dietary']).distinct()
        
        # Time filters
        if form_data.get('max_prep_time'):
            recipes = recipes.filter(prep_time__lte=form_data['max_prep_time'])
            
        if form_data.get('max_cook_time'):
            recipes = recipes.filter(cook_time__lte=form_data['max_cook_time'])
            
        if form_data.get('max_total_time'):
            recipes = recipes.filter(
                total_time__lte=form_data['max_total_time']
            )
        
        # Servings filters
        if form_data.get('min_servings'):
            recipes = recipes.filter(servings__gte=form_data['min_servings'])
            
        if form_data.get('max_servings'):
            recipes = recipes.filter(servings__lte=form_data['max_servings'])
        
        # Difficulty filter (based on total time)
        difficulty = form_data.get('difficulty')
        if difficulty == 'easy':
            recipes = recipes.filter(total_time__lt=30)
        elif difficulty == 'medium':
            recipes = recipes.filter(total_time__gte=30, total_time__lte=60)
        elif difficulty == 'hard':
            recipes = recipes.filter(total_time__gt=60)
        
        # Sorting
        sort_by = form_data.get('sort_by', '-created_at')
        if sort_by == '-average_rating':
            # Sort by average rating
            from django.db.models import Avg
            recipes = recipes.annotate(
                avg_rating=Avg('ratings__rating')
            ).order_by('-avg_rating', '-created_at')
        else:
            recipes = recipes.order_by(sort_by)
    else:
        # Default sorting if no form or invalid form
        recipes = recipes.order_by('-created_at')
    
    # Check if user wants personalized recommendations
    if request.user.is_authenticated and request.GET.get('for_you') == '1':
        # Get personalized recommendations
        recommended_recipes = request.user.profile.get_recommended_recipes(
            limit=50)
        if recommended_recipes:
            recipes = recommended_recipes
    
    # Apply dietary restrictions for authenticated users
    if (request.user.is_authenticated and
            request.user.profile.dietary_tags.exists() and
            not request.GET.get('tags') and not request.GET.get('dietary') and
            not request.GET.get('search')):
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
    
    # Get cuisine tags for carousel (use any tags as cuisines)
    cuisine_tags = Tag.objects.filter(
        recipe__isnull=False
    ).distinct()[:5]  # Get 5 tags that have recipes
    carousel_data = []
    for cuisine in cuisine_tags:
        cuisine_recipes = Recipe.objects.filter(tags=cuisine)[:6]
        if cuisine_recipes.exists():
            carousel_data.append({
                'cuisine': cuisine,
                'recipes': cuisine_recipes
            })

    context = {
        'page_obj': page_obj,
        'all_tags': all_tags,
        'dietary_tags': dietary_tags,
        'carousel_data': carousel_data,
        'search_form': search_form,
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
    
    # Get comments for this recipe (only approved top-level comments)
    comments = Comment.objects.filter(
        recipe=recipe,
        parent_comment=None,
        is_approved=True
    ).order_by('-created_at')
    
    # Get user's existing rating if logged in
    user_rating = None
    is_liked = False
    is_following = False
    my_pending_comments = None
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=request.user)
        except Rating.DoesNotExist:
            pass
        
        # Check if user has liked this recipe
        from .models import RecipeLike, Follow
        is_liked = (
            RecipeLike.objects
            .filter(user=request.user, recipe=recipe)
            .exists()
        )
        
        # Check if user is following the recipe author
        is_following = (
            Follow.objects
            .filter(follower=request.user, followed=recipe.user)
            .exists()
        )
        
    # Show user's own pending comments (not visible publicly until
    # approved)
        my_pending_comments = Comment.objects.filter(
            recipe=recipe,
            user=request.user,
            is_approved=False
        ).order_by('-created_at')
    
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
                        messages.info(
                            request,
                            (
                                "Reply submitted! It will appear after admin "
                                "approval."
                            ),
                        )
                    except Comment.DoesNotExist:
                        messages.error(request, "Invalid comment to reply to.")
                        return redirect(
                            'recipes:recipe_detail',
                            slug=recipe.slug,
                        )
                else:
                    messages.info(
                        request,
                        (
                            "Comment submitted! It will appear after admin "
                            "approval."
                        ),
                    )
                
                comment.save()
                
                # Send notification to recipe owner (if not commenting on own
                # recipe)
                if comment.user != recipe.user:
                    send_comment_notification(comment, recipe.user)
                
                return redirect('recipes:recipe_detail', slug=recipe.slug)
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
                    # Send notification to recipe owner (if not rating own
                    # recipe)
                    if rating.user != recipe.user:
                        send_rating_notification(rating, recipe.user)
                else:
                    messages.success(request, "Rating updated successfully!")
                return redirect('recipes:recipe_detail', slug=recipe.slug)
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
        'my_pending_comments': my_pending_comments,
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
            
            # Save ingredients with automatic ordering
            ingredients = ingredient_formset.save(commit=False)
            for i, ingredient in enumerate(ingredients, 1):
                ingredient.recipe = recipe
                ingredient.order = i
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
            return redirect('recipes:recipe_detail', slug=recipe.slug)
        else:
            # Form validation failed - errors will be displayed in template
            pass
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
            
            # Save ingredients with automatic ordering
            ingredients = ingredient_formset.save(commit=False)
            for i, ingredient in enumerate(ingredients, 1):
                if ingredient.recipe_id:  # Only update existing ingredients
                    ingredient.order = i
                    ingredient.save()
            if hasattr(ingredient_formset, 'save_m2m'):
                ingredient_formset.save_m2m()
            
            # Save steps with automatic numbering
            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps, 1):
                if step.recipe_id:  # Only update existing steps
                    step.step_number = i
                    step.save()
            if hasattr(step_formset, 'save_m2m'):
                step_formset.save_m2m()

            messages.success(
                request,
                'Recipe updated successfully! Your changes have been saved.'
            )
            return redirect('recipes:recipe_detail', slug=recipe.slug)
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
        recipe_title = recipe.title
        recipe.delete()
        messages.success(
            request, f'Recipe "{recipe_title}" deleted successfully!'
        )
    return redirect('accounts:profile_detail', username=request.user.username)

    # If GET request, redirect back to recipe detail page
    return redirect('recipes:recipe_detail', slug=slug)


def ingredients_api(request):
    """API endpoint to get all ingredients for autocomplete."""
    ingredients = Ingredient.objects.all().order_by('name')
    data = [{'name': ingredient.name} for ingredient in ingredients]
    return JsonResponse(data, safe=False)


@login_required
def toggle_like(request, slug):
    """Toggle like status for a recipe."""
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
            messages.success(
                request,
                (
                    f'Removed "{recipe.title}" from your liked recipes.'
                ),
            )
        else:
            # Like the recipe
            liked = True
            messages.success(
                request,
                (
                    f'Added "{recipe.title}" to your liked recipes!'
                ),
            )
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': liked,
                'like_count': recipe.like_count
            })
    
    return redirect('recipes:recipe_detail', slug=slug)


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
            messages.success(
                request,
                (
                    f'You are no longer following '
                    f'{user_to_follow.username}.'
                ),
            )
        else:
            # Follow the user
            following = True
            messages.success(
                request,
                (
                    f'You are now following {user_to_follow.username}!'
                ),
            )
        
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

