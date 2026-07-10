from django.shortcuts import redirect, render
from django.urls import resolve, Resolver404
from django.core.exceptions import PermissionDenied
from account.models import Company

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude paths that don't need authentication or are handled by Django Admin
        path = request.path
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/') or path.startswith('/accounts/'):
            return self.get_response(request)

        try:
            resolver_match = resolve(path)
            url_name = resolver_match.url_name
        except Resolver404:
            url_name = None

        # Public views
        public_url_names = ['landing', 'login', 'logout', 'register']
        if url_name in public_url_names:
            return self.get_response(request)

        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')

        # Check onboarding progress
        onboarding_url_names = ['company_setup', 'loading', 'company_profile', 'business_profile', 'onboarding_complete']
        
        try:
            company = request.user.company
            step = company.onboarding_step
        except Company.DoesNotExist:
            company = None
            step = 0

        # If onboarding is incomplete, redirect to the appropriate step
        if step < 3:
            if url_name not in onboarding_url_names:
                if step == 0 or company is None:
                    return redirect('company_setup')
                elif step == 1:
                    return redirect('company_profile')
                elif step == 2:
                    return redirect('business_profile')

        # Define URL name to permission mapping
        # Maps URL names to the required django permission codename
        permission_mapping = {
            # Items module
            'items_list': 'my_account.view_item',
            'inventory': 'my_account.view_item',
            'item_create': 'my_account.add_item',
            'item_import': 'my_account.add_item',
            'item_edit': 'my_account.change_item',
            'item_detail': 'my_account.view_item',
            
            # Invoices
            'invoices_list': 'my_account.view_invoice',
            'invoice_detail': 'my_account.view_invoice',
            'invoice_create': 'my_account.add_invoice',
            'invoice_import': 'my_account.add_invoice',
            'invoice_edit': 'my_account.change_invoice',
            'invoice_delete': 'my_account.delete_invoice',
            
            # Customers
            'customer_home': 'my_account.view_customer',
            'customers_list': 'my_account.view_customer',
            'customer_create': 'my_account.add_customer',
            'customer_import': 'my_account.add_customer',
            'customer_edit': 'my_account.change_customer',
            'customer_delete': 'my_account.delete_customer',
            'ajax_customer_create': 'my_account.add_customer',
            
            # Bills
            'bills_landing': 'my_account.view_bill',
            'bill_list': 'my_account.view_bill',
            'bill_new': 'my_account.add_bill',
            'bill_save': 'my_account.add_bill',
            'bill_import': 'my_account.add_bill',
            'bill_import_excel': 'my_account.add_bill',
            
            # Vendors
            'vendor_home': 'my_account.view_vendor',
            'vendors_list': 'my_account.view_vendor',
            'vendor_create': 'my_account.add_vendor',
            'vendor_import': 'my_account.add_vendor',
            'vendor_edit': 'my_account.change_vendor',
            'vendor_delete': 'my_account.delete_vendor',
            
            # Accounts
            'account_list': 'my_account.view_account',
            'account_create': 'my_account.add_account',
            'account_edit': 'my_account.change_account',
            'account_delete': 'my_account.delete_account',
            
            # Transactions
            'transaction_list': 'my_account.view_incometransaction',  # Account Manager / Admin
            'new_income': 'my_account.add_incometransaction',
            'save_income': 'my_account.add_incometransaction',
            'new_expense': 'my_account.add_expensetransaction',
            'save_expense': 'my_account.add_expensetransaction',
            
            # Transfers
            'transfers_landing': 'my_account.view_transfer',
            'view_transfer': 'my_account.view_transfer',
            'new_transfer': 'my_account.add_transfer',
            'import_transfers': 'my_account.add_transfer',
            'edit_transfer': 'my_account.change_transfer',
            'delete_transfer': 'my_account.delete_transfer',
            
            # Reconciliation
            'reconciliation_landing': 'my_account.view_reconciliation',
            'load_reconciliation_transactions': 'my_account.view_reconciliation',
            'new_reconciliation': 'my_account.add_reconciliation',
            'save_reconciliation': 'my_account.add_reconciliation',
            'delete_reconciliation': 'my_account.delete_reconciliation',
            
            # Reports
            'reports_landing': 'my_account.view_report',
            'create_report': 'my_account.add_report',
            'schedule_report': 'my_account.add_report',
            'update_report': 'my_account.change_report',
            'edit_report': 'my_account.change_report',
            'pin_report': 'my_account.change_report',
            'unpin_report': 'my_account.change_report',
            'delete_report': 'my_account.delete_report',
        }

        # Check permissions
        if url_name in permission_mapping:
            required_perm = permission_mapping[url_name]
            if not request.user.has_perm(required_perm):
                return render(request, 'authentication/403.html', status=403)

        # Admin only modules / views
        admin_only_url_names = [
            'double_entry_landing',
            'apps_marketplace',
            'app_detail',
            'install_app',
            'open_app',
        ]
        if url_name in admin_only_url_names:
            # Check if user is in 'Admin' group or has superuser status
            is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
            if not is_admin:
                return render(request, 'authentication/403.html', status=403)

        return self.get_response(request)
