from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Company

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class CompanySetupForm(forms.ModelForm):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('zh-hans', '简体中文'),
        ('fr', 'Français'),
        ('es', 'Español'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD - US Dollar'),
        ('CNY', 'CNY - Chinese Yuan'),
        ('EUR', 'EUR - Euro'),
        ('GBP', 'GBP - British Pound'),
    ]
    
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Company
        fields = ['name', 'language', 'currency', 'country']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['tax_number', 'financial_year', 'address', 'country', 'logo']
        widgets = {
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tax Number'}),
            'financial_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Financial Year (e.g. 2026)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'logo': forms.FileInput(attrs={'class': 'd-none', 'id': 'logo-file-input'}),
        }


class BusinessProfileForm(forms.ModelForm):
    BUSINESS_TYPE_CHOICES = [
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('partnership', 'Partnership'),
        ('corporation', 'Corporation'),
        ('llc', 'Limited Liability Company (LLC)'),
        ('other', 'Other'),
    ]
    ROLE_CHOICES = [
        ('owner', 'Business Owner'),
        ('manager', 'Manager'),
        ('accountant', 'Accountant'),
        ('developer', 'Developer / Admin'),
        ('other', 'Other'),
    ]
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (less than 1 year)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3+ years)'),
    ]
    TEAM_SIZE_CHOICES = [
        ('1', 'Only me'),
        ('2-5', '2-5 people'),
        ('6-10', '6-10 people'),
        ('11-50', '11-50 people'),
        ('50+', 'More than 50 people'),
    ]
    BILLING_METHOD_CHOICES = [
        ('hourly', 'Hourly Rate'),
        ('fixed', 'Fixed Price / Project-based'),
        ('subscription', 'Subscription / Retainer'),
        ('milestone', 'Milestones'),
    ]
    PURPOSE_CHOICES = [
        ('invoicing', 'Send Invoices & Get Paid'),
        ('expense_tracking', 'Track Expenses & Receipts'),
        ('accounting', 'Full Accounting & Bookkeeping'),
        ('reporting', 'Tax Reporting & Business Analytics'),
        ('all', 'All of the above'),
    ]

    business_type = forms.ChoiceField(
        choices=BUSINESS_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    company_role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    business_experience = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    team_size = forms.ChoiceField(
        choices=TEAM_SIZE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    billing_method = forms.ChoiceField(
        choices=BILLING_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    purpose = forms.ChoiceField(
        choices=PURPOSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Company
        fields = ['business_type', 'company_role', 'business_experience', 'team_size', 'billing_method', 'purpose']


from .models import Item, Category, Tax, IncomeAccount, ExpenseAccount

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'type', 'name', 'category', 'description', 
            'sale_enabled', 'purchase_enabled', 'sale_price', 'purchase_price', 
            'income_account', 'expense_account', 'tax'
        ]
        widgets = {
            'type': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Description'}),
            'sale_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_sale_enabled'}),
            'purchase_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_purchase_enabled'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sale Price', 'step': '0.01'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Purchase Price', 'step': '0.01'}),
            'income_account': forms.Select(attrs={'class': 'form-select'}),
            'expense_account': forms.Select(attrs={'class': 'form-select'}),
            'tax': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(status='Active')
        self.fields['tax'].queryset = Tax.objects.filter(status='Active')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.company:
            qs = Item.objects.filter(company__name=self.company.name, name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An item with this name already exists in your company.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        sale_enabled = cleaned_data.get('sale_enabled')
        purchase_enabled = cleaned_data.get('purchase_enabled')
        sale_price = cleaned_data.get('sale_price')
        purchase_price = cleaned_data.get('purchase_price')

        if sale_enabled and sale_price is None:
            self.add_error('sale_price', "Sale price is required when Sale Information is enabled.")

        if purchase_enabled and purchase_price is None:
            self.add_error('purchase_price', "Purchase price is required when Purchase Information is enabled.")

        return cleaned_data


from .models import Customer, Invoice, InvoiceItem, InvoiceCategory, InvoiceAttachment

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Customer Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Customer Address'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer', 'invoice_number', 'order_number', 'invoice_date', 
            'due_date', 'currency', 'notes', 'category'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Number'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Order Number'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Notes'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['customer'].queryset = Customer.objects.filter(company__name=self.company.name)
        self.fields['category'].queryset = InvoiceCategory.objects.filter(status='Active')


from .models import CustomerContact

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'email', 'phone', 'website', 'reference', 'invite_to_client_portal', 
            'tax_number', 'currency', 'chart_of_account', 'address', 'city', 'state', 
            'postal_code', 'country'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Website'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Reference'}),
            'invite_to_client_portal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Tax Number'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
            'chart_of_account': forms.Select(choices=[('400', '400 - Sales'), ('410', '410 - Interest Income')], attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Town / City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Province / State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Postal / Zip Code'}),
            'country': forms.Select(choices=[('India', 'India'), ('United States', 'United States')], attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.company:
            qs = Customer.objects.filter(company=self.company, name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A customer with this name already exists in your company.")
        return name


from .models import Vendor, Bill, BillItem

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'email', 'phone', 'address', 'gst_number', 'currency']
        widgets = {
            'vendor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Vendor Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor Phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Vendor Address'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'vendor', 'bill_number', 'order_number', 'bill_date', 
            'due_date', 'currency', 'notes', 'category', 'footer'
        ]
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'bill_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bill Number'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Order Number'}),
            'bill_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Notes'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category'}),
            'footer': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Footer Text'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)


from .models import VendorContact

class VendorDetailsForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            'vendor_name', 'email', 'phone', 'website', 'reference', 'logo', 
            'tax_number', 'currency', 'chart_of_account', 'address_finder', 
            'address', 'city', 'postal_code', 'state', 'country'
        ]
        widgets = {
            'vendor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Website'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Reference'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'logo-file-input'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Tax Number'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
            'chart_of_account': forms.Select(choices=[('628', '628 - General Expenses'), ('600', '600 - Cost of Goods Sold')], attrs={'class': 'form-select'}),
            'address_finder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address Finder'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Town / City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Postal / Zip Code'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Province / State'}),
            'country': forms.Select(choices=[('India', 'India'), ('United States', 'United States')], attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

    def clean_vendor_name(self):
        name = self.cleaned_data.get('vendor_name')
        if self.company:
            qs = Vendor.objects.filter(company=self.company, vendor_name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A vendor with this name already exists in your company.")
        return name


from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'type', 'name', 'number', 'currency', 'opening_balance', 
            'default_account', 'bank_name', 'bank_phone', 'bank_address'
        ]
        widgets = {
            'type': forms.RadioSelect(choices=[('Bank', 'Bank'), ('Credit Card', 'Credit Card')]),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Number'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
            'opening_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'default_account': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Name'}),
            'bank_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Phone'}),
            'bank_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Bank Address'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if self.company:
            qs = Account.objects.filter(company=self.company, number__iexact=number)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An account with this number already exists in your company.")
        return number


