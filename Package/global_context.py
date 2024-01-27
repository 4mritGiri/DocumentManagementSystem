from .models import Package, Branch, Compartment, Rack, Document, StoreRoom, DOCUMENT_CHOICES, DOCUMENT_TYPE_CHOICES, CONDITION_CHOICES, DESTRUCTION_ELIGIBLE_TIME , PACKAGING_SIZE_CHOICES, STATUS_CHOICES
from DocumentApps.models import DocumentAccessLog, DocumentRequest
from PackageCollection.models import PackageCollection

def global_context(request):
    '''
    This function is used to create a compartment
    '''
    branches = Branch.objects.all()
    compartments = Compartment.objects.all()
    racks = Rack.objects.all()
    documents = Document.objects.all()
    store_rooms = StoreRoom.objects.all()

    doc_type = DOCUMENT_TYPE_CHOICES
    document_select = DOCUMENT_CHOICES
    condition = CONDITION_CHOICES
    destruction_eligible_time = DESTRUCTION_ELIGIBLE_TIME
    packaging_size = PACKAGING_SIZE_CHOICES
    verification_status = STATUS_CHOICES

    # Document Access log
    document_access_logs = DocumentAccessLog.objects.all()
    # Document Request log
    # document_request_logs = DocumentRequestLog.objects.all()
    packages = Package.objects.all()
    package_collections = PackageCollection.objects.all()

    # zipped_data = zip(packages, package_collections)
# show only package status is approved and package collection status is not verified
    # zipped_data = zip(packages, package_collections)

    return {
        'branches': branches, 
        'compartments': compartments, 
        'racks': racks, 
        'documents': documents, 
        'store_rooms': store_rooms, 
        'doc_type': doc_type, 
        'document_select': document_select, 
        'condition': condition, 
        'destruction_eligible_time': destruction_eligible_time, 
        'packaging_size': packaging_size, 
        'verification_status': verification_status, 
        'document_access_logs': document_access_logs,

        'packages': packages,
        # 'zipped_data': zipped_data,
    }