from .common import db
from .like import question_like


class QuestionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(16), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_model.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("UserModel", backref=db.backref("question_set"))
    modified_date = db.Column(db.DateTime(), nullable=True)
    like = db.relationship(
        "UserModel", secondary=question_like, backref=db.backref("question_like_set")
    )
