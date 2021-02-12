from flask import (
    Blueprint,
    url_for,
    render_template,
    flash,
    request,
    redirect,
    session,
    g,
)

from ..models.common import db
from ..models.user import UserModel
from ..forms import SignUpForm, SignInForm
from ..utils import crypto

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/signup/", methods=("GET", "POST"))
def signup():
    form = SignUpForm()
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
    return render_template("account/signup.html", form=form)


@bp.route("/signin/", methods=("GET", "POST"))
def signin():
    form = SignInForm()
    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = UserModel.query.filter_by(username=form.username.data).first()
        if not user:
            error = "User not found"
        elif not crypto.bcrypt.check_password_hash(user.password, form.password.data):
            error = "Wrong password"
        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.index"))
        flash(error)
    return render_template("account/signin.html", form=form)


@bp.route("/signout/")
def signout():
    session.clear()
    return redirect(url_for("main.index"))


@bp.before_app_request
def load_signed_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = UserModel.query.get(user_id)
