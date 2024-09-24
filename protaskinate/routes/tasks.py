"""protaskinate/routes/tasks.py"""

from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from protaskinate.entities.task import TaskPriority, TaskStatus
from protaskinate.services import task_service, user_service

blueprint = Blueprint("tasks", __name__)


class CreateTaskForm(FlaskForm):
    """Form for creating a task"""
    title = StringField("Title", validators=[DataRequired()])
    status = SelectField("Status",
                         choices=[
                             (status.value, status.name.lower().replace("_"," ").title())
                              for status in TaskStatus])
    priority = SelectField("Priority",
                           choices=[
                               (priority.value, priority.name.lower().replace("_"," ").title())
                                for priority in TaskPriority])
    submit = SubmitField("Create Task")


@blueprint.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks_route():
    """Render the tasks page"""
    form = CreateTaskForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        status = form.status.data
        priority = form.priority.data
        task_service.create(title=title,
                            status=status,
                            priority=priority,
                            creator_id=current_user.id,
                            created_at=datetime.now().isoformat())
        return redirect(url_for("tasks.tasks_route"))

    tasks = task_service.get_all(order_by_fields=["priority", "created_at"],
                                 reverse=[True, False])
    users_dict = {user.id: user for user in user_service.get_all()}

    return render_template("tasks.html", form=form, tasks=tasks, users_dict=users_dict)

@blueprint.route("/tasks/<int:task_id>", methods=["POST"])
@login_required
def update_task_route(task_id):
    """Update the task"""
    data = request.form
    if data:
        task_service.update(task_id, **data)

    return redirect(url_for("tasks.tasks_route"))
