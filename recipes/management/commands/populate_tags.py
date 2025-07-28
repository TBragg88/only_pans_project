# recipes/management/commands/populate_tags.py
from django.core.management.base import BaseCommand
from recipes.models import Tag

class Command(BaseCommand):
    help = 'Populate the database with default tags for recipes'

    def handle(self, *args, **options):
        default_tags = [
            "British", "Quick", "Vegetarian", "Comfort Food",
            "Breakfast", "Protein",
            "Italian", "Dinner",
            "Dessert", "Baking", "Sweet", "American",
            "Salad", "Roman", "Starter",
            "Asian", "Healthy"
        ]

        self.stdout.write("Starting tag population...")
        created_count = 0
        existing_count = 0
        for tag_name in set(default_tags):
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created tag: {tag_name}"))
            else:
                existing_count += 1
                self.stdout.write(f"- Tag already exists: {tag_name}")
        self.stdout.write(f"\nDone! Created {created_count} new tags, {existing_count} already existed.")
        self.stdout.write(self.style.SUCCESS("Your tag database is now ready for recipes!"))
