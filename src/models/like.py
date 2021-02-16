from .common import db


question_like = db.Table(
    "question_like",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user_model.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "question_id",
        db.Integer,
        db.ForeignKey("question_model.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

answer_like = db.Table(
    "answer_like",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user_model.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "answer_id",
        db.Integer,
        db.ForeignKey("answer_model.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
