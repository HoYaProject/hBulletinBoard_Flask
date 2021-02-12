import config
from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

from .filter import format_datetime
from .models.common import db
from .views import main_views, question_views, answer_views, auth_views
from .utils import crypto

app = Flask(__name__)

# Configuration
app.config.from_object(config)
crypto.bcrypt = Bcrypt(app)

# DB ORM
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

# Blueprint
app.register_blueprint(main_views.bp)
app.register_blueprint(question_views.bp)
app.register_blueprint(answer_views.bp)
app.register_blueprint(auth_views.bp)

# Filter
app.jinja_env.filters["datetime"] = format_datetime

# Bootstrap
Bootstrap(app)


if __name__ == "__main__":
    app.run()