import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Connect to database
db_path = 'instance/construction_v2.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("SEEDING DATABASE WITH UNIFIED EXPENSE MODEL")
print("=" * 60)

# 0. ENSURE COMPANY AND USERS EXIST
print("\n0. Checking Company and Users...")

# Check Company
cursor.execute("SELECT company_id FROM company WHERE name = 'Sorgavasal'")
company = cursor.fetchone()

if not company:
    print("   Creating 'Sorgavasal' Company...")
    cursor.execute("""
        INSERT INTO company (name, address, phone, email, created_at)
        VALUES ('Sorgavasal', '123 Construction St, Chennai', '9876543210', 'info@sorgavasal.com', datetime('now'))
    """)
    company_id = cursor.lastrowid
else:
    company_id = company[0]
    print(f"   Found Company ID: {company_id}")

# Check Users
users_to_create = [
    ('nithiarrvind@gmail.com', 'Nithi', 'OWNER', 'password'), # Replace with secure password in prod
    ('admin@sorgavasal.com', 'Admin User', 'ADMIN', 'admin123'),
    ('manager@tsconst.com', 'Project Manager', 'MANAGER', 'manager123'),
    ('accountant@tsconst.com', 'Accountant', 'ACCOUNTANT', 'accountant123'),
    ('engineer@tsconst.com', 'Site Engineer', 'ENGINEER', 'engineer123'),
]

