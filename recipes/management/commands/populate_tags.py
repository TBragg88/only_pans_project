# recipes/management/commands/populate_tags.py
from django.core.management.base import BaseCommand
from recipes.models import Tag

class Command(BaseCommand):
    help = 'Populate the database with predefined tags for recipes'

    def handle(self, *args, **options):
        # Define comprehensive tag sets with colors for each category
        tags_data = [
            # Dietary tags - Green tones
            ('dietary', 'Vegetarian', '#28a745'),
            ('dietary', 'Vegan', '#20c997'),
            ('dietary', 'Gluten-Free', '#17a2b8'),
            ('dietary', 'Dairy-Free', '#6f42c1'),
            ('dietary', 'Nut-Free', '#fd7e14'),
            ('dietary', 'Keto', '#e83e8c'),
            ('dietary', 'Low-Carb', '#6610f2'),
            ('dietary', 'Paleo', '#795548'),
            ('dietary', 'Sugar-Free', '#f8f9fa'),
            ('dietary', 'Low-Sodium', '#6c757d'),
            ('dietary', 'Heart-Healthy', '#dc3545'),
            ('dietary', 'Diabetic-Friendly', '#ffc107'),
            
            # Cuisine tags - Blue tones
            ('cuisine', 'Italian', '#007bff'),
            ('cuisine', 'Mexican', '#fd7e14'),
            ('cuisine', 'Chinese', '#dc3545'),
            ('cuisine', 'Indian', '#ffc107'),
            ('cuisine', 'Thai', '#20c997'),
            ('cuisine', 'Japanese', '#e83e8c'),
            ('cuisine', 'French', '#6610f2'),
            ('cuisine', 'Greek', '#17a2b8'),
            ('cuisine', 'American', '#6c757d'),
            ('cuisine', 'Mediterranean', '#28a745'),
            ('cuisine', 'Korean', '#fd7e14'),
            ('cuisine', 'Middle Eastern', '#795548'),
            ('cuisine', 'Spanish', '#ffc107'),
            ('cuisine', 'German', '#6c757d'),
            ('cuisine', 'British', '#17a2b8'),
            ('cuisine', 'Vietnamese', '#20c997'),
            ('cuisine', 'Moroccan', '#e83e8c'),
            ('cuisine', 'Brazilian', '#28a745'),
            ('cuisine', 'Caribbean', '#fd7e14'),
            ('cuisine', 'Russian', '#6610f2'),
            
            # Meal type tags - Orange/Yellow tones
            ('meal_type', 'Breakfast', '#ffc107'),
            ('meal_type', 'Lunch', '#fd7e14'),
            ('meal_type', 'Dinner', '#dc3545'),
            ('meal_type', 'Snack', '#20c997'),
            ('meal_type', 'Dessert', '#e83e8c'),
            ('meal_type', 'Appetizer', '#17a2b8'),
            ('meal_type', 'Side Dish', '#6c757d'),
            ('meal_type', 'Beverage', '#28a745'),
            ('meal_type', 'Brunch', '#6610f2'),
            ('meal_type', 'Late Night', '#495057'),
            
            # Cooking method tags - Purple tones
            ('cooking_method', 'Baking', '#6610f2'),
            ('cooking_method', 'Grilling', '#dc3545'),
            ('cooking_method', 'Roasting', '#fd7e14'),
            ('cooking_method', 'Sautéing', '#28a745'),
            ('cooking_method', 'Steaming', '#17a2b8'),
            ('cooking_method', 'Frying', '#ffc107'),
            ('cooking_method', 'Slow Cooking', '#6c757d'),
            ('cooking_method', 'Pressure Cooking', '#e83e8c'),
            ('cooking_method', 'No Cook', '#20c997'),
            ('cooking_method', 'One Pot', '#795548'),
            ('cooking_method', 'Air Frying', '#6610f2'),
            ('cooking_method', 'Smoking', '#495057'),
            ('cooking_method', 'Braising', '#fd7e14'),
            ('cooking_method', 'Poaching', '#17a2b8'),
            
            # Difficulty tags - Red to Green gradient
            ('difficulty', 'Beginner', '#28a745'),
            ('difficulty', 'Easy', '#20c997'),
            ('difficulty', 'Intermediate', '#ffc107'),
            ('difficulty', 'Advanced', '#fd7e14'),
            ('difficulty', 'Expert', '#dc3545'),
        ]

        created_count = 0
        updated_count = 0

        for tag_type, name, color in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=name,
                defaults={
                    'tag_type': tag_type,
                    'color': color
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created tag: {name} ({tag_type})')
                )
            else:
                # Update color if it has changed
                if tag.color != color or tag.tag_type != tag_type:
                    tag.color = color
                    tag.tag_type = tag_type
                    tag.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated tag: {name} ({tag_type})')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nTag population complete!\n'
                f'Created: {created_count} tags\n'
                f'Updated: {updated_count} tags\n'
                f'Total tags in database: {Tag.objects.count()}'
            )
        )

        # Show summary by category
        self.stdout.write('\nTags by category:')
        for tag_type_code, tag_type_name in Tag.TAG_TYPES:
            count = Tag.objects.filter(tag_type=tag_type_code).count()
            self.stdout.write(f'  {tag_type_name}: {count} tags')
