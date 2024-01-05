# Package/views.py
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from .models import Package
from django.http import JsonResponse
from django.urls import reverse

def qr_scanner(request):
    return render(request, 'qr_scanner.html')

def realtime_scan(request):
    return render(request, 'realtime_scan.html')

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def process_qr_code(request):
    if request.method == 'GET':
        # Handle GET request if needed
        return render(request, 'qr_scanner_result.html', {'result': 'Invalid request method. Use POST instead.'})

    if request.method == 'POST':
        if 'image' in request.FILES:
            # Handling file upload
            image_data = request.FILES['image'].read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            decoded_objects = decode(img)

            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                data = json.loads(qr_data)
                # Split the QR code data into lines and take the first line
                # first_line = qr_data.strip().split('\n')[0]
                # print(first_line)

                # Extract the numeric part (Package ID) from the first line
                try:
                    # package_id = int(first_line.split(':')[-1].strip())
                    # print(package_id)
                    package_id = data.get('PackageID')

                    package = Package.objects.get(pkg_id=package_id)
                    print(package)
                    # Render a template to select the condition
                    return render(request, 'select_condition.html', {'package': package})

                except (ValueError, Package.DoesNotExist):
                    return render(request, 'qr_scanner_result.html', {'result': 'Package not found or invalid QR code data.'})
                
            return render(request, 'qr_scanner_result.html', {'result': 'QR code does not contain a valid package ID.'})

        # Decode the QR code from real-time video stream
        else:
            # Get the PackageId from the POST request
            scanned_data = request.POST.get('scanned_data')
            data = json.loads(scanned_data)
            package_id = data.get('PackageID')
            print(package_id)
            
            try:
                package = Package.objects.get(pkg_id=package_id)
                print(package)
                # Render a template to select the condition
                return render(request, 'select_condition.html', {'package': package})
            except (ValueError, Package.DoesNotExist):
                return render(request, 'qr_scanner_result.html', {'result': 'Package not found or invalid QR code data.'})
        
    return render(request, 'qr_scanner_result.html', {'result': 'Invalid request method. NOT GET or POST.'})

def update_condition(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        condition = request.POST.get('condition')

        try:
            package = Package.objects.get(pkg_id=package_id)
            package.condition = condition
            package.save()

            # Pass the selected condition to qr_scanner_result.html
            return render(request, 'qr_scanner_result.html', {'result': 'Package condition updated successfully.', 'package_condition': condition})

        except (ValueError, Package.DoesNotExist):
            return render(request, 'qr_scanner_result.html', {'result': 'Package not found or invalid data.'})

    return redirect('qr_scanner')  # Redirect back to the QR scanner if accessed directly
