# urls.py
from django.urls import path
from .views import *


urlpatterns = [
    # package urls
    path('create', createPackage, name='create-package'),
    path('list', packageList, name='list-package'),
    path('edit/<int:id>', editPackage, name='edit-package'),
    path('delete/<int:id>', deletePackage, name='delete-package'),

    # Branch urls 
    path('create-branch', createBranch, name='create-branch'),
    path('list-branch', listBranch, name='list-branch'),
    path('edit-branch/<int:id>', editBranch, name='edit-branch'),
    path('delete-branch/<int:id>', deleteBranch, name='delete-branch'),

    # compartment urls
    path('create-compartment', createCompartment, name='create-compartment'),
    path('list-compartment', listCompartment, name='list-compartment'),
    path('edit-compartment/<int:id>', editCompartment, name='edit-compartment'),
    path('delete-compartment/<int:id>', deleteCompartment, name='delete-compartment'),

    # Rack urls
    path('create-rack', createRack, name='create-rack'),
    path('list-rack', listRack, name='list-rack'),
    path('delete-rack/<int:id>', deleteRack, name='delete-rack'),
    path('edit-rack/<int:id>', editRack, name='edit-rack'),

    # Store Room urls
    path('list-store-room', listStoreRoom, name='list-store-room'), # list store room
    path('add-store-room', addStoreRoom, name='add-store-room'), # add store room
    path('store-room/<str:id>', storeRoom, name='store-room'), # show indivisual store room
    path('edit-store-room/<str:id>', editStoreRoom, name='edit-store-room'), # edit store room
    path('delete-store-room/<str:id>', deleteStoreRoom, name='delete-store-room'), # delete store 
    
    # Package Verification urls
    path('list-package-verification', listPackageVerification, name='list-package-verification'), # list package verification
    path('package-verification', packageVerification, name='package-verification'), # add package verification
    path('edit-package-verification/<str:id>', editPackageVerification, name='edit-package-verification'), # edit package verification
    path('delete-package-verification/<str:id>', deletePackageVerification, name='delete-package-verification'), # delete package verification
]
