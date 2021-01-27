from flask import Blueprint


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/hello")
def hello():
    return "Hello, Flask"


@bp.route("/")
def index():
    return "hBB"
