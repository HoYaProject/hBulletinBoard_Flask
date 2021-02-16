from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, redirect, flash

from .account_views import signin_required
from ..forms import CommentForm
from ..models.answer import AnswerModel
from ..models.comment import CommentModel
from ..models.common import db
from ..models.question import QuestionModel

bp = Blueprint("comment", __name__, url_prefix="/comment")


@bp.route("/create/question/<int:question_id>", methods=("GET", "POST"))
@signin_required
def create_comment_for_question(question_id):
    form = CommentForm()
    question = QuestionModel.query.get_or_404(question_id)
    if request.method == "POST" and form.validate_on_submit():
        comment = CommentModel(
            user=g.user,
            content=form.content.data.strip(),
            created_date=datetime.now(),
            question=question,
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(
            f"{url_for('question.detail', question_id=question_id)}#comment_{comment.id}"
        )
    return render_template("comment/comment_form.html", form=form)


@bp.route("/modify/question/<int:comment_id>", methods=("GET", "POST"))
@signin_required
def modify_comment_for_question(comment_id):
    comment = CommentModel.query.get_or_404(comment_id)

    if g.user != comment.user:
        flash("No authority for modification")
        return redirect(url_for("question.detail", question_id=comment.question.id))

    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modified_date = datetime.now()
            db.session.commit()
            return redirect(
                f"{url_for('question.detail', question_id=comment.question.id)}#comment_{comment.id}"
            )
    else:
        form = CommentForm(obj=comment)

    return render_template("comment/comment_form.html", form=form)


@bp.route("/delete/question/<int:comment_id>")
@signin_required
def delete_comment_for_question(comment_id):
    comment = CommentModel.query.get_or_404(comment_id)
    question_id = comment.question.id
    if g.user != comment.user:
        flash("No authority for deletion")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))


@bp.route("/create/answer/<int:answer_id>", methods=("GET", "POST"))
@signin_required
def create_comment_for_answer(answer_id):
    form = CommentForm()
    answer = AnswerModel.query.get_or_404(answer_id)
    if request.method == "POST" and form.validate_on_submit():
        comment = CommentModel(
            user=g.user,
            content=form.content.data.strip(),
            created_date=datetime.now(),
            answer=answer,
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(
            f"{url_for('question.detail', question_id=answer.question.id)}#comment_{comment.id}"
        )
    return render_template("comment/comment_form.html", form=form)


@bp.route("/modify/answer/<int:comment_id>", methods=("GET", "POST"))
@signin_required
def modify_comment_for_answer(comment_id):
    comment = CommentModel.query.get_or_404(comment_id)

    if g.user != comment.user:
        flash("No authority for modification")
        return redirect(url_for("question.detail", question_id=comment.answer.id))

    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modified_date = datetime.now()
            db.session.commit()
            return redirect(
                f"{url_for('question.detail', question_id=comment.answer.question.id)}#comment_{comment.id}"
            )
    else:
        form = CommentForm(obj=comment)

    return render_template("comment/comment_form.html", form=form)


@bp.route("/delete/answer/<int:comment_id>")
@signin_required
def delete_comment_for_answer(comment_id):
    comment = CommentModel.query.get_or_404(comment_id)
    question_id = comment.answer.question.id
    if g.user != comment.user:
        flash("No authority for deletion")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("question.detail", question_id=question_id))
