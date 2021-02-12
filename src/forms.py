from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])


class AnswerForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])


class CreateUserForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    password1 = PasswordField(
        "Password",
        validators=[DataRequired(), EqualTo("password2", "Password doesn't match")],
    )
    password2 = PasswordField("Password Confirm", validators=[DataRequired()])
    email = EmailField("Email", [DataRequired(), Email()])
