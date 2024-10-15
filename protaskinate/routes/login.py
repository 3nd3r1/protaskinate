"""protaskinate/routes/login.py"""

from flask import Blueprint, redirect, render_template, request, url_for

from protaskinate.routes.forms.login_forms import LoginForm
from protaskinate.routes.handlers.login_handlers import handle_login
from protaskinate.utils.login_manager import login_redirect

blueprint = Blueprint("login", __name__)

@blueprint.route("/login", methods=["GET", "POST"])
@login_redirect
def login_route():
    """Render the login page"""
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        if handle_login(form):
            return redirect(url_for("dashboard.dashboard_route"))

    return render_template("login.html", form=form)
