from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class login_form(forms.Form):
    email_or_username = forms.CharField(
        label="Email or Username",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Enter email or username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }