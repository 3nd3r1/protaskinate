"""protaskinate/routes/handlers/login_handlers.py"""

from flask import flash
from flask_login import login_user

from protaskinate.routes.forms.login_forms import LoginForm
from protaskinate.services import user_service


def handle_login(form: LoginForm) -> bool:
    """Handle the login of a user"""
    username = form.username.data
    password = form.password.data

    if not username or not password:
        flash("Invalid username or password", "error")
        return False

    user = user_service.login(username, password)
    if not user:
        flash("Invalid username or password", "error")
        return False

    login_user(user)
    flash("You have been logged in", "success")
    return True
