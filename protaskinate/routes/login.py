"""protaskinate/routes/login.py"""

import logging

from flask import Blueprint, redirect, render_template, request, session

from protaskinate.services import user_service

blueprint = Blueprint("login", __name__)

@blueprint.route("/login", methods=["GET", "POST"])
def login_route():
    """Render the login page"""
    if session.get("user_id"):
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("login.html", error="Username and password are required")

        user = user_service.login(username, password)
        logging.debug("User: %s", user)
        if user:
            session["user_id"] = user.id
            return redirect("/")
        return render_template("login.html", error="Invalid username or password")
    return redirect("/login")
