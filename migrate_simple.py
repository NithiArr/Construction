#!/usr/bin/env python3
"""
Simple SQLite to MongoDB Migration using direct SQL queries
"""

import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
from mongoengine import connect
from models_mongo import Company, User, Project, Vendor, Expense, ExpenseItem, Payment, ClientPayment

load_dotenv()

# Helper function to safely get value from sqlite3.Row
def safe_get(row, key, default=None):
    try:
        return row[key] if row[key] is not None else default
    except (KeyError, IndexError):
        return default

print("=" * 60)
print("SQLite to MongoDB Migration Script  (Simple Version)")
print("=" * 60)

# Connect to SQLite
sqlite_db = 'instance/construction_v2.db'
print(f"\n[1/9] Connecting to SQLite: {sqlite_db}")
conn = sqlite3.connect(sqlite_db)
conn.row_factory = sqlite3.Row  # Return rows as dictionaries
cursor = conn.cursor()
print(f"✓ Connected to SQLite")

# Connect to MongoDB
print("\n[2/9] Connecting to MongoDB...")
mongodb_uri = os.environ.get('MONGODB_HOST', 'mongodb://mongodb:27017/construction_db')
connect(host=mongodb_uri)
print("✓ Connected to MongoDB")

# Clear MongoDB
print("\n[3/9] Clearing existing MongoDB data...")
Company.drop_collection()
User.drop_collection()
Project.drop_collection()
Vendor.drop_collection()
Expense.drop_collection()
Payment.drop_collection()
ClientPayment.drop_collection()
print("✓ MongoDB collections cleared")

# Mappings
company_map = {}
user_map = {}
project_map = {}
vendor_map = {}
expense_map = {}

# Migrate Companies
print("\n[4/9] Migrating Companies...")
cursor.execute("SELECT * FROM company")
companies = cursor.fetchall()
for row in companies:
    company = Company(
        name=row['name'],
        address=row['address'],
        phone=row['phone'],
        email=row['email'],
        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now()
    )
    company.save()
    company_map[row['company_id']] = company
    print(f"  ✓ {company.name}")
print(f"✓ Migrated {len(companies)} companies")

# Migrate Users
print("\n[5/9] Migrating Users...")
cursor.execute("SELECT * FROM user")
users = cursor.fetchall()
for row in users:
    company = company_map.get(row['company_id'])
    if not company:
        continue
    user = User(
        company=company,
        name=row['name'],
        email=row['email'],
        password_hash=row['password_hash'],
        role=row['role'],
        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now()
    )
    user.save()
    user_map[row['user_id']] = user
    print(f"  ✓ {user.email} ({user.role})")
print(f"✓ Migrated {len(users)} users")

# Migrate Projects
print("\n[6/9] Migrating Projects...")
cursor.execute("SELECT * FROM project")
projects = cursor.fetchall()
for row in projects:
    company = company_map.get(row['company_id'])
    if not company:
        continue
    project = Project(
        company=company,
        name=row['name'],
        location=row['location'],
        start_date=datetime.fromisoformat(row['start_date']).date() if row['start_date'] else None,
        end_date=datetime.fromisoformat(row['end_date']).date() if row['end_date'] else None,
        budget=row['budget'],
        status=row['status'],
        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now()
    )
    project.save()
    project_map[row['project_id']] = project
    print(f"  ✓ {project.name}")
print(f"✓ Migrated {len(projects)} projects")

# Migrate Vendors
print("\n[7/9] Migrating Vendors...")
cursor.execute("SELECT * FROM vendor")
vendors = cursor.fetchall()
for row in vendors:
    company = company_map.get(row['company_id'])
    if not company:
        continue
    vendor = Vendor(
        company=company,
        name=row['name'],
        phone=row['phone'],
        email=row['email'],
        gst_number=row['gst_number'],
        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now()
    )
    vendor.save()
    vendor_map[row['vendor_id']] = vendor
    print(f"  ✓ {vendor.name}")
print(f"✓ Migrated {len(vendors)} vendors")

