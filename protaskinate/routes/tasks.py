"""protaskinate/routes/tasks.py"""

from flask import Blueprint, redirect, request, render_template, session, jsonify

from protaskinate.services import task_service

blueprint = Blueprint("tasks", __name__)

@blueprint.route("/tasks", methods=["GET"])
def tasks_route():
    """Render the tasks page"""
    if not session.get("user_id"):
        return redirect("/")
    return render_template("tasks.html", tasks=task_service.get_all())

@blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    """Update the task"""
    if not session.get("user_id"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    task_service.update(task_id, status=data["status"])

    return jsonify({"success": True})
