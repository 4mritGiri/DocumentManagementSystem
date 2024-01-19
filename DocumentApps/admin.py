from django.contrib import admin
from .models import DocumentRequest, DocumentAccess, DocumentAccessLog

# Register your models here.
@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'remarks', 'authorizer', 'authorization_remarks', 'access_type')
    list_filter = ('requester', 'authorizer', 'access_type')
    search_fields = ('requester_username', 'authorizer_username')

    fieldsets = (
        (
            "Requester Details",{
                'fields': ('requester', 'remarks', 'package')
            }
        ),
        (
            "Requester authorizer",{
                'fields': ('authorizer', 'authorization_remarks')
            }
        ),
        (
            "Requester Access Type",{
                'fields': ('access_type',)
            }
        )
    )

@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_request', 'access_type', 'reseal_package')
    list_filter = ('access_type', 'reseal_package')
    search_fields = ('document_request_id',)
    fieldsets = (
        (None, {
            'fields': ('document_request', 'access_type', 'reseal_package')
        }),
    )

@admin.register(DocumentAccessLog)
class DocumentAccessLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_access', 'access_provided_by', 'access_date', 'return_date', 'return_condition')
    list_filter = ('access_provided_by',)
    search_fields = ('document_access_id', 'access_provided_by_username')
    fieldsets = (
        (
            "Document Access Details",{
                'fields': ('document_access', 'access_provided_by')
            }
        ),
        (
            "Return Details",{
                'fields': ('return_date', 'return_condition')
            }
        )
    )