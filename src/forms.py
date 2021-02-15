from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])


class AnswerForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    password1 = PasswordField(
        "Password",
        validators=[DataRequired(), EqualTo("password2", "Password doesn't match")],
    )
    password2 = PasswordField("Password Confirm", validators=[DataRequired()])
    email = EmailField("Email", [DataRequired(), Email()])


class SignInForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
