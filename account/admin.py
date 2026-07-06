from django.contrib import admin
from .models import Company, Category, Tax, IncomeAccount, ExpenseAccount, Item, Customer, CustomerContact, InvoiceCategory, Invoice, InvoiceItem, InvoiceAttachment, Vendor, VendorContact, Bill, BillItem, Account, IncomeTransaction, ExpenseTransaction, Transfer, Reconciliation, ReconciliationTransaction, Report, PinnedReport, ScheduledReport, App, AppInstallation, DashboardWidget, Dashboard

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Tax)
admin.site.register(IncomeAccount)
admin.site.register(ExpenseAccount)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(CustomerContact)
admin.site.register(InvoiceCategory)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(InvoiceAttachment)
admin.site.register(Vendor)
admin.site.register(VendorContact)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(Account)
admin.site.register(IncomeTransaction)
admin.site.register(ExpenseTransaction)

class TransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_number', 'from_account', 'to_account', 'date', 'amount', 'payment_method')
    search_fields = ('transfer_number', 'reference')
    list_filter = ('payment_method', 'date', 'created_by')

admin.site.register(Transfer, TransferAdmin)

admin.site.register(Reconciliation)
admin.site.register(ReconciliationTransaction)

admin.site.register(Report)
admin.site.register(PinnedReport)
admin.site.register(ScheduledReport)

admin.site.register(App)
admin.site.register(AppInstallation)

admin.site.register(DashboardWidget)
admin.site.register(Dashboard)


