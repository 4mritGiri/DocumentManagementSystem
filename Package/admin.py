from django.contrib import admin
from .models import Document, Store, RoomRackCompartment, Package, Branche, PackageVerification
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'doc_id', 'doc_classification_type', 'doc_details')
    list_filter = ('doc_classification_type', 'doc_type')
    search_fields = ('doc_id', 'doc_classification_type', 'doc_type', 'doc_details')

# Branch
@admin.register(Branche)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'uid', 'branch_code')
    list_filter = ('branch_name', 'branch_code')
    search_fields = ('branch_name', 'branch_code')


# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'store_id', 'store_location')
    list_filter = ('store_name', 'store_location')
    search_fields = ('store_id', 'store_name', 'store_location')

# Register your models here.
@admin.register(RoomRackCompartment)
class RoomRackCompartmentAdmin(admin.ModelAdmin):
    list_display = ('room_rack_compartment_id', 'Store', 'room', 'rack', 'compartment')
    list_filter = ('room', 'rack', 'compartment')
    search_fields = ('room_rack_compartment_id', 'room', 'rack', 'compartment')

    def Store(self, obj):
        return f'id: {obj.store.store_id}, {obj.store.store_name}, {obj.store.store_location}'


# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('pkg_name', 'pkg_id', 'document', 'branch_name', 'details', 'packaging_size', 'status', 'destruction_eligible_time', 'remarks', 'storeLocation', 'created_at', 'updated_at')

    search_fields = ('pkg_id', 'pkg_name', 'document_type', 'branch', 'details', 'packaging_size', 'status', 'destruction_eligible_time', 'remarks', 'store_location', 'created_at', 'updated_at')

   
    def document(self, obj):
        return obj.document_type.doc_type
    
    def branch_name(self, obj):
        return obj.branch.branch_name
    
    def storeLocation(self, obj):
        return obj.store_location.room + ', ' + obj.store_location.rack + ', ' + obj.store_location.compartment
    
    # package_id.short_description = 'Package ID'
    # document.short_description = 'Document'
    # store.short_description = 'Store'
    # room.short_description = 'Room'
    # rack.short_description = 'Rack'
    # compartment.short_description = 'Compartment'
    # packaging_size.short_description = 'Packaging Size'
    # status.short_description = 'Status'
    # destruction_eligible_time.short_description = 'Destruction Eligible Time'
    
   
    # def save_model(self, request, obj, form, change):
    #     obj.store_location = RoomRackCompartment.objects.get(store__store_name__exact=request.user.username)
    #     obj.save()

# Compare this snippet from DocumentManagementSystem/Package/views.py:
        
# Compare this snippet from DocumentManagementSystem/Package/urls.py:
        
# Compare this snippet from DocumentManagementSystem/Package/admin.py:
        
# Compare this snippet from DocumentManagementSystem/Package/models.py:
        

# Package verification
@admin.register(PackageVerification)
class PackageVerificationAdmin(admin.ModelAdmin):
    list_display = ('package_id',
'authorizer',
'verification_remarks',
'verification_date', 'verification_date')