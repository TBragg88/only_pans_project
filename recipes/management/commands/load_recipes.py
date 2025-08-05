from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import (
    Recipe, Tag, Ingredient, Unit, RecipeIngredient, RecipeStep
)
import json


class Command(BaseCommand):
    help = 'Load recipes from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get or create a default user
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@onlypans.com',
                    'first_name': 'Admin',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            if created:
                user.set_password('admin123')
                user.save()
                self.stdout.write('Created admin user')
            
            recipes_created = 0
            
            # Process each recipe
            for recipe_data in data:
                # Create recipe
                recipe = Recipe.objects.create(
                    title=recipe_data.get('title', ''),
                    description=recipe_data.get('description', ''),
                    prep_time=recipe_data.get('prep_time', 15),
                    cook_time=recipe_data.get('cook_time', 30),
                    servings=recipe_data.get('servings', 4),
                    user=user
                )
                
                # Add ingredients
                if 'ingredients' in recipe_data:
                    ingredients = recipe_data.get('ingredients', [])
                    for i, ing_data in enumerate(ingredients, 1):
                        # Get or create ingredient
                        ingredient, _ = Ingredient.objects.get_or_create(
                            name=ing_data.get('name', ''),
                            defaults={'category': 'other'}
                        )
                        
                        # Get or create unit
                        unit, _ = Unit.objects.get_or_create(
                            name=ing_data.get('unit', 'pieces'),
                            defaults={
                                'abbreviation': ing_data.get('unit', 'pcs')
                            }
                        )
                        
                        # Create recipe ingredient
                        RecipeIngredient.objects.create(
                            recipe=recipe,
                            ingredient=ingredient,
                            quantity=ing_data.get('quantity', 1),
                            unit=unit,
                            order=i
                        )
                
                # Add steps
                if 'instructions' in recipe_data:
                    instructions = recipe_data['instructions']
                    for i, step_text in enumerate(instructions, 1):
                        RecipeStep.objects.create(
                            recipe=recipe,
                            step_number=i,
                            instruction=step_text
                        )
                
                # Add tags
                if 'tags' in recipe_data:
                    for tag_name in recipe_data['tags']:
                        tag, _ = Tag.objects.get_or_create(
                            name=tag_name,
                            defaults={
                                'tag_type': 'cuisine',
                                'color': '#007bff'
                            }
                        )
                        recipe.tags.add(tag)
                
                # Add difficulty as a tag if provided
                if 'difficulty' in recipe_data:
                    difficulty_tag, _ = Tag.objects.get_or_create(
                        name=recipe_data['difficulty'].title(),
                        defaults={
                            'tag_type': 'difficulty',
                            'color': '#28a745'
                        }
                    )
                    recipe.tags.add(difficulty_tag)
                
                recipes_created += 1
                self.stdout.write(f'Created recipe: {recipe.title}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {recipes_created} recipes'
                )
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file}')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON in file: {json_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading recipes: {str(e)}')
            )
