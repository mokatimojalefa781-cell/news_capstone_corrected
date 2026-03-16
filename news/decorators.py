from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(role):
    """Decorator to restrict access to users with a specific role"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, "role") or request.user.role != role:
                messages.error(request, f"Access denied. {role.capitalize()}s only.")
                return redirect("home")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

reader_required = role_required("reader")
journalist_required = role_required("journalist")
editor_required = role_required("editor")
