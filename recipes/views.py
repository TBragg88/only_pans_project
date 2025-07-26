from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Recipe, Tag

def recipe_list(request):
    """Display all recipes with pagination and filtering"""
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
    
    # Get all tags for filter dropdown
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