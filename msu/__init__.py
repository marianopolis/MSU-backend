from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import configs

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object(configs[app.env])

    db.init_app(app)
    migrate.init_app(app)

    from . import api
    from . import view
    app.register_blueprint(api.bp)
    app.register_blueprint(view.bp)

    return app
