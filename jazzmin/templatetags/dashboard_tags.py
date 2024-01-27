# dashboard_tags.py
from django import template
from django.contrib.auth.models import User
from Package.models import Package, Branch, Document, PackageVerification,Compartment, Rack, StoreRoom
from DestructionEligible.models import DestructionEligible
from datetime import timedelta
from django.utils import timezone
from dmsApp.models import CustomUser

register = template.Library()

@register.simple_tag
def get_total_users():
    return CustomUser.objects.count()

@register.simple_tag
def get_total_store_room():
    return StoreRoom.objects.count()

@register.simple_tag
def get_total_branch():
    return Branch.objects.count()

# Get Profile Picture
@register.simple_tag
def get_profile_picture(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        return user.profile_picture if user.profile_picture else 'default/default-avatar.png'
    except CustomUser.DoesNotExist:
        return None 

@register.simple_tag
def get_total_package():
    return Package.objects.count()

@register.simple_tag
def get_total_document():
    return Document.objects.count()

@register.simple_tag
def get_total_package_verification():
    return PackageVerification.objects.count()

# @register.simple_tag


@register.simple_tag
def get_total_items_by_status(model, status):
    """
    Get the total count of items in a model filtered by status.

    Args:
        model (django.db.models.Model): The Django model to query.
        status (str): The status by which to filter items.

    Returns:
        int: The total count of items.
    """
    try:
        return model.objects.filter(status=status).count()
    except:
        return 0

# @register.simple_tag
# def get_total_room_rack_compartment_by_type(type):
#     return RoomRackCompartment.objects.values(type).distinct().count()



@register.simple_tag
def get_expired_destruction_eligible():
    return DestructionEligible.objects.filter(destruction_eligible_status=True).filter(created_at__lte=timezone.now() - timedelta(days=1)).count()



@register.inclusion_tag('dashboard/custom_card.html')
def render_custom_cards():
    cards = [
        {
            "category": 'User', 'icon': 'fas fa-users fa-3x', 'link': 'dmsApp/customuser/', 'badge_color': "primary", 'title': 'Total Users', 'value': get_total_users
        },
        # {
        #     "category": 'Store', 'icon': 'fas fa-store fa-3x', 'link': 'Package/store/', 'badge_color': "warning", 'title': 'Total Store', 'value': get_total_store
        # },
        {
            "category": 'Branch', 'icon': 'fas fa-code-branch fa-3x', 'link': 'Package/branch/', 'badge_color': "success", 'title': 'Total Branch', 'value': get_total_branch
        },
        {
            "category": 'Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "danger", 'title': 'Total Package', 'value': get_total_package
        },
        {
            "category": 'Document', 'icon': 'fas fa-file-alt fa-3x', 'link': 'Package/document/', 'badge_color': "info", 'title': 'Total Document', 'value': get_total_document
        },
        {
            "category": 'Package Verification', 'icon': 'fas fa-address-card fa-3x', 'link': 'Package/packageverification/', 'badge_color': "secondary", 'title': 'Total Verified Package', 'value': get_total_package_verification
        },
        # {
        #     "category": 'Room Rack Compartment', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Room Rack Compartment', 'value': get_total_room_rack_compartment
        # },
        {
            "category": 'Pending Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "danger", 'title': 'Total Pending Package', 'value': get_total_items_by_status(Package,'Pending')
        },
        {
            "category": 'Approved Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "success", 'title': 'Total Approved Package', 'value': get_total_items_by_status(Package,'Approved')
        },
        {
            "category": 'Rejected Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "warning", 'title': 'Total Rejected Package', 'value': get_total_items_by_status(Package, 'Rejected')
        },
        # {
        #     "category": 'Total Room', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Room', 'value': get_total_room_rack_compartment_by_type('room')
        # },
        # {
        #     "category": 'Total Rack', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Rack', 'value': get_total_room_rack_compartment_by_type('rack')
        # },
        # {
        #     "category": 'Total Compartment', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Compartment', 'value': get_total_room_rack_compartment_by_type('compartment')
        # },
    ]
    return {'cards': cards}


