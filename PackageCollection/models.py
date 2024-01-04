from django.db import models
from Package.models import Package,User, Compartment, StoreRoom

# PackageCollection models
class PackageCollection(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    collector = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_date = models.DateTimeField(auto_now_add=True)
    tampering_verification_remarks = models.TextField()
    store_location = models.ForeignKey(StoreRoom, on_delete=models.CASCADE)
    is_tampered = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
   
    def __str__(self):
        return f"{self.package.pkg_name} - {self.package.status}"
    
    class Meta:
        verbose_name_plural = 'Package Collection'
        verbose_name = 'Package Collection'
        ordering = ['package']

# # PackageCollectionVerification models
# class PackageCollectionVerification(models.Model):
#     package_collection = models.ForeignKey(PackageCollection, on_delete=models.CASCADE)
#     verifier = models.ForeignKey(User, on_delete=models.CASCADE)
#     verification_date = models.DateTimeField(auto_now_add=True)
#     is_verified = models.BooleanField(default=False)
#     verification_remarks = models.TextField()
    
#     def __str__(self):
#         return self.package_collection.package.package_id
    
#     class Meta:
#         verbose_name_plural = 'Package Collection Verification'
#         verbose_name = 'Package Collection Verification'
#         ordering = ['package_collection']