from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    """
    Form for registering a new user.

    Inherits from Django's UserCreationForm and adds support for:
    - username: unique identifier for the user
    - email: email address of the user
    - role: the role of the user (e.g., reader, journalist, editor)
    - password1: password
    - password2: password confirmation
    """
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2',
        ]

    def clean_email(self):
        """
        Validate that the email is unique.
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form for user authentication.

    Adds Bootstrap styling to the username and password input fields
    for improved UI/UX.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )




