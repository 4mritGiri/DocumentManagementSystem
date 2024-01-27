from django.contrib import admin

from .models import BroadcastNotification
# Register your models here.

@admin.register(BroadcastNotification)
class BroadcastNotificationAdmin(admin.ModelAdmin):
    '''
    This class is used to define the admin panel of the broadcast notification
    '''
    list_display = ['title', 'message', 'broadcast_on', 'sent']
    list_filter = ['broadcast_on', 'sent']
    search_fields = ['title', 'message']
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'broadcast_on'
    fieldsets = (
        ('Broadcast Notification', {
            'fields': ('title', 'message', 'broadcast_on', 'sent')
        }),
    )


