"""
Views for user authentication and account management.

This module provides user registration and login views with role-based
redirection to user dashboards.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import RegistrationForm, CustomLoginForm


def redirect_user_by_role(user):
    """
    Redirect users to their dashboard based on role.
    """
    if user.role == "reader":
        return redirect("reader_dashboard")
    elif user.role == "journalist":
        return redirect("journalist_dashboard")
    elif user.role == "editor":
        return redirect("editor_dashboard")
    return redirect("home")


def register(request):
    """
    Role-based registration view.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect_user_by_role(user)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    """
    Role-based login view.
    """
    template_name = "accounts/login.html"
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"Welcome back, {user.username}!")
        # redirect users straight to their dashboard after login
        from .views import redirect_user_by_role  # avoid circular import
        return redirect_user_by_role(user)
        return redirect_user_by_role(user)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
