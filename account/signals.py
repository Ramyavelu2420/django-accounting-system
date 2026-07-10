from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Invoice, Bill, Vendor, Customer, IncomeTransaction, ExpenseTransaction, Transfer, Company, Item, Category, InvoiceCategory, Account, Estimate
from .services import NotificationService

def get_users_in_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return list(group.user_set.all())
    except Group.DoesNotExist:
        return []

def get_admins():
    return list(User.objects.filter(is_superuser=True)) + get_users_in_group('Admin')

def notify_roles(roles, sender, company, module, object_id, title, message, url, notification_type):
    recipients = []
    for role in roles:
        if role == 'Admin':
            recipients.extend(get_admins())
        else:
            recipients.extend(get_users_in_group(role))
            
    # De-duplicate recipients
    recipients = list(set(recipients))
    
    for r in recipients:
        # Don't notify the sender themselves
        if r != sender:
            r_company = getattr(r, 'company', None) or company
            NotificationService.notify(
                recipient=r,
                sender=sender,
                company=r_company,
                module=module,
                object_id=object_id,
                title=title,
                message=message,
                url=url,
                notification_type=notification_type
            )

@receiver(post_save, sender=Invoice)
def invoice_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        created_by = instance.created_by or company.user
        # Sales Executive creates Invoice -> Notify Account Manager & Admin
        notify_roles(
            roles=['Account Manager', 'Admin'],
            sender=created_by,
            company=company,
            module='Invoices',
            object_id=instance.id,
            title='Invoice Created',
            message=f"Invoice {instance.invoice_number} created for {instance.customer.name} (Total: Rs.{instance.total})",
            url=f"/sales/invoices/{instance.id}/",
            notification_type='Invoice Created'
        )

@receiver(post_save, sender=Bill)
def bill_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        created_by = instance.created_by or company.user
        # Purchase Executive creates Bill -> Notify Account Manager & Admin
        notify_roles(
            roles=['Account Manager', 'Admin'],
            sender=created_by,
            company=company,
            module='Bills',
            object_id=instance.id,
            title='Bill Created',
            message=f"Bill {instance.bill_number} created from {instance.vendor.vendor_name} (Total: Rs.{instance.total})",
            url=f"/purchases/bills/list/",
            notification_type='Bill Created'
        )

@receiver(post_save, sender=IncomeTransaction)
def payment_received_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Account Manager creates Income -> Notify Admin
        notify_roles(
            roles=['Admin'],
            sender=company.user, # fallback
            company=company,
            module='Transactions',
            object_id=instance.id,
            title='Payment Received',
            message=f"Payment of Rs.{instance.amount} received (Tx: {instance.number})",
            url=f"/banking/transactions/",
            notification_type='Payment Received'
        )

@receiver(post_save, sender=ExpenseTransaction)
def payment_sent_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Account Manager creates Expense -> Notify Admin
        notify_roles(
            roles=['Admin'],
            sender=company.user, # fallback
            company=company,
            module='Transactions',
            object_id=instance.id,
            title='Payment Sent',
            message=f"Expense of Rs.{instance.amount} recorded (Tx: {instance.number})",
            url=f"/banking/transactions/",
            notification_type='Payment Sent'
        )

@receiver(post_save, sender=Transfer)
def transfer_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Account Manager creates Transfer -> Notify Admin
        notify_roles(
            roles=['Admin'],
            sender=company.user, # fallback
            company=company,
            module='Transfers',
            object_id=instance.id,
            title='Transfer Created',
            message=f"Transfer of Rs.{instance.amount} completed from {instance.from_account.name} to {instance.to_account.name}",
            url=f"/transfers/",
            notification_type='Transfer Created'
        )

@receiver(post_save, sender=Account)
def account_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Account Manager creates Account -> Notify Admin
        notify_roles(
            roles=['Admin'],
            sender=company.user, # fallback
            company=company,
            module='Accounts',
            object_id=instance.id,
            title='Account Created',
            message=f"Account '{instance.name}' created (No: {instance.number})",
            url=f"/banking/accounts/",
            notification_type='Account Created'
        )

