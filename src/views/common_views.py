from flask import Blueprint, redirect, url_for, render_template, request, g, flash
from sqlalchemy import func

from ..models.common import db
from ..models.user import UserModel
from ..models.question import QuestionModel
from ..models.answer import AnswerModel
from ..models.comment import CommentModel
from ..models.like import question_like, answer_like
from ..forms import BaseForm, PasswordForm
from ..utils import crypto

bp = Blueprint("common", __name__, url_prefix="/common")


@bp.route("/settings")
def settings():
    return redirect(url_for("common.settings_base"))


@bp.route("/settings/base", methods=["GET", "POST"])
def settings_base():
    user = UserModel.query.filter(UserModel.username == g.user.username).first()
    if request.method == "POST":
        form = BaseForm()
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            flash("Successfully changed", "info")
            return redirect(url_for("common.settings_base"))
    else:
        form = BaseForm(obj=user)
    return render_template("common/settings.html", tabs="base", form=form)


@bp.route("/settings/password", methods=["GET", "POST"])
def password():
    user = UserModel.query.filter(UserModel.username == g.user.username).first()
    form = PasswordForm()
    if request.method == "POST" and form.validate_on_submit():
        if crypto.bcrypt.check_password_hash(user.password, form.old_password.data):
            user.password = crypto.bcrypt.generate_password_hash(
                form.new_password1.data
            )
            db.session.commit()
            flash("Successfully changed", "info")
            return redirect(url_for("common.password"))
        else:
            flash("Wrong password", "error")
    return render_template("common/settings.html", tabs="password", form=form)


@bp.route("/profile/base/<int:id>")
def profile_base(id):
    user = UserModel.query.filter(UserModel.id == id).first()
    return render_template("common/profile.html", tabs="base", user=user)


@bp.route("/profile/question/<int:id>")
def profile_question(id):
    page = request.args.get("page", type=int, default=1)
    sort = request.args.get("sort", type=str, default="recent")

    question_list = QuestionModel.query.filter(QuestionModel.user_id == id)

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
    else:
        question_list = question_list.order_by(QuestionModel.created_date.desc())

    question_list = question_list.paginate(page, per_page=10)

    return render_template(
        "common/profile.html",
        tabs="question",
        user=g.user,
        posting_list=question_list,
        page=page,
        sort=sort,
    )


@bp.route("/profile/answer/<int:id>")
def profile_answer(id):
    page = request.args.get("page", type=int, default=1)
    sort = request.args.get("sort", type=str, default="recent")

    answer_list = AnswerModel.query.filter(AnswerModel.user_id == id)

    # Sort
    if sort == "recommend":
        sub_query = (
            db.session.query(answer_like.c.answer_id, func.count("*").label("num_like"))
            .group_by(answer_like.c.answer_id)
            .subquery()
        )
        answer_list = answer_list.outerjoin(
            sub_query, AnswerModel.id == sub_query.c.answer_id
        ).order_by(sub_query.c.num_like.desc(), AnswerModel.created_date.desc())
    else:
        answer_list = answer_list.order_by(AnswerModel.created_date.desc())

    answer_list = answer_list.paginate(page, per_page=5)

    return render_template(
        "common/profile.html",
        tabs="answer",
        user=g.user,
        posting_list=answer_list,
        page=page,
        sort=sort,
    )


@bp.route("/profile/comment/<int:id>")
def profile_comment(id):
    page = request.args.get("page", type=int, default=1)
    sort = request.args.get("sort", type=str, default="recent")

    comment_list = CommentModel.query.filter(CommentModel.user_id == id)
    comment_list = comment_list.order_by(CommentModel.created_date.desc())
    comment_list = comment_list.paginate(page, per_page=5)

    return render_template(
        "common/profile.html",
        tabs="comment",
        user=g.user,
        posting_list=comment_list,
        page=page,
        sort=sort,
    )
