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
    
    # Dietary preferences as JSON field (for now, simple text)
    dietary_preferences = models.TextField(
        blank=True,
        help_text='Enter dietary restrictions: vegan, gluten-free, etc.'
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
