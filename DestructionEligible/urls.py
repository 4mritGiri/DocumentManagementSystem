from django.urls import path
from .views import *

urlpatterns = [
    path('list-destruction-eligible/', listDestructionEligible, name='list-destruction-eligible'),
]

