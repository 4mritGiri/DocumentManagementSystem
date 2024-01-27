from Package.models import Package, StoreRoom
from django.contrib.auth.models import Group
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

class DocumentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    ACCESS_TYPE_CHOICES = [
        ('copy', 'Request for Copy'),
        ('original', 'Request for Original Copy'),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document_requests')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='document_requests', help_text='Package (mandatory)')
    remarks = models.TextField(help_text='Remarks (mandatory)')
    authorizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authorized_requests')
    authorization_remarks = models.TextField(help_text='Authorization Remarks (mandatory)')
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document Request #{self.pk}"

class DocumentAccess(models.Model):
    ACCESS_TYPE_CHOICES = [
        ('photocopy', 'Provide Photocopy'),
        ('original', 'Provide Original Copy'),
    ]

    RETURN_STATUS_CHOICES = [
        ('not_returned', 'Not Returned'),
        ('returned', 'Returned'),
    ]

    document_request = models.OneToOneField(DocumentRequest, on_delete=models.CASCADE, related_name='access')
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPE_CHOICES)
    reseal_package = models.BooleanField(default=False)
    return_status = models.CharField(max_length=15, choices=RETURN_STATUS_CHOICES, default='not_returned')

    def __str__(self):
        return f"Document Access #{self.pk}"

@receiver(post_save, sender=DocumentAccess)
def create_document_access_log(sender, instance, created, **kwargs):
    if created:
        DocumentAccessLog.objects.create(document_access=instance, access_provided_by=instance.document_request.authorizer)

class DocumentAccessLog(models.Model):
    document_access = models.ForeignKey(DocumentAccess, on_delete=models.CASCADE, related_name='access_logs')
    access_provided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    return_condition = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Document Access Log #{self.pk}"
    