from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from exchange.models import Student


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]


class UserUpdateForm(forms.ModelForm):
    
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name'
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'index_number',
            'semester',
            'path'
        ]