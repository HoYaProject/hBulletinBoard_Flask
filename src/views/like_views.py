from flask import Blueprint, url_for, redirect, g, flash

from .account_views import signin_required
from src.models.common import db
from src.models.question import QuestionModel
from src.models.answer import AnswerModel

bp = Blueprint("like", __name__, url_prefix="/like")


@bp.route("/question/<int:question_id>/")
@signin_required
def question(question_id):
    _question = QuestionModel.query.get_or_404(question_id)
    if g.user == _question.user:
        flash("Can't like own question", "error")
    else:
        _question.like.append(g.user)
        db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))


@bp.route("/answer/<int:answer_id>/")
@signin_required
def answer(answer_id):
    _answer = AnswerModel.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash("Can't like own answer", "error")
    else:
        _answer.like.append(g.user)
        db.session.commit()
    return redirect(url_for("question.detail", question_id=_answer.question.id))
