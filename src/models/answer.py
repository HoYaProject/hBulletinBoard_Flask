from .common import db


class AnswerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question_model.id", ondelete="CASCADE")
    )
    question = db.relationship(
        "QuestionModel",
        backref=db.backref(
            "answer_set",
        ),
    )
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)