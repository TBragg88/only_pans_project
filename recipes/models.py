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

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

    class Meta:
        ordering = ['unit_type', 'name']


class Recipe(models.Model):
    """Main recipe model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='recipes')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True,
                                   help_text='Tell us about this recipe!')

    # Timing
    prep_time = models.PositiveIntegerField(
        help_text='Preparation time in minutes'
    )
    cook_time = models.PositiveIntegerField(
        help_text='Cooking time in minutes'
    )
    servings = models.PositiveIntegerField(default=4)

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
        return reverse('recipe_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        """Get image URL - prioritize Cloudinary, fallback to URL field"""
        if self.image:
            try:
                return self.image.url
            except Exception:
                # Fallback if Cloudinary config is dummy/invalid
                if self.image_url:
                    return self.image_url
                return 'https://via.placeholder.com/400x300?text=Recipe+Image'
        elif self.image_url:
            return self.image_url
        return 'https://via.placeholder.com/400x300?text=Recipe+Image'

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
        
        for recipe_ingredient in self.recipeingredient_set.all():
            if recipe_ingredient.ingredient:
                # Convert quantity to grams (assuming most quantities are in grams)
                quantity_in_grams = recipe_ingredient.quantity
                
                # Calculate nutrition based on quantity
                if recipe_ingredient.ingredient.calories_per_100g:
                    total_calories += (quantity_in_grams / 100) * float(recipe_ingredient.ingredient.calories_per_100g)
                if recipe_ingredient.ingredient.protein_per_100g:
                    total_protein += (quantity_in_grams / 100) * float(recipe_ingredient.ingredient.protein_per_100g)
                if recipe_ingredient.ingredient.carbs_per_100g:
                    total_carbs += (quantity_in_grams / 100) * float(recipe_ingredient.ingredient.carbs_per_100g)
                if recipe_ingredient.ingredient.fat_per_100g:
                    total_fat += (quantity_in_grams / 100) * float(recipe_ingredient.ingredient.fat_per_100g)
        
        # Divide by servings
        servings = self.servings or 1
        return {
            'calories': round(total_calories / servings, 1),
            'protein': round(total_protein / servings, 1),
            'carbs': round(total_carbs / servings, 1),
            'fat': round(total_fat / servings, 1),
        }

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

    class Meta:
        ordering = ['order']


class RecipeStep(models.Model):
    """Individual steps in a recipe"""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='steps')
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()

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
        help_text='Share your experience with this recipe'
    )
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Reply to another comment'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = (self.recipe.title[:20] + "..."
                 if len(self.recipe.title) > 20
                 else self.recipe.title)
        comment_type = "replied to" if self.parent_comment else "commented on"
        return f"{self.user.username} {comment_type} {title}"

    @property
    def is_reply(self):
        """Check if this is a reply to another comment"""
        return self.parent_comment is not None

    class Meta:
        ordering = ['-created_at']
