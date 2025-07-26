# Create this directory structure in your recipes app:
# recipes/
#   management/
#     __init__.py
#     commands/
#       __init__.py
#       populate_ingredients.py

# recipes/management/commands/populate_ingredients.py
import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Populate the database with common ingredients'

    def handle(self, *args, **options):
        # Complete ingredient data with ALL nutritional fields
        # Format: (name, category, unit, dietary_flags_list, calories, protein, carbs, fat, fiber, sugars, sodium_mg, sat_fat)
        ingredients_data = [
            # Produce
            ('Carrots', 'produce', 'grams', [], 41, 0.9, 9.6, 0.2, 2.8, 4.7, 69, 0.04),
            ('Onions', 'produce', 'grams', [], 40, 1.1, 9.3, 0.1, 1.7, 4.2, 4, 0.04),
            ('Garlic', 'produce', 'grams', [], 149, 6.4, 33, 0.5, 2.1, 1, 17, 0.09),
            ('Tomatoes', 'produce', 'grams', [], 18, 0.9, 3.9, 0.2, 1.2, 2.6, 5, 0.03),
            ('Potatoes', 'produce', 'grams', [], 77, 2.0, 17, 0.1, 2.2, 0.8, 6, 0.03),
            ('Bell Peppers', 'produce', 'grams', [], 31, 1.0, 7, 0.3, 2.5, 4.2, 4, 0.07),
            ('Spinach', 'produce', 'grams', [], 23, 2.9, 3.6, 0.4, 2.2, 0.4, 79, 0.06),
            ('Broccoli', 'produce', 'grams', [], 34, 2.8, 7, 0.4, 2.6, 1.5, 33, 0.06),
            ('Mushrooms', 'produce', 'grams', [], 22, 3.1, 3.3, 0.3, 1.0, 2.0, 5, 0.05),
            ('Lettuce', 'produce', 'grams', [], 15, 1.4, 2.9, 0.2, 1.3, 0.8, 28, 0.03),
            
            # Meat & Protein
            ('Chicken Breast', 'meat', 'grams', [], 165, 31, 0, 3.6, 0, 0, 74, 1.0),
            ('Ground Beef', 'meat', 'grams', [], 250, 26, 0, 15, 0, 0, 78, 6.1),
            ('Salmon', 'fish', 'grams', [], 208, 22, 0, 12, 0, 0, 48, 1.9),
            ('Eggs', 'protein', 'pieces', [], 155, 13, 1.1, 11, 0, 0.7, 124, 3.1),
            ('Bacon', 'meat', 'grams', [], 541, 37, 1.4, 42, 0, 0, 1717, 13.5),
            ('Tuna', 'fish', 'grams', [], 132, 28, 0, 0.6, 0, 0, 50, 0.2),
            
            # Dairy
            ('Milk', 'dairy', 'ml', ['dairy'], 64, 3.2, 4.8, 3.6, 0, 5.1, 44, 2.3),
            ('Butter', 'dairy', 'grams', ['dairy'], 717, 0.9, 0.1, 81, 0, 0.1, 11, 51),
            ('Cheddar Cheese', 'dairy', 'grams', ['dairy'], 403, 25, 1.3, 33, 0, 0.5, 653, 21),
            ('Yogurt', 'dairy', 'grams', ['dairy'], 61, 3.5, 4.7, 3.3, 0, 4.7, 36, 2.1),
            ('Heavy Cream', 'dairy', 'ml', ['dairy'], 340, 2.8, 2.8, 36, 0, 2.9, 38, 23),
            
            # Grains & Starches  
            ('Rice', 'grains', 'grams', [], 365, 7.1, 80, 0.7, 1.3, 0.1, 5, 0.2),
            ('Pasta', 'grains', 'grams', ['gluten'], 371, 13, 74, 1.5, 3.2, 2.7, 6, 0.3),
            ('Bread', 'grains', 'slices', ['gluten'], 265, 9, 49, 3.2, 2.7, 5.7, 491, 0.6),
            ('Flour', 'baking', 'grams', ['gluten'], 364, 10, 76, 1.0, 2.7, 0.3, 2, 0.2),
            ('Oats', 'grains', 'grams', [], 389, 17, 66, 7, 10.6, 0.99, 2, 1.2),
            
            # Pantry Staples
            ('Olive Oil', 'oils', 'ml', [], 884, 0, 0, 100, 0, 0, 2, 14),
            ('Salt', 'seasonings', 'grams', [], 0, 0, 0, 0, 0, 0, 38758, 0),
            ('Black Pepper', 'spices', 'grams', [], 251, 10, 64, 3.3, 25, 0.6, 20, 1.4),
            ('Sugar', 'baking', 'grams', [], 387, 0, 100, 0, 0, 99.8, 1, 0),
            ('Honey', 'sweeteners', 'grams', [], 304, 0.3, 82, 0, 0.2, 82.4, 4, 0),
            
            # Herbs & Spices
            ('Basil', 'herbs', 'grams', [], 22, 3.2, 2.6, 0.6, 1.6, 0.3, 4, 0.04),
            ('Oregano', 'herbs', 'grams', [], 265, 9, 69, 4.3, 42.5, 4.1, 25, 1.6),
            ('Thyme', 'herbs', 'grams', [], 276, 9.1, 64, 7.4, 37, 1.7, 9, 4.9),
            ('Paprika', 'spices', 'grams', [], 282, 14, 54, 13, 37, 10, 68, 2.1),
            ('Cumin', 'spices', 'grams', [], 375, 18, 44, 22, 11, 2.2, 168, 1.5),
            ('Garlic Powder', 'spices', 'grams', [], 331, 16, 73, 0.7, 9, 2.4, 599, 0.2),
            
            # Condiments
            ('Soy Sauce', 'condiments', 'ml', ['soy'], 8, 1.3, 0.8, 0, 0.1, 0.4, 5493, 0),
            ('Lemon Juice', 'condiments', 'ml', [], 22, 0.4, 6.9, 0.2, 0.3, 1.4, 2, 0.04),
            ('Vinegar', 'condiments', 'ml', [], 18, 0, 0.04, 0, 0, 0.04, 2, 0),
            ('Mustard', 'condiments', 'grams', [], 66, 4.4, 7.1, 3.3, 3.3, 2.8, 1135, 0.2),
        ]

        self.stdout.write("Starting ingredient population...")
        
        created_count = 0
        existing_count = 0

        for name, category, unit, dietary_flags_list, calories, protein, carbs, fat, fiber, sugars, sodium_mg, sat_fat in ingredients_data:
            # Convert dietary flags list to JSON string
            dietary_flags_json = json.dumps(dietary_flags_list)
            
            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'common_unit': unit,
                    'dietary_flags': dietary_flags_json,
                    'calories_per_100g': calories,
                    'protein_per_100g': protein,
                    'carbs_per_100g': carbs,
                    'fat_per_100g': fat,
                    'fibre_per_100g': fiber,
                    'sugars_per_100g': sugars,
                    'sodium_mg_per_100g': sodium_mg,
                    'saturated_fat_per_100g': sat_fat,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created: {name}"))
            else:
                existing_count += 1
                self.stdout.write(f"- Already exists: {name}")

        self.stdout.write(f"\nDone! Created {created_count} new ingredients, {existing_count} already existed.")
        self.stdout.write(self.style.SUCCESS("Your ingredient database is now ready for recipes!"))