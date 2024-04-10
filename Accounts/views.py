from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from .forms import UserRegistration, UpdatePasswords
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
 
context = {
    'page_title' : 'Document Management System',
}
#login
def login_user(request):
    context['page_title'] = "Login"
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
                if user.is_superuser:
                    resp['is_superuser']=True
                    return JsonResponse(resp)
                else:
                    resp['is_superuser']=False
                    return JsonResponse(resp)
            else:
                resp['msg'] = "Incorrect username or password. Please try again."
                return JsonResponse(resp)
        else:
            resp['msg'] = "Incorrect username or password"
    return redirect('dashboard')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('Accounts:login')

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            messages.success(request, "Account has been created successfully")
            # set form to empty
            form = UserRegistration()
            return redirect('dashboard')
        else:
            context['reg_form'] = form
            form = UserRegistration()
    return render(request,'Auth/register.html',context)

# @login_required
# def update_profile(request):
#     context['page_title'] = 'Update Profile'
#     user = CustomUser.objects.get(id = request.user.id)
#     print(user)
#     if not request.method == 'POST':
#         form = UpdateProfile(instance=user)
#         context['form'] = form

#     else:
#         form = UpdateProfile(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile has been updated")
#             return redirect("profile")
#         else:
#             context['form'] = form
            
#     return render(request, 'Post/manage_profile.html',context)


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'Auth/update_password.html',context)

