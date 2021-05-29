"""Form object declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    SelectField,
)
from wtforms import validators
from wtforms.fields.core import DateTimeField, DecimalField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from wtforms.widgets.core import Select


class SignUpForm(FlaskForm):
    """Contact form."""

    email = StringField(
        "Email", [Email(message=("Not a valid email address.")), DataRequired()]
    )
    name = StringField(
        "Name", [DataRequired(), Length(min=1, max=64, message="range(1-64)")]
    )
    password = PasswordField("Password", [DataRequired()])
    password2 = PasswordField("Password (Confirm)", [DataRequired()])
    # recaptcha = RecaptchaField()
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", [Email(message=("Not a valid email")), DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class AppointmentForm(FlaskForm):
    client = StringField(
        "Client", [DataRequired(), Length(min=1, max=64, message="range(1-64)")]
    )
    service = SelectField("Service", validate_choice=False)
    employee = SelectField("Employee", validate_choice=False)
    appt_datetime = SelectField("Appointment Date/Time", validate_choice=False)
    tip = DecimalField("Tip", [NumberRange(min=0), DataRequired()])
    total = DecimalField("Total", [NumberRange(min=0), DataRequired()])
    add = SubmitField("New appointment")


class EmployeeForm(FlaskForm):
    name = StringField(
        "Name", [DataRequired(), Length(min=1, max=64, message="range(1-64)")]
    )
    add = SubmitField("New employee")


class ServiceForm(FlaskForm):
    name = StringField(
        "Name", [DataRequired(), Length(min=1, max=64, message="range(1-64)")]
    )
    price = DecimalField("Price", [NumberRange(min=0.01)])
    add = SubmitField("New service")
