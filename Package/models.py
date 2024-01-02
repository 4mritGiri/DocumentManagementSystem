from django.db import models
from django.contrib.auth.models import User

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


    def __str__(self):
        return f'{self.compartment_id} - {self.compartment_name} - {self.compartment_location}'

# Rack
class Rack(models.Model):
    rack_id = models.AutoField(primary_key=True)
    rack_name = models.CharField(max_length=90)
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rack_id} - {self.rack_name} - {self.rack_location}'
    

# Store
class StoreRoom(models.Model):
    store_room_id = models.AutoField(primary_key=True)
    store_room_name = models.CharField(max_length=90)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_room_id} - {self.store_room_name} - {self.rack} - {self.branch}'


# # room rack compartment
# class RoomRackCompartment(models.Model):
#     room_rack_compartment_id = models.AutoField(primary_key=True)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     room = models.CharField(max_length=90)
#     rack = models.CharField(max_length=90)
#     compartment = models.CharField(max_length=90)

#     def __str__(self):
#         return f'{self.room_rack_compartment_id} - {self.store.store_id} - {self.room} - {self.rack} - {self.compartment}'


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
    # branch = models.ForeignKey(Branche, on_delete=models.CASCADE)
    details = models.TextField()
    packaging_size = models.CharField(choices=PACKAGING_SIZE_CHOICES, default='Box size 1', max_length=90)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=90)
    destruction_eligible_time = models.CharField(choices=DESTRUCTION_ELIGIBLE_TIME, default='1 Year', max_length=90)
    remarks = models.TextField(blank=True, null=True)
    store_location = models.ForeignKey(StoreRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

# 					* assign dcoument type - c		** API connection with current HR system for auto user creation and update				
# 					* destruction period - f						
# WORKFLOW											
# 				a. Packages	b. Document *	c. Document Type	d. User Role**	e. Branch**	f. store	g. Room/Rack/Compartment	f. destruction eligible time
# 1. User Login				Box size 1	Vouchers	Normal	Admin	Branch 1	Store 1		1 year
# Username	Roles	Access		Box Size 2	Cheques	Classified	Inputter	Branch 2	Store 2		2 year
#  USER 1 	Create Package / Request for access to package	Specified Branch		Plastic Bag	Client File		Authoriser	Branch 3	Store 3		3 year
#  USER 2 	Verify Packages Created / Verify Request for access to pakage	Specified Branch			Demand Draft						4 year
# 					Guarantee						5 year
# 2. Package Creation	can be editable unless verified				Contracts						6 year
# 	- create new package for document transfer at Store	Unique ID (Branch Code,FY,001 and so on)									7 year
# 	- select document	single document type only									8 year
# 	- define document details like  date and user for deposit voucher voucher nuber for vouchers, file number for client file etc										
# 	- select packaging size										
# 	- provide remarks (optional)										
# 	- save and print details 2 copies										
											
# 3. Verifiy Package Created	cannot be edited after verification, if required (edit request to admin)										
# 	- Authoriser verify the package created										
# 	- provide remarks (mandatory) and verify										
# 	- verified package to sealed and processed to store location (write package ID in package with permanent marker)										
											
											
# 4. Collection of Package	store person collect the package from branch and acknowledge package in system and print one copy for branch										
# 	- verify for the tamering/sealing of packages before receiving 										
# 	- provide remarks (mandatory)										
# 	- print barcode/qr code tag and paste it in the package										
# 	- assign package to defined conpartment in the store										
											
											
# 5. Store Operation	scheduled monitoring of the store room										
# 	- provide scheduled monitoring 										
# 	- provide review to the damaged packages  damages due to mouse / fire / accident etc	package scan and update the package condition if damaged (alert the respective package owner regarding the damage with CC to assign operation person)									
											
											
# 6. Document request	branch request to access document										
# 	- inuptter request for the access of store documents at store  remarks (mandatory)										
# 	- authoriser authorize the request remarks (mandatory)										
# 	 document access type  - request for the copy (photocopy to be provided)  - request for the original copy (return condition to be provided)										
											
											
# 7. Document Access	store incharge provide access to specified document under the supervision										
# 	 document access type  - provide photocopy of required document  - provide original copy as requested with return condition i.e. return date and other details	once document access is provided, the package should be re-sealed and updated, which is to be updated in system									
# 	- document access logs to be created 										
# 	- alret user for document return as defined period										
											
# 8. Destruction Eligible doument list	system should be able to alret the eligible packages for the destruction										
# 	- destruction eligible packages to be listed in store user and branch user dashboard										
											
											
# 9. Admin User	admin user update store manangement										
# 	create store room										
# 	create rack in store room										
# 	create compartment in rack in store room										
# 	assign branch/department to store room/ rack/ compartment										
# 	view storing capacity of the storeroom										
# 	view destrcution eligible packages for space management										
# 	view for pending returnable documents and follow up										
											
											
# Additional Requirement	provide web app for barcode/qr code scan for the package verification from compartment										


# class Package(models.Model):
#     package_id = models.AutoField(primary_key=True)
#     package_name = models.CharField(max_length=100)
#     document_type = models.ForeignKey(Document, on_delete=models.CASCADE)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     details = models.TextField()
#     packaging_size = models.CharField(choices=PACKAGING_SIZE_CHOICES, default='Box size 1', max_length=90)
#     status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=90)
#     destruction_eligible_time = models.CharField(choices=DESTRUCTION_ELIGIBLE_TIME, default='1 Year', max_length=90)
#     remarks = models.TextField(blank=True, null=True)
#     store_location = models.ForeignKey(StoreRoom, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# Package verification
class PackageVerification(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    authorizer = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_remarks = models.TextField()
    verification_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.package_id} - {self.authorizer} - {self.verification_remarks} - {self.verification_date}'