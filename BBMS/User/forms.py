# from attr import field
import email
from django import forms
from User.models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','style':'color:red'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password','type':'password'}))

class UserRegistrationForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = ['first_name','last_name','username','email']
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)



