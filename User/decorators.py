from django.shortcuts import redirect


def role_required(allowed_roles=[], redirect_route=""):
    def decorator(func):
        def wrap(request, *args, **kwargs):
            if request.user_role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                return redirect(redirect_route)

        return wrap

    return decorator
