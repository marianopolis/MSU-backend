from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_simplemde import SimpleMDE

from config import configs

db = SQLAlchemy()
migrate = Migrate()
simplemde = SimpleMDE()

def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config.from_object(configs['testing'])
    else:
        app.config.from_object(configs[app.env])

    db.init_app(app)
    migrate.init_app(app, db)
    simplemde.init_app(app)


    from . import api, view
    app.register_blueprint(api.bp)
    app.register_blueprint(view.bp)

    return app
