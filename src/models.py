from src import db


class QuestionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)


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
