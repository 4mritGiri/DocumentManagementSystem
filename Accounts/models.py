from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _


# User permissions
USER_ROLE_CHOICES = (
    ('Inputter', 'Inputter'),
    ('Authorizer', 'Authorizer'),
    ('Admin', 'Admin'),
    # ('Super Admin', 'Super Admin'),
)

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(choices=USER_ROLE_CHOICES, default='Inputter', max_length=90)

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=_('groups'))
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )

    def save(self, *args, **kwargs):
        # Delete old profile picture if updating
        try:
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.profile_picture and self.profile_picture != old_user.profile_picture:
                old_user.profile_picture.delete(save=False)
        except CustomUser.DoesNotExist:
            pass

        super().save(*args, **kwargs)



