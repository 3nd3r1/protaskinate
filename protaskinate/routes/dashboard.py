"""protaskinate/routes/dashboard.py"""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from protaskinate.services import task_service

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
    task_counts_by_status = task_service.count_by_assignee_grouped_by_status(current_user.id)
    return render_template("dashboard.html", task_counts_by_status=task_counts_by_status)
