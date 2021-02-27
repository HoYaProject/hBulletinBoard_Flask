from flask import Blueprint, redirect, url_for, render_template, request, g, flash

from ..models.common import db
from ..models.user import UserModel
from ..forms import BaseForm, PasswordForm
from ..utils import crypto

bp = Blueprint("common", __name__, url_prefix="/common/settings")


@bp.route("/")
def index():
    return redirect(url_for("common.base"))


@bp.route("/base", methods=["GET", "POST"])
def base():
    user = UserModel.query.filter(UserModel.username == g.user.username).first()
    if request.method == "POST":
        form = BaseForm()
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            flash("Successfully changed", "info")
            return redirect(url_for("common.base"))
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
