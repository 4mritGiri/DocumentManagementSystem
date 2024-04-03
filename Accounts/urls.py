from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

app_name = 'Accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="Auth/login.html", redirect_authenticated_user=True), name='login'),
    path('redirect-admin/', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('userlogin/', views.login_user, name="login-user"),
    path('logout/', views.logoutuser, name='logout'),
    path('user-register', views.registerUser, name="register-user"),
    path('update-password', views.update_password, name='update-password'),
]
