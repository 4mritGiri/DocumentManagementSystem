from django.shortcuts import render, redirect

from .models import PackageCollection
from Package.models import Package, StoreRoom
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

# Function to list packageCollection
def packageCollection(request):
    package_collections = PackageCollection.objects.all()
    return render(request, 'PackageCollection/package-collection.html', {'package_collections': package_collections})

# Function of create packageCollection 

@login_required(login_url='login')
def createPackageCollection(request):
    if request.method == 'POST':
        package_collection = PackageCollection()
        
        # Retrieve the Package instance based on the package ID
        package_id = request.POST['package']
        package = get_object_or_404(Package, pk=package_id)

        package_collection.package = package
        package_collection.collector = request.user
        # package_collection.collection_date = request.POST['collection_date']
        package_collection.tampering_verification_remarks = request.POST['tampering_verification_remarks']

        # Retrieve the StoreRoom instance based on the store room ID
        store_room_id = request.POST['store_location']
        store_room = get_object_or_404(StoreRoom, pk=store_room_id)
        package_collection.store_location = store_room

        if 'tampering_detected' in request.POST:
                package_collection.tampering_detected = request.POST['tampering_detected']
            
        # package_collection.tampering_detected = request.POST['tampering_detected']
        package_collection.is_verified = request.POST['is_verified']
        package_collection.save()
    
        messages.success(request, 'Package Collection created successfully')
        return redirect('list-package-collection')
    else:
        messages.error(request, 'Package Collection failed to create')
        return render(request, 'PackageCollection/create-package-collection.html')
