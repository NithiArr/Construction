import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_cms.settings')
django.setup()

from django.contrib.auth import authenticate
from users.models import User

# Test with the known user
email = "accountant@tsconst.com"
password = "password123" # I need to know the password to test, but I can't know it for sure.
# Wait, I don't know the user's password. 
# But I can check if the hasher is even CALLED.

print(f"Testing auth for {email}")
try:
    user = User.objects.get(email=email)
    print(f"User found: {user.email}")
    print(f"Stored hash: {user.password}")
    
    # Check if hasher is recognized
    from django.contrib.auth.hashers import check_password, get_hasher
    hasher = get_hasher(user.password)
    print(f"Hasher for password: {hasher.algorithm}")
    
except User.DoesNotExist:
    print("User not found")
except Exception as e:
    print(f"Error: {e}")
