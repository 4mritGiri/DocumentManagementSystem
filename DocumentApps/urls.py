from django.urls import path
from .views import *

urlpatterns = [
    path('add-document', addDocument, name='add-document'),
    path('list-document', listDocument, name='list-document'),
    path('edit-document/<int:id>', editDocument, name='edit-document'),
    path('delete-document/<int:id>', deleteDocument, name='delete-document'),

    # ==================== Document Request ====================
    path('add-document-request', addDocumentRequest, name='add-document-request'),
    path('list-document-request', listDocumentRequest, name='list-document-request'),

    # ==================== Document Access ====================
    path('add-document-access', addDocumentAccess, name='add-document-access'),
    path('list-document-access', listDocumentAccess, name='list-document-access'),

    # ==================== Document Access Log ====================
    path('list-document-access-log', listDocumentAccessLog, name='list-document-access-log'),

]
 