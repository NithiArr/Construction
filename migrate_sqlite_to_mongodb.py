#!/usr/bin/env python3
"""
SQLite to MongoDB Migration Script
Migrates all data from SQLite database to MongoDB
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLAlchemy imports (for reading SQLite)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Create Flask app for SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/construction.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db FIRST before importing models
db_sqlite = SQLAlchemy(app)

# Now set models.db to our db_sqlite instance
import models
models.db = db_sqlite  # Use the same db instance

# MongoEngine imports (for writing to MongoDB)
from mongoengine import connect
from models_mongo import Company, User, Project, Vendor, Expense, ExpenseItem, Payment, ClientPayment

print("=" * 60)
print("SQLite to MongoDB Migration Script")
print("=" * 60)

def migrate_data():
    """Main migration function"""
    
    # Connect to MongoDB
    print("\n[1/9] Connecting to MongoDB...")
    mongodb_uri = os.environ.get('MONGODB_HOST', 'mongodb://mongodb:27017/construction_db')
    connect(host=mongodb_uri)
    print("✓ Connected to MongoDB")
    
    # Clear existing MongoDB data (optional - comment out if you want to keep existing data)
    print("\n[2/9] Clearing existing MongoDB data...")
    Company.drop_collection()
    User.drop_collection()
    Project.drop_collection()
    Vendor.drop_collection()
    Expense.drop_collection()
    Payment.drop_collection()
    ClientPayment.drop_collection()
    print("✓ MongoDB collections cleared")
    
    # Create mappings for foreign keys
    company_map = {}  # old_id -> new MongoDB Company object
    user_map = {}
    project_map = {}
    vendor_map = {}
    expense_map = {}
    
    with app.app_context():
        # Migrate Companies
        print("\n[3/9] Migrating Companies...")
        old_companies = models.Company.query.all()
        for old_company in old_companies:
            new_company = Company(
                name=old_company.name,
                address=old_company.address,
                phone=old_company.phone,
                email=old_company.email,
                created_at=old_company.created_at
            )
            new_company.save()
            company_map[old_company.company_id] = new_company
            print(f"  ✓ Migrated company: {old_company.name}")
        print(f"✓ Migrated {len(old_companies)} companies")
        
        # Migrate Users
        print("\n[4/9] Migrating Users...")
        old_users = models.User.query.all()
        for old_user in old_users:
            new_company = company_map.get(old_user.company_id)
            if not new_company:
                print(f"  ⚠ Skipping user {old_user.email} - company not found")
                continue
                
            new_user = User(
                company=new_company,
                name=old_user.name,
                email=old_user.email,
                password_hash=old_user.password_hash,
                role=old_user.role,
                created_at=old_user.created_at
            )
            new_user.save()
            user_map[old_user.user_id] = new_user
            print(f"  ✓ Migrated user: {old_user.email} ({old_user.role})")
        print(f"✓ Migrated {len(old_users)} users")
        
        # Migrate Projects
        print("\n[5/9] Migrating Projects...")
        old_projects = models.Project.query.all()
        for old_project in old_projects:
            new_company = company_map.get(old_project.company_id)
            if not new_company:
                print(f"  ⚠ Skipping project {old_project.name} - company not found")
                continue
                
            new_project = Project(
                company=new_company,
                name=old_project.name,
                location=old_project.location,
                start_date=old_project.start_date,
                end_date=old_project.end_date,
                budget=old_project.budget,
                status=old_project.status,
                created_at=old_project.created_at
            )
            new_project.save()
            project_map[old_project.project_id] = new_project
            print(f"  ✓ Migrated project: {old_project.name}")
        print(f"✓ Migrated {len(old_projects)} projects")
        
        # Migrate Vendors
        print("\n[6/9] Migrating Vendors...")
        old_vendors = models.Vendor.query.all()
        for old_vendor in old_vendors:
            new_company = company_map.get(old_vendor.company_id)
            if not new_company:
                print(f"  ⚠ Skipping vendor {old_vendor.name} - company not found")
                continue
                
            new_vendor = Vendor(
                company=new_company,
                name=old_vendor.name,
                phone=old_vendor.phone,
                email=old_vendor.email,
                gst_number=old_vendor.gst_number,
                created_at=old_vendor.created_at
            )
            new_vendor.save()
            vendor_map[old_vendor.vendor_id] = new_vendor
            print(f"  ✓ Migrated vendor: {old_vendor.name}")
        print(f"✓ Migrated {len(old_vendors)} vendors")
        
        # Migrate Expenses (including purchases with items)
        print("\n[7/9] Migrating Expenses...")
        old_expenses = models.Expense.query.all()
        for old_expense in old_expenses:
            new_company = company_map.get(old_expense.company_id)
            new_project = project_map.get(old_expense.project_id)
            new_vendor = vendor_map.get(old_expense.vendor_id) if old_expense.vendor_id else None
            
            if not new_company or not new_project:
                print(f"  ⚠ Skipping expense - missing company or project")
                continue
            
            # Migrate expense items (if any)
            items = []
            if hasattr(old_expense, 'items') and old_expense.items:
                for old_item in old_expense.items:
                    item = ExpenseItem(
                        item_name=old_item.item_name,
                        quantity=old_item.quantity,
                        unit_price=old_item.unit_price,
                        total_price=old_item.total_price
                    )
                    items.append(item)
            
            new_expense = Expense(
                company=new_company,
                project=new_project,
                vendor=new_vendor,
                category=old_expense.category,
                subcategory=old_expense.subcategory,
                amount=old_expense.amount,
                payment_mode=old_expense.payment_mode,
                expense_date=old_expense.expense_date,
                description=old_expense.description,
                invoice_number=old_expense.invoice_number,
                bill_url=old_expense.bill_url,
                items=items,
                created_at=old_expense.created_at
            )
            new_expense.save()
            expense_map[old_expense.expense_id] = new_expense
            print(f"  ✓ Migrated expense: {old_expense.category} - ₹{old_expense.amount}")
        print(f"✓ Migrated {len(old_expenses)} expenses")
        
        # Migrate Vendor Payments
        print("\n[8/9] Migrating Vendor Payments...")
        old_payments = models.Payment.query.all()
        for old_payment in old_payments:
            new_company = company_map.get(old_payment.company_id)
            new_vendor = vendor_map.get(old_payment.vendor_id)
            new_project = project_map.get(old_payment.project_id)
            new_expense = expense_map.get(old_payment.expense_id) if old_payment.expense_id else None
            
            if not new_company or not new_vendor or not new_project:
                print(f"  ⚠ Skipping payment - missing company/vendor/project")
                continue
            
            new_payment = Payment(
                company=new_company,
                vendor=new_vendor,
                project=new_project,
                expense=new_expense,
                amount=old_payment.amount,
                payment_date=old_payment.payment_date,
                payment_mode=old_payment.payment_mode,
                created_at=old_payment.created_at
            )
            new_payment.save()
            print(f"  ✓ Migrated payment: ₹{old_payment.amount} to {new_vendor.name}")
        print(f"✓ Migrated {len(old_payments)} vendor payments")
        
        # Migrate Client Payments
        print("\n[9/9] Migrating Client Payments...")
        old_client_payments = models.ClientPayment.query.all()
        for old_cp in old_client_payments:
            new_company = company_map.get(old_cp.company_id)
            new_project = project_map.get(old_cp.project_id)
            
            if not new_company or not new_project:
                print(f"  ⚠ Skipping client payment - missing company/project")
                continue
            
            new_cp = ClientPayment(
                company=new_company,
                project=new_project,
                amount=old_cp.amount,
                payment_date=old_cp.payment_date,
                payment_mode=old_cp.payment_mode,
                reference_number=old_cp.reference_number,
                remarks=old_cp.remarks,
                created_at=old_cp.created_at
            )
            new_cp.save()
            print(f"  ✓ Migrated client payment: ₹{old_cp.amount}")
        print(f"✓ Migrated {len(old_client_payments)} client payments")
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Companies: {len(old_companies)}")
    print(f"  Users: {len(old_users)}")
    print(f"  Projects: {len(old_projects)}")
    print(f"  Vendors: {len(old_vendors)}")
    print(f"  Expenses: {len(old_expenses)}")
    print(f"  Vendor Payments: {len(old_payments)}")
    print(f"  Client Payments: {len(old_client_payments)}")
    print("\n🎉 Your data has been migrated to MongoDB!")
    print("You can now login with your existing credentials.")

if __name__ == '__main__':
    try:
        migrate_data()
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
