from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email']



class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Full Name", "class": "form-control"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder": "Tell us about yourself...", "class": "form-control", "rows": 3}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "e.g. +1 234 567 8900", "class": "form-control"}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']