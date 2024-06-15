from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def guest_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect authenticated users to the home page or any other page
            return redirect(reverse('ups:home'))
        else:
            # Allow access for guests
            return view_func(request, *args, **kwargs)
    return _wrapped_view
