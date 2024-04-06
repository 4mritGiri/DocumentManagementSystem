from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from . import signals

# Create your models here.
DOCUMENT_TYPE_CHOICES = (
    ('Normal', 'Normal'),
    ('Classified', 'Classified'),
)

# Document type
DOCUMENT_CHOICES = (
    ('Vouchers', 'Vouchers'),
    ('Cheques', 'Cheques'),
    ('Client File', 'Client File'),
    ('Demand Draft', 'Demand Draft'),
    ('Guarantee', 'Guarantee'),
    ('Contracts', 'Contracts'),
)

class Document(models.Model):
    doc_id = models.AutoField(primary_key=True)
    document = models.CharField(choices=DOCUMENT_CHOICES, default='Vouchers', max_length=90)
    doc_type = models.CharField(choices=DOCUMENT_TYPE_CHOICES, default='Normal', max_length=90)
    doc_details = models.TextField(blank=True, null=True)
    file_no = models.CharField(max_length=90, blank=True, null=True)
    voucher_no = models.CharField(max_length=90, blank=True, null=True)
    # cheque_no = models.CharField(max_length=90, blank=True, null=True)
    user_for_deposit = models.CharField(max_length=90, blank=True, null=True)
    date_for_deposit = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.document} - {self.doc_type} - {self.doc_details}'

# Branch 
class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_code = models.CharField(max_length=60)
    branch_name = models.CharField(max_length=110)
    branch_location = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.branch_id} - {self.branch_code} - {self.branch_name} - {self.branch_location}'



# Compartment
class Compartment(models.Model):
    compartment_id = models.AutoField(primary_key=True)
    compartment_name = models.CharField(max_length=90)
    compartment_location = models.CharField(max_length=150)
    rack = models.ForeignKey('Rack', on_delete=models.CASCADE, related_name='compartments', null=True)

    def __str__(self):
        return f'{self.compartment_id} - {self.compartment_name} - {self.compartment_location}'

# Rack
class Rack(models.Model):
    rack_id = models.AutoField(primary_key=True)
    rack_name = models.CharField(max_length=90)

    def __str__(self):
        return f'{self.rack_id} - {self.rack_name}'


# Store
class StoreRoom(models.Model):
    store_room_id = models.AutoField(primary_key=True)
    store_room_name = models.CharField(max_length=90)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_room_id} - {self.store_room_name} - {self.rack} - {self.branch}'

# Packaging size choice
PACKAGING_SIZE_CHOICES = (
    ('Box size 1', 'Box size 1'),
    ('Box size 2', 'Box size 2'),
    ('Plastic Bag', 'Plastic Bag'),
)

# Status choice
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

# destruction eligible time
DESTRUCTION_ELIGIBLE_TIME = (
    ('1 Year', '1 Year'),
    ('2 Years', '2 Years'),
    ('3 Years', '3 Years'),
    ('4 Years', '4 Years'),
    ('5 Years', '5 Years'),
    ('6 Years', '6 Years'),
    ('7 Years', '7 Years'),
    ('8 Years', '8 Years'),
)

CONDITION_CHOICES = [
        ('Good', 'Good'),
        ('Damaged (Mouse)', 'Damaged (Mouse)'),
        ('Damaged (Fire)', 'Damaged (Fire)'),
        ('Damaged (Accident)', 'Damaged (Accident)'),
    ]

class Package(models.Model):
    pkg_id = models.AutoField(primary_key=True)
    pkg_name = models.CharField(max_length=100)
    document_type = models.ForeignKey(Document, on_delete=models.CASCADE)
    details = models.TextField()
    packaging_size = models.CharField(choices=PACKAGING_SIZE_CHOICES, default='Box size 1', max_length=90)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=90)
    destruction_eligible_time = models.CharField(choices=DESTRUCTION_ELIGIBLE_TIME, default='1 Year', max_length=90)
    remarks = models.TextField(blank=True, null=True)
    condition = models.CharField(choices=CONDITION_CHOICES, default='Good', max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='packages', null=True)
    is_sealed = models.BooleanField(default=False)
    is_collected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'{self.pkg_name} - {self.document_type.doc_type} - {self.status}'

    class Meta:
        ordering = ['-created_at']
    
# Package verification
class PackageVerification(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='verifications')
    authorizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class VerificationStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    verification_remarks = models.TextField()
    verification_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If the status is changed during verification, update the Package status
        if self.status != self._state.adding and self.status != self.package.status:
            self.package.status = self.status
            self.package.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.package} - {self.authorizer} - {self.status} - {self.verification_date}'

    class Meta:
        ordering = ['-verification_date']

# Send notification when package is verified by authorizer to the user who created the package
def send_verification_notification(sender, instance, created, **kwargs):
    if kwargs['created']:
        package = instance.package
        user_to_notify = package.created_by

        # Send notification to user_to_notify
        print("Sending notification to user_to_notify")


        try:
            from notifications.models import BroadcastNotification
            notification = BroadcastNotification.objects.create(
                user=user_to_notify,
                title='Package Verification',
                message=f'Your package {package.pkg_name} has been {instance.status} by {instance.authorizer}.',
                icon='fas fa-box fa-lg',
                url=f'/package/{package.pkg_id}/',
            )
            notification.save()
            print("Notification sent to user_to_notify")
        except Exception as e:
            print("Error sending notification to user_to_notify")
            print(e)


