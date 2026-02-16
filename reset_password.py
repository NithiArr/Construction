import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_cms.settings')
django.setup()

from users.models import User

try:
    user = User.objects.get(email="accountant@tsconst.com")
    user.set_password("admin123")
    user.save()
    print(f"Password for {user.email} reset to 'admin123'")
except User.DoesNotExist:
    # Try creating it if it doesn't exist (unlikely with migration success)
    print("User not found.")
except Exception as e:
    print(f"Error: {e}")
