# # Package/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Package, Branch, Compartment, Rack, Document, StoreRoom
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create Branch view
@login_required
def createBranch(request):
    '''
    This function is used to create a branch
    '''
    if request.method == 'POST':
        branch = Branch()
        branch.branch_code = request.POST.get('branch_code')
        branch.branch_name = request.POST.get('branch_name')
        branch.branch_location = request.POST.get('branch_location')
        branch.save()
        messages.success(request, 'Branch added successfully')
        return redirect('/package/list-branch')
    else:
        return render(request, 'package/Branch/create-branch.html')

# View Branch list
@login_required
def listBranch(request):
    '''
    This function is used to list all branches
    '''
    branches = Branch.objects.all()
    return render(request, 'package/Branch/list-branch.html', {'branches': branches})

# Function to edit branch
@login_required
def editBranch(request, id):
    '''
    This function is used to edit a branch
    '''
    branch = Branch.objects.get(pk=id)
    if request.method == 'POST':
        branch.branch_code = request.POST.get('branch_code')
        branch.branch_name = request.POST.get('branch_name')
        branch.branch_location = request.POST.get('branch_location')
        branch.save()
        messages.success(request, 'Branch edited successfully')
        return redirect('/package/list-branch')
    else:
        return render(request, 'package/Branch/edit-branch.html', {'branch': branch})
    
# Function to delete branch
@login_required
def deleteBranch(request, id):
    '''
    This function is used to delete a branch
    '''
    branch = Branch.objects.get(pk=id)
    branch.delete()
    messages.success(request, 'Branch deleted successfully')
    return redirect('/package/list-branch')

# ================= Package =================
# Function to create package
@login_required
def createPackage(request):
    '''
    This function is used to create a package
    '''
    if request.method == 'POST':
        if (
            request.POST.get('pkg_name')
            and request.POST.get('document_type')
            and request.POST.get('details')
            and request.POST.get('packaging_size')
            and request.POST.get('destruction_eligible_time')
            and request.POST.get('condition')
            or request.POST.get('remarks')
        ):
            package = Package()
            package.pkg_name = request.POST.get('pkg_name')
            package.document_type = Document.objects.get(pk=request.POST.get('document_type'))
            package.details = request.POST.get('details')
            package.packaging_size = request.POST.get('packaging_size')
            # package.status = request.POST.get('status')
            package.destruction_eligible_time = request.POST.get('destruction_eligible_time')
            package.remarks = request.POST.get('remarks')
            package.condition = request.POST.get('condition')
            package.save()
            messages.success(request, 'Package added successfully')
            return redirect('/package/list')
        else:
            # Handle the case when the required conditions are not met
            messages.error(request, 'All fields are required')
            return redirect('/package/list')
    else:
        return redirect('/package/list')
    

# Package list view
@login_required
def packageList(request):
    '''
    This function is used to list all packages
    '''
    packages = Package.objects.all()
    return render(request, 'package/list.html', {'packages': packages})

# Function to edit package


# Function to delete package
@login_required
def deletePackage(request, id):
    '''
    This function is used to delete a package
    '''
    package = Package.objects.get(pk=id)
    package.delete()
    messages.success(request, 'Package deleted successfully')
    return redirect('/package/list')


# ====================================== Compartment =======================================
# Compartment add view
@login_required
def createCompartment(request):
    '''
    This function is used to create a compartment
    '''
    if request.method == 'POST':
        if request.POST.get('compartment_name') and request.POST.get('compartment_location'):
            compartment = Compartment()
            compartment.compartment_name = request.POST.get('compartment_name')
            compartment.compartment_location = request.POST.get('compartment_location')
            compartment.save()
            messages.success(request, 'Compartment added successfully')
            return redirect('/package/list-compartment')
    else:
        return render(request, 'package/Compartment/create-compartment.html')
    
# Compartment list view 
@login_required
def listCompartment(request):
    ''' 
    This function is used to list all compartments
    '''
    compartments = Compartment.objects.all()
    return render(request, 'package/Compartment/list-compartment.html', {'compartments': compartments})

# Function to edit Compartment
@login_required
def editCompartment(request, id):
    '''
    This function is used to edit a compartment
    '''
    compartment = Compartment.objects.get(pk=id)
    if request.method == 'POST':
        compartment.compartment_name = request.POST.get('compartment_name')
        compartment.compartment_location = request.POST.get('compartment_location')
        compartment.save()
        messages.success(request, 'Compartment edited successfully')
        return redirect('/package/list-compartment')
    else:
        return render(request, 'package/Compartment/edit-compartment.html', {'compartment': compartment})
    
# Function to delete Compartment
@login_required
def deleteCompartment(request, id):
    '''
    This function is used to delete a compartment
    '''
    compartment = Compartment.objects.get(pk=id)
    compartment.delete()
    messages.success(request, 'Compartment deleted successfully')
    return redirect('/package/list-compartment')


