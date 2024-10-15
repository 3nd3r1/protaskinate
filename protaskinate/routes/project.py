"""protaskinate/routes/project.py"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from protaskinate.routes.forms.project_forms import (
    CreateCommentForm,
    CreateProjectForm,
    CreateProjectUserForm,
    CreateTaskForm,
)
from protaskinate.routes.handlers.project_handlers import (
    handle_create_comment,
    handle_create_project,
    handle_create_project_user,
    handle_create_task,
    handle_update_task,
    handle_update_user_role,
)
from protaskinate.services import (
    comment_service,
    project_service,
    task_service,
    user_service,
)
from protaskinate.utils.project import (
    project_read_access_required,
    project_update_access_required,
    task_update_access_required,
)

blueprint = Blueprint("project", __name__)


@blueprint.route("/projects", methods=["GET", "POST"])
@login_required
def project_list_route():
    """Render the projects page"""
    form = CreateProjectForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        handle_create_project(form)

    projects_with_roles = project_service.get_all_by_user_with_role(current_user.id)
    return render_template(
        "project_list.html", form=form, projects_with_roles=projects_with_roles
    )


@blueprint.route("/projects/<int:project_id>", methods=["GET", "POST"])
@login_required
@project_read_access_required
def project_view_route(project_id: int):
    """Render the single project view page"""
    create_task_form = CreateTaskForm(request.form, prefix="create_task")
    create_project_user_form = CreateProjectUserForm(
        request.form, prefix="create_project_user"
    )

    if create_task_form.submit.data and create_task_form.validate_on_submit():
        handle_create_task(project_id, create_task_form)

    if (
        create_project_user_form.submit.data
        and create_project_user_form.validate_on_submit()
    ):
        handle_create_project_user(project_id, create_project_user_form)

    project = project_service.get_by_id(project_id)
    tasks = task_service.get_all_by_project(
        project_id, order_by_fields=["priority", "created_at"], reverse=[True, False]
    )
    project_users = project_service.get_all_users_in_project(project_id)
    user_project_role = project_service.get_user_role(current_user.id, project_id)
    users_dict = {user.id: user for user in user_service.get_all()}

    return render_template(
        "project_view.html",
        create_task_form=create_task_form,
        create_project_user_form=create_project_user_form,
        project=project,
        user_project_role=user_project_role,
        tasks=tasks,
        project_users=project_users,
        users_dict=users_dict,
    )


@blueprint.route("/projects/<int:project_id>/board", methods=["GET"])
@login_required
@project_read_access_required
def project_board_route(project_id: int):
    """Render the project board view page"""
    project = project_service.get_by_id(project_id)
    tasks = task_service.get_all_by_project(project_id)
    user_project_role = project_service.get_user_role(current_user.id, project_id)
    users_dict = {user.id: user for user in user_service.get_all()}
    return render_template(
        "project_board.html",
        project=project,
        tasks=tasks,
        user_project_role=user_project_role,
        users_dict=users_dict,
    )


@blueprint.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
@project_update_access_required
def project_delete_route(project_id: int):
    """Delete a project"""
    project_service.delete(project_id)
    return redirect(url_for("project.project_list_route"))


@blueprint.route(
    "/projects/<int:project_id>/users/<int:user_id>/edit", methods=["POST"]
)
@login_required
@project_update_access_required
def project_user_edit_route(project_id: int, user_id: int):
    """Edit the role of a user in a project"""
    if request.form:
        handle_update_user_role(project_id, user_id, request.form)
    return redirect(request.referrer)


@blueprint.route(
    "/projects/<int:project_id>/tasks/<int:task_id>", methods=["GET", "POST"]
)
@login_required
@project_read_access_required
def project_task_view_route(project_id: int, task_id: int):
    """View of a single task in a project"""
    form = CreateCommentForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        handle_create_comment(task_id, form)

    task = task_service.get_by_id_and_project(task_id, project_id)
    comments = comment_service.get_all_by_task(task_id)
    project = project_service.get_by_id(project_id)
    user_project_role = project_service.get_user_role(current_user.id, project_id)
    users_dict = {user.id: user for user in user_service.get_all()}

    if not project:
        return redirect(url_for("dashboard.dashboard_route"))
    if not task:
        return redirect(url_for("project.project_view_route", project_id=project_id))

    return render_template(
        "project_task_view.html",
        project=project,
        task=task,
        comments=comments,
        users_dict=users_dict,
        user_project_role=user_project_role,
        form=form,
    )


@blueprint.route(
    "/projects/<int:project_id>/tasks/<int:task_id>/edit", methods=["POST"]
)
@login_required
@task_update_access_required
def project_task_edit_route(project_id: int, task_id: int):
    """Edit a task in a project"""
    if request.form:
        handle_update_task(task_id, project_id, request.form)

    return redirect(request.referrer)


@blueprint.route(
    "/projects/<int:project_id>/tasks/<int:task_id>/delete", methods=["POST"]
)
@login_required
@task_update_access_required
def project_task_delete_route(project_id: int, task_id: int):
    """Delete a task from a project"""
    task_service.delete(task_id, project_id)
    return redirect(url_for("project.project_view_route", project_id=project_id))
