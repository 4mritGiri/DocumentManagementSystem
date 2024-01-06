# signals.py
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

@receiver(post_delete, sender='Package.Package')
def delete_qr_code(sender, instance, **kwargs):
    # Delete associated QR code file when a package is deleted
    print("Deleting QR code...")
    qr_code_path = f"{settings.MEDIA_ROOT}/qr_codes/{instance.pkg_id}_qr_code.png"
    if os.path.isfile(qr_code_path):
        os.remove(qr_code_path)

# Register the signal
post_delete.connect(delete_qr_code, sender='Package.Package')
