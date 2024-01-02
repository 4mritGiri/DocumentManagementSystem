from django.contrib import admin
from .models import Document, StoreRoom, Compartment, Package, Branch, PackageVerification, Rack
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'doc_id', 'doc_classification_type', 'doc_details')
    list_filter = ('doc_classification_type', 'doc_type')
    search_fields = ('doc_id', 'doc_classification_type', 'doc_type', 'doc_details')

# Branch
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'branch_id', 'branch_code', 'branch_location')
    list_filter = ('branch_name', 'branch_code', 'branch_location')
    search_fields = ('branch_id', 'branch_name', 'branch_code', 'branch_location')

# Compartment
@admin.register(Compartment)
class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('compartment_name', 'compartment_id', 'compartment_location')
    list_filter = ('compartment_name', 'compartment_location')
    search_fields = ('compartment_id', 'compartment_name', 'compartment_location')


# Rack
@admin.register(StoreRoom)
class StoreRoomAdmin(admin.ModelAdmin):
    list_display = ('room', 'room_id', 'room_location')
    list_filter = ('store_room_name', 'store_room_id')
    search_fields = ('store_room_id', 'store_room_name')

    def room(self, obj):
        return obj.store_room_name
    
    def room_id(self, obj):
        return obj.store_room_id
    
    def room_location(self, obj):
        return obj.rack.rack_name + ', ' + obj.branch.branch_name
    
    def get_queryset(self, request):
        qs = super(StoreRoomAdmin, self).get_queryset(request)
        return qs.select_related('rack', 'branch')
    

# Rack
@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('rack_name', 'rack_id', 'rack_location')
    list_filter = ('rack_name', 'rack_id')
    search_fields = ('rack_id', 'rack_name')

    def rack_name(self, obj):
        return obj.rack_name
    
    def rack_id(self, obj):
        return obj.rack_id
    
    def rack_location(self, obj):
        return obj.compartment.compartment_name + ', ' + obj.compartment.compartment_location

# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('pkg_id', 'pkg_name', 'document', 'details', 'packaging_size', 'status', 'destruction_eligible_time', 'remarks', 'storeLocation', 'created_at', 'updated_at')

   
    def document(self, obj):
        return obj.document_type.doc_type
    
    def storeLocation(self, obj):
        return obj.store_location.store_room_name + ', ' + obj.store_location.branch.branch_name
        

# Package verification
@admin.register(PackageVerification)
class PackageVerificationAdmin(admin.ModelAdmin):
    list_display = ('package_id', 'authorizer', 'verification_remarks', 'verification_date')

    def package_id(self, obj):
        return obj.package.pkg_id
    
    def authorizer(self, obj):
        return obj.authorizer.username
    
    