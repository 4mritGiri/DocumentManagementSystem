from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
# Create your models here.

class BroadcastNotification(models.Model):
    '''
    This model is used to create a broadcast notification
    '''
    title = models.CharField(max_length=255)
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        '''
        This function is used to return the title of the broadcast notification
        '''
        return self.title
    
    class Meta:
        '''
        This class is used to define the name of the table in the database
        '''
        db_table = 'broadcast_notification'
        verbose_name = 'Broadcast Notification'
        verbose_name_plural = 'Broadcast Notifications'
        ordering = ['-broadcast_on']


@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    ''''
    Call group_send to send function directly to send notifications or you can create a dynamic task beat schedule
    '''
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notifications.tasks.broadcast_notification", args=json.dumps((instance.id,)))



