# dashboard/views.py

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from dmsApp.models import CustomUser as User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    current_date = timezone.now()
    start_date = current_date - timezone.timedelta(days=365)

    monthly_registrations = User.objects.filter(
        date_joined__gte=start_date,
        date_joined__lte=current_date
    ).annotate(month=Count('date_joined__month')).values('month', 'date_joined__month')

    monthly_counts = {month['month']: month['date_joined__month'] for month in monthly_registrations}
    monthly_data = [monthly_counts.get(i, 0) for i in range(1, 13)]

    # Simulate data for monthly logins and logouts (replace this with your actual data)
    monthly_logins = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
    monthly_logouts = [5, 8, 12, 15, 18, 22, 25, 28, 32, 35, 38, 40]

    total_users = User.objects.count()

    return render(request, 'dashboard/dashboard.html', {
        'total_users': total_users,
        'monthly_data': monthly_data,
        'monthly_logins': monthly_logins,
        'monthly_logouts': monthly_logouts,
    })
