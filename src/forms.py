from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])


class AnswerForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
