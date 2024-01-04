from django.contrib import admin
from .models import DestructionEligible


@admin.register(DestructionEligible)
class DestructionEligibleAdmin(admin.ModelAdmin):
    list_display = ['destruction_eligible_id', 'related_package', 'is_expired', 'destruction_time', 'created_at']
    list_filter = ['is_expired', 'created_at']
    search_fields = ['related_package__pkg_name', 'is_expired', 'created_at']
    list_per_page = 25
    readonly_fields = ['is_expired', 'destruction_time', 'created_at']
    fieldsets = (
        ('Destruction Eligibility', {
            'fields': ('related_package', 'is_expired', )
        }),
        (
            'Destruction Eligibility Status', {
                'fields': ('destruction_time', 'created_at'),
                # 'classes': ('collapse',)
            }
        )
    )

    def package_name(self, obj):
        return obj.related_package.pkg_name
    
    
   
    
