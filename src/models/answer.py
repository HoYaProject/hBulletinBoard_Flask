from .common import db
from .like import answer_like


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
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user_model.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = db.relationship("UserModel", backref=db.backref("answer_set"))
    modified_date = db.Column(db.DateTime(), nullable=True)
    like = db.relationship(
        "UserModel", secondary=answer_like, backref=db.backref("answer_like_set")
    )
