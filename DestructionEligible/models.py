from django.db import models
from Package.models import Package
from datetime import timedelta
from django.utils import timezone

class DestructionEligible(models.Model):
    destruction_eligible_id = models.AutoField(primary_key=True)
    related_package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='destruction_eligibilities')
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    destruction_time = models.IntegerField(null = True, blank = True)

    def check_is_expired(self):
        # Check if expiration time has passed
        expiration_time = self.created_at + timedelta(seconds=self.destruction_time if self.destruction_time else 100)
        expired = expiration_time <= timezone.now()

        # Update is_expired based on expiration status
        self.is_expired = expired

        return expired

    def save(self, *args, **kwargs):
        # Set created_at to the value of Package's created_at
        if not hasattr(self, 'id') and self.related_package:  
            self.created_at = self.related_package.created_at

        # Set destruction_eligible_time to the value of Package's destruction_eligible_time
        if hasattr(self.related_package, 'destruction_eligible_date'):
            destruction_eligible_date = self.related_package.destruction_eligible_time

            if destruction_eligible_date == '1 Year':
                self.destruction_time = 31536000
            elif destruction_eligible_date == '2 Years':
                self.destruction_time = 63072000
            elif destruction_eligible_date == '3 Years':
                self.destruction_time = 94608000
            elif destruction_eligible_date == '4 Years':
                self.destruction_time = 126144000
            elif destruction_eligible_date == '5 Years':
                self.destruction_time = 157680000
            elif destruction_eligible_date == '6 Years':
                self.destruction_time = 189216000
            elif destruction_eligible_date == '7 Years':
                self.destruction_time = 220752000
            elif destruction_eligible_date == '8 Years':
                self.destruction_time = 252288000
            else:
                self.destruction_time = 31536000

        super().save(*args, **kwargs)

    def __str__(self):
        expired_status = "Expired" if self.check_is_expired() else "Not Expired"
        return f'{self.destruction_eligible_id} - {self.related_package.pkg_name} - {self.is_expired} - {expired_status}'

    class Meta:
        ordering = ['-created_at']
