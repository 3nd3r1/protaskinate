"""protaskinate/routes/handlers/register_handlers.py"""
from flask import flash
from flask_login import login_user
from protaskinate.routes.forms.register_forms import RegisterForm
from protaskinate.services import user_service


def handle_register(form: RegisterForm) -> bool:
    """Handle the registration of a user"""
    username = form.username.data
    password = form.password.data

    if not username or not password:
        flash("Invalid username or password", "error")
        return False

    if user_service.get_by_username(username):
        flash("Username already exists", "error")
        return False

    registered_user = user_service.register(username, password)
    if not registered_user:
        flash("Failed to register user", "error")
        return False

    login_user(registered_user)
    flash("You have been registered", "success")
    return True
