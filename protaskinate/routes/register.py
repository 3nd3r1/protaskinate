"""protaskinate/routes/register.py"""

from flask import Blueprint, redirect, render_template, request, url_for

from protaskinate.routes.forms.register_forms import RegisterForm
from protaskinate.routes.handlers.register_handlers import handle_register
from protaskinate.utils.login_manager import login_redirect

blueprint = Blueprint("register", __name__)


@blueprint.route("/register", methods=["GET", "POST"])
@login_redirect
def register_route():
    """Render the register page"""
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        if handle_register(form):
            return redirect(url_for("dashboard.dashboard_route"))

    return render_template("register.html", form=form)
