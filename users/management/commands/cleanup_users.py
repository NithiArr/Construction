from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Delete all users except admin@sorgavasal.com and set that user role to ADMIN'

    def handle(self, *args, **options):
        keep_email = 'admin@sorgavasal.com'

        # Delete all users except the admin
        deleted_users = User.objects.exclude(email=keep_email)
        count = deleted_users.count()
        deleted_users.delete()
        self.stdout.write(self.style.WARNING(f'Deleted {count} user(s).'))

        # Update the admin user
        try:
            admin = User.objects.get(email=keep_email)
            admin.role = 'ADMIN'
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                f'User "{admin.email}" (name: {admin.name}) role set to ADMIN.'
            ))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'User "{keep_email}" not found! No admin user was configured.'
            ))

        self.stdout.write(self.style.SUCCESS('Cleanup complete.'))
