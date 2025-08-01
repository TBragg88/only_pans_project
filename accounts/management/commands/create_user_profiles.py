"""
Management command to create user profiles for existing users.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Create user profiles for existing users who do not have profiles'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        created_count = 0
        
        for user in users_without_profiles:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created profile for user: {user.username}'
                    )
                )
        
        if created_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {created_count} user profiles.'
                )
            )
