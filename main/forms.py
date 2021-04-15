from django import forms
from .models import UserList
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserList, UIList
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# User List Form
class UserForm(forms.ModelForm):
    # Defines form attributes
    class Meta:
        model = UserList
        fields = ["title", "genre", "rating"]
        # Customizes form field labels to display
        labels = {'title': "Title", 'genre': "Genre", 'rating': "Rating"}


# Log In Form
class LogInForm(forms.Form):
    username = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100)


# Register Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def clean_user(self):
        username = self.cleaned_data.get("username")
        for instance in User.objects.all():
            if instance.username == username:
                raise forms.ValidationError()
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        for instance in User.objects.all():
            if instance.email == email:
                raise forms.ValidationError('Email is already in use')
        return email


# UI Home
