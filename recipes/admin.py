from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Tag, Ingredient, Unit, Recipe, RecipeIngredient, 
    RecipeStep, Comment, Rating
)


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
    fields = ['step_number', 'instruction', 'image', 'image_url']  # Added 'image'

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'prep_time', 'cook_time', 'servings', 'created_at']
    list_filter = ['created_at', 'tags']
    search_fields = ['title', 'description']
    filter_horizontal = ['tags']
    inlines = [RecipeIngredientInline, RecipeStepInline]
   
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description', 'image', 'image_url')  # Added 'image'
        }),
        ('Timing & Servings', {
            'fields': ('prep_time', 'cook_time', 'servings')
        }),
        ('Categorization', {
            'fields': ('tags',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'recipe_title', 'content_preview', 
        'is_approved', 'created_at'
    ]
    list_filter = ['is_approved', 'created_at', 'recipe']
    search_fields = ['user__username', 'recipe__title', 'content']
    actions = ['approve_comments', 'unapprove_comments']
    ordering = ['-created_at']
    
    def recipe_title(self, obj):
        """Display recipe title with link"""
        return format_html(
            '<a href="/admin/recipes/recipe/{}/change/">{}</a>',
            obj.recipe.pk, obj.recipe.title
        )
    recipe_title.short_description = 'Recipe'
    
    def content_preview(self, obj):
        """Show first 50 characters of content"""
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def approve_comments(self, request, queryset):
        """Bulk approve selected comments"""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request, 
            f'{updated} comment{"s" if updated != 1 else ""} approved successfully.'
        )
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        """Bulk unapprove selected comments"""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request, 
            f'{updated} comment{"s" if updated != 1 else ""} unapproved.'
        )
    unapprove_comments.short_description = "Unapprove selected comments"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'recipe__title']