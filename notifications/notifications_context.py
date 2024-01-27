from .models import BroadcastNotification

def notifications_context(request):
    room_name = 'broadcast'
    notifications = BroadcastNotification.objects.filter(sent=True)
    return {
        'room_name': room_name,
        'notifications': notifications,
    }
