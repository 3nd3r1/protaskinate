"""protaskinate/routes/login.py"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from protaskinate.services import user_service
from protaskinate.utils.login_manager import lm, login_redirect

blueprint = Blueprint("login", __name__)

class LoginForm(FlaskForm):
    """Form for login"""
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@blueprint.route("/login", methods=["GET", "POST"])
@login_redirect
def login_route():
    """Render the login page"""
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = user_service.login(username, password)
        if user:
            login_user(user)
            flash("You have been logged in", "success")
            return redirect(url_for("dashboard.dashboard_route"))
        flash("Invalid username or password", "error")

    return render_template("login.html", form=form)

@lm.user_loader
def load_user(user_id):
    """Load the user"""
    return user_service.get_by_id(user_id)
