"""
Quick setup script for Local Store E-commerce Platform
Run this script to set up the project quickly
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("Local Store E-commerce Platform - Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Create media directory
    if not os.path.exists('media'):
        os.makedirs('media')
        print("\n✓ Created media directory")
    else:
        print("\n✓ Media directory already exists")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("\nWarning: Failed to install dependencies. Please run: pip install -r requirements.txt")
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("\nWarning: Failed to create migrations")
    
    if not run_command("python manage.py migrate", "Running migrations"):
        print("\nWarning: Failed to run migrations")
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000/")
    print("4. Login to admin at http://127.0.0.1:8000/admin/ to add products")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
