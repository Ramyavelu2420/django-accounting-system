from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=10, default='en')
    currency = models.CharField(max_length=10, default='USD')
    country = models.CharField(max_length=100)
    
    # Step 1 Profile Wizard Fields
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    financial_year = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    # Step 2 Business Profile Wizard Fields
    business_type = models.CharField(max_length=100, blank=True, null=True)
    company_role = models.CharField(max_length=100, blank=True, null=True)
    business_experience = models.CharField(max_length=100, blank=True, null=True)
    team_size = models.CharField(max_length=100, blank=True, null=True)
    billing_method = models.CharField(max_length=100, blank=True, null=True)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    
    # Onboarding tracking: 0=not setup, 1=company created/needs profiles, 2=wizard 1 done, 3=wizard 2 (fully) done
    onboarding_step = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tax(models.Model):
    tax_name = models.CharField(max_length=255)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return f"{self.tax_name} ({self.tax_percentage}%)"


class IncomeAccount(models.Model):
    account_name = models.CharField(max_length=255)
    account_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"


class ExpenseAccount(models.Model):
    account_name = models.CharField(max_length=255)
    account_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"


class Item(models.Model):
    TYPE_CHOICES = [
        ('product', 'Product'),
        ('service', 'Service'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='product')
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
    description = models.TextField(blank=True, null=True)
    
    sale_enabled = models.BooleanField(default=True)
    purchase_enabled = models.BooleanField(default=True)
    
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    income_account = models.ForeignKey(IncomeAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
    expense_account = models.ForeignKey(ExpenseAccount, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'name'], name='unique_item_name_per_company')
        ]

    def __str__(self):
        return self.name


class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    invite_to_client_portal = models.BooleanField(default=False)
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, default='INR')
    chart_of_account = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=255, default='India')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomerContact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name



class InvoiceCategory(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return self.name


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=100)
    order_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='INR')
    notes = models.TextField(blank=True, null=True)
    category = models.ForeignKey(InvoiceCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoices')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'invoice_number'], name='unique_invoice_number_per_company')
        ]

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoice_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name


class InvoiceAttachment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='invoice_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Vendor(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vendors', null=True, blank=True)
    vendor_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='vendors/', blank=True, null=True)
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, default='INR')
    chart_of_account = models.CharField(max_length=255, blank=True, null=True)
    address_finder = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, default='India')
    gst_number = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name


class VendorContact(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name



class Bill(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bills')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='bills')
    bill_number = models.CharField(max_length=100)
    order_number = models.CharField(max_length=100, blank=True, null=True)
    bill_date = models.DateField()
    due_date = models.DateField()
    currency = models.CharField(max_length=10, default='INR')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    footer = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='bill_attachments/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_bills')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'bill_number'], name='unique_bill_number_per_company')
        ]

    def __str__(self):
        return self.bill_number


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.item_name


class Account(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='accounts', null=True, blank=True)
    type = models.CharField(max_length=50, choices=[('Bank', 'Bank'), ('Credit Card', 'Credit Card')], default='Bank')
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default='INR')
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    default_account = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_phone = models.CharField(max_length=50, blank=True, null=True)
    bank_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'number'], name='unique_account_number_per_company')
        ]

    def __str__(self):
        return f"{self.name} ({self.number})"


class IncomeTransaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='income_transactions')
    date = models.DateField()
    payment_method = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='income_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    chart_of_account = models.ForeignKey(IncomeAccount, on_delete=models.PROTECT, related_name='income_transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='income_transactions', blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='income_transactions', blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT, related_name='income_transactions', blank=True, null=True)
    number = models.CharField(max_length=100)
    reference = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.FileField(upload_to='transaction_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number} - {self.amount}"


class ExpenseTransaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='expense_transactions')
    date = models.DateField()
    payment_method = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='expense_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    chart_of_account = models.ForeignKey(ExpenseAccount, on_delete=models.PROTECT, related_name='expense_transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='expense_transactions', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='expense_transactions', blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT, related_name='expense_transactions', blank=True, null=True)
    number = models.CharField(max_length=100)
    reference = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.FileField(upload_to='transaction_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number} - {self.amount}"


class Transfer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='transfers')
    transfer_number = models.CharField(max_length=100)
    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transfers_from')
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transfers_to')
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=100)
    reference = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.FileField(upload_to='transfer_attachments/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_transfers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transfer_number} ({self.amount})"


class Reconciliation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reconciliations')
    start_date = models.DateField()
    end_date = models.DateField()
    closing_balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_reconciliations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reconciliation for {self.account.name} ({self.start_date} to {self.end_date})"


class ReconciliationTransaction(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='reconciliation_transactions')
    income_transaction = models.ForeignKey(IncomeTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='reconciliations')
    expense_transaction = models.ForeignKey(ExpenseTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='reconciliations')
    is_cleared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reconciliation Item for {self.reconciliation.id}"


class Report(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, default='bi-bar-chart')
    report_type = models.CharField(max_length=100, default='Standard')
    group_by = models.CharField(max_length=100, default='None')
    period = models.CharField(max_length=100, default='Monthly')
    basis = models.CharField(max_length=100, default='Accrual')
    is_system = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='Active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PinnedReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pinned_reports')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='pinned_by')
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'report'], name='unique_user_pinned_report')
        ]

    def __str__(self):
        return f"{self.user.username} pinned {self.report.name}"


class ScheduledReport(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='schedules')
    frequency = models.CharField(max_length=50, choices=[
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly')
    ])
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, default='Active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='scheduled_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule for {self.report.name} to {self.email}"


class App(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.CharField(max_length=100, default='bi-cpu')
    banner_color = models.CharField(max_length=50, default='#565895')
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    version = models.CharField(max_length=50, default='1.0.0')
    developer = models.CharField(max_length=255, default='Akaunting')
    website = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AppInstallation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='installations')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='installed_users')
    installed = models.BooleanField(default=False)
    installed_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Installed')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'app'], name='unique_user_app_installation')
        ]

    def __str__(self):
        return f"{self.user.username} installed {self.app.name}"


class Dashboard(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_dashboards')
    users = models.ManyToManyField(User, related_name='accessible_dashboards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['created_by', 'name'], name='unique_created_by_dashboard_name')
        ]

    def __str__(self):
        return self.name


class DashboardWidget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='widgets')
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets', null=True, blank=True)
    widget_name = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=100)
    width = models.IntegerField(default=50)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'dashboard', 'widget_name'], name='unique_user_dashboard_widget_name')
        ]

    def __str__(self):
        return f"{self.widget_name} ({self.width}%)"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notifications')
    module = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"


class Estimate(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('converted', 'Converted'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='estimates')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='estimates')
    estimate_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='INR')
    notes = models.TextField(blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='estimates')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_estimates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'estimate_number'], name='unique_estimate_number_per_company')
        ]

    def __str__(self):
        return self.estimate_number


class EstimateItem(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True, related_name='estimate_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name








