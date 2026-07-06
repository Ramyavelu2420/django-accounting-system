from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
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
