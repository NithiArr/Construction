#!/usr/bin/env python3
"""
Password Reset Script for MongoDB
"""

import os
from dotenv import load_dotenv
from mongoengine import connect
from models_mongo import User

load_dotenv()

print("=" * 60)
print("Password Reset Script")
print("=" * 60)

# Connect to MongoDB
print("\nConnecting to MongoDB...")
mongodb_uri = os.environ.get('MONGODB_HOST', 'mongodb://mongodb:27017/construction_db')
connect(host=mongodb_uri)
print("✓ Connected to MongoDB")

# Get user email
print("\nAvailable users:")
users = User.objects.all()
for i, user in enumerate(users, 1):
    print(f"{i}. {user.email} ({user.role})")

email = input("\nEnter email address to reset password: ").strip()

# Find user
user = User.objects(email=email).first()
if not user:
    print(f"\n❌ Error: User with email '{email}' not found!")
    exit(1)

print(f"\n✓ Found user: {user.name} ({user.role})")

# Get new password
new_password = input("Enter new password: ").strip()
confirm_password = input("Confirm new password: ").strip()

if new_password != confirm_password:
    print("\n❌ Error: Passwords do not match!")
    exit(1)

if len(new_password) < 6:
    print("\n❌ Error: Password must be at least 6 characters!")
    exit(1)

# Set new password
user.set_password(new_password)
user.save()

print("\n" + "=" * 60)
print("✅ Password reset successfully!")
print("=" * 60)
print(f"\nYou can now login with:")
print(f"  Email: {user.email}")
print(f"  Password: {new_password}")
print(f"\n🌐 Access your app at: http://localhost:8080")
