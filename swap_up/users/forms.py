from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from exchange.models import Student


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    index = forms.IntegerField()
    confirm_index = forms.IntegerField()
    semester = forms.IntegerField()


# class UserForm(forms.ModelForm):
#     password=forms.CharField(widget=forms.PasswordInput())
#     confirm_password=forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model=User
#         fields=('username','email','password')

#     def clean(self):
#         cleaned_data = super(UserForm, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise forms.ValidationError(
#                 "password and confirm_password does not match"
#             )


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

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        index = cleaned_data.get("index")
        confirm_index = cleaned_data.get("confirm_index")

        if index != confirm_index:
            raise forms.ValidationError(
                "index and confirm_index does not match"
            )



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
            'path',
            'subscribed'
        ]