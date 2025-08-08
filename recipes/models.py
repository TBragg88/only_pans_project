from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Tag(models.Model):
    """Tags for categorizing recipes (cuisine, dietary, etc.)"""
    TAG_TYPES = [
        ('cuisine', 'Cuisine'),
        ('dietary', 'Dietary'),
        ('meal_type', 'Meal Type'),
        ('cooking_method', 'Cooking Method'),
        ('difficulty', 'Difficulty'),
    ]

    name = models.CharField(max_length=100, unique=True)
    tag_type = models.CharField(max_length=50, choices=TAG_TYPES)
    color = models.CharField(max_length=7, default='#6c757d',
                             help_text='Hex color like #FF5733')

    def __str__(self):
        return f"{self.name} ({self.get_tag_type_display()})"

    class Meta:
        ordering = ['tag_type', 'name']


class Ingredient(models.Model):
    """Global list of ingredients with nutritional data"""
    CATEGORIES = [
        ('produce', 'Produce'),
        ('meat', 'Meat & Poultry'),
        ('fish', 'Fish & Seafood'),
        ('dairy', 'Dairy'),
        ('protein', 'Protein'),
        ('grains', 'Grains & Bread'),
        ('baking', 'Baking'),
        ('oils', 'Oils'),
        ('seasonings', 'Seasonings'),
        ('spices', 'Spices'),
        ('herbs', 'Herbs'),
        ('sweeteners', 'Sweeteners'),
        ('condiments', 'Condiments'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(
        max_length=100,
        choices=CATEGORIES,
        default='other'
    )
    common_unit = models.CharField(
        max_length=50,
        default='grams',
        help_text='Most common unit for this ingredient'
    )

    # Nutritional data per 100g/100ml
    calories_per_100g = models.DecimalField(max_digits=8,
                                            decimal_places=2,
                                            null=True, blank=True)
    protein_per_100g = models.DecimalField(max_digits=8,
                                           decimal_places=2,
                                           null=True, blank=True)
    carbs_per_100g = models.DecimalField(max_digits=8,
                                         decimal_places=2,
                                         null=True, blank=True)
    fat_per_100g = models.DecimalField(max_digits=8,
                                       decimal_places=2,
                                       null=True, blank=True)
    fibre_per_100g = models.DecimalField(max_digits=8,
                                         decimal_places=2,
                                         null=True, blank=True)
    sugars_per_100g = models.DecimalField(max_digits=8,
                                          decimal_places=2,
                                          null=True, blank=True)
    sodium_mg_per_100g = models.DecimalField(max_digits=8,
                                             decimal_places=2,
                                             null=True, blank=True)
    saturated_fat_per_100g = models.DecimalField(max_digits=8,
                                                 decimal_places=2,
                                                 null=True, blank=True)

    # Dietary tags (e.g., gluten-free, dairy-free, vegan, etc.)
    dietary_tags = models.ManyToManyField(
        'Tag', blank=True,
        limit_choices_to={'tag_type': 'dietary'},
        help_text='Dietary restriction tags'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Unit(models.Model):
    """Units of measurement"""
    UNIT_TYPES = [
        ('volume', 'Volume'),
        ('weight', 'Weight'),
        ('count', 'Count'),
    ]

    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    
    # Conversion to grams - for nutritional calculations
    # For weight units: direct conversion (e.g., 1 kg = 1000g)
    # For volume units: approximate for water-like density (e.g., 1 cup ≈ 240g)
    # For count units: average weight (e.g., 1 can ≈ 400g, 1 egg ≈ 50g)
    grams_per_unit = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Approximate grams per unit for nutritional calculations'
    )

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

    class Meta:
        ordering = ['unit_type', 'name']


class Recipe(models.Model):
    """Main recipe model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='recipes')
    title = models.CharField(
        max_length=200,  # Reasonable recipe title length
        help_text='Recipe title (max 200 characters)'
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(
        max_length=1000,  # Prevent extremely long descriptions
        blank=True,
        help_text='Tell us about this recipe! (max 1000 characters)'
    )

    # Timing (reasonable limits to prevent abuse)
    prep_time = models.PositiveIntegerField(
        help_text='Preparation time in minutes (max 1440 = 24 hours)',
        validators=[MinValueValidator(1), MaxValueValidator(1440)]
    )
    cook_time = models.PositiveIntegerField(
        help_text='Cooking time in minutes (max 1440 = 24 hours)',
        validators=[MinValueValidator(1), MaxValueValidator(1440)]
    )
    servings = models.PositiveIntegerField(
        default=4,
        help_text='Number of servings (max 100)',
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    # Media - Cloudinary integration
    image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='recipes/',
        help_text='Upload recipe image'
    )

    # Keep URL field as fallback for external images
    image_url = models.URLField(blank=True, help_text='Or paste image URL')

    # Categorization
    tags = models.ManyToManyField(Tag, blank=True)

    # Engagement stats (we'll calculate these)
    view_count = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # Ensure unique slug
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        """Get image URL - prioritize Cloudinary, fallback to URL field"""
        from django.templatetags.static import static
        
        if self.image:
            try:
                return self.image.url
            except Exception:
                # Fallback if Cloudinary config is dummy/invalid
                if self.image_url:
                    return self.image_url
                return static('images/default_recipe.png')
        elif self.image_url:
            return self.image_url
        return static('images/default_recipe.png')

    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time

    @property
    def average_rating(self):
        """Calculate average rating"""
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0

    @property
    def rating_count(self):
        """Count of ratings"""
        return self.ratings.count()

    @property
    def nutrition_per_serving(self):
        """Calculate nutritional information per serving"""
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for recipe_ingredient in self.ingredients.all():
            if recipe_ingredient.ingredient and recipe_ingredient.unit:
                # Convert quantity to grams using unit conversion
                if recipe_ingredient.unit.grams_per_unit:
                    quantity_in_grams = (
                        float(recipe_ingredient.quantity) * 
                        float(recipe_ingredient.unit.grams_per_unit)
                    )
                else:
                    # Fallback: assume quantity is already in grams
                    quantity_in_grams = float(recipe_ingredient.quantity)
                
                # Calculate nutrition based on quantity in grams
                ingredient = recipe_ingredient.ingredient
                if ingredient.calories_per_100g:
                    total_calories += (
                        (quantity_in_grams / 100) * 
                        float(ingredient.calories_per_100g)
                    )
                if ingredient.protein_per_100g:
                    total_protein += (
                        (quantity_in_grams / 100) * 
                        float(ingredient.protein_per_100g)
                    )
                if ingredient.carbs_per_100g:
                    total_carbs += (
                        (quantity_in_grams / 100) * 
                        float(ingredient.carbs_per_100g)
                    )
                if ingredient.fat_per_100g:
                    total_fat += (
                        (quantity_in_grams / 100) * 
                        float(ingredient.fat_per_100g)
                    )
        
        # Divide by servings
        servings = self.servings or 1
        return {
            'calories': round(total_calories / servings, 1),
            'protein': round(total_protein / servings, 1),
            'carbs': round(total_carbs / servings, 1),
            'fat': round(total_fat / servings, 1),
        }

    @property
    def like_count(self):
        """Count of likes"""
        return self.likes.count()

    def is_liked_by(self, user):
        """Check if a user has liked this recipe"""
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    class Meta:
        ordering = ['-created_at']


class RecipeIngredient(models.Model):
    """Ingredients used in a specific recipe"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.CharField(
        max_length=100,
        blank=True,
        help_text='e.g., "room temperature", "diced"'
    )
    order = models.PositiveIntegerField(help_text='Order in ingredient list')

    def __str__(self):
        return (
            f"{self.quantity} {self.unit.abbreviation} "
            f"{self.ingredient.name}"
        )

    def formatted_quantity(self):
        """Return quantity without unnecessary decimals"""
        if self.quantity == int(self.quantity):
            return str(int(self.quantity))
        else:
            return str(self.quantity).rstrip('0').rstrip('.')

    def smart_display(self):
        """Return a smart display format that handles 'to taste' style units"""
        # Units that don't need quantities displayed
        no_quantity_units = [
            'to taste', 'taste', 'pinch', 'dash', 'handful', 
            'splash', 'drizzle', 'sprinkle', 'garnish'
        ]
        
        unit_name = self.unit.name.lower()
        
        # Check if this is a "no quantity" unit
        if any(no_qty_unit in unit_name for no_qty_unit in no_quantity_units):
            return self.unit.name  # Just return the unit name (e.g., "To taste", "Pinch")
        
        # For normal units, show quantity + unit
        return f"{self.formatted_quantity()} {self.unit.abbreviation}"

    def smart_display_scaled(self, scale_factor=1.0):
        """Return smart display with scaling, but don't scale 'to taste' type units"""
        # Units that don't scale
        no_scale_units = [
            'to taste', 'taste', 'pinch', 'dash', 'handful', 
            'splash', 'drizzle', 'sprinkle', 'garnish'
        ]
        
        unit_name = self.unit.name.lower()
        
        # Check if this is a "no scale" unit
        if any(no_scale_unit in unit_name for no_scale_unit in no_scale_units):
            return self.unit.name  # Just return the unit name without scaling
        
        # For normal units, show scaled quantity + unit
        scaled_qty = self.get_scaled_quantity(scale_factor)
        return f"{scaled_qty} {self.unit.abbreviation}"
        """Return quantity scaled by a factor"""
        scaled = self.quantity * scale_factor
        if scaled == int(scaled):
            return str(int(scaled))
        else:
            return str(scaled).rstrip('0').rstrip('.')

    def get_american_conversion(self, scale_factor=1.0):
        """Convert metric units to American equivalents where possible"""
        scaled_quantity = float(self.quantity) * scale_factor
        
        # Conversion mappings (metric to american)
        conversions = {
            # Volume conversions
            'ml': {250: ('cup', 1), 500: ('cups', 2), 1000: ('cups', 4)},
            'milliliter': {250: ('cup', 1), 500: ('cups', 2), 1000: ('cups', 4)},
            'liter': {1: ('cups', 4.2)},
            'l': {1: ('cups', 4.2)},
            
            # Weight conversions  
            'gram': {450: ('lb', 1), 225: ('½ lb', 0.5), 900: ('lbs', 2)},
            'g': {450: ('lb', 1), 225: ('½ lb', 0.5), 900: ('lbs', 2)},
            'kilogram': {1: ('lbs', 2.2), 0.5: ('lb', 1.1)},
            'kg': {1: ('lbs', 2.2), 0.5: ('lb', 1.1)},
            
            # Temperature (if ever needed)
            'celsius': {200: ('°F', 400), 180: ('°F', 350), 220: ('°F', 425)},
        }
        
        unit_name = self.unit.name.lower()
        
        # Try exact conversions first
        if unit_name in conversions:
            for metric_amount, (us_unit, us_amount) in conversions[unit_name].items():
                if abs(scaled_quantity - metric_amount) < 0.1:
                    return f"{us_amount} {us_unit}"
        
        # Common volume conversions
        if unit_name in ['ml', 'milliliter']:
            if scaled_quantity >= 1000:
                cups = scaled_quantity / 240  # 1 cup ≈ 240ml
                if cups == int(cups):
                    return f"{int(cups)} cup{'s' if cups > 1 else ''}"
                else:
                    return f"{cups:.1f} cup{'s' if cups > 1 else ''}"
            elif scaled_quantity >= 250:
                return f"{scaled_quantity/240:.1f} cups"
            elif scaled_quantity >= 15:
                tbsp = scaled_quantity / 15  # 1 tbsp ≈ 15ml
                return f"{tbsp:.1f} tbsp"
            elif scaled_quantity >= 5:
                tsp = scaled_quantity / 5  # 1 tsp ≈ 5ml
                return f"{tsp:.1f} tsp"
        
        # Common weight conversions
        elif unit_name in ['gram', 'g']:
            if scaled_quantity >= 450:
                lbs = scaled_quantity / 453.6
                return f"{lbs:.1f} lb{'s' if lbs > 1 else ''}"
            elif scaled_quantity >= 28:
                oz = scaled_quantity / 28.35
                return f"{oz:.1f} oz"
        
        # If no conversion found, return original with scale
        return f"{self.get_scaled_quantity(scale_factor)} {self.unit.abbreviation}"

    class Meta:
        ordering = ['order']


class RecipeStep(models.Model):
    """Individual steps in a recipe"""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='steps')
    step_number = models.PositiveIntegerField()
    instruction = models.TextField(
        max_length=2000,  # Reasonable step instruction length
        help_text='Step instruction (max 2000 characters)'
    )

    # Cloudinary field for step images
    image = CloudinaryField(
        'image', 
        blank=True, 
        null=True,
        folder='recipe_steps/',
        help_text='Upload step image'
    )
    
    # Keep URL field as fallback
    image_url = models.URLField(blank=True, help_text='Or paste image URL')

    def __str__(self):
        return f"{self.recipe.title} - Step {self.step_number}"
    
    def get_image_url(self):
        """Get image URL - prioritize Cloudinary, fallback to URL field"""
        if self.image:
            try:
                return self.image.url
            except Exception:
                # Fallback if Cloudinary config is dummy/invalid
                if self.image_url:
                    return self.image_url
                return None
        elif self.image_url:
            return self.image_url
        return None
 
    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')


class Rating(models.Model):
    """User ratings for recipes (1-5 stars)."""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = (self.recipe.title[:20] + "..."
                 if len(self.recipe.title) > 20
                 else self.recipe.title)
        return f"{self.user.username} rated {title}: {self.rating}/5"

    class Meta:
        unique_together = ('recipe', 'user')
        ordering = ['-created_at']


class Comment(models.Model):
    """User comments/reviews for recipes."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(
        max_length=1500,  # Reasonable comment length
        help_text='Share your experience with this recipe (max 1500 characters)'
    )
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Reply to another comment'
    )
    is_approved = models.BooleanField(
        default=False,
        help_text='Admin approval required before comment is visible to public'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        title = (self.recipe.title[:20] + "..."
                 if len(self.recipe.title) > 20
                 else self.recipe.title)
        comment_type = "replied to" if self.parent_comment else "commented on"
        approval_status = " (pending)" if not self.is_approved else ""
        return f"{self.user.username} {comment_type} {title}{approval_status}"

    @property
    def is_reply(self):
        """Check if this is a reply to another comment"""
        return self.parent_comment is not None

    @property
    def status_display(self):
        """Display status for admin"""
        return "Approved" if self.is_approved else "Pending Approval"


class Follow(models.Model):
    """Users following other users"""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']


class RecipeLike(models.Model):
    """Users liking recipes"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"

    class Meta:
        unique_together = ('user', 'recipe')
        ordering = ['-created_at']
