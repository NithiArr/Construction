import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_cms.settings')
django.setup()

from users.models import User

# Get the first user
user = User.objects.first()
print(f"Email: {user.email}")
print(f"Password Hash: {user.password}")
