# # views.py
# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Package
# from .utils import generate_qr 

# def package_qr_code_view(request, pkg_id):
#     try:
#         # Retrieve the Package object
#         package = Package.objects.get(pkg_id=pkg_id)

#         # Generate QR code data
#         data = f"""
#         Package ID: {package.pkg_id}
#         Package Name: {package.pkg_name}
#         Document Type: {package.document_type.doc_type}
#         Details: {package.details}
#         Packaging Size: {package.packaging_size}
#         Status: {package.status}
#         Destruction Eligible Time: {package.destruction_eligible_time}
#         Remarks: {package.remarks}
#         Store Location: {package.store_location.store_room_name}, {package.store_location.branch.branch_name}
#         """

#         # Generate QR code and get the image content
#         qr_code_image = generate_qr(data)

#         # Return the image as HttpResponse
#         response = HttpResponse(content_type="image/png")
#         qr_code_image.save(response, "PNG")
#         return response

#     except Package.DoesNotExist:
#         return HttpResponse("Package not found", status=404)
