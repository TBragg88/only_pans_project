# recipes/admin.py
from django.contrib import admin
from .models import Tag, Ingredient, Unit, Recipe, RecipeIngredient, RecipeStep


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag_type', 'color']
    list_filter = ['tag_type']
    search_fields = ['name']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'unit_type']
    list_filter = ['unit_type']


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    fields = ['ingredient', 'quantity', 'unit', 'notes', 'order']


class RecipeStepInline(admin.StackedInline):
    model = RecipeStep
    extra = 3
    fields = ['step_number', 'instruction', 'image_url']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'prep_time', 'cook_time', 'servings', 'created_at']
    list_filter = ['created_at', 'tags']
    search_fields = ['title', 'description']
    filter_horizontal = ['tags']
    inlines = [RecipeIngredientInline, RecipeStepInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description', 'image_url')
        }),
        ('Timing & Servings', {
            'fields': ('prep_time', 'cook_time', 'servings')
        }),
        ('Categorization', {
            'fields': ('tags',)
        }),
    )