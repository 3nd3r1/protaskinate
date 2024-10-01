"""protaskinate/routes/dashboard.py"""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

blueprint = Blueprint("dashboard", __name__)

@blueprint.route("/", methods=["GET"])
@login_required
def index_route():
    """Redirect to the dashboard"""
    return redirect(url_for("dashboard.dashboard_route"))

@blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard_route():
    """Render the dashboard page"""
    return render_template("dashboard.html")
