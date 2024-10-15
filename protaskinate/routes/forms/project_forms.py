""" protaskinate/routes/forms/project_forms.py """

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

from protaskinate.entities.project import ProjectRole
from protaskinate.entities.task import TaskPriority, TaskStatus
from protaskinate.services import user_service


class CreateTaskForm(FlaskForm):
    """Form for creating a task"""

    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])
    status = SelectField(
        "Status",
        choices=[
            (status.value, status.name.lower().replace("_", " ").title())
            for status in TaskStatus
        ],
    )
    priority = SelectField(
        "Priority",
        choices=[
            (priority.value, priority.name.lower().replace("_", " ").title())
            for priority in TaskPriority
        ],
    )
    assignee_id = SelectField("Assignee", coerce=int)
    deadline = DateField("Deadline", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Create Task")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignee_id.choices = [(0, "Not Assigned")] + [
            (user.id, user.username) for user in user_service.get_all()
        ]  # type: ignore


class CreateCommentForm(FlaskForm):
    """Form for creating a comment"""

    content = TextAreaField("Content", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Send")


class CreateProjectForm(FlaskForm):
    """Form for creating a project"""

    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Create Project")


class CreateProjectUserForm(FlaskForm):
    """Form for adding a user to a project"""

    user_id = SelectField("User", coerce=int)
    role = SelectField(
        "Role",
        choices=[(role.value, role.name.lower().title()) for role in ProjectRole],
    )
    submit = SubmitField("Add User")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id.choices = [
            (user.id, user.username) for user in user_service.get_all()
        ]
