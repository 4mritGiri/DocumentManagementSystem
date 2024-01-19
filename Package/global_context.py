from .models import Package, Branch, Compartment, Rack, Document, StoreRoom, CLASSIFICATION_TYPE_CHOICES, DOCUMENT_TYPE_CHOICES, CONDITION_CHOICES, DESTRUCTION_ELIGIBLE_TIME , PACKAGING_SIZE_CHOICES, STATUS_CHOICES
from DocumentApps.models import DocumentAccessLog, DocumentRequest

def global_context(request):
    '''
    This function is used to create a compartment
    '''
    branches = Branch.objects.all()
    compartments = Compartment.objects.all()
    racks = Rack.objects.all()
    documents = Document.objects.all()
    store_rooms = StoreRoom.objects.all()

    doc_classification_type = CLASSIFICATION_TYPE_CHOICES
    doc_type = DOCUMENT_TYPE_CHOICES
    condition = CONDITION_CHOICES
    destruction_eligible_time = DESTRUCTION_ELIGIBLE_TIME
    packaging_size = PACKAGING_SIZE_CHOICES
    status = STATUS_CHOICES

    # Document Access log
    document_access_logs = DocumentAccessLog.objects.all()
    # Document Request log
    # document_request_logs = DocumentRequestLog.objects.all()
    
    return {'branches': branches, 'compartments': compartments, 'racks': racks, 'documents': documents, 'store_rooms': store_rooms, 'doc_classification_type': doc_classification_type, 'doc_type': doc_type, 'condition': condition, 'destruction_eligible_time': destruction_eligible_time, 'packaging_size': packaging_size, 'status': status, 'document_access_logs': document_access_logs}