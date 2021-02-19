from flask import Flask, render_template
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flaskext.markdown import Markdown

from .filter import format_datetime
from .models.common import db
from .views import (
    main_views,
    account_views,
    question_views,
    answer_views,
    comment_views,
    like_views,
)
from .utils import crypto


def page_not_found(e):
    return render_template("404.html"), 404


app = Flask(__name__)

# Configuration
app.config.from_envvar("APP_CONFIG_FILE")
crypto.bcrypt = Bcrypt(app)

# DB ORM
migrate = Migrate()
db.init_app(app)
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    migrate.init_app(app, db, render_as_batch=True)
else:
    migrate.init_app(app, db)

# Blueprint
app.register_blueprint(main_views.bp)
app.register_blueprint(account_views.bp)
app.register_blueprint(question_views.bp)
app.register_blueprint(answer_views.bp)
app.register_blueprint(comment_views.bp)
app.register_blueprint(like_views.bp)

# Error Handler
app.register_error_handler(404, page_not_found)

# Filter
app.jinja_env.filters["datetime"] = format_datetime

# Bootstrap
Bootstrap(app)

# Markdown
Markdown(app, extensions=["nl2br", "fenced_code"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
