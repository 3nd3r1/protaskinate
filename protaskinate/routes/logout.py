"""protaskinate/routes/logout.py"""

from flask import Blueprint, redirect, url_for
from flask_login import logout_user

blueprint = Blueprint("logout", __name__)

@blueprint.route("/logout", methods=["GET"])
def logout_route():
    """Render the logout page"""
    logout_user()
    return redirect(url_for("login.login_route"))