for email, name, role, pwd in users_to_create:
    cursor.execute("SELECT user_id FROM user WHERE email = ?", (email,))
    if not cursor.fetchone():
        pwd_hash = generate_password_hash(pwd)
        cursor.execute("""
            INSERT INTO user (company_id, name, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (company_id, name, email, pwd_hash, role))
        print(f"   Created user: {email} ({role})")

# 1. CREATE PROJECTS
print("\n1. Creating Projects...")
projects_data = [
    ('Skyline Tower', 'Bandra West, Mumbai', '2025-01-01', '2025-12-31', 15000000, 'ACTIVE'),
    ('Green Valley Apartments', 'Powai, Mumbai', '2025-02-15', '2026-03-15', 8000000, 'ACTIVE'),
    ('Corporate Office Complex', 'Andheri East, Mumbai', '2024-11-01', '2025-10-30', 12000000, 'ACTIVE'),
    ('Luxury Villa Project', 'Lonavala', '2025-03-01', '2025-09-30', 5000000, 'PLANNING'),
    ('Old City Mall Renovation', 'Dadar', '2024-08-01', '2024-12-31', 3000000, 'COMPLETED'),
]

project_ids = []
for project in projects_data:
    # Check if project exists by name and company
    cursor.execute("SELECT project_id FROM project WHERE name = ? AND company_id = ?", (project[0], company_id))
    existing = cursor.fetchone()
    if existing:
        project_ids.append(existing[0])
    else:
        cursor.execute("""
            INSERT INTO project (company_id, name, location, start_date, end_date, budget, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (company_id,) + project)
        project_ids.append(cursor.lastrowid)

print(f"   Projects ready: {len(project_ids)}")

# 2. CREATE VENDORS
print("\n2. Creating Vendors...")
vendors_data = [
    ('Steel Suppliers Ltd', '9876543210', 'steel@suppliers.com', '27AABCS1234F1Z1'),
    ('Cement Corporation', '9876543211', 'info@cement.com', '27AABCC5678G2Z2'),
    ('Brick Masters', '9876543212', 'sales@brickmasters.com', '27AABCB9012H3Z3'),
    ('Electrical Solutions', '9876543213', 'contact@electrical.com', '27AABCE3456I4Z4'),
    ('Plumbing Pro', '9876543214', 'info@plumbingpro.com', '27AABCP7890J5Z5'),
    ('Paint & Finishes Co', '9876543215', 'sales@paints.com', '27AABCF1122K6Z6'),
    ('Hardware Traders', '9876543216', 'orders@hardware.com', '27AABCH3344L7Z7'),
]

vendor_ids = []
for vendor in vendors_data:
    cursor.execute("SELECT vendor_id FROM vendor WHERE name = ? AND company_id = ?", (vendor[0], company_id))
    existing = cursor.fetchone()
    if existing:
        vendor_ids.append(existing[0])
    else:
        cursor.execute("""
            INSERT INTO vendor (company_id, name, phone, email, gst_number, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (company_id,) + vendor)
        vendor_ids.append(cursor.lastrowid)

print(f"   Vendors ready: {len(vendor_ids)}")

# 3. CREATE MATERIAL PURCHASES (as Expenses)
print("\n3. Creating Material Purchases (in Expenses table)...")
# Structure: (project_id_idx, vendor_id_idx, invoice_num, date, amount, payment_mode, items_list)
purchases_data = [
    # Project 1 - Skyline Tower
    (0, 0, 'INV-2025-001', '2025-01-15', 500000, 'CREDIT', [
        ('Steel Bars', 1000, 450, 450000), # Used as Subcategory too
        ('Steel Plates', 50, 1000, 50000)
    ]),
    (0, 1, 'INV-2025-002', '2025-01-20', 300000, 'CREDIT', [
        ('Cement', 1000, 300, 300000)
    ]),
    (0, 2, 'INV-2025-003', '2025-02-01', 200000, 'CASH', [
        ('Red Bricks', 10000, 15, 150000),
        ('AAC Blocks', 500, 100, 50000)
    ]),
    
    # Project 2 - Green Valley
    (1, 0, 'INV-2025-010', '2025-02-20', 350000, 'CREDIT', [
        ('Steel Bars', 800, 400, 320000),
        ('Binding Wire', 100, 300, 30000)
    ]),
    (1, 3, 'INV-2025-011', '2025-03-01', 180000, 'CREDIT', [
        ('Electrical Cables', 500, 200, 100000),
        ('Switch Boards', 100, 800, 80000)
    ]),
    
    # Project 3 - Corporate Office
    (2, 1, 'INV-2025-020', '2025-01-10', 400000, 'CREDIT', [
        ('Cement', 1200, 300, 360000),
        ('Sand', 4, 10000, 40000)
    ]),
    (2, 5, 'INV-2025-021', '2025-02-15', 250000, 'CREDIT', [
        ('Asian Paints', 500, 400, 200000),
        ('Interior Emulsion', 250, 200, 50000)
    ]),
]

purchase_ids = [] # Store created expense_ids that are purchases

for purchase in purchases_data:
    p_idx, v_idx, invoice_num, invoice_date, total, payment_mode, items = purchase
    
    pid = project_ids[p_idx]
    vid = vendor_ids[v_idx]
    
    # Determine subcategory (first item name or generic)
    subcategory = items[0][0] if items else "Material"
    
    # Check if invoice exists
    cursor.execute("SELECT expense_id FROM expense WHERE invoice_number = ? AND company_id = ?", (invoice_num, company_id))
    existing = cursor.fetchone()
    
    if existing:
        purchase_ids.append(existing[0])
    else:
        cursor.execute("""
            INSERT INTO expense (company_id, project_id, vendor_id, category, subcategory, 
                               amount, payment_mode, expense_date, description, invoice_number, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (company_id, pid, vid, 'Material Purchase', subcategory, 
              total, payment_mode, invoice_date, f'Invoice #{invoice_num}', invoice_num))
        
        expense_id = cursor.lastrowid
        purchase_ids.append(expense_id)
        
        # Insert items into expense_item
        for item in items:
            cursor.execute("""
                INSERT INTO expense_item (expense_id, item_name, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            """, (expense_id,) + item)

print(f"   Created {len(purchase_ids)} material purchases")

# 4. CREATE REGULAR EXPENSES
print("\n4. Creating Regular Expenses...")
expenses_data = [
    (project_ids[0], 'Labor', 'Skilled Labor', 150000, 'BANK', '2025-01-25', 'Monthly wages for masons'),
    (project_ids[0], 'Labor', 'Helper', 80000, 'CASH', '2025-01-25', 'Monthly wages for helpers'),
    (project_ids[0], 'Equipment', 'Crane Rental', 45000, 'UPI', '2025-02-01', 'Crane rental for 5 days'),
    (project_ids[0], 'Transportation', 'Truck', 25000, 'CASH', '2025-02-05', 'Material transportation'),
    
    (project_ids[1], 'Labor', 'Skilled Labor', 120000, 'BANK', '2025-02-28', 'Monthly wages'),
    (project_ids[1], 'Labor', 'Site Supervision', 60000, 'BANK', '2025-03-01', 'Engineer salary'),
    (project_ids[1], 'Safety', 'Safety Equipment', 35000, 'UPI', '2025-03-05', 'Helmets, boots, safety nets'),
    
    (project_ids[2], 'Labor', 'Skilled Labor', 180000, 'BANK', '2025-01-31', 'Monthly wages for masons'),
    (project_ids[2], 'General', 'Miscellaneous', 15000, 'CASH', '2025-02-10', 'Small tools and supplies'),
    (project_ids[2], 'Utilities', 'Electricity Bill', 42000, 'BANK', '2025-02-20', 'Site electricity charges'),
]

count_expenses = 0
for expense in expenses_data:
    pid, cat, subcat, amount, mode, date, desc = expense
    
    # Check duplicate roughly (by description and date and amount)
    cursor.execute("SELECT expense_id FROM expense WHERE description = ? AND amount = ? AND company_id = ?", (desc, amount, company_id))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO expense (company_id, project_id, category, subcategory, amount, payment_mode, 
                               expense_date, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (company_id, pid, 'Regular Expense', subcat, amount, mode, date, desc))
        count_expenses += 1

print(f"   Created {count_expenses} regular expenses")

# 5. CREATE VENDOR PAYMENTS
print("\n5. Creating Vendor Payments...")
payments_data = [
    # (vendor_idx, project_idx, purchase_idx, amount, date, mode)
    (0, 0, 0, 250000, '2025-02-01', 'BANK'),  # Steel payment (Purchase 0)
    (1, 0, 1, 150000, '2025-02-05', 'BANK'),  # Cement payment (Purchase 1)
    (2, 0, 2, 200000, '2025-02-10', 'CASH'),  # Bricks full payment (Purchase 2)
    
    (0, 1, 3, 200000, '2025-03-10', 'BANK'),  # Steel partial (Purchase 3)
    (3, 1, 4, 100000, '2025-03-15', 'UPI'),   # Electrical partial (Purchase 4)
    
    (1, 2, 5, 400000, '2025-02-15', 'BANK'),  # Cement full (Purchase 5)
]

count_payments = 0
for payment in payments_data:
    v_idx, p_idx, pur_idx, amount, date, mode = payment
    
    vid = vendor_ids[v_idx]
    pid = project_ids[p_idx]
    eid = purchase_ids[pur_idx]
    
    # Check if payment exists
    cursor.execute("SELECT payment_id FROM payment WHERE expense_id = ? AND amount = ? AND company_id = ?", (eid, amount, company_id))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO payment (company_id, vendor_id, project_id, expense_id, amount, 
                               payment_date, payment_mode, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (company_id, vid, pid, eid, amount, date, mode))
        count_payments += 1

print(f"   Created {count_payments} vendor payments")

# 6. CREATE CLIENT PAYMENTS
print("\n6. Creating Client Payments...")
client_payments_data = [
    (project_ids[0], 5000000, '2025-01-10', 'BANK', 'CHQ-001234', 'Initial advance payment'),
    (project_ids[0], 3000000, '2025-02-15', 'BANK', 'CHQ-001456', 'First milestone payment'),
    
    (project_ids[1], 2500000, '2025-02-25', 'BANK', 'NEFT-789012', 'Booking amount'),
    (project_ids[1], 1500000, '2025-03-20', 'BANK', 'NEFT-789345', 'Construction start payment'),
    
    (project_ids[2], 4000000, '2025-01-05', 'BANK', 'CHQ-002345', 'Advance payment'),
    (project_ids[2], 3500000, '2025-02-25', 'BANK', 'CHQ-002678', 'Progress payment'),
    
    (project_ids[4], 3000000, '2024-12-30', 'BANK', 'CHQ-000123', 'Final payment on completion'),
]

count_client_payments = 0
for payment in client_payments_data:
    # project_ids is list of IDs. 
    # client_payments_data[0] is tuple (project_id, amount, ...)
    # But wait, in client_payments_data definition above:
    # `(project_ids[0], ...)` -> this logic is correct.
    
    # Check if payment exists
    cursor.execute("SELECT client_payment_id FROM client_payment WHERE reference_number = ? AND company_id = ?", (payment[4], company_id))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO client_payment (company_id, project_id, amount, payment_date, 
                                      payment_mode, reference_number, remarks, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (company_id,) + payment)
        count_client_payments += 1

print(f"   Created {count_client_payments} client payments")

# Commit all changes
conn.commit()
conn.close()

print("\n" + "=" * 60)
print("DB SETUP AND SEEDING COMPLETE!")
print("=" * 60)
