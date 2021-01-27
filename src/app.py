from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import config
from .models.common import db
from .views import main_views, question_views, answer_views


app = Flask(__name__)
migrate = Migrate()

# Configuration
app.config.from_object(config)

# ORM
db.init_app(app)
migrate.init_app(app, db)

# Blueprint
app.register_blueprint(main_views.bp)
app.register_blueprint(question_views.bp)
app.register_blueprint(answer_views.bp)

# Bootstrap
Bootstrap(app)


if __name__ == "__main__":
    app.run()