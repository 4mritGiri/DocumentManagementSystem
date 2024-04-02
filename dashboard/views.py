# dashboard/views.py

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from Package.models import Package, Branch, Compartment, PackageVerification


User = get_user_model()

# @login_required(login_url='Accounts:login')
# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     current_date = timezone.now()
#     start_date = current_date - timezone.timedelta(days=365)

#     monthly_registrations = User.objects.filter(
#         date_joined__gte=start_date,
#         date_joined__lte=current_date
#     ).annotate(month=Count('date_joined__month')).values('month', 'date_joined__month')

#     monthly_counts = {month['month']: month['date_joined__month'] for month in monthly_registrations}
#     monthly_data = [monthly_counts.get(i, 0) for i in range(1, 13)]

#     # Simulate data for monthly logins and logouts (replace this with your actual data)
#     monthly_logins = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
#     monthly_logouts = [5, 8, 12, 15, 18, 22, 25, 28, 32, 35, 38, 40]

#     total_users = User.objects.count()

#     return render(request, 'dashboard/dashboard.html', {
#         'total_users': total_users,
#         'monthly_data': monthly_data,
#         'monthly_logins': monthly_logins,
#         'monthly_logouts': monthly_logouts,
#     })


@login_required(login_url='Accounts:login')
def dashboard(request):
    totalUsers = User.objects.count()
    totalUsersActive = User.objects.filter(is_active=True).count()
    totalUsersInactive = User.objects.filter(is_active=False).count()

    # Packages
    totalPackages = Package.objects.count()
    totalPackagesApproved = Package.objects.filter(status="Approved").count()
    totalPackagesRejected = Package.objects.filter(status="Rejected").count()
    totalPackagesPending = Package.objects.filter(status="Pending").count()

    totalVerifiedPackages = PackageVerification.objects.filter(status="Approved").count()
    totalUnverifiedPackages = PackageVerification.objects.filter(status="Rejected").count()
    totalPendingPackages = PackageVerification.objects.filter(status="Pending").count()

    # Packages Today
    totalPackagesVerifiedToday = PackageVerification.objects.filter(status="Approved", verification_date=timezone.now().date()).count()
    totalPackagesUnverifiedToday = PackageVerification.objects.filter(status="Rejected", verification_date=timezone.now().date()).count()
    totalPackagesPendingToday = PackageVerification.objects.filter(status="Pending", verification_date=timezone.now().date()).count()    
    
    totalBranches = Branch.objects.count()
    totalCompartments = Compartment.objects.count()

    cards = [
        {
            'title': 'Total Users',
            'value': totalUsers,
            'icon': 'fa fa-users',
            'color': 'primary'
        },
        {
            'title': 'Active Users',
            'value': totalUsersActive,
            'icon': 'fa fa-user-check',
            'color': 'success'
        },
        {
            'title': 'Inactive Users',
            'value': totalUsersInactive,
            'icon': 'fa fa-user-times',
            'color': 'danger'
        },
        {
            'title': 'Total Packages',
            'value': totalPackages,
            'icon': 'fa fa-boxes',
            'color': 'primary'
        },
        {
            'title': 'Total Branches',
            'value': totalBranches,
            'icon': 'fa fa-code-branch',
            'color': 'primary'
        },
        {
            'title': 'Total Compartments',
            'value': totalCompartments,
            'icon': 'fa fa-box-open',
            'color': 'primary'
        },
        {
            'title': 'Total Pending Packages',
            'value': totalPackagesPending,
            'icon': 'fa fa-spinner',
            'color': 'warning'
        },
        {
            'title': 'Total Verified Packages',
            'value': totalPackagesApproved,
            'icon': 'fa fa-check-circle',
            'color': 'success'
        },
        {
            'title': 'Total Unverified Packages',
            'value': totalPackagesRejected,
            'icon': 'fa fa-times-circle',
            'color': 'danger'
        },
        {
            'title': 'Pending Today',
            'value': totalPackagesPendingToday,
            'icon': 'fa fa-spinner',
            'color': 'warning'
        },
        {
            'title': 'Verified Today',
            'value': totalPackagesVerifiedToday,
            'icon': 'fa fa-check-circle',
            'color': 'success'
        },
        {
            'title': 'Unverified Today',
            'value': totalPackagesUnverifiedToday,
            'icon': 'fa fa-times-circle',
            'color': 'danger'
        },
        {
            'title': 'Total Verified Packages',
            'value': totalVerifiedPackages,
            'icon': 'fa fa-check-circle',
            'color': 'success'
        },
        {
            'title': 'Total Unverified Packages',
            'value': totalUnverifiedPackages,
            'icon': 'fa fa-times-circle',
            'color': 'danger'
        },
        {
            'title': 'Total Pending Packages',
            'value': totalPendingPackages,
            'icon': 'fa fa-spinner',
            'color': 'warning'
        }
    ]

    return render(request, 'dashboard/dashboard.html', {'cards': cards})

