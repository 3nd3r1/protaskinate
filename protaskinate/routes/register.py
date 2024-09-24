"""protaskinate/routes/register.py"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from protaskinate.services import user_service

blueprint = Blueprint("register", __name__)

class RegisterForm(FlaskForm):
    """Form for registering a user"""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                                                                     EqualTo("password")])
    submit = SubmitField("Register")

@blueprint.route("/register", methods=["GET", "POST"])
def register_route():
    """Render the register page"""
    form = RegisterForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_route"))

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        registered_user = user_service.register(username, password)
        if registered_user:
            login_user(registered_user)
            return redirect("/")

        return render_template("register.html", form=form, error="Something went wrong")
    return render_template("register.html", form=form)
