import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from account.models import Customer, Invoice, Vendor, Bill, Account, Transfer, Reconciliation, Report, Item, IncomeTransaction, ExpenseTransaction, Estimate

class Command(BaseCommand):
    help = 'Initialize Django Groups and Permissions for Accounting App'

    def handle(self, *args, **options):
        self.stdout.write("Initializing groups and permissions...")

        # 1. Define custom content types and custom permissions if they don't exist
        customer_ct = ContentType.objects.get_for_model(Customer)
        invoice_ct = ContentType.objects.get_for_model(Invoice)
        vendor_ct = ContentType.objects.get_for_model(Vendor)
        bill_ct = ContentType.objects.get_for_model(Bill)
        account_ct = ContentType.objects.get_for_model(Account)
        transfer_ct = ContentType.objects.get_for_model(Transfer)
        reconciliation_ct = ContentType.objects.get_for_model(Reconciliation)
        report_ct = ContentType.objects.get_for_model(Report)
        item_ct = ContentType.objects.get_for_model(Item)
        estimate_ct = ContentType.objects.get_for_model(Estimate)

        # Create custom permissions programmatically
        custom_perms = [
            # Invoice custom permissions
            ('approve_invoice', 'Can approve invoice', invoice_ct),
            ('import_invoice', 'Can import invoice', invoice_ct),
            ('export_invoice', 'Can export invoice', invoice_ct),
            # Customer custom permissions
            ('import_customer', 'Can import customer', customer_ct),
            ('export_customer', 'Can export customer', customer_ct),
            # Vendor custom permissions
            ('import_vendor', 'Can import vendor', vendor_ct),
            ('export_vendor', 'Can export vendor', vendor_ct),
            # Bill custom permissions
            ('import_bill', 'Can import bill', bill_ct),
            ('export_bill', 'Can export bill', bill_ct),
            ('approve_bill', 'Can approve bill', bill_ct),
            # Transfer custom permissions
            ('import_transfer', 'Can import transfer', transfer_ct),
            # Report custom permissions
            ('export_report', 'Can export report', report_ct),
            # Estimate custom permissions
            ('convert_estimate', 'Can convert estimate', estimate_ct),
            ('import_estimate', 'Can import estimate', estimate_ct),
            ('export_estimate', 'Can export estimate', estimate_ct),
        ]

        created_perms = {}
        for codename, name, ct in custom_perms:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={'name': name}
            )
            created_perms[codename] = perm

        # Helper to get permission objects
        def get_perm(codename):
            if codename in created_perms:
                return created_perms[codename]
            try:
                return Permission.objects.get(codename=codename)
            except Permission.DoesNotExist:
                return None

        # 2. Define Groups
        groups_def = {
            'Admin': {
                'permissions': [
                    # Full access to everything
                    'add_customer', 'change_customer', 'delete_customer', 'view_customer', 'import_customer', 'export_customer',
                    'add_invoice', 'change_invoice', 'delete_invoice', 'view_invoice', 'approve_invoice', 'import_invoice', 'export_invoice',
                    'add_vendor', 'change_vendor', 'delete_vendor', 'view_vendor', 'import_vendor', 'export_vendor',
                    'add_bill', 'change_bill', 'delete_bill', 'view_bill', 'import_bill', 'export_bill', 'approve_bill',
                    'add_account', 'change_account', 'delete_account', 'view_account',
                    'add_incometransaction', 'change_incometransaction', 'delete_incometransaction', 'view_incometransaction',
                    'add_expensetransaction', 'change_expensetransaction', 'delete_expensetransaction', 'view_expensetransaction',
                    'add_transfer', 'change_transfer', 'delete_transfer', 'view_transfer', 'import_transfer',
                    'add_reconciliation', 'change_reconciliation', 'delete_reconciliation', 'view_reconciliation',
                    'add_report', 'change_report', 'delete_report', 'view_report', 'export_report',
                    'add_item', 'change_item', 'delete_item', 'view_item',
                    'add_estimate', 'change_estimate', 'delete_estimate', 'view_estimate', 'convert_estimate', 'import_estimate', 'export_estimate',
                ]
            },
            'Sales Executive': {
                'permissions': [
                    # Customers
                    'add_customer', 'change_customer', 'delete_customer', 'view_customer', 'import_customer', 'export_customer',
                    # Invoices
                    'add_invoice', 'change_invoice', 'delete_invoice', 'view_invoice', 'approve_invoice', 'import_invoice', 'export_invoice',
                    # Items
                    'view_item',
                    # Estimates
                    'add_estimate', 'change_estimate', 'view_estimate', 'convert_estimate', 'import_estimate', 'export_estimate',
                ]
            },
            'Account Manager': {
                'permissions': [
                    # Accounts
                    'add_account', 'change_account', 'delete_account', 'view_account',
                    # Transactions
                    'add_incometransaction', 'change_incometransaction', 'delete_incometransaction', 'view_incometransaction',
                    'add_expensetransaction', 'change_expensetransaction', 'delete_expensetransaction', 'view_expensetransaction',
                    # Transfers
                    'add_transfer', 'change_transfer', 'delete_transfer', 'view_transfer', 'import_transfer',
                    # Reconciliation
                    'add_reconciliation', 'change_reconciliation', 'delete_reconciliation', 'view_reconciliation',
                    # Reports
                    'add_report', 'change_report', 'delete_report', 'view_report', 'export_report',
                    # Invoices (View Only)
                    'view_invoice',
                    # Items
                    'view_item',
                    # Estimates (View Only)
                    'view_estimate',
                ]
            },
            'Purchase Executive': {
                'permissions': [
                    # Vendors
                    'add_vendor', 'change_vendor', 'delete_vendor', 'view_vendor', 'import_vendor', 'export_vendor',
                    # Bills
                    'add_bill', 'change_bill', 'delete_bill', 'view_bill', 'import_bill', 'export_bill', 'approve_bill',
                    # Items
                    'view_item',
                ]
            },
            'Viewer / Auditor': {
                'permissions': [
                    # View only permissions
                    'view_customer', 'view_invoice', 'view_vendor', 'view_bill', 'view_account', 'view_report', 'view_item'
                ]
            }
        }

        missing_perms = []

        for group_name, info in groups_def.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Created group: {group_name}")
            else:
                self.stdout.write(f"Group already exists: {group_name}")

            # Clear existing permissions to make this process idempotent and ensure exact match
            group.permissions.clear()

            # Assign permissions
            perms_to_add = []
            for perm_code in info['permissions']:
                p = get_perm(perm_code)
                if p:
                    perms_to_add.append(p)
                else:
                    missing_perms.append((group_name, perm_code))
            
            group.permissions.add(*perms_to_add)
            self.stdout.write(self.style.SUCCESS(f"Assigned {len(perms_to_add)} permissions to {group_name}"))

        # Report missing permissions
        if missing_perms:
            self.stdout.write(self.style.ERROR("\n--- MISSING PERMISSIONS DETECTED ---"))
            for group_name, perm_code in missing_perms:
                self.stdout.write(self.style.ERROR(f"Group: {group_name} is missing permission: {perm_code}"))
        else:
            self.stdout.write(self.style.SUCCESS("\nNo missing permissions detected."))

        # 3. Complete Audit Output
        self.stdout.write("\n==================================================")
        self.stdout.write("              RBAC AUDIT REPORT")
        self.stdout.write("==================================================")
        for group in Group.objects.all():
            self.stdout.write(f"\nGroup: {group.name}")
            perms = list(group.permissions.values_list('codename', flat=True))
            self.stdout.write(f"  Permissions assigned ({len(perms)}): {sorted(perms)}")
        
        # User permissions audit
        from django.contrib.auth.models import User
        self.stdout.write("\n--- Logged-in / Existing Users Audit ---")
        for user in User.objects.all():
            self.stdout.write(f"\nUser: {user.username}")
            groups = list(user.groups.values_list('name', flat=True))
            self.stdout.write(f"  Groups: {groups}")
            # Clear cache to get fresh permissions
            if hasattr(user, '_perm_cache'):
                delattr(user, '_perm_cache')
            user_perms = list(user.get_all_permissions())
            self.stdout.write(f"  All available permissions ({len(user_perms)}): {sorted(user_perms)}")

        # Sidebar checks matching
        sidebar_perms_required = [
            'my_account.view_item',
            'my_account.view_invoice',
            'my_account.view_customer',
            'my_account.view_bill',
            'my_account.view_vendor',
            'my_account.view_account',
            'my_account.view_incometransaction',
            'my_account.view_expensetransaction',
            'my_account.view_transfer',
            'my_account.view_reconciliation',
            'my_account.view_report',
        ]
        self.stdout.write("\n--- Sidebar Permission Check Audit ---")
        for perm in sidebar_perms_required:
            exists = Permission.objects.filter(codename=perm.split('.')[-1]).exists()
            status = "VALID" if exists else "INVALID / MISSING"
            self.stdout.write(f"  Sidebar check: {perm} -> {status}")

        self.stdout.write(self.style.SUCCESS("\nInitialization and Audit completed successfully."))