from .models import IncomeTransaction, ExpenseTransaction, IncomeAccount, ExpenseAccount, Tax

class IncomeTransactionForm(forms.ModelForm):
    class Meta:
        model = IncomeTransaction
        fields = [
            'date', 'payment_method', 'account', 'amount', 'description', 
            'chart_of_account', 'category', 'customer', 'tax', 'number', 'reference', 'attachment'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Credit Card', 'Credit Card')], attrs={'class': 'form-select'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '₹0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Description'}),
            'chart_of_account': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'tax': forms.Select(attrs={'class': 'form-select'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TRA-00001'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Reference'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'attachment-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['account'].queryset = Account.objects.filter(company=self.company)
            self.fields['chart_of_account'].queryset = IncomeAccount.objects.all()
            self.fields['category'].queryset = Category.objects.all()
            self.fields['customer'].queryset = Customer.objects.filter(company=self.company)
            self.fields['tax'].queryset = Tax.objects.all()


class ExpenseTransactionForm(forms.ModelForm):
    class Meta:
        model = ExpenseTransaction
        fields = [
            'date', 'payment_method', 'account', 'amount', 'description', 
            'chart_of_account', 'category', 'vendor', 'tax', 'number', 'reference', 'attachment'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Credit Card', 'Credit Card')], attrs={'class': 'form-select'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '₹0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Description'}),
            'chart_of_account': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'tax': forms.Select(attrs={'class': 'form-select'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TRA-00001'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Reference'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'attachment-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['account'].queryset = Account.objects.filter(company=self.company)
            self.fields['chart_of_account'].queryset = ExpenseAccount.objects.all()
            self.fields['category'].queryset = Category.objects.all()
            self.fields['vendor'].queryset = Vendor.objects.filter(company=self.company)
            self.fields['tax'].queryset = Tax.objects.all()


from .models import Transfer

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = [
            'from_account', 'to_account', 'date', 'amount', 'description',
            'payment_method', 'reference', 'attachment'
        ]
        widgets = {
            'from_account': forms.Select(attrs={'class': 'form-select'}),
            'to_account': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '₹0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Description'}),
            'payment_method': forms.Select(choices=[('Cash', 'Cash'), ('Bank', 'Bank'), ('Cheque', 'Cheque'), ('Card', 'Card'), ('UPI', 'UPI')], attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Reference'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'attachment-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['from_account'].queryset = Account.objects.filter(company=self.company)
            self.fields['to_account'].queryset = Account.objects.filter(company=self.company)

    def clean(self):
        cleaned_data = super().clean()
        from_acc = cleaned_data.get('from_account')
        to_acc = cleaned_data.get('to_account')
        amount = cleaned_data.get('amount')

        if from_acc and to_acc and from_acc == to_acc:
            raise forms.ValidationError("Cannot transfer from same account to same account.")
        if amount is not None and amount <= 0:
            self.add_error('amount', "Amount must be greater than zero.")
        return cleaned_data


from .models import Reconciliation

class ReconciliationForm(forms.ModelForm):
    class Meta:
        model = Reconciliation
        fields = ['start_date', 'end_date', 'closing_balance', 'account']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'closing_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '₹0.00'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['account'].queryset = Account.objects.filter(company=self.company)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        closing_balance = cleaned_data.get('closing_balance')
        account = cleaned_data.get('account')

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "End Date must be greater than or equal to Start Date.")
        if closing_balance is not None and closing_balance < 0:
            self.add_error('closing_balance', "Closing Balance cannot be negative.")

        if account and start_date and end_date:
            overlapping = Reconciliation.objects.filter(
                account=account,
                start_date__lte=end_date,
                end_date__gte=start_date
            )
            if self.instance and self.instance.pk:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            if overlapping.exists():
                raise forms.ValidationError("A reconciliation already exists for this account in the specified date range.")

        return cleaned_data


from .models import Report, ScheduledReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'category', 'description', 'report_type', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Report Name'}),
            'category': forms.Select(choices=[('Accounting', 'Accounting'), ('Income & Expense', 'Income & Expense'), ('Custom', 'Custom')], attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Description'}),
            'report_type': forms.Select(choices=[('Standard', 'Standard'), ('Custom', 'Custom')], attrs={'class': 'form-select'}),
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], attrs={'class': 'form-select'}),
        }

class ScheduledReportForm(forms.ModelForm):
    class Meta:
        model = ScheduledReport
        fields = ['report', 'frequency', 'email', 'start_date', 'end_date', 'status']
        widgets = {
            'report': forms.Select(attrs={'class': 'form-select'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', "End Date must be after Start Date.")
        return cleaned_data


class ReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'report_type', 'description', 'group_by', 'period', 'basis']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'report_type': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'group_by': forms.Select(choices=[
                ('Category', 'Category'),
                ('Chart of Accounts', 'Chart of Accounts'),
                ('Customer', 'Customer'),
                ('Vendor', 'Vendor'),
                ('Month', 'Month'),
                ('Year', 'Year'),
                ('None', 'None')
            ], attrs={'class': 'form-select'}),
            'period': forms.Select(choices=[
                ('Daily', 'Daily'),
                ('Weekly', 'Weekly'),
                ('Monthly', 'Monthly'),
                ('Quarterly', 'Quarterly'),
                ('Yearly', 'Yearly'),
                ('Custom', 'Custom')
            ], attrs={'class': 'form-select'}),
            'basis': forms.Select(choices=[
                ('Accrual', 'Accrual'),
                ('Cash', 'Cash')
            ], attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Report.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A report with this name already exists.")
        return name


from .models import DashboardWidget

class DashboardWidgetForm(forms.ModelForm):
    class Meta:
        model = DashboardWidget
        fields = ['widget_name', 'widget_type', 'width', 'sort_order']
        widgets = {
            'widget_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'widget_type': forms.Select(choices=[
                ('Chart', 'Chart'),
                ('Table', 'Table'),
                ('Card', 'Card'),
                ('Graph', 'Graph'),
                ('Statistics', 'Statistics'),
                ('Summary', 'Summary'),
                ('List', 'List')
            ], attrs={'class': 'form-select'}),
            'width': forms.Select(choices=[
                (25, '25%'),
                (33, '33%'),
                (50, '50%'),
                (66, '66%'),
                (75, '75%'),
                (100, '100%')
            ], attrs={'class': 'form-select'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_widget_name(self):
        name = self.cleaned_data.get('widget_name')
        if self.user:
            qs = DashboardWidget.objects.filter(user=self.user, dashboard=self.instance.dashboard, widget_name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("You already have a dashboard widget with this name on this dashboard.")
        return name


from .models import Dashboard

class DashboardForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Dashboard
        fields = ['name', 'users']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.user:
            qs = Dashboard.objects.filter(created_by=self.user, name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("You already have a dashboard with this name.")
        return name


from .models import Estimate, EstimateItem

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = [
            'customer', 'estimate_number', 'issue_date', 'expiry_date', 
            'currency', 'notes', 'status'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'estimate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estimate Number'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.Select(choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar')], attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Notes'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['customer'].queryset = Customer.objects.filter(company__name=self.company.name)












