"""protaskinate/routes/dashboard.py"""

from flask import Blueprint, redirect, render_template, session

blueprint = Blueprint("dashboard", __name__)

@blueprint.route("/")
@blueprint.route("/dashboard", methods=["GET"])
def dashboard_router():
    """Render the dashboard page"""
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("dashboard.html")
