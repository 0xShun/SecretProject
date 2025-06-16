from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import UserCredential

def login_required(view_func=None, redirect_url='login'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_data = request.session.get('user_data')
            if user_data:
                user_id = user_data.get('user_id')
            else:
                user_id = None

            if not user_id or not UserCredential.objects.filter(id=user_id).exists():
                return redirect(reverse(redirect_url))
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if view_func:
        return decorator(view_func)
    return decorator
