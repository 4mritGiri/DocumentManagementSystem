from django.urls import reverse
from django.contrib import admin
from .models import Document, StoreRoom, Compartment, Package, Branch, PackageVerification, Rack
from django.utils.html import mark_safe
from .utils import generate_qr

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
    list_display = ('pkg_id', 'qr_code', 'pkg_name', 'document', 'details', 'packaging_size', 'status', 'destruction_eligible_time', 'remarks', 'storeLocation', 'created_at', 'updated_at')

    def document(self, obj):
        return obj.document_type.doc_type
    
    def storeLocation(self, obj):
        return obj.store_location.store_room_name + ', ' + obj.store_location.branch.branch_name

    def qr_code(self, obj):
        # Generate QR code and get the path
        qr_code_path = f"./media/uploads/qr_codes/{obj.pkg_id}_qr_code.png"

        data = f"""
        Package ID: {obj.pkg_id}
        Package Name: {obj.pkg_name}
        Document Type: {obj.document_type.doc_type}
        Details: {obj.details}
        Packaging Size: {obj.packaging_size}
        Status: {obj.status}
        Destruction Eligible Time: {obj.destruction_eligible_time}
        Remarks: {obj.remarks}
        Store Location: {obj.store_location.store_room_name}, {obj.store_location.branch.branch_name}
        """
        
        generate_qr(data, output_path=qr_code_path)
        
        # url = reverse("admin:package_package_qr_code", kwargs={"pkg_id": obj.pkg_id})
        # if update page is open, ../../../../../
        return mark_safe(f'<a href="../../../../../{qr_code_path}" target="_blank"><img src="../../../../../{qr_code_path}" alt="{obj.pkg_name}" width="100" height="100" /></a>')

    qr_code.short_description = "QR Code"  # Column header in the admin
    readonly_fields = ['qr_code']

# Package verification
@admin.register(PackageVerification)
class PackageVerificationAdmin(admin.ModelAdmin):
    list_display = ('packages', 'authorizer', 'verification_remarks', 'verification_date')

    def packages(self, obj):
        return obj.package_id.pkg_id
    
    def authorizer(self, obj):
        return obj.authorizer.username
    
    