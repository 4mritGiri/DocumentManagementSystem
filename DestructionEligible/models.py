from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from Package.models import Package
from datetime import timedelta
from django.utils import timezone

class DestructionEligible(models.Model):
    DESTRUCTION_TIME_MAPPING = {
        '1 Year': 31536000,
        '2 Years': 63072000,
        '3 Years': 94608000,
        '4 Years': 126144000,
        '5 Years': 157680000,
        '6 Years': 189216000,
        '7 Years': 220752000,
        '8 Years': 252288000,
    }

    destruction_eligible_id = models.AutoField(primary_key=True)
    related_package = models.OneToOneField(Package, on_delete=models.CASCADE, related_name='destruction_eligibility')
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    destruction_time = models.IntegerField(null=True, blank=True)

    def check_is_expired(self):
        expiration_time = self.created_at + timedelta(seconds=self.destruction_time or 100)
        expired = expiration_time <= timezone.now()
        self.is_expired = expired
        return expired

    def save(self, *args, **kwargs):
        if self.related_package:   
            self.created_at = self.related_package.created_at

            if self.related_package.destruction_eligible_time:
                self.destruction_time = self.DESTRUCTION_TIME_MAPPING.get(self.related_package.destruction_eligible_time, 31536000)

        super().save(*args, **kwargs)

    def __str__(self):
        expired_status = "Expired" if self.check_is_expired() else "Not Expired"
        return f'{self.destruction_eligible_id} - {self.related_package.pkg_name} - {self.is_expired} - {expired_status}'

    class Meta:
        ordering = ['-created_at']

@receiver(post_save, sender=Package)
def update_destruction_eligibility(sender, instance, **kwargs):
    # When a Package is saved, update the associated DestructionEligible instance
    destruction_eligibility, created = DestructionEligible.objects.get_or_create(related_package=instance)
    destruction_eligibility.save()
