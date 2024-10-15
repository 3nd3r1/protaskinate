"""protaskinate/routes/forms/register_forms.py"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    """Form for registering a user"""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                                                                     EqualTo("password")])
    submit = SubmitField("Register")
