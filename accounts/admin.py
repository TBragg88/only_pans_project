from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = (
        'profile_image', 'bio', 'dietary_preferences',
        'show_dietary_preferences', 'show_email',
        'is_premium', 'subscription_type',
        'total_followers', 'total_following'
    )
    readonly_fields = ('total_followers', 'total_following')


class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with profile information."""
    inlines = (UserProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'get_recipe_count', 'get_average_rating', 'date_joined'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'date_joined',
        'profile__is_premium', 'profile__subscription_type'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_recipe_count(self, obj):
        """Get the number of recipes for this user."""
        count = obj.recipes.count()
        if count > 0:
            return format_html(
                '<a href="/admin/recipes/recipe/?user__id__exact={}" '
                'style="color: #007cba;">{} recipes</a>',
                obj.id, count
            )
        return '0 recipes'
    get_recipe_count.short_description = 'Recipes'
    
    def get_average_rating(self, obj):
        """Get the user's average recipe rating."""
        try:
            avg_rating = obj.profile.get_average_recipe_rating()
            if avg_rating > 0:
                return f'{avg_rating}/5 ⭐'
            return 'No ratings'
        except AttributeError:
            return 'No profile'
    get_average_rating.short_description = 'Avg Rating'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    list_display = (
        'user', 'get_full_name', 'get_recipe_count', 'get_average_rating',
        'is_premium', 'subscription_type', 'total_followers'
    )
    list_filter = (
        'is_premium', 'subscription_type', 'show_dietary_preferences',
        'show_email', 'created_at'
    )
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'bio', 'dietary_preferences'
    )
    readonly_fields = (
        'user', 'created_at', 'updated_at', 'get_recipe_count',
        'get_average_rating'
    )
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('Profile Information', {
            'fields': ('profile_image', 'bio', 'dietary_preferences')
        }),
        ('Privacy Settings', {
            'fields': ('show_dietary_preferences', 'show_email')
        }),
        ('Premium Features', {
            'fields': (
                'is_premium', 'subscription_type', 'subscription_expires_at'
            )
        }),
        ('Social Stats', {
            'fields': ('total_followers', 'total_following')
        }),
        ('Recipe Stats', {
            'fields': ('get_recipe_count', 'get_average_rating'),
            'classes': ('collapse',)
        })
    )
    
    def get_full_name(self, obj):
        """Get the user's full name."""
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'
    
    def get_recipe_count(self, obj):
        """Get the number of recipes for this user."""
        count = obj.user.recipes.count()
        if count > 0:
            return format_html(
                '<a href="/admin/recipes/recipe/?user__id__exact={}" '
                'style="color: #007cba;">{} recipes</a>',
                obj.user.id, count
            )
        return '0 recipes'
    get_recipe_count.short_description = 'Recipes'
    
    def get_average_rating(self, obj):
        """Get the user's average recipe rating."""
        avg_rating = obj.get_average_recipe_rating()
        if avg_rating > 0:
            return f'{avg_rating}/5 ⭐'
        return 'No ratings'
    get_average_rating.short_description = 'Average Rating'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
