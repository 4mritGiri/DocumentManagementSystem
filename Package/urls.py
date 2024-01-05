# urls.py
from django.urls import path
from .views import qr_scanner, process_qr_code, update_condition, realtime_scan

urlpatterns = [
    path('qr-scanner/', qr_scanner, name='qr_scanner'),
    path('process-qr-code/', process_qr_code, name='process_qr_code'),
    path('update-condition/', update_condition, name='update_condition'),
    path('realtime_scan/', realtime_scan, name='realtime_scan'),
]
