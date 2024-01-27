from django.conf import settings
from django.db import models
from Package.models import Package,User, Compartment, StoreRoom

# PackageCollection models
class PackageCollection(models.Model):
    id = models.AutoField(primary_key=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    collection_date = models.DateTimeField(auto_now_add=True)
    tampering_verification_remarks = models.TextField()
    tampering_detected = models.BooleanField(default=False, blank=True, null=True)
    store_location = models.ForeignKey(StoreRoom, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
   
    def __str__(self):
        return f"{self.package.pkg_name} - {self.collector.username}"
    
    def save(self, *args, **kwargs):
        # Call the save method of the parent class
        super().save(*args, **kwargs)

        # Set is_collected to True if the package collection is verified
        if self.is_verified and not self.package.is_collected:
            self.package.is_collected = True
            self.package.save()
    
    class Meta:
        verbose_name_plural = 'Package Collection'
        verbose_name = 'Package Collection'
        ordering = ['package']
