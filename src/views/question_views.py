from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from ..models.common import db
from src.models.question import QuestionModel
from ..forms import QuestionForm, AnswerForm


bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/create/", methods=["GET", "POST"])
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = QuestionModel(
            subject=form.subject.data,
            content=form.content.data,
            created_date=datetime.now(),
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("question/question_form.html", form=form)


@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)
    question_list = QuestionModel.query.order_by(QuestionModel.created_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template("question/question_list.html", question_list=question_list)


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    form = AnswerForm()
    question = QuestionModel.query.get_or_404(question_id)
    return render_template(
        "question/question_detail.html", question=question, form=form
    )
