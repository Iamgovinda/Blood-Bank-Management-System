# from attr import field
import email
from django import forms
from User.models import Profile
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','style':'color:red'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password','type':'password'}))

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

    # first_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=30)
    # username = forms.CharField(max_length=30)
    # email = forms.EmailField(max_length=30)
    # password1 = forms.CharField(widget=forms.PasswordInput)
    # password2 = forms.CharField(widget=forms.PasswordInput)

    def save(self,commit=True):
        usergroup = Group.objects.get(name='Client')

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        usergroup.user_set.add(user)
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','gender','address','mobile','bloodgroup','age']


