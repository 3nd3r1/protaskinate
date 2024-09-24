"""protaskinate/routes/tasks.py"""

from datetime import datetime

from flask import Blueprint, redirect, render_template, request, session
from flask_login import current_user, login_required

from protaskinate.services import task_service, user_service

blueprint = Blueprint("tasks", __name__)

@blueprint.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks_route():
    """Render the tasks page"""

    if request.method == "POST":
        data = request.form
        if not data:
            return redirect("/tasks")
        task_service.create(**data, creator_id=session["user_id"],
                            created_at=datetime.now().isoformat())
        return redirect("/tasks")

    if request.method == "GET":
        tasks = task_service.get_all(order_by_fields=["priority", "created_at"],
                                     reverse=[True, False])
        users_dict = {user.id: user for user in user_service.get_all()}
        return render_template("tasks.html", tasks=tasks, users_dict=users_dict)

    return redirect("/tasks")

@blueprint.route("/tasks/<int:task_id>", methods=["POST"])
@login_required
def update_task_route(task_id):
    """Update the task"""
    data = request.form
    if not data:
        return redirect("/tasks")


    task_service.update(task_id, **data)

    return redirect("/tasks")
