from django.db import models

# Create your models here.
CLASSIFICATION_TYPE_CHOICES = (
    ('Normal', 'Normal'),
    ('Classified', 'Classified'),
)

# Document type
DOCUMENT_TYPE_CHOICES = (
    ('Vouchers', 'Vouchers'),
    ('Cheques', 'Cheques'),
    ('Client File', 'Client File'),
    ('Demand Draft', 'Demand Draft'),
    ('Guarantee', 'Guarantee'),
    ('Contracts', 'Contracts'),
)

class Document(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_classification_type = models.CharField(choices=CLASSIFICATION_TYPE_CHOICES, default='Normal', max_length=90)
    doc_type = models.CharField(choices=DOCUMENT_TYPE_CHOICES, default='Vouchers', max_length=90)
    doc_details = models.TextField()

    def __str__(self):
        return f'{self.doc_id} - {self.doc_classification_type} - {self.doc_type} - {self.doc_details}'

# Store
class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=90)
    store_location = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.store_id} - {self.store_name} - {self.store_location}'

# Branch 
class Branch(models.Model):
    uid = models.AutoField(primary_key=True)
    branch_code = models.CharField(max_length=60)
    branch_name = models.CharField(max_length=110)

    def __str__(self):
        return f'{self.uid} - {self.branch_code} - {self.branch_name}'


# room rack compartment
class RoomRackCompartment(models.Model):
    room_rack_compartment_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    room = models.CharField(max_length=90)
    rack = models.CharField(max_length=90)
    compartment = models.CharField(max_length=90)

    def __str__(self):
        return f'{self.room_rack_compartment_id} - {self.store.store_id} - {self.room} - {self.rack} - {self.compartment}'


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

class Package(models.Model):
    pkg_id = models.AutoField(primary_key=True)
    pkg_name = models.CharField(max_length=100)
    document_type = models.ForeignKey(Document, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    details = models.TextField()
    packaging_size = models.CharField(choices=PACKAGING_SIZE_CHOICES, default='Box size 1', max_length=90)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=90)
    destruction_eligible_time = models.CharField(choices=DESTRUCTION_ELIGIBLE_TIME, default='1 Year', max_length=90)
    remarks = models.TextField(blank=True, null=True)
    store_location = models.ForeignKey(RoomRackCompartment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

# Package verification
class PackageVerification(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    authorizer = models.CharField(max_length=90)
    verification_remarks = models.TextField()
    verification_date = models.DateTimeField(auto_now_add=True)
    
