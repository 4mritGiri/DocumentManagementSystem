
from django.urls import path
from . import views

urlpatterns = [
    path('broadcast_notification/', views.broadcast_notification, name='broadcast_notification'),
]