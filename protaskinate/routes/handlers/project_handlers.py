"""protaskinate/routes/handlers/project_handlers.py"""

from datetime import datetime
from typing import Dict

from flask import flash
from flask_login import current_user

from protaskinate.entities.project import ProjectRole
from protaskinate.routes.forms.project_forms import (
    CreateCommentForm,
    CreateProjectForm,
    CreateProjectUserForm,
    CreateTaskForm,
)
from protaskinate.services import comment_service, project_service, task_service


def handle_create_project(form: CreateProjectForm):
    """Handle the creation of a project"""
    data = {
        "name": form.name.data,
        "description": form.description.data if form.description.data else None,
    }

    project_service.create(
        name=data["name"],
        creator_id=current_user.id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        description=data["description"],
    )

    form.name.data = ""
    form.description.data = ""
    flash("Project created successfully", "success")


def handle_create_task(project_id: int, form: CreateTaskForm):
    """Handle the creation of a task"""
    data = {
        "title": form.title.data,
        "status": form.status.data,
        "priority": form.priority.data,
        "assignee_id": form.assignee_id.data if form.assignee_id.data != 0 else None,
        "deadline": form.deadline.data.isoformat() if form.deadline.data else None,
        "description": form.description.data if form.description.data else None,
    }

    if not project_service.check_user_write_access(current_user.id, project_id):
        flash("You do not have write-access to this project", "error")
        return

    task_service.create(
        title=data["title"],
        status=data["status"],
        priority=data["priority"],
        creator_id=current_user.id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        assignee_id=data["assignee_id"],
        deadline=data["deadline"],
        project_id=project_id,
        description=data["description"],
    )
    form.title.data = ""
    form.assignee_id.data = 0
    form.deadline.data = None
    form.description.data = ""
    flash("Task created successfully", "success")


def handle_create_project_user(project_id: int, form: CreateProjectUserForm):
    """Handle the creation of a project user"""
    data = {"user_id": form.user_id.data}

    if not project_service.check_user_update_access(current_user.id, project_id):
        flash("You do not have update-access to this project", "error")
        return

    try:
        data["role"] = ProjectRole(form.role.data)
    except ValueError:
        flash("Invalid role", "error")
        return

    if project_service.get_user_role(data["user_id"], project_id) is not None:
        flash("User already in project", "error")
        return

    project_service.add_user(project_id, data["user_id"], data["role"])
    flash("User added to project", "success")


def handle_update_user_role(project_id: int, user_id: int, form: Dict):
    """Handle the update of a user's role in a project"""
    try:
        role = ProjectRole(form["role"])
    except ValueError:
        flash("Invalid role", "error")
        return

    project_service.update_user_role(project_id, user_id, role)


def handle_create_comment(task_id: int, form: CreateCommentForm):
    """Handle the creation of a comment"""
    content = form.content.data

    new_comment = comment_service.create(
        task_id=task_id,
        creator_id=current_user.id,
        created_at=datetime.now().isoformat(),
        content=content,
    )

    if not new_comment:
        flash("Failed to create comment", "error")
        return

    form.content.data = ""


def handle_update_task(task_id: int, project_id: int, form: Dict):
    """Handle the update of a task"""
    update_data = {}
    if "status" in form:
        update_data["status"] = form["status"]
    if "priority" in form:
        update_data["priority"] = form["priority"]
    if "assignee_id" in form:
        update_data["assignee_id"] = int(form["assignee_id"])
        if update_data["assignee_id"] == 0:
            update_data["assignee_id"] = None
    if "deadline" in form:
        update_data["deadline"] = form["deadline"]

    task_service.update(task_id, project_id, **update_data)
