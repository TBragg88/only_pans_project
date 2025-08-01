# recipes/management/commands/populate_unit_conversions.py
from django.core.management.base import BaseCommand
from recipes.models import Unit


class Command(BaseCommand):
    help = 'Populate units with gram conversion values'

    def handle(self, *args, **options):
        # Weight conversions (exact)
        weight_conversions = {
            'Grams': 1,
            'Kilograms': 1000,
            'Pounds': 453.592,
            'Ounces': 28.3495,
        }

        # Volume conversions (approximate, assuming water-like density)
        volume_conversions = {
            'Cup': 240,  # 1 cup ≈ 240ml ≈ 240g (for water)
            'Tablespoon': 15,  # 1 tbsp ≈ 15ml ≈ 15g
            'Teaspoon': 5,  # 1 tsp ≈ 5ml ≈ 5g
            'Milliliter': 1,  # 1ml ≈ 1g (for water)
            'Liter': 1000,  # 1L ≈ 1000g
            'Fluid Ounce': 30,  # 1 fl oz ≈ 30ml ≈ 30g
            'Pint': 473,  # 1 US pint ≈ 473ml
            'Quart': 946,  # 1 US quart ≈ 946ml
        }

        # Count conversions (approximate average weights)
        count_conversions = {
            'Can': 400,  # Standard can (400g)
            'Jar': 250,  # Small jar
            'Package': 200,  # Average package
            'Bottle': 330,  # Standard bottle
            'Each': 100,  # Generic item
            'Piece': 50,  # Generic piece
            'Slice': 25,  # Bread slice
            'Clove': 3,  # Garlic clove
            'Bunch': 150,  # Herbs/vegetables
            'Head': 500,  # Lettuce/cabbage
            'Whole': 1000,  # Whole chicken/fish
            'Egg': 50,  # Large egg
            'Breast': 200,  # Chicken breast
            'Fillet': 150,  # Fish fillet
        }

        all_conversions = {**weight_conversions, **volume_conversions, **count_conversions}

        updated_count = 0
        for unit in Unit.objects.all():
            if unit.name in all_conversions:
                unit.grams_per_unit = all_conversions[unit.name]
                unit.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated {unit.name}: {unit.grams_per_unit}g per unit'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'No conversion found for unit: {unit.name}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} units with conversion values'
            )
        )
