from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import configs

db = SQLAlchemy()
migrate = Migrate()

def create_app(testing: bool):
    app = Flask(__name__)

    if testing:
        app.config.from_object(configs['testing'])
    else:
        app.config.from_object(configs[app.env])

    db.init_app(app)
    migrate.init_app(app, db)

    from . import api, view
    app.register_blueprint(api.bp)
    app.register_blueprint(view.bp)

    return app
