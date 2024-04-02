# Package/views.py
import json
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Package, StoreRoom
from .models import StoreMonitoring

@login_required(login_url='Accounts:login')
def qr_scanner(request):

    return render(request, 'ScheduledMonitoring/qr_scanner.html')

@csrf_exempt
@login_required(login_url='Accounts:login')
def process_qr_code(request):

    if request.method == 'GET':
        messages.error(request, 'Invalid request method. Use POST instead.')
        return render(request, 'ScheduledMonitoring/qr_scanner.html')

    if request.method == 'POST':
        if 'image' in request.FILES:
            image_data = request.FILES['image'].read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            decoded_objects = decode(img)

            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')

                try:
                    data = json.loads(qr_data)
                    package_id = data.get('PackageID')
                    package = get_object_or_404(Package, pkg_id=package_id)
                    
                    return render(request, 'ScheduledMonitoring/select_condition.html', {'package': package})

                except (ValueError, Package.DoesNotExist):
                    messages.error(request, 'Package not found or invalid QR code data.')
                    return render(request, 'ScheduledMonitoring/qr_scanner.html')

            messages.error(request, 'Package not found or invalid QR code data.')
            return render(request, 'ScheduledMonitoring/qr_scanner.html')

        else:
            scanned_data = request.POST.get('scanned_data')
            data = json.loads(scanned_data)
            package_id = data.get('PackageID')

            try:
                package = get_object_or_404(Package, pkg_id=package_id)
                messages.success(request, 'Package found. Please select the condition.')
                return render(request, 'ScheduledMonitoring/select_condition.html', {'package': package})

            except (ValueError, Package.DoesNotExist):
                messages.error(request, 'Package not found or invalid QR code data.')
                return render(request, 'ScheduledMonitoring/qr_scanner.html')

    messages.error(request, 'Invalid request method. NOT GET or POST.')
    return render(request, 'ScheduledMonitoring/qr_scanner.html')

@login_required(login_url='Accounts:login')
def update_condition(request):

    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        condition = request.POST.get('condition')

        try:
            package = get_object_or_404(Package, pkg_id=package_id)
            package.condition = condition
            package.save()
            
            messages.success(request, 'Package condition updated successfully.')
            return redirect('list-package')

        except (ValueError, Package.DoesNotExist):
            messages.error(request, 'Package not found or invalid data.')
            return redirect('list-package')
        
    return redirect('qr-scanner')


# *****************
# Store Monitoring
# *****************

# Function to list all StoreMonitoring
@login_required(login_url='Accounts:login')
def listStoreMonitoring(request):
    store_monitoring = StoreMonitoring.objects.all()
    return render(request, 'ScheduledMonitoring/StoreMonitoring/list_store_monitoring.html', {'store_monitoring': store_monitoring})


# Function to Store Monitoring
@login_required(login_url='Accounts:login')
def addStoreMonitoring(request):
    if request.method == 'POST':
        store_room = request.POST.get('store_room')
        scheduled_date = request.POST.get('scheduled_date')
        comments = request.POST.get('comments')

        try:
            store_monitoring = StoreMonitoring(store_room=store_room, scheduled_date=scheduled_date, comments=comments)
            store_monitoring.save()
            messages.success(request, 'Store Monitoring added successfully.')
            return redirect('list-store-monitoring')

        except ValueError:
            messages.error(request, 'Invalid data.')
            return redirect('list-store-monitoring')

    return render(request, 'ScheduledMonitoring/StoreMonitoring/add_store_monitoring.html')

def add_store_monitoring(request):
    template_name = 'ScheduledMonitoring/StoreMonitoring/add_store_monitoring.html'

    if request.method == 'GET':
        store_rooms = StoreRoom.objects.all()
        return render(request, template_name, {'store_rooms': store_rooms})

    elif request.method == 'POST':
        store_room_id = request.POST.get('store_room')
        scheduled_date = request.POST.get('scheduled_date')
        comments = request.POST.get('comments')

        store_room = StoreRoom.objects.get(id=store_room_id)
        
        StoreMonitoring.objects.create(
            store_room=store_room,
            scheduled_date=scheduled_date,
            comments=comments
        )

        return redirect('list-store-monitoring')


