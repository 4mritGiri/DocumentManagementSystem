from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from cryptography.fernet import Fernet
from django.conf import settings
import base64, os
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='uploads/',blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + '-' + self.title

    def get_share_url(self):
        fernet = Fernet(settings.ID_ENCRYPTION_KEY)
        value = fernet.encrypt(str(self.pk).encode())
        value = base64.urlsafe_b64encode(value).decode()
        return reverse("share-file-id", kwargs={"id": (value)})

@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)

@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file_path
    except sender.DoesNotExist:
        return False

    new_file = instance.file_path
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            

# Create your models here.
class DocumentType(models.Model):
    name = models.CharField(max_length=100)


class UserRoles(models.Model):
    name = models.CharField(max_length=100)

class Branch(models.Model):
    name = models.CharField(max_length=100)

class Store(models.Model):
    name = models.CharField(max_length=100)
    # Add more fields here

class Document(models.Model):
    name = models.CharField(max_length=100)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='uploads/',blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_share_url(self):
        fernet = Fernet(settings.ID_ENCRYPTION_KEY)
        value = fernet.encrypt(str(self.pk).encode())
        value = base64.urlsafe_b64encode(value).decode()
        return reverse("share-file-id", kwargs={"id": (value)})

class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    package_id = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


class PackageVerification(models.Model):
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    authorizer = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_remarks = models.TextField()
    verification_date = models.DateTimeField(auto_now_add=True)


class PackageCollection(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    store_person = models.ForeignKey(User, on_delete=models.CASCADE)
    is_tampered = models.BooleanField(default=False)
    remarks = models.TextField()
    barcode_qr_code = models.CharField(max_length=255)
    compartment = models.CharField(max_length=255)
    collection_date = models.DateTimeField(auto_now_add=True)


class StoreOperation(models.Model):
    package_collection = models.ForeignKey(PackageCollection, on_delete=models.CASCADE)
    review_remarks = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

class DocumentRequest(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    inputter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inputted_document_requests')
    authorizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorized_document_requests')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    remarks = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)



class DocumentAccess(models.Model):
    document_request = models.ForeignKey(DocumentRequest, on_delete=models.CASCADE)
    store_incharge = models.ForeignKey(User, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=100)
    remarks = models.TextField()
    access_date = models.DateTimeField(auto_now_add=True)
