from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Post
from django.utils.html import mark_safe # type: ignore




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        ("General", {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'profile_picture')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'groups', 'user_permissions'),
        }),
        ('Additional info', {'fields': ('bio', 'address')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),   
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'get_profile_picture', 'is_staff')

    def get_profile_picture(self, obj):
        default_profile = '/media/default/default-avatar.png'
        if obj.profile_picture:
            return mark_safe('''
                <img style="border-radius: 100%" src="{url}" width="{width}" height={height} />
            '''.format(
                url = obj.profile_picture.url,
                width = 40,
                height = 40,
            )
        )
        else:
            return mark_safe('''
                <img style="border-radius: 100%" src="{default_url}" width="{width}" height={height} />
            '''.format(
                default_url = default_profile,
                width = 40,
                height = 40,
            )
            )

    get_profile_picture.short_description = 'Profile Picture'
    get_profile_picture.admin_order_field = 'profile_picture'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        form.base_fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        form.base_fields['email'].widget.attrs['placeholder'] = 'example@gmail.com'
        form.base_fields['username'].widget.attrs['placeholder'] = 'Username'
        form.base_fields['password'].widget.attrs['placeholder'] = 'Password'
        form.base_fields['phone_number'].widget.attrs['placeholder'] = '+977 9862345678'
        form.base_fields['address'].widget.attrs['placeholder'] = 'Address'
        form.base_fields['bio'].widget.attrs['placeholder'] = 'Write something about user'

        form.base_fields['is_staff'].widget.attrs['class'] = 'form-check-input'
        form.base_fields['is_superuser'].widget.attrs['class'] = 'form-check-input'
        form.base_fields['is_active'].widget.attrs['class'] = 'form-check-input'
        form.base_fields['user_type'].widget.attrs['class'] = 'form-control'

        form.base_fields['profile_picture'].widget.attrs['accept'] = 'image/*'
        form.base_fields['profile_picture'].widget.attrs['onchange'] = 'loadFile(event)'
        form.base_fields['profile_picture'].widget.attrs['id'] = 'id_profile_picture_preview'

        return form
    
    class Meta:
        js = ('js/admin_image_preview.js',)

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'file_path', 'date_created', 'date_updated')
    list_filter = ('user', 'title', 'date_created', 'date_updated')
    search_fields = ('user', 'title', 'description', 'file_path', 'date_created', 'date_updated')
    readonly_fields = ('date_created', 'date_updated')
