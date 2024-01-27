from django.shortcuts import render
from channels.layers import get_channel_layer
from django.http import HttpResponse

from .models import BroadcastNotification
# Create your views here.

from asgiref.sync import async_to_sync
def broadcast_notification(request):
    channel_layer = get_channel_layer()
    # login user
    user = request.user
    notifications = BroadcastNotification.objects.filter(sent=True)
    for notification in notifications:
        async_to_sync(channel_layer.group_send)(
            "notification_broadcast",
            {
                "type": "send_notification",
                "message": {
                    "icon": "fas fa-bell fa-lg",
                    "user": notification.title,
                    "message": notification.message
                },
            },
        )
    return HttpResponse("<h1>Notification Sent</h1>")

