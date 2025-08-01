"""
Views for the recipes app.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm, RecipeIngredientFormSet, RecipeStepFormSet
from .models import Recipe, Tag


def test_view(request):
    """Simple test view for debugging."""
    return HttpResponse("Test view works!")


def recipe_list(request):
    """Display all recipes with pagination and filtering."""
    recipes = Recipe.objects.all()
    
    # Filter by tag if provided
    tag_filter = request.GET.get('tag')
    if tag_filter:
        recipes = recipes.filter(tags__name=tag_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        recipes = recipes.filter(title__icontains=search_query)
    
    # Pagination - 12 recipes per page
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_tags = Tag.objects.all()

    context = {
        'page_obj': page_obj,
        'all_tags': all_tags,
        'current_tag': tag_filter,
        'search_query': search_query,
    }
    
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, slug):
    """Display individual recipe details"""
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Increment view count
    recipe.view_count += 1
    recipe.save()
    
    # Get related recipes (same tags)
    related_recipes = Recipe.objects.filter(
        tags__in=recipe.tags.all()
    ).exclude(id=recipe.id).distinct()[:4]
    
    context = {
        'recipe': recipe,
        'related_recipes': related_recipes,
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
                f'Recipe "{recipe.title}" created successfully!'
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
        
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save()
            ingredient_formset.save()
            step_formset.save()
            
            messages.success(request, f'Recipe "{recipe.title}" updated successfully!')
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(instance=recipe, prefix='ingredients')
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
        messages.success(request, f'Recipe "{recipe_title}" deleted successfully!')
        return redirect('recipe_list')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})