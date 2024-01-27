from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Package.models import Document
from .models import DocumentAccess, DocumentAccessLog, DocumentRequest


#                  **********
# ================= Document =================
#                  **********

# Create Add Document View 
@login_required
def addDocument(request):
    '''
    This function is used to add a document
    '''
    if request.method == 'POST':
        if (
            request.POST.get('document') and
            request.POST.get('doc_type') and
            request.POST.get('doc_details') or
            request.POST.get('file_no') or
            request.POST.get('voucher_no') or
            request.POST.get('user_for_deposit') or
            request.POST.get('date_for_deposit')
        ):
            document = Document()
            document.document = request.POST.get('document')
            document.doc_type = request.POST.get('doc_type')
            document.doc_details = request.POST.get('doc_details')
            document.file_no = request.POST.get('file_no')
            document.voucher_no = request.POST.get('voucher_no')
            document.user_for_deposit = request.POST.get('user_for_deposit')
            document.date_for_deposit = request.POST.get('date_for_deposit')
            document.save()
            messages.success(request, 'Document added successfully')
            return redirect('/document/list-document')
    else:
        return render(request, 'DocumentApps/add-document.html')
    
# Function to list documents
@login_required
def listDocument(request):
    '''
    This function is used to list all documents
    '''
    documents = Document.objects.all()
    return render(request, 'DocumentApps/list-document.html', {'documents': documents})

# Function to edit document
@login_required
def editDocument(request, id):
    '''
    This function is used to edit a document
    '''
    document = Document.objects.get(pk=id)

    if request.method == 'POST':
        doc_classification_type = request.POST.get('doc_classification_type')
        doc_type = request.POST.get('doc_type')
        doc_details = request.POST.get('doc_details')

        # Validate form data
        if not doc_classification_type or not doc_type or not doc_details:
            messages.error(request, 'All fields are required.')
            return render(request, 'DocumentApps/edit-document.html', {'document': document})

        # Create and save Document instance
        document.doc_classification_type = doc_classification_type
        document.doc_type = doc_type
        document.doc_details = doc_details
        document.save()

        messages.success(request, 'Document updated successfully')
        return redirect('/document/list-document')
    else:
        return render(request, 'DocumentApps/edit-document.html', {'document': document})
    
# Function to delete document
@login_required
def deleteDocument(request, id):
    '''
    This function is used to delete a document
    '''
    document = Document.objects.get(pk=id)
    document.delete()
    messages.success(request, 'Document deleted successfully')
    return redirect('/document/list-document')


#                  ******************
# ================= Document Request =================
#                  ******************

# Function to add document request
@login_required
def addDocumentRequest(request):
    '''
    This function is used to add a document request
    '''
    if request.method == 'POST':
        remarks = request.POST.get('remarks')
        access_type = request.POST.get('access_type')

        # Validate form data
        if not remarks or not access_type:
            messages.error(request, 'All fields are required.')
            return render(request, 'DocumentApps/DocRequest/add-document-request.html')

        # Create and save DocumentRequest instance
        document_request = DocumentRequest(
            requester=request.user,
            remarks=remarks,
            access_type=access_type
        )
        document_request.save()

        messages.success(request, 'Document request added successfully')
        return redirect('/document/list-document-request')
    else:
        return render(request, 'DocumentApps/DocRequest/add-document-request.html')
    

# Function to list document requests
@login_required
def listDocumentRequest(request):
    '''
    This function is used to list all document requests
    '''
    document_requests = DocumentRequest.objects.all()
    return render(request, 'DocumentApps/DocRequest/list-document-request.html', {'document_requests': document_requests})


#                   *****************
#  ================= Document Access =================
#                   *****************

# Function to add document access
@login_required
def addDocumentAccess(request):
    '''
    This function is used to add a document access
    '''
    if request.method == 'POST':
        document_request_id = request.POST.get('document_request_id')
        access_type = request.POST.get('access_type')
        reseal_package = request.POST.get('reseal_package')

        # Validate form data
        if not document_request_id or not access_type or not reseal_package:
            messages.error(request, 'All fields are required.')
            return render(request, 'DocumentApps/add-document-access.html')

        # Create and save DocumentAccess instance
        document_access = DocumentAccess(
            document_request_id=document_request_id,
            access_type=access_type,
            reseal_package=reseal_package
        )
        document_access.save()

        messages.success(request, 'Document access added successfully')
        return redirect('/document/list-document-access')
    else:
        return render(request, 'DocumentApps/add-document-access.html')

# Function to Document Access List View
@login_required
def listDocumentAccess(request):
    '''
    This function is used to list all document access
    '''
    document_accesses = DocumentAccess.objects.all()
    return render(request, 'DocumentApps/DocAccess/list-document-access.html', {'document_accesses': document_accesses})


#                   *********************
#  ================= Document Access Log =================
#                   *********************
# Function to document access log list view
@login_required
def listDocumentAccessLog(request):
    '''
    This function is used to list all document access log
    '''
    document_access_logs = DocumentAccessLog.objects.all()
    return render(request, 'DocumentApps/DocAccessLog/list-document-access-log.html', {'document_access_logs': document_access_logs})


