from django.contrib import admin
from .models import Document, DocumentType, DocumentAccess, DocumentRequest, Post

# Register your models here.
admin.site.site_header = 'DMS Admin'
admin.site.site_title = 'DMS Admin Portal'
admin.site.index_title = 'Welcome to DMS Admin Portal'


# admin.site.register(Post)
# admin.site.register(Document)
# admin.site.register(DocumentType)
# admin.site.register(DocumentAccess)
# admin.site.register(DocumentRequest)

