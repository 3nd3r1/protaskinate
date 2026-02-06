""" protaskinate/utils/login_manager.py """

from functools import wraps
from flask import redirect, url_for
from flask_login import LoginManager, current_user

from protaskinate.services import user_service

lm = LoginManager()
lm.login_view = "login.login_route"  # type: ignore
lm.login_message = None


def login_redirect(f):
    """Decorator to redirect to dashboard if user is authenticated."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.dashboard_route"))
        return f(*args, **kwargs)

    return decorated_function


@lm.user_loader
def load_user(user_id):
    """Load the user"""
    return user_service.get_by_id(user_id)
