from django.contrib import admin
from .models import Document, DocumentType, DocumentAccess, DocumentRequest,Branch, Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'file_path', 'date_created', 'date_updated')
    list_filter = ('user', 'title', 'date_created', 'date_updated')
    search_fields = ('user', 'title', 'description', 'file_path', 'date_created', 'date_updated')
    readonly_fields = ('date_created', 'date_updated')
    # prepopulated_fields = {'slug': ('title',)}
    # ordering = ('user', 'title', 'date_created', 'date_updated')
    # filter_horizontal = ()
    # fieldsets = ()

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'user', 'file_path', 'date_created', 'date_updated')
   
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    # readonly_fields = ('date_created', 'date_updated')
    # prepopulated_fields = {'slug': ('title',)}
    # ordering = ('user', 'title', 'date_created', 'date_updated')
    # filter_horizontal = ()
    # fieldsets = ()

@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    list_display = ('document_request', 'store_incharge', 'access_type', 'remarks')


@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ('branch', 'inputter', 'authorizer', 'document_type', 'remarks', 'request_date')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)

