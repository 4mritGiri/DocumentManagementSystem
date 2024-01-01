# dashboard_tags.py
from django import template
from django.contrib.auth.models import User
from Package.models import Package, Store, Branch, Document, PackageVerification, RoomRackCompartment

register = template.Library()

@register.simple_tag
def get_total_users():
    return User.objects.count()

@register.simple_tag
def get_total_store():
    return Store.objects.count()

@register.simple_tag
def get_total_branch():
    return Branch.objects.count()

@register.simple_tag
def get_total_package():
    return Package.objects.count()

@register.simple_tag
def get_total_document():
    return Document.objects.count()

@register.simple_tag
def get_total_package_verification():
    return PackageVerification.objects.count()

@register.simple_tag
def get_total_room_rack_compartment():
    return RoomRackCompartment.objects.count()

@register.simple_tag
def get_total_package_by_status(status):
    return Package.objects.filter(status=status).count()

@register.simple_tag
def get_room_rack(status):
    return RoomRackCompartment.objects.values(status).distinct().count()



@register.inclusion_tag('dashboard/custom_card.html')
def render_custom_cards():
    cards = [
        {
            "category": 'User', 'icon': 'fas fa-users fa-3x', 'link': 'auth/user/', 'badge_color': "primary", 'title': 'Total Users', 'value': get_total_users
        },
        {
            "category": 'Store', 'icon': 'fas fa-store fa-3x', 'link': 'Package/store/', 'badge_color': "warning", 'title': 'Total Store', 'value': get_total_store
        },
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
        {
            "category": 'Room Rack Compartment', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Room Rack Compartment', 'value': get_total_room_rack_compartment
        },
        {
            "category": 'Pending Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "danger", 'title': 'Total Pending Package', 'value': get_total_package_by_status('Pending')
        },
        {
            "category": 'Approved Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "success", 'title': 'Total Approved Package', 'value': get_total_package_by_status('Approved')
        },
        {
            "category": 'Rejected Package', 'icon': 'fas fa-box-open fa-3x', 'link': 'Package/package/', 'badge_color': "warning", 'title': 'Total Rejected Package', 'value': get_total_package_by_status('Rejected')
        },
        {
            "category": 'Total Room', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Room', 'value': get_room_rack('room')
        },
        {
            "category": 'Total Rack', 'icon': 'fas fa-warehouse fa-3x', 'link': 'Package/roomrackcompartment/', 'badge_color': "dark", 'title': 'Total Rack', 'value': get_room_rack('rack')
        },
    ]
    return {'cards': cards}