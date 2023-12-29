from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, DocumentType, UserRoles, Branch, Store

class UserRegistration(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text="The email field is required")
    first_name = forms.CharField(max_length=250, help_text="The first name field is required")
    last_name = forms.CharField(max_length=250, help_text="The last name field is required")
    # role = forms.ModelChoiceField(queryset=UserRoles.objects.all(), help_text="The role field is required")
    # branch = forms.ModelChoiceField(queryset=Branch.objects.all(), help_text="The branch field is required")
    # document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(), help_text="The document type field is required")
    # store = forms.ModelChoiceField(queryset=Store.objects.all(), help_text="The store field is required")
    # Add more fields here

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1','password2')
        # fields = ('username', 'email', 'first_name', 'last_name', 'password1','password2','role','branch','document_type','store')
        # Add more fields here

        def clean_email(self):
            email = self.clean_data['email'].lower()
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                return email
            raise forms.ValidationError(f"Email {user.email} mail is already exists/taken.")
        
        def clean_username(self):
            username = self.clean_data['username'].lower()
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                return username
            raise forms.ValidationError(f"Username {user.username} is already exists/taken.")