from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from dmsApp.forms import UserRegistration # SavePost, UpdateProfile, UpdatePasswords
from DocumentManagementSystem.settings import MEDIA_ROOT, MEDIA_URL
from dmsApp.models import Post
from cryptography.fernet import Fernet
from django.conf import settings
import base64


# Create your views here.

context = {
    'page_title': "Document Management System",
}

# login page
def login_user(request):
    logout(request)
    response = {"status": 'failed', "message":'' }
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                response['status'] = 'success'
            else:
                response['message'] = 'Incorrect username or password'
        else: 
            response['message'] = "Incorrect username or password"

    return HttpResponse(json.dumps(response), content_type="application/json")

# logout page
def logoutuser(request):
    logout(request)
    return redirect('/')

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
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request,'register.html',context)

@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html',context)

@login_required
def home(request):
    context['page_title'] = "Home"
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(user = request.user).all()

    context['posts'] = posts
    context['postsLen'] = posts.count()
    print(request.build_absolute_uri())
    return render(request, 'home.html', context)



@login_required
def posts_mgt(request):
    context['page_title'] = 'Uploads'

    posts = Post.objects.filter(user = request.user).order_by('title', '-date_created').all()
    context['posts'] = posts
    return render(request, 'posts_mgt.html', context)

