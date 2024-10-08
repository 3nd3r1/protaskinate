"""protaskinate/utils/project.py"""

from functools import wraps

from flask import flash, request, redirect
from flask_login import current_user

from protaskinate.services import project_service


def project_read_access_required(f):
    """Decorator to check if user has read-access to a project"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        project_id = kwargs.get("project_id")
        if (not project_id or
            not project_service.check_user_read_access(current_user.id, project_id)):
            flash("You do not have read-access to this project", "error")
            return redirect(request.referrer)
        return f(*args, **kwargs)
    return decorated_function

def project_write_access_required(f):
    """decorator to check if user has read-access to a project"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        project_id = kwargs.get("project_id")
        if (not project_id or
            not project_service.check_user_read_access(current_user.id, project_id)):
            flash("You do not have read-access to this project", "error")
            return redirect(request.referrer)
        return f(*args, **kwargs)
    return decorated_function

def project_update_access_required(f):
    """Decorator to check if user has update-access to a project"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        project_id = kwargs.get("project_id")
        if (not project_id or
            not project_service.check_user_update_access(current_user.id, project_id)):
            flash("You do not have update-access to this project", "error")
            return redirect(request.referrer)
        return f(*args, **kwargs)
    return decorated_function

def task_update_access_required(f):
    """Decorator to check if user has update-access to a task"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        project_id = kwargs.get("project_id")
        task_id = kwargs.get("task_id")
        if (not project_id or not task_id or
            not project_service.check_user_task_update_access(current_user.id, project_id,
                                                              task_id)):
            flash("You do not have update-access to this task", "error")
            return redirect(request.referrer)
        return f(*args, **kwargs)
    return decorated_function
