from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DestructionEligible

# Create your views here.

# Destruction Eligible

# Function to show list of all destruction eligible packages
@login_required(login_url='login')
def listDestructionEligible(request):
    destruction_eligibles = DestructionEligible.objects.all()

    print(destruction_eligibles)
    return render(request, 'DestructionEligible/list_destruction_eligible.html', {'destruction_eligibles': destruction_eligibles})