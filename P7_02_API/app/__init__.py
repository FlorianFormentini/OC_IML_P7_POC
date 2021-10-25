import os
from flask import Flask

from .config import config_by_name
# import flask_monitoringdashboard as dashboard


def create_app(config_name=os.getenv('CONFIG_ENV', 'dev')) -> Flask:
    """Create and configure the app instance"""
    print("config", config_name)
    app = Flask(__name__, instance_relative_config=False, template_folder='./homepage/templates', static_folder='./homepage/static')
    # load config
    app.config.from_object(config_by_name[config_name])
    # dashboard.bind(app)

    # initialize db
    # from .database.relationnal import db  # sqlite/postgres
    from .database.mongodb import db  # mongodb
    db.init_app(app)

    with app.app_context():
        # import blueprints
        from .api import api_blueprint
        # register blueprints
        app.register_blueprint(api_blueprint)  # url_prefix='/api' to add a prefix
        return app
