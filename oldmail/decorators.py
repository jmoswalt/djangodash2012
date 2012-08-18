from functools import wraps
from django.contrib.auth.views import login


def staff_or_super_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is staff or is a super user, displaying the login page if necessary.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and (request.user.is_staff or request.user.is_superuser):
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        return login(request)
    return _checklogin
