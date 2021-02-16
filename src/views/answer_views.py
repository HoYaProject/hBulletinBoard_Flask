from datetime import datetime
from flask import Blueprint, request, url_for, redirect, render_template, g, flash

from src.models.common import db
from src.models.question import QuestionModel
from src.models.answer import AnswerModel
from src.forms import AnswerForm
from .account_views import signin_required


bp = Blueprint("answer", __name__, url_prefix="/answer")


@bp.route("/create/<int:question_id>", methods=["POST"])
@signin_required
def create(question_id):
    form = AnswerForm()
    question = QuestionModel.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form["content"]
        answer = AnswerModel(content=content, created_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(
            f"{url_for('question.detail', question_id=question_id)}#answer_{answer.id}"
        )
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/modify/<int:answer_id>", methods=("GET", "POST"))
@signin_required
def modify(answer_id):
    answer = AnswerModel.query.get_or_404(answer_id)
    if g.user != answer.user:
        flsh("No authority for modification")
        return redirect(url_for("question.detail", question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modified_date = datetime.now()
            db.session.commit()
            return redirect(
                f"{url_for('question.detail', question_id=answer.question.id)}#answer_{answer.id}"
            )
    else:
        form = AnswerForm(obj=answer)
    return render_template("answer/answer_form.html", answer=answer, form=form)


@bp.route("/delete/<int:answer_id>")
@signin_required
def delete(answer_id):
    answer = AnswerModel.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash("No authority for deletion")
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))
