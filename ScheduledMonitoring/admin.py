from django.contrib import admin
from .models import StoreMonitoring, DamagedPackageReview

# Register your models here.

# StoreMonitoring
@admin.register(StoreMonitoring)
class StoreMonitoringAdmin(admin.ModelAdmin):
    list_display = ('store_room', 'scheduled_date', 'comments')
    list_filter = ('store_room',)
    search_fields = ('store_room__store_room_name', 'comments')

    fieldsets = (
        ("Store Room", {
            "fields": (
                'store_room',
            ),
        }),
        ("Monitoring Details", {
            "fields": (
                'scheduled_date',
                'comments',
            ),
        }),
    )

# DamagedPackageReview
@admin.register(DamagedPackageReview)
class DamagedPackageReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'reviewer', 'review_date', 'damage_comments', 'is_resolved')
    list_filter = ('reviewer', 'is_resolved')
    search_fields = ('package_pkg_name', 'reviewer_username')

    fieldsets = (
        ("Package", {
            "fields": (
                'package',
            ),
        }),
        ("Review Details", {
            "fields": (
                'reviewer',
                # 'review_date',
                'damage_comments',
                'is_resolved',
            ),
        }),
    )

