"""protaskinate/routes/dashboard.py"""

from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("dashboard", __name__)

@blueprint.route("/")
@blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard_route():
    """Render the dashboard page"""
    return render_template("dashboard.html")
