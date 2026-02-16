
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from users.models import User, Company
from core.models import Project, Vendor, MasterCategory, SubCategory
from finance.models import Expense, ExpenseItem, Payment, ClientPayment
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Migrates data from old Flask tables (flask_*) to new Django models'

    def handle(self, *args, **options):
        self.stdout.write("Starting migration...")
        
        with transaction.atomic():
            with connection.cursor() as cursor:
                # 1. Companies
                self.stdout.write("Migrating Companies...")
                cursor.execute("SELECT company_id, name, address, phone, email, created_at FROM flask_company")
                companies = cursor.fetchall()
                for row in companies:
                    Company.objects.create(
                        company_id=row[0],
                        name=row[1],
                        address=row[2],
                        phone=row[3],
                        email=row[4],
                        created_at=row[5] or timezone.now()
                    )
                self.stdout.write(f"Migrated {len(companies)} companies.")

                # 2. Users
                self.stdout.write("Migrating Users...")
                # Flask User: user_id, company_id, name, email, password_hash, role, created_at
                cursor.execute("SELECT user_id, company_id, name, email, password_hash, role, created_at FROM flask_user")
                users = cursor.fetchall()
                for row in users:
                    user = User(
                        user_id=row[0],
                        company_id=row[1],
                        name=row[2],
                        email=row[3],
                        password=row[4], # Store existing hash
                        role=row[5],
                        date_joined=row[6] or timezone.now(),
                        is_active=True,
                        is_staff=(row[5] in ['OWNER', 'ADMIN']), # Grant staff access to Owner/Admin
                        is_superuser=(row[5] == 'OWNER') # Grant superuser to Owner
                    )
                    user.save()
                self.stdout.write(f"Migrated {len(users)} users.")

                # 3. Master Categories
                self.stdout.write("Migrating Master Categories...")
                cursor.execute("SELECT category_id, name, type, is_active FROM flask_master_category")
                cats = cursor.fetchall()
                for row in cats:
                    MasterCategory.objects.create(
                        category_id=row[0],
                        name=row[1],
                        type=row[2],
                        is_active=row[3]
                    )
                self.stdout.write(f"Migrated {len(cats)} master categories.")

                # 4. Sub Categories
                self.stdout.write("Migrating Sub Categories...")
                cursor.execute("SELECT subcategory_id, parent_category_id, name, default_unit FROM flask_sub_category")
                subcats = cursor.fetchall()
                for row in subcats:
                    SubCategory.objects.create(
                        subcategory_id=row[0],
                        parent_category_id=row[1],
                        name=row[2],
                        default_unit=row[3]
                    )
                self.stdout.write(f"Migrated {len(subcats)} sub categories.")

                # 5. Projects
                self.stdout.write("Migrating Projects...")
                cursor.execute("SELECT project_id, company_id, name, location, start_date, end_date, budget, status, created_at FROM flask_project")
                projects = cursor.fetchall()
                for row in projects:
                    Project.objects.create(
                        project_id=row[0],
                        company_id=row[1],
                        name=row[2],
                        location=row[3],
                        start_date=row[4],
                        end_date=row[5],
                        budget=row[6],
                        status=row[7],
                        created_at=row[8] or timezone.now()
                    )
                self.stdout.write(f"Migrated {len(projects)} projects.")

                # 6. Vendors
                self.stdout.write("Migrating Vendors...")
                cursor.execute("SELECT vendor_id, company_id, name, phone, email, gst_number, created_at FROM flask_vendor")
                vendors = cursor.fetchall()
                for row in vendors:
                    Vendor.objects.create(
                        vendor_id=row[0],
                        company_id=row[1],
                        name=row[2],
                        phone=row[3],
                        email=row[4],
                        gst_number=row[5],
                        created_at=row[6] or timezone.now()
                    )
                self.stdout.write(f"Migrated {len(vendors)} vendors.")

                # 7. Expenses
                self.stdout.write("Migrating Expenses...")
                # expense_id, company_id, project_id, vendor_id, expense_type, category, amount, payment_mode, expense_date, description, invoice_number, bill_url, created_at
                cursor.execute("SELECT expense_id, company_id, project_id, vendor_id, expense_type, category, amount, payment_mode, expense_date, description, invoice_number, bill_url, created_at FROM flask_expense")
                expenses = cursor.fetchall()
                for row in expenses:
                    Expense.objects.create(
                        expense_id=row[0],
                        company_id=row[1],
                        project_id=row[2],
                        vendor_id=row[3],
                        expense_type=row[4],
                        category=row[5],
                        amount=row[6],
                        payment_mode=row[7],
                        expense_date=row[8],
                        description=row[9],
                        invoice_number=row[10],
                        bill_url=row[11],
                        created_at=row[12] or timezone.now()
                    )
                self.stdout.write(f"Migrated {len(expenses)} expenses.")

                # 8. Expense Items
                self.stdout.write("Migrating Expense Items...")
                # expense_item_id, expense_id, item_name, quantity, measuring_unit, unit_price, total_price
                cursor.execute("SELECT expense_item_id, expense_id, item_name, quantity, measuring_unit, unit_price, total_price FROM flask_expense_item")
                items = cursor.fetchall()
                for row in items:
                    ExpenseItem.objects.create(
                        expense_item_id=row[0],
                        expense_id=row[1],
                        item_name=row[2],
                        quantity=row[3],
                        measuring_unit=row[4],
                        unit_price=row[5],
                        total_price=row[6]
                    )
                self.stdout.write(f"Migrated {len(items)} expense items.")

                # 9. Payments
                self.stdout.write("Migrating Payments...")
                # payment_id, company_id, vendor_id, project_id, expense_id, amount, payment_date, payment_mode, created_at
                cursor.execute("SELECT payment_id, company_id, vendor_id, project_id, expense_id, amount, payment_date, payment_mode, created_at FROM flask_payment")
                payments = cursor.fetchall()
                for row in payments:
                    Payment.objects.create(
                        payment_id=row[0],
                        company_id=row[1],
                        vendor_id=row[2],
                        project_id=row[3],
                        expense_id=row[4],
                        amount=row[5],
                        payment_date=row[6],
                        payment_mode=row[7],
                        created_at=row[8] or timezone.now()
                    )
                self.stdout.write(f"Migrated {len(payments)} payments.")

                # 10. Client Payments
                self.stdout.write("Migrating Client Payments...")
                # client_payment_id, company_id, project_id, amount, payment_date, payment_mode, reference_number, remarks, created_at
                cursor.execute("SELECT client_payment_id, company_id, project_id, amount, payment_date, payment_mode, reference_number, remarks, created_at FROM flask_client_payment")
                cpayments = cursor.fetchall()
                for row in cpayments:
                    ClientPayment.objects.create(
                        client_payment_id=row[0],
                        company_id=row[1],
                        project_id=row[2],
                        amount=row[3],
                        payment_date=row[4],
                        payment_mode=row[5],
                        reference_number=row[6],
                        remarks=row[7],
                        created_at=row[8] or timezone.now()
                    )
                self.stdout.write(f"Migrated {len(cpayments)} client payments.")
        
        self.stdout.write(self.style.SUCCESS('Successfully migrated all data!'))
