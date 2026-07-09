import threading
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Notification

def send_notification_email_async(subject, body, recipient_email):
    def run():
        try:
            send_mail(
                subject,
                body,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@accounting.com'),
                [recipient_email],
                fail_silently=True
            )
        except Exception:
            pass
    threading.Thread(target=run).start()

class NotificationService:
    @staticmethod
    def notify(recipient, sender, company, module, object_id, title, message, url, notification_type):
        # 1. Create Notification record in PostgreSQL
        notif = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            company=company,
            module=module,
            object_id=object_id,
            title=title,
            message=message,
            url=url,
            notification_type=notification_type
        )
        
        # 2. Queue/Send Asynchronous Email
        if recipient.email:
            subject = f"[Akaunting Alert] {title}"
            body = (
                f"Title: {title}\n"
                f"Summary: {message}\n"
                f"Created By: {sender.username if sender else 'System'}\n"
                f"Company: {company.name}\n"
                f"Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Direct URL: {url}\n"
            )
            send_notification_email_async(subject, body, recipient.email)
            
        return notif
