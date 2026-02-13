"""
Create initial admin user for MongoDB
Run this script to create the first admin user in your system
"""
import os
from dotenv import load_dotenv
from mongoengine import connect
from models_mongo import Company, User

# Load environment variables
load_dotenv()

def create_admin():
    """Create initial admin user and company"""
    
    # Connect to MongoDB
    mongodb_host = os.environ.get('MONGODB_HOST', 'mongodb://localhost:27017/construction_db')
    print(f"Connecting to MongoDB...")
    connect(host=mongodb_host)
    print("Connected successfully!")
    
    # Create company
    company_name = input("\nEnter company name: ")
    company_email = input("Enter company email: ")
    company_phone = input("Enter company phone: ")
    
    company = Company(
        name=company_name,
        email=company_email,
        phone=company_phone
    )
    company.save()
    print(f"\n✓ Company '{company_name}' created successfully!")
    
    # Create admin user
    admin_name = input("\nEnter admin name: ")
    admin_email = input("Enter admin email: ")
    admin_password = input("Enter admin password: ")
    
    admin = User(
        company=company,
        name=admin_name,
        email=admin_email,
        role='ADMIN'
    )
    admin.set_password(admin_password)
    admin.save()
    
    print(f"\n✓ Admin user '{admin_name}' created successfully!")
    print(f"\nCompany ID: {company.id}")
    print(f"Admin User ID: {admin.id}")
    print(f"\nYou can now login with:")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_password}")
    print("\nIMPORTANT: Save these credentials securely!")

if __name__ == '__main__':
    print("=" * 50)
    print("Construction Management System")
    print("Initial Admin Setup")
    print("=" * 50)
    
    try:
        create_admin()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
