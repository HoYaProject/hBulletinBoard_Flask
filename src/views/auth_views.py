from flask import Blueprint, url_for, render_template, flash, request, redirect

from ..models.common import db
from ..models.user import UserModel
from ..forms import CreateUserForm
from ..utils import crypto

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup/", methods=("GET", "POST"))
def signup():
    form = CreateUserForm()
    if request.method == "POST" and form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if not user:
            user = UserModel(
                username=form.username.data,
                password=crypto.bcrypt.generate_password_hash(form.password1.data),
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("Already exists")
    return render_template("auth/signup.html", form=form)
