#!/usr/bin/env python
"""
Build script for Vercel deployment
This script is run during the build phase to collect static files
"""
import os
import subprocess

def build():
    """Run Django collectstatic command."""
    print("Starting build process...")
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    
    # Collect static files
    print("Collecting static files...")
    subprocess.run(["python", "manage.py", "collectstatic", "--noinput", "--clear"], check=True)
    
    print("Build completed successfully!")

if __name__ == "__main__":
    build()
