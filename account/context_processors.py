from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        latest = Notification.objects.filter(recipient=request.user, company__name=request.user.company.name).order_by('-timestamp')[:5]
        unread = Notification.objects.filter(recipient=request.user, read_status=False, company__name=request.user.company.name).count()
        return {
            'latest_notifications': latest,
            'unread_notification_count': unread
        }
    return {
        'latest_notifications': [],
        'unread_notification_count': 0
    }
