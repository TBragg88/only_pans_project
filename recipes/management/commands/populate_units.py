# recipes/management/commands/populate_units.py
from django.core.management.base import BaseCommand
from recipes.models import Unit

class Command(BaseCommand):
    help = 'Populate the database with common units of measurement'

    def handle(self, *args, **options):
        units_data = [
            # Volume units
            ('Cup', 'cup', 'volume'),
            ('Tablespoon', 'tbsp', 'volume'),
            ('Teaspoon', 'tsp', 'volume'),
            ('Milliliter', 'ml', 'volume'),
            ('Liter', 'L', 'volume'),
            ('Fluid Ounce', 'fl oz', 'volume'),
            ('Pint', 'pt', 'volume'),
            ('Quart', 'qt', 'volume'),
            
            # Weight units
            ('Gram', 'g', 'weight'),
            ('Kilogram', 'kg', 'weight'),
            ('Ounce', 'oz', 'weight'),
            ('Pound', 'lb', 'weight'),
            
            # Count units
            ('Piece', 'pc', 'count'),
            ('Each', 'each', 'count'),
            ('Slice', 'slice', 'count'),
            ('Clove', 'clove', 'count'),
            ('Bunch', 'bunch', 'count'),
            ('Package', 'pkg', 'count'),
            ('Can', 'can', 'count'),
            
            # Special units
            ('Pinch', 'pinch', 'volume'),
            ('Dash', 'dash', 'volume'),
            ('To taste', 'to taste', 'volume'),
        ]

        self.stdout.write("Starting units population...")
        
        created_count = 0
        existing_count = 0

        for name, abbreviation, unit_type in units_data:
            unit, created = Unit.objects.get_or_create(
                name=name,
                defaults={
                    'abbreviation': abbreviation,
                    'unit_type': unit_type,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created: {name} ({abbreviation})"))
            else:
                existing_count += 1
                self.stdout.write(f"- Already exists: {name}")

        self.stdout.write(f"\nDone! Created {created_count} new units, {existing_count} already existed.")
        self.stdout.write(self.style.SUCCESS("Your units database is now ready!"))