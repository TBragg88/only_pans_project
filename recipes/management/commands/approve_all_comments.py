"""
Management command to approve all existing comments
"""
from django.core.management.base import BaseCommand
from recipes.models import Comment


class Command(BaseCommand):
    help = 'Approve all existing comments (useful for migration)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        unapproved_comments = Comment.objects.filter(is_approved=False)
        count = unapproved_comments.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No unapproved comments found.')
            )
            return

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would approve {count} comments'
                )
            )
            for comment in unapproved_comments[:10]:  # Show first 10
                self.stdout.write(f'  - {comment.user.username}: {comment.content[:50]}...')
            if count > 10:
                self.stdout.write(f'  ... and {count - 10} more')
        else:
            unapproved_comments.update(is_approved=True)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully approved {count} comments!'
                )
            )
