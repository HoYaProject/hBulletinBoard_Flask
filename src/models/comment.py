from .common import db


class CommentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_model.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("UserModel", backref=db.backref("comment_set"))
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    modified_date = db.Column(db.DateTime())
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("question_model.id", ondelete="CASCADE"),
        nullable=True,
    )
    question = db.relationship("QuestionModel", backref=db.backref("comment_set"))
    answer_id = db.Column(
        db.Integer, db.ForeignKey("answer_model.id", ondelete="CASCADE"), nullable=True
    )
    answer = db.relationship("AnswerModel", backref=db.backref("comment_set"))
