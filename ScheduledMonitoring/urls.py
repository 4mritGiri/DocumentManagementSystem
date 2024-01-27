# urls.py
from django.urls import path
from .views import qr_scanner, process_qr_code, update_condition

urlpatterns = [
    path('qr-scanner/', qr_scanner, name='qr-scanner'),
    path('process-qr-code/', process_qr_code, name='process-qr-code'),
    path('update-condition/', update_condition, name='update-condition'),
]