# ================= Rack =================
# Function to Create Rack 
@login_required
def createRack(request):
    '''
    This function is used to create a rack
    '''
    if request.method == 'POST':
        if request.POST.get('rack_name') and request.POST.get('compartment'):
            rack = Rack()
            rack.rack_name = request.POST.get('rack_name')
            rack.compartment = Compartment.objects.get(pk=request.POST.get('compartment'))
            rack.save()
            messages.success(request, 'Rack added successfully')
            return redirect('/package/list-rack')
    else:
        compartments = Compartment.objects.all()
        return render(request, 'package/Rack/create-rack.html', {'compartments': compartments})
       

# Rack list view
@login_required
def listRack(request):
    '''
    This function is used to list all racks
    '''
    racks = Rack.objects.all()
    # Prepare data in the required format for DataTables
    data = []
    for rack in racks:
        data.append({
            'id': rack.rack_id,
            'rack_name': rack.rack_name,
            'compartment': str(rack.compartment),  # Convert Compartment to string
            # 'actions': f'<a href="{reverse("rack_show", args=[rack.rack_id])}">show</a> <a href="{reverse("rack_edit", args=[rack.rack_id])}">edit</a>',
        })

    # Check if the request is an Ajax request
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'data': data}, safe=False)

    # If it's a regular request, render the template
    return render(request, 'package/Rack/list-rack.html', {'racks': racks})

# Rack delete view
@login_required
def deleteRack(request, id):
    '''
    This function is used to delete a rack
    '''
    rack = Rack.objects.get(pk=id)
    rack.delete()
    messages.success(request, 'Rack deleted successfully')
    return redirect('/package/list-rack')

# Rack edit view
@login_required
def editRack(request, id):
    '''
    This function is used to edit a rack
    '''
    rack = Rack.objects.get(pk=id)
    compartments = Compartment.objects.all()

    if request.method == 'POST':
        rack.rack_name = request.POST.get('rack_name')
        # compartment_id = request.POST.get('compartment')
        compartment_value = request.POST.get('compartment')
        compartment_id = compartment_value.split('-')[0].strip()

        rack.compartment = Compartment.objects.get(pk=compartment_id)
        rack.save()
        messages.success(request, 'Rack edited successfully')
        return redirect('/package/list-rack')
    else:
        return render(request, 'package/Rack/edit-rack.html', {'rack': rack, 'compartments': compartments})


# ========================= Store Room =========================
# Function to show store room list
@login_required
def listStoreRoom(request):
    '''
    This function is used to list all store rooms
    '''
    store_rooms = StoreRoom.objects.all()
    return render(request, 'package/StoreRoom/list-store-room.html', {'store_rooms': store_rooms,})


# Function to add store room
@login_required
def addStoreRoom(request):
    '''
    This function is used to add a store room
    '''
    store_rooms = StoreRoom.objects.all()
    racks = Rack.objects.all()
    branches = Branch.objects.all()

    if request.method == 'POST':
        if request.POST.get('store_room_name') and request.POST.get('rack') and request.POST.get('branch'):
            store_room = StoreRoom()
            store_room.store_room_name = request.POST.get('store_room_name')
            store_room.rack = Rack.objects.get(pk=request.POST.get('rack'))
            store_room.branch = Branch.objects.get(pk=request.POST.get('branch'))
            store_room.save()
            messages.success(request, 'Store room added successfully')
            return redirect('/package/list-store-room')

    return render(request, 'package/StoreRoom/list-store-room.html', {'store_room': store_rooms, 'racks': racks, 'branches': branches})

    

# Function to show indivisual store room
@login_required
def storeRoom(request, id):
    '''
    This function is used to show a store room
    '''
    store_room = StoreRoom.objects.get(pk=id)
    if store_room != None:
        return render(request, 'package/StoreRoom/store-room.html', {'store_room': store_room})


# Function to delete store room
@login_required
def deleteStoreRoom(request, id):
    '''
    This function is used to delete a store room
    '''
    store_room = StoreRoom.objects.get(pk=id)
    store_room.delete()
    messages.success(request, 'Store room deleted successfully')
    return redirect('/package/list-store-room')


# Function to edit store room
@login_required
def editStoreRoom(request, id):
    '''
    This function is used to edit a store room
    '''
    store_room = StoreRoom.objects.get(pk=id)
    if request.method == 'POST':
        store_room.store_room_name = request.POST.get('store_room_name')
        store_room.rack = Rack.objects.get(pk=request.POST.get('rack'))
        store_room.branch = Branch.objects.get(pk=request.POST.get('branch'))
        store_room.save()
        messages.success(request, 'Store room edited successfully')
        return redirect('/package/list-store-room')
    else:
        racks = Rack.objects.all()
        branches = Branch.objects.all()
        return render(request, 'package/StoreRoom/edit-store-room.html', {'store_room': store_room, 'racks': racks, 'branches': branches})

