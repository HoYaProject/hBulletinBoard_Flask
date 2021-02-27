import functools
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
from flask_mail import Message

from ..models.common import db
from ..models.user import UserModel
from ..forms import SignUpForm, SignInForm, ForgotPasswordForm
from ..utils import crypto, email

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
            flash("Already exists", "error")
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
        flash(error, "error")
    return render_template("account/signin.html", form=form)


@bp.route("/signout/")
def signout():
    session.clear()
    return redirect(url_for("main.index"))


@bp.route("/forgot_password", methods=("GET", "POST"))
def forgot_password():
    form = ForgotPasswordForm()
    user = UserModel.query.filter(UserModel.email == form.email.data).first()
    if user:
        new_password = "1234"

        msg = Message("[hBB] Temporary Password", sender="", recipients=[user.email])
        msg.body = f"Your temporary password is {new_password}.\nYou should change it after using it."
        email.email.send(msg)

        user.password = new_password
        db.session.commit()
        flash(f"Sent a temporary password to {user.email}", "info")
    return render_template("account/forgot_password.html", form=form)


@bp.before_app_request
def load_signed_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = UserModel.query.get(user_id)


def signin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("account.signin"))
        return view(**kwargs)

    return wrapped_view