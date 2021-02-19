from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from sqlalchemy import func

from ..models.common import db
from ..models.user import UserModel
from ..models.question import QuestionModel
from ..models.answer import AnswerModel
from ..models.like import question_like
from ..forms import QuestionForm, AnswerForm
from .account_views import signin_required


bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/create/", methods=["GET", "POST"])
@signin_required
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = QuestionModel(
            subject=form.subject.data,
            content=form.content.data,
            created_date=datetime.now(),
            user=g.user,
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("question/question_form.html", form=form)


@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)
    keyword = request.args.get("keyword", type=str, default="")
    sort = request.args.get("sort", type=str, default="recent")

    # Sort
    if sort == "recommend":
        sub_query = (
            db.session.query(
                question_like.c.question_id, func.count("*").label("num_like")
            )
            .group_by(question_like.c.question_id)
            .subquery()
        )
        question_list = QuestionModel.query.outerjoin(
            sub_query, QuestionModel.id == sub_query.c.question_id
        ).order_by(sub_query.c.num_like.desc(), QuestionModel.created_date.desc())
    elif sort == "popular":
        sub_query = (
            db.session.query(
                AnswerModel.question_id, func.count("*").label("num_answer")
            )
            .group_by(AnswerModel.question_id)
            .subquery()
        )
        question_list = QuestionModel.query.outerjoin(
            sub_query, QuestionModel.id == sub_query.c.question_id
        ).order_by(sub_query.c.num_answer.desc(), QuestionModel.created_date.desc())
    else:
        question_list = QuestionModel.query.order_by(QuestionModel.created_date.desc())

    # Search
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = (
            db.session.query(
                AnswerModel.question_id, AnswerModel.content, UserModel.username
            )
            .join(UserModel, AnswerModel.user_id == UserModel.id)
            .subquery()
        )
        question_list = (
            question_list.join(UserModel)
            .outerjoin(sub_query, sub_query.c.question_id == QuestionModel.id)
            .filter(
                QuestionModel.subject.ilike(search)
                | QuestionModel.content.ilike(search)
                | UserModel.username.ilike(search)
                | sub_query.c.content.ilike(search)
                | sub_query.c.username.ilike(search),
            )
            .distinct()
        )
    question_list = question_list.paginate(page, per_page=10)

    return render_template(
        "question/question_list.html",
        question_list=question_list,
        page=page,
        keyword=keyword,
        sort=sort,
    )


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    form = AnswerForm()
    question = QuestionModel.query.get_or_404(question_id)
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/modify/<int:question_id>", methods=["GET", "POST"])
@signin_required
def modify(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    if g.user != question.user:
        flash("No authority for modification")
        return redirect(url_for("question.detail", question_id=question_id))
    if request.method == "POST":
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modified_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template("question/question_form.html", form=form)


@bp.route("/delete/<int:question_id>")
@signin_required
def delete(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    if g.user != question.user:
        flash("No authority for deletion")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question._list"))
