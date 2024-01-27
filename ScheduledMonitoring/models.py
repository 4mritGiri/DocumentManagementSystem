from django.conf import settings
from django.db import models
from Package.models import StoreRoom, Package

# Model for scheduled monitoring of the store room
class StoreMonitoring(models.Model):
    store_room = models.ForeignKey(StoreRoom, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Scheduled monitoring of {self.store_room} on {self.scheduled_date}'

# Model to represent the review of damaged packages
class DamagedPackageReview(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True)
    damage_comments = models.TextField()
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Review of damaged package {self.package} by {self.reviewer} on {self.review_date}'
