from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, CustomLoginForm


def register(request):
    """
    Handle user registration.

    GET: Display the registration form.
    POST: Validate and create a new user, then log them in automatically.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the registration page or redirects to article list on success.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            login(request, user)  # Automatically log in the user after registration
            return redirect("article_list")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    """
    Custom login view using a styled login form.

    Attributes:
        template_name (str): Path to the login template.
        authentication_form (Form): Form class for authentication.
    """
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm





