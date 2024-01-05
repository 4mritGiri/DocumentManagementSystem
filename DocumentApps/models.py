from django.db import models
from Package.models import User, Package, StoreRoom


class DocumentRequest(models.Model):
    ACCESS_TYPE_CHOICES = [
        ('copy', 'Request for Copy'),
        ('original', 'Request for Original Copy'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_requests')
    remarks = models.TextField(help_text='Remarks (mandatory)')
    authorizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorized_requests')
    authorization_remarks = models.TextField(help_text='Authorization Remarks (mandatory)')
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPE_CHOICES)

    def _str_(self):
        return f"Document Request #{self.pk}"

class DocumentAccess(models.Model):
    ACCESS_TYPE_CHOICES = [
        ('photocopy', 'Provide Photocopy'),
        ('original', 'Provide Original Copy'),
    ]

    document_request = models.OneToOneField(DocumentRequest, on_delete=models.CASCADE, related_name='access')
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPE_CHOICES)
    reseal_package = models.BooleanField(default=False)

    def _str_(self):
        return f"Document Access #{self.pk}"

class DocumentAccessLog(models.Model):
    document_access = models.ForeignKey(DocumentAccess, on_delete=models.CASCADE, related_name='access_logs')
    access_provided_by = models.ForeignKey(User, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    return_condition = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"Document Access Log #{self.pk}"