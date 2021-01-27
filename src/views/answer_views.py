from datetime import datetime
from flask import Blueprint, request, url_for, redirect
from src.models.common import db
from src.models.question import QuestionModel
from src.models.answer import AnswerModel


bp = Blueprint("answer", __name__, url_prefix="/answer")


@bp.route("/create/<int:question_id>", methods=["POST"])
def create(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    content = request.form["content"]
    answer = AnswerModel(content=content, created_date=datetime.now())
    question.answer_set.append(answer)
    db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))