# Migrate Expenses
print("\n[8/9] Migrating Expenses...")
cursor.execute("SELECT * FROM expense")
expenses = cursor.fetchall()
for row in expenses:
    company = company_map.get(row['company_id'])
    project = project_map.get(row['project_id'])
    vendor_id = row[3] if len(row) > 3 and row[3] else None  # vendor_id is 4th column
    vendor = vendor_map.get(vendor_id) if vendor_id else None
    
    if not company or not project:
        continue
    
    # Get expense items (if table exists)
    items = []
    try:
        cursor.execute("SELECT * FROM expense_item WHERE expense_id = ?", (row['expense_id'],))
        item_rows = cursor.fetchall()
        items = [
            ExpenseItem(
                item_name=item['item_name'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                total_price=item['total_price']
            )
            for item in item_rows
        ]
    except sqlite3.OperationalError:
        # Table doesn't exist, skip items
        pass
    
    # Helper function to safely get value from Row
    def safe_get(row, key, default=None):
        try:
            return row[key] if row[key] is not None else default
        except (KeyError, IndexError):
            return default
    
    expense = Expense(
        company=company,
        project=project,
        vendor=vendor,
        category=safe_get(row, 'category', 'Regular Expense'),
        subcategory=safe_get(row, 'subcategory'),
        amount=safe_get(row, 'amount', 0),
        payment_mode=safe_get(row, 'payment_mode', 'CASH'),
        expense_date=datetime.fromisoformat(row['expense_date']).date() if safe_get(row, 'expense_date') else datetime.now().date(),
        description=safe_get(row, 'description'),
        invoice_number=safe_get(row, 'invoice_number'),
        bill_url=safe_get(row, 'bill_url'),
        items=items,
        created_at=datetime.fromisoformat(row['created_at']) if safe_get(row, 'created_at') else datetime.now()
    )
    expense.save()
    expense_map[row['expense_id']] = expense
    print(f"  ✓ {expense.category} - ₹{expense.amount}")
print(f"✓ Migrated {len(expenses)} expenses")

# Migrate Payments
print("\n[9/9] Migrating Vendor Payments...")
cursor.execute("SELECT * FROM payment")
payments = cursor.fetchall()
for row in payments:
    company = company_map.get(safe_get(row, 'company_id'))
    vendor = vendor_map.get(safe_get(row, 'vendor_id'))
    project = project_map.get(safe_get(row, 'project_id'))
    expense = expense_map.get(safe_get(row, 'expense_id')) if safe_get(row, 'expense_id') else None
    
    if not company or not vendor or not project:
        continue
    
    payment = Payment(
        company=company,
        vendor=vendor,
        project=project,
        expense=expense,
        amount=safe_get(row, 'amount', 0),
        payment_date=datetime.fromisoformat(row['payment_date']).date() if safe_get(row, 'payment_date') else datetime.now().date(),
        payment_mode=safe_get(row, 'payment_mode', 'CASH'),
        created_at=datetime.fromisoformat(row['created_at']) if safe_get(row, 'created_at') else datetime.now()
    )
    payment.save()
    print(f"  ✓ ₹{payment.amount} to {vendor.name}")
print(f"✓ Migrated {len(payments)} payments")

# Migrate Client Payments
print("\n[10/10] Migrating Client Payments...")
cursor.execute("SELECT * FROM client_payment")
client_payments = cursor.fetchall()
for row in client_payments:
    company = company_map.get(safe_get(row, 'company_id'))
    project = project_map.get(safe_get(row, 'project_id'))
    
    if not company or not project:
        continue
    
    cp = ClientPayment(
        company=company,
        project=project,
        amount=safe_get(row, 'amount', 0),
        payment_date=datetime.fromisoformat(row['payment_date']).date() if safe_get(row, 'payment_date') else datetime.now().date(),
        payment_mode=safe_get(row, 'payment_mode', 'CASH'),
        reference_number=safe_get(row, 'reference_number'),
        remarks=safe_get(row, 'remarks'),
        created_at=datetime.fromisoformat(row['created_at']) if safe_get(row, 'created_at') else datetime.now()
    )
    cp.save()
    print(f"  ✓ ₹{cp.amount}")
print(f"✓ Migrated {len(client_payments)} client payments")

conn.close()

print("\n" + "=" * 60)
print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
print("=" * 60)
print(f"\nSummary:")
print(f"  Companies: {len(companies)}")
print(f"  Users: {len(users)}")
print(f"  Projects: {len(projects)}")
print(f"  Vendors: {len(vendors)}")
print(f"  Expenses: {len(expenses)}")
print(f"  Vendor Payments: {len(payments)}")
print(f"  Client Payments: {len(client_payments)}")
print("\n🎉 You can now login with your existing credentials!")
print(f"   Access your app at: http://localhost:8080")

