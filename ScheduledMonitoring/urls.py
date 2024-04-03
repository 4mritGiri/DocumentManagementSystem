# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('qr-scanner/', qr_scanner, name='qr-scanner'),
    path('process-qr-code/', process_qr_code, name='process-qr-code'),
    path('update-condition/', update_condition, name='update-condition'),

    # Store Monitoring
    path('store-monitoring/', listStoreMonitoring, name='store-monitoring'),
    path('store-monitoring/create/', addStoreMonitoring, name='add-store-monitoring'),
]
