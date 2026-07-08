from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from django.utils import timezone
from account.models import Company

class RBACTestCase(TestCase):
    def setUp(self):
        # 1. Run the group initialization command
        from django.core.management import call_command
        call_command('initialize_groups')
        
        # 2. Create users for different roles
        self.admin_user = User.objects.create_user(username='admin', email='admin@test.com', password='password123')
        self.sales_user = User.objects.create_user(username='sales', email='sales@test.com', password='password123')
        self.acc_user = User.objects.create_user(username='accountant', email='accountant@test.com', password='password123')
        self.purchase_user = User.objects.create_user(username='purchase', email='purchase@test.com', password='password123')
        self.viewer_user = User.objects.create_user(username='viewer', email='viewer@test.com', password='password123')

        # Assign groups
        Group.objects.get(name='Admin').user_set.add(self.admin_user)
        Group.objects.get(name='Sales Executive').user_set.add(self.sales_user)
        Group.objects.get(name='Account Manager').user_set.add(self.acc_user)
        Group.objects.get(name='Purchase Executive').user_set.add(self.purchase_user)
        Group.objects.get(name='Viewer / Auditor').user_set.add(self.viewer_user)

        # Refresh from database to clear cached permissions
        self.admin_user = User.objects.get(pk=self.admin_user.pk)
        self.sales_user = User.objects.get(pk=self.sales_user.pk)
        self.acc_user = User.objects.get(pk=self.acc_user.pk)
        self.purchase_user = User.objects.get(pk=self.purchase_user.pk)
        self.viewer_user = User.objects.get(pk=self.viewer_user.pk)

        # Create company and set onboarding complete for all users
        for u in [self.admin_user, self.sales_user, self.acc_user, self.purchase_user, self.viewer_user]:
            Company.objects.create(user=u, name=f"{u.username}'s Company", country='India', onboarding_step=3)

    def test_group_permissions_assignment(self):
        # Admin has invoice permissions
        self.assertTrue(self.admin_user.has_perm('my_account.view_invoice'))
        self.assertTrue(self.admin_user.has_perm('my_account.add_invoice'))
        
        # Sales Executive has customer & invoice permissions
        self.assertTrue(self.sales_user.has_perm('my_account.view_customer'))
        self.assertTrue(self.sales_user.has_perm('my_account.add_customer'))
        self.assertTrue(self.sales_user.has_perm('my_account.view_invoice'))
        # Sales Executive does NOT have vendor permissions
        self.assertFalse(self.sales_user.has_perm('my_account.view_vendor'))

        # Accountant has accounts and transactions, but view-only invoices
        self.assertTrue(self.acc_user.has_perm('my_account.view_account'))
        self.assertTrue(self.acc_user.has_perm('my_account.view_incometransaction'))
        self.assertTrue(self.acc_user.has_perm('my_account.view_invoice'))
        self.assertFalse(self.acc_user.has_perm('my_account.add_invoice'))
        self.assertFalse(self.acc_user.has_perm('my_account.view_vendor'))

        # Purchase Executive has vendor and bill permissions
        self.assertTrue(self.purchase_user.has_perm('my_account.view_vendor'))
        self.assertTrue(self.purchase_user.has_perm('my_account.view_bill'))
        self.assertFalse(self.purchase_user.has_perm('my_account.view_customer'))

        # Viewer / Auditor has view-only permissions and NO transactions/add/delete
        self.assertTrue(self.viewer_user.has_perm('my_account.view_customer'))
        self.assertTrue(self.viewer_user.has_perm('my_account.view_invoice'))
        self.assertFalse(self.viewer_user.has_perm('my_account.add_customer'))
        self.assertFalse(self.viewer_user.has_perm('my_account.view_incometransaction'))

    def test_url_security_middleware(self):
        # 1. Sales Executive accessing customers: Allowed (Status 200)
        client = Client()
        client.login(username='sales', password='password123')
        response = client.get(reverse('customer_home'))
        self.assertEqual(response.status_code, 200)

        # 2. Sales Executive accessing vendors: Forbidden (Status 403)
        response = client.get(reverse('vendor_home'))
        self.assertEqual(response.status_code, 403)

        # 3. Accountant accessing accounts: Allowed
        client.login(username='accountant', password='password123')
        response = client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)

        # 4. Accountant accessing customers: Forbidden
        response = client.get(reverse('customer_home'))
        self.assertEqual(response.status_code, 403)

        # 5. Purchase Executive accessing vendors: Allowed
        client.login(username='purchase', password='password123')
        response = client.get(reverse('vendor_home'))
        self.assertEqual(response.status_code, 200)

        # 6. Purchase Executive accessing accounts: Forbidden
        response = client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 403)

    def test_dashboard_realtime_calculations(self):
        from account.models import Customer, Vendor, Invoice, Bill, Account, IncomeTransaction, ExpenseTransaction, Transfer, IncomeAccount, ExpenseAccount, Category, Tax
        
        # Get the admin client
        client = Client()
        client.login(username='admin', password='password123')
        
        # Access dashboard initially (empty database)
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_receivables'], 0.0)
        self.assertEqual(response.context['total_payables'], 0.0)
        self.assertEqual(response.context['total_incoming'], 0.0)
        self.assertEqual(response.context['total_outgoing'], 0.0)
        self.assertEqual(response.context['net_profit'], 0.0)
        self.assertEqual(len(response.context['dashboard_accounts']), 0)
        
        # Create models linked to Admin's company
        company = self.admin_user.company
        
        customer = Customer.objects.create(company=company, name='Test Customer')
        vendor = Vendor.objects.create(company=company, vendor_name='Test Vendor')
        
        # Create Invoices & Bills
        Invoice.objects.create(company=company, customer=customer, invoice_number='INV-001', invoice_date=timezone.now().date(), due_date=timezone.now().date(), total=500.00)
        Bill.objects.create(company=company, vendor=vendor, bill_number='BILL-001', bill_date=timezone.now().date(), due_date=timezone.now().date(), total=200.00)
        
        # Create Account and Transaction
        acc = Account.objects.create(company=company, name='Main Account', number='12345', opening_balance=1000.00)
        
        # Setup Chart of Accounts dependencies
        inc_coa = IncomeAccount.objects.create(account_name='Sales Income', account_code='4000')
        exp_coa = ExpenseAccount.objects.create(account_name='Office Expenses', account_code='5000')
        
        IncomeTransaction.objects.create(
            company=company, account=acc, amount=150.00, date=timezone.now().date(),
            payment_method='Cash', chart_of_account=inc_coa, number='TX-INC-001'
        )
        ExpenseTransaction.objects.create(
            company=company, account=acc, amount=50.00, date=timezone.now().date(),
            payment_method='Cash', chart_of_account=exp_coa, number='TX-EXP-001'
        )
        
        # Access dashboard again to check if live ORM values are populated
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Verify Receivables (Invoice)
        self.assertEqual(response.context['total_receivables'], 500.00)
        self.assertEqual(response.context['open_receivables'], 500.00)
        
        # Verify Payables (Bill)
        self.assertEqual(response.context['total_payables'], 200.00)
        self.assertEqual(response.context['open_payables'], 200.00)
        
        # Verify Cash Flow (Incoming: 150, Outgoing: 50, Profit: 100)
        self.assertEqual(response.context['total_incoming'], 150.00)
        self.assertEqual(response.context['total_outgoing'], 50.00)
        self.assertEqual(response.context['net_profit'], 100.00)
        
        # Verify Account Balances (Opening: 1000 + 150 - 50 = 1100)
        self.assertEqual(len(response.context['dashboard_accounts']), 1)
        self.assertEqual(response.context['dashboard_accounts'][0]['name'], 'Main Account')
        self.assertEqual(response.context['dashboard_accounts'][0]['balance'], 1100.00)
        
        # Verify Recent Activities
        self.assertTrue(len(response.context['recent_activities']) >= 4)


