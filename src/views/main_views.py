from flask import Blueprint, url_for, redirect, current_app


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    current_app.logger.info("This is a user log")
    return redirect(url_for("question._list", category="qna"))
