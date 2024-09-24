""" protaskinate/utils/login_manager.py """
from functools import wraps
from flask import redirect, url_for
from flask_login import LoginManager, current_user

lm = LoginManager()
lm.login_view = "login.login_route" #type: ignore

def login_redirect(f):
    """Decorator to redirect to dashboard if user is authenticated."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.dashboard_route"))
        return f(*args, **kwargs)
    return decorated_function
