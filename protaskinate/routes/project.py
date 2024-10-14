"""protaskinate/routes/project.py"""

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import (DateField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length, Optional

from protaskinate.entities.task import TaskPriority, TaskStatus
from protaskinate.services import (comment_service, project_service,
                                   task_service, user_service)
from protaskinate.utils.project import (project_read_access_required,
                                        project_update_access_required,
                                        task_update_access_required)

blueprint = Blueprint("project", __name__)

class CreateTaskForm(FlaskForm):
    """Form for creating a task"""
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])
    status = SelectField("Status",
                         choices=[
                             (status.value, status.name.lower().replace("_"," ").title())
                              for status in TaskStatus])
    priority = SelectField("Priority",
                           choices=[
                               (priority.value, priority.name.lower().replace("_"," ").title())
                                for priority in TaskPriority])
    assignee_id = SelectField("Assignee", coerce=int)
    deadline = DateField("Deadline", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Create Task")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignee_id.choices = [(0, "Not Assigned")] + [
                (user.id, user.username) for user in user_service.get_all()] # type: ignore

class CreateCommentForm(FlaskForm):
    """Form for creating a comment"""
    content = TextAreaField("Content", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Send")

class CreateProjectForm(FlaskForm):
    """Form for creating a project"""
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Create Project")

@blueprint.route("/projects", methods=["GET", "POST"])
@login_required
def project_list_route():
    """Render the projects page"""
    form = CreateProjectForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        description = form.description.data if form.description.data else None
        project_service.create(name=name, creator_id=current_user.id,
                               created_at=datetime.now().isoformat(),
                               updated_at=datetime.now().isoformat(),
                               description=description)
        form.name.data = ""
        form.description.data = ""
        flash("Project created successfully", "success")

    projects_with_roles = project_service.get_all_by_user_with_role(current_user.id)
    return render_template("project_list.html", form=form, projects_with_roles=projects_with_roles)

@blueprint.route("/projects/<int:project_id>", methods=["GET", "POST"])
@login_required
@project_read_access_required
def project_view_route(project_id: int):
    """Render the single project view page"""
    form = CreateTaskForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        status = form.status.data
        priority = form.priority.data
        assignee_id = form.assignee_id.data if form.assignee_id.data != 0 else None
        deadline = form.deadline.data.isoformat() if form.deadline.data else None
        description = form.description.data if form.description.data else None
        if not project_service.check_user_write_access(current_user.id, project_id):
            flash("You do not have write-access to this project", "error")
        else:
            task_service.create(title=title,
                                status=status,
                                priority=priority,
                                creator_id=current_user.id,
                                created_at=datetime.now().isoformat(),
                                updated_at=datetime.now().isoformat(),
                                assignee_id=assignee_id,
                                deadline=deadline,
                                project_id=project_id,
                                description=description)
            form.title.data = ""
            form.assignee_id.data = 0
            form.deadline.data = None
            form.description.data = ""

    project = project_service.get_by_id(project_id)
    tasks = task_service.get_all_by_project(project_id,
                                            order_by_fields=["priority", "created_at"],
                                            reverse=[True, False])
    user_project_role = project_service.get_user_role(current_user.id, project_id)
    users_dict = {user.id: user for user in user_service.get_all()}

    return render_template("project_view.html",
                           form=form,
                           project=project,
                           user_project_role=user_project_role,
                           tasks=tasks,
                           users_dict=users_dict)

@blueprint.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
@project_update_access_required
def project_delete_route(project_id: int):
    """Delete a project"""
    project_service.delete(project_id)
    return redirect(url_for("project.project_list_route"))

@blueprint.route("/projects/<int:project_id>/tasks/<int:task_id>", methods=["GET", "POST"])
@login_required
@project_read_access_required
def project_task_view_route(project_id: int, task_id: int):
    """View of a single task in a project"""
    form = CreateCommentForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        content = form.content.data
        new_comment = comment_service.create(task_id=task_id, creator_id=current_user.id,
                               created_at=datetime.now().isoformat(), content=content)
        if not new_comment:
            flash("Failed to create comment", "error")
        else:
            form.content.data = ""

    task = task_service.get_by_id_and_project(task_id, project_id)
    comments = comment_service.get_all_by_task(task_id)
    project = project_service.get_by_id(project_id)
    user_project_role = project_service.get_user_role(current_user.id, project_id)
    users_dict = {user.id: user for user in user_service.get_all()}

    if not project:
        return redirect(url_for("dashboard.dashboard_route"))
    if not task:
        return redirect(url_for("project.project_view_route", project_id=project_id))

    return render_template("project_task_view.html", project=project,
                           task=task, comments=comments, users_dict=users_dict,
                           user_project_role=user_project_role, form=form)

@blueprint.route("/projects/<int:project_id>/tasks/<int:task_id>/edit", methods=["POST"])
@login_required
@task_update_access_required
def project_task_edit_route(project_id: int, task_id: int):
    """Edit a task in a project"""
    data = request.form
    if data:
        update_data = {}
        if "status" in data:
            update_data["status"] = data["status"]
        if "priority" in data:
            update_data["priority"] = data["priority"]
        if "assignee_id" in data:
            update_data["assignee_id"] = int(data["assignee_id"])
            if update_data["assignee_id"] == 0:
                update_data["assignee_id"] = None
        if "deadline" in data:
            update_data["deadline"] = data["deadline"]

        task_service.update(task_id, project_id, **update_data)

    return redirect(request.referrer)

@blueprint.route("/projects/<int:project_id>/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
@task_update_access_required
def project_task_delete_route(project_id: int, task_id: int):
    """Delete a task from a project"""
    task_service.delete(task_id, project_id)
    return redirect(url_for("project.project_view_route", project_id=project_id))
