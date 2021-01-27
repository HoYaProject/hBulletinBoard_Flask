from flask import Flask
from flask_migrate import Migrate
import config
from .models.common import db
from .views import main_views


app = Flask(__name__)
migrate = Migrate()

# Configuration
app.config.from_object(config)

# ORM
db.init_app(app)
migrate.init_app(app, db)

# Blueprint
app.register_blueprint(main_views.bp)


if __name__ == "__main__":
    app.run()