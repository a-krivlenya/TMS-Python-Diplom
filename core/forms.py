from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": "w-5/6 mx-auto py-4 px-6 rounded-xl dark:text-black",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": "w-5/6 mx-auto py-4 px-6 rounded-xl dark:text-black",
            }
        )
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": "w-5/6 mx-auto py-4 px-6 rounded-xl dark:text-black",
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email address",
                "class": "w-5/6 mx-auto py-4 px-6 rounded-xl dark:text-black",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": "w-5/6 mx-auto  py-4 px-6 rounded-xl dark:text-black",
                "type": "password",
                "autocomplete": "new-password",
                "required": True,
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": "w-5/6 mx-auto  py-4 px-6 rounded-xl dark:text-black",
                "type": "password",
                "autocomplete": "new-password",
                "required": True,
            }
        )
    )
