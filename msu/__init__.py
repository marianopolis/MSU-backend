"""Entrypoint into flask application.

Given a module (msu in our case), flask runs the create_app function
and subsequently uses the created app.
"""

from datetime import datetime

from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import configs


class CustomJSONEncoder(JSONEncoder):
    """Custom encoder to encode datetimes as ISO8061.

    Used to override the default JSON encoder used by flask,
    which doesn't properly format dates.
    """

    def default(self, obj):
        # Override only the format of datetime instances.
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)

db = SQLAlchemy()
migrate = Migrate()

def create_app(testing=False):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    # Use relevant configuration based on value
    # of FLASK_ENV environment variable.
    if testing:
        app.config.from_object(configs['testing'])
    else:
        app.config.from_object(configs[app.env])

    db.init_app(app)
    migrate.init_app(app, db)

    from . import api, view
    app.register_blueprint(api.bp)
    app.register_blueprint(view.bp)

    # Custom jinja2 filter used in templates to format dates
    @app.template_filter('datetime')
    def format_datetime(d: datetime):
        return d.strftime('%H:%M %d %b %Y')

    return app