class CRUDTestCase(TestCase):
    def setUp(self):
        from django.core.management import call_command
        call_command('initialize_groups')
        self.admin_user = User.objects.create_user(username='admin_crud', email='admin_crud@test.com', password='password123')
        Group.objects.get(name='Admin').user_set.add(self.admin_user)
        self.company = Company.objects.create(user=self.admin_user, name="CRUD Test Company", onboarding_step=3)
        self.client = Client()
        self.client.login(username='admin_crud', password='password123')

    def test_customer_crud(self):
        from account.models import Customer
        # Create
        response = self.client.post(reverse('customer_create'), {
            'name': 'Customer A', 'email': 'a@a.com', 'phone': '123', 'currency': 'INR', 'country': 'India'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(company=self.company, name='Customer A').exists())
        customer = Customer.objects.get(company=self.company, name='Customer A')

        # Read
        response = self.client.get(reverse('customers_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Customer A')

        # Update
        response = self.client.post(reverse('customer_edit', args=[customer.id]), {
            'name': 'Customer A Updated', 'email': 'a@a.com', 'phone': '123', 'currency': 'INR', 'country': 'India'
        })
        self.assertEqual(response.status_code, 302)
        customer.refresh_from_db()
        self.assertEqual(customer.name, 'Customer A Updated')

        # Delete
        response = self.client.get(reverse('customer_delete', args=[customer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())

    def test_vendor_crud(self):
        from account.models import Vendor
        # Create
        response = self.client.post(reverse('vendor_create'), {
            'vendor_name': 'Vendor A', 'email': 'v@v.com', 'phone': '456', 'currency': 'INR', 'country': 'India'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vendor.objects.filter(company=self.company, vendor_name='Vendor A').exists())
        vendor = Vendor.objects.get(company=self.company, vendor_name='Vendor A')

        # Read
        response = self.client.get(reverse('vendors_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vendor A')

        # Update
        response = self.client.post(reverse('vendor_edit', args=[vendor.id]), {
            'vendor_name': 'Vendor A Updated', 'email': 'v@v.com', 'phone': '456', 'currency': 'INR', 'country': 'India'
        })
        self.assertEqual(response.status_code, 302)
        vendor.refresh_from_db()
        self.assertEqual(vendor.vendor_name, 'Vendor A Updated')

        # Delete
        response = self.client.get(reverse('vendor_delete', args=[vendor.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Vendor.objects.filter(id=vendor.id).exists())

    def test_item_crud(self):
        from account.models import Item, Category, Tax
        category = Category.objects.create(name="ProdCategory", status="Active")
        tax = Tax.objects.create(tax_name="VAT", tax_percentage=5.0)
        # Create
        response = self.client.post(reverse('item_create'), {
            'type': 'product', 'name': 'Item A', 'category': category.id, 'sale_enabled': True, 'purchase_enabled': True,
            'sale_price': 100.0, 'purchase_price': 80.0, 'tax': tax.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(company=self.company, name='Item A').exists())
        item = Item.objects.get(company=self.company, name='Item A')

        # Read
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item A')


