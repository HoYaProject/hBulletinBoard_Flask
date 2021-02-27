from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from sqlalchemy import func

from ..models.common import db
from ..models.user import UserModel
from ..models.question import QuestionModel
from ..models.answer import AnswerModel
from ..models.like import question_like, answer_like
from ..forms import QuestionForm, AnswerForm
from .account_views import signin_required


bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/create/<string:category>", methods=["GET", "POST"])
@signin_required
def create(category="qna"):
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = QuestionModel(
            category=category,
            subject=form.subject.data,
            content=form.content.data,
            created_date=datetime.now(),
            user=g.user,
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("question._list", category=category))
    return render_template("question/question_form.html", form=form)


@bp.route("/list/<string:category>")
def _list(category="qna"):
    page = request.args.get("page", type=int, default=1)
    keyword = request.args.get("keyword", type=str, default="")
    sort = request.args.get("sort", type=str, default="recent")

    # Category
    question_list = QuestionModel.query.filter(QuestionModel.category == category)

    # Sort
    if sort == "recommend":
        sub_query = (
            db.session.query(
                question_like.c.question_id, func.count("*").label("num_like")
            )
            .group_by(question_like.c.question_id)
            .subquery()
        )
        question_list = question_list.outerjoin(
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
        question_list = question_list.outerjoin(
            sub_query, QuestionModel.id == sub_query.c.question_id
        ).order_by(sub_query.c.num_answer.desc(), QuestionModel.created_date.desc())
    else:
        question_list = question_list.order_by(QuestionModel.created_date.desc())

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
        category=category,
        question_list=question_list,
        page=page,
        keyword=keyword,
        sort=sort,
    )


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    page = request.args.get("page", type=int, default=1)
    sort = request.args.get("sort", type=str, default="recent")

    # Category
    category = QuestionModel.query.get_or_404(question_id).category

    # Sort
    if sort == "recommend":
        sub_query = (
            db.session.query(answer_like.c.answer_id, func.count("*").label("num_like"))
            .group_by(answer_like.c.answer_id)
            .subquery()
        )
        answer_list = (
            AnswerModel.query.filter(AnswerModel.question_id == question_id)
            .outerjoin(sub_query, AnswerModel.id == sub_query.c.answer_id)
            .order_by(sub_query.c.num_like.desc(), AnswerModel.created_date.desc())
        )
    else:
        answer_list = AnswerModel.query.filter(
            AnswerModel.question_id == question_id
        ).order_by(AnswerModel.created_date.desc())
    answer_list = answer_list.paginate(page, per_page=5)

    form = AnswerForm()
    question = QuestionModel.query.get_or_404(question_id)
    return render_template(
        "question/question_detail.html",
        category=category,
        question=question,
        answer_list=answer_list,
        page=page,
        sort=sort,
        form=form,
    )


@bp.route("/modify/<int:question_id>", methods=["GET", "POST"])
@signin_required
def modify(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    if g.user != question.user:
        flash("No authority for modification", "error")
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
    category = question.category
    if g.user != question.user:
        flash("No authority for deletion", "error")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question._list", category=category))
