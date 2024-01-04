from django.contrib import admin
from .models import PackageCollection, Package
from Package.admin import PackageAdmin


@admin.register(PackageCollection)
class PackageCollectionAdmin(admin.ModelAdmin):
    list_display = ('package', 'collector', 'collection_date', 'tampering_verification_remarks', 'store_location', 'is_tampered', 'is_verified', 'display_qr_code')
    list_filter = ('package', 'collector', 'collection_date', 'store_location', 'is_tampered', 'is_verified')
    search_fields = ('package', 'collector', 'collection_date', 'store_location', 'is_tampered', 'is_verified')

    def package(self, obj):
        return obj.package.pkg_name
    
    def collector(self, obj):
        return obj.collector.username
    
    def store_location(self, obj):
        return obj.store_location.store_room_name + ', ' + obj.store_location.branch.branch_name

    def display_qr_code(self, obj):
        # Create an instance of PackageAdmin and call the qr_code method
        package_admin_instance = PackageAdmin(Package, admin.site)
        return package_admin_instance.qr_code(obj.package)

    display_qr_code.short_description = "QR Code"

    fieldsets = (
        ('Package Collection', {
            'fields': ('package', 'collector','store_location')
        }),
         (
            'Package Collection Status', {
                'fields': ('tampering_verification_remarks', 'is_tampered', 'is_verified'),
                # 'classes': ('collapse',) 
            }
        )
    )
    list_per_page = 25



    
