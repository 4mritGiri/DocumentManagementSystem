# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Package Collection urls
    path('create-package-collection', createPackageCollection, name='create-package-collection'),
    path('list-package-collection', packageCollection, name='list-package-collection'),

]