@receiver(post_save, sender=Vendor)
def vendor_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Purchase Executive creates Vendor -> Notify Account Manager & Admin
        notify_roles(
            roles=['Account Manager', 'Admin'],
            sender=company.user, # fallback
            company=company,
            module='Vendors',
            object_id=instance.id,
            title='Vendor Created',
            message=f"Vendor '{instance.vendor_name}' added to contacts",
            url=f"/purchases/vendors/list/",
            notification_type='Vendor Created'
        )

@receiver(post_save, sender=Customer)
def customer_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Sales Executive creates Customer -> Notify Account Manager & Admin
        notify_roles(
            roles=['Account Manager', 'Admin'],
            sender=company.user, # fallback
            company=company,
            module='Customers',
            object_id=instance.id,
            title='Customer Created',
            message=f"Customer '{instance.name}' added to contacts",
            url=f"/customers/list/",
            notification_type='Customer Created'
        )

@receiver(post_save, sender=Item)
def item_created_signal(sender, instance, created, **kwargs):
    if created:
        company = instance.company
        # Admin creates Item -> Notify Sales Executive
        notify_roles(
            roles=['Sales Executive'],
            sender=company.user, # fallback
            company=company,
            module='Items',
            object_id=instance.id,
            title='Item Created',
            message=f"New Item {instance.name} has been added.",
            url=f"/items/",
            notification_type='Item Created'
        )

@receiver(post_save, sender=Category)
def vendor_category_created_signal(sender, instance, created, **kwargs):
    if created:
        # Categorized under Category (Vendor Category) -> Notify Purchase Executive
        # Get first company as fallback since Category doesn't link directly to company
        company = Company.objects.first()
        if company:
            notify_roles(
                roles=['Purchase Executive'],
                sender=company.user,
                company=company,
                module='Categories',
                object_id=instance.id,
                title='Vendor Category Created',
                message=f"New Vendor Category {instance.name} has been added.",
                url=f"/purchases/bills/",
                notification_type='Category Created'
            )

@receiver(post_save, sender=InvoiceCategory)
def customer_category_created_signal(sender, instance, created, **kwargs):
    if created:
        company = Company.objects.first()
        if company:
            notify_roles(
                roles=['Sales Executive'],
                sender=company.user,
                company=company,
                module='Categories',
                object_id=instance.id,
                title='Customer Category Created',
                message=f"New Customer Category {instance.name} has been added.",
                url=f"/sales/invoices/",
                notification_type='InvoiceCategory Created'
            )

@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    if created:
        company = Company.objects.first()
        if company:
            # Notify Admins
            notify_roles(
                roles=['Admin'],
                sender=instance,
                company=company,
                module='Users',
                object_id=instance.id,
                title='User Created',
                message=f"New user {instance.username} has registered",
                url=f"/admin/",
                notification_type='User Created'
            )


@receiver(post_save, sender=Estimate)
def estimate_saved_signal(sender, instance, created, **kwargs):
    company = instance.company
    created_by = instance.created_by or company.user
    
    if created:
        is_admin = created_by.is_superuser or created_by.groups.filter(name='Admin').exists()
        is_sales = created_by.groups.filter(name='Sales Executive').exists()
        
        if is_sales:
            notify_roles(
                roles=['Admin'],
                sender=created_by,
                company=company,
                module='Estimates',
                object_id=instance.id,
                title='Estimate Created',
                message=f"Sales Executive created Estimate {instance.estimate_number}.",
                url=f"/sales/estimates/{instance.id}/",
                notification_type='Estimate Created'
            )
        elif is_admin:
            notify_roles(
                roles=['Sales Executive'],
                sender=created_by,
                company=company,
                module='Estimates',
                object_id=instance.id,
                title='Estimate Created',
                message=f"Admin created Estimate {instance.estimate_number}.",
                url=f"/sales/estimates/{instance.id}/",
                notification_type='Estimate Created'
            )
    else:
        if instance.status == 'accepted':
            notify_roles(
                roles=['Sales Executive'],
                sender=created_by,
                company=company,
                module='Estimates',
                object_id=instance.id,
                title='Estimate Accepted',
                message=f"Estimate {instance.estimate_number} has been accepted.",
                url=f"/sales/estimates/{instance.id}/",
                notification_type='Estimate Accepted'
            )
