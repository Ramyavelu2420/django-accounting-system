from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        latest = Notification.objects.filter(recipient=request.user).order_by('read_status', '-timestamp')[:5]
        unread = Notification.objects.filter(recipient=request.user, read_status=False).count()
        return {
            'latest_notifications': latest,
            'unread_notification_count': unread
        }
    return {
        'latest_notifications': [],
        'unread_notification_count': 0
    }
