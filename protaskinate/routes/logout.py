"""protaskinate/routes/logout.py"""

from flask import Blueprint, redirect, session


blueprint = Blueprint("logout", __name__)

@blueprint.route("/logout", methods=["GET"])
def logout_route():
    """Render the logout page"""
    if session.get("user_id"):
        session.pop("user_id")
    return redirect("/login")
