from django.contrib import admin
from .models import (
    Tag, Ingredient, Unit, Recipe, RecipeIngredient, RecipeStep, Comment
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
    list_display = ['user', 'recipe', 'content_preview', 'created_at', 'is_reply']
    list_filter = ['created_at', 'recipe']
    search_fields = ['content', 'user__username', 'recipe__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        """Show a preview of the comment content."""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def is_reply(self, obj):
        """Show if this is a reply to another comment."""
        return bool(obj.parent_comment)
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'
    
    fieldsets = (
        ('Comment Details', {
            'fields': ('user', 'recipe', 'content', 'parent_comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )