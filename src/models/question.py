from .common import db


class QuestionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)