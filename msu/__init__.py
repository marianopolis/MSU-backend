from datetime import datetime

from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_simplemde import SimpleMDE

from config import configs

# Custom encoder to encode datetimes as ISO8061
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)

db = SQLAlchemy()
migrate = Migrate()
simplemde = SimpleMDE()

def create_app(testing=False):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

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
