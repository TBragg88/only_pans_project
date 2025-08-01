from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    """Extended user profile with additional fields from ERD."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True, help_text='Tell us about yourself!')
    
    # Profile image - Cloudinary integration
    profile_image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='profiles/',
        help_text='Upload profile image'
    )
    
    # Dietary preferences as JSON field (for future expansion)
    dietary_preferences = models.TextField(
        blank=True,
        help_text='Legacy field - use dietary_tags instead'
    )
    
    # New tag-based preferences
    dietary_tags = models.ManyToManyField(
        'recipes.Tag',
        blank=True,
        related_name='users_with_dietary_preference',
        limit_choices_to={'tag_type': 'dietary'},
        help_text='Select your dietary restrictions and preferences'
    )
    
    favorite_cuisines = models.ManyToManyField(
        'recipes.Tag',
        blank=True,
        related_name='users_who_favorite',
        limit_choices_to={'tag_type': 'cuisine'},
        help_text='Select your favorite cuisines'
    )
    
    preferred_difficulty = models.ForeignKey(
        'recipes.Tag',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users_with_preferred_difficulty',
        limit_choices_to={'tag_type': 'difficulty'},
        help_text='Your preferred recipe difficulty level'
    )
    
    # Premium features (for future expansion)
    is_premium = models.BooleanField(default=False)
    subscription_type = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
        ],
        default='free'
    )
    subscription_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Social features (for future expansion)
    total_followers = models.PositiveIntegerField(default=0)
    total_following = models.PositiveIntegerField(default=0)
    
    # Privacy settings
    show_dietary_preferences = models.BooleanField(
        default=True,
        help_text='Allow other users to see your dietary preferences'
    )
    show_email = models.BooleanField(
        default=False,
        help_text='Allow other users to see your email address'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    def get_profile_image_url(self):
        """Get profile image URL with fallback."""
        if self.profile_image:
            try:
                return self.profile_image.url
            except Exception:
                return 'https://via.placeholder.com/150x150?text=Profile'
        return 'https://via.placeholder.com/150x150?text=Profile'
    
    @property
    def display_name(self):
        """Return first name if available, otherwise username."""
        if self.user.first_name:
            return self.user.first_name
        return self.user.username
    
    @property
    def full_display_name(self):
        """Return full name if available, otherwise username."""
        if self.user.first_name or self.user.last_name:
            return self.user.get_full_name()
        return self.user.username
    
    def get_average_recipe_rating(self):
        """Calculate user's average recipe rating score."""
        user_recipes = self.user.recipes.all()
        if not user_recipes:
            return 0
        
        total_rating = 0
        total_recipes_with_ratings = 0
        
        for recipe in user_recipes:
            avg_rating = recipe.average_rating
            if avg_rating > 0:
                total_rating += avg_rating
                total_recipes_with_ratings += 1
        
        if total_recipes_with_ratings == 0:
            return 0
        
        return round(total_rating / total_recipes_with_ratings, 1)
    
    def get_recommended_recipes(self, limit=10):
        """Get recipes recommended based on user preferences."""
        from recipes.models import Recipe
        
        # Start with all recipes
        recipes = Recipe.objects.all()
        
        # Filter by dietary preferences (must match ALL dietary restrictions)
        if self.dietary_tags.exists():
            for dietary_tag in self.dietary_tags.all():
                recipes = recipes.filter(tags=dietary_tag)
        
        # Prefer recipes from favorite cuisines
        if self.favorite_cuisines.exists():
            cuisine_recipes = Recipe.objects.filter(
                tags__in=self.favorite_cuisines.all()
            ).distinct()
            
            # If we have dietary restrictions, apply them to cuisine prefs
            if self.dietary_tags.exists():
                for dietary_tag in self.dietary_tags.all():
                    cuisine_recipes = cuisine_recipes.filter(tags=dietary_tag)
            
            # Combine dietary-filtered recipes with cuisine preferences
            recipes = recipes.union(cuisine_recipes)
        
        # Filter by preferred difficulty if set
        if self.preferred_difficulty:
            preferred_recipes = recipes.filter(tags=self.preferred_difficulty)
            if preferred_recipes.exists():
                recipes = preferred_recipes
        
        # Order by rating and limit
        return (recipes.distinct()
                .order_by('-view_count', '-created_at')[:limit])
    
    def matches_dietary_restrictions(self, recipe):
        """Check if a recipe matches user's dietary restrictions."""
        if not self.dietary_tags.exists():
            return True
        
        # Recipe must have ALL user's dietary tags
        user_dietary_tags = set(self.dietary_tags.all())
        recipe_tags = set(recipe.tags.filter(tag_type='dietary'))
        
        return user_dietary_tags.issubset(recipe_tags)
    
    def get_dietary_summary(self):
        """Get a readable summary of dietary preferences."""
        if not self.dietary_tags.exists():
            return "No dietary restrictions"
        
        tags = [tag.name for tag in self.dietary_tags.all()]
        if len(tags) == 1:
            return tags[0]
        elif len(tags) == 2:
            return f"{tags[0]} and {tags[1]}"
        else:
            return f"{', '.join(tags[:-1])}, and {tags[-1]}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
