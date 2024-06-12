import datetime
import os
from http.client import INTERNAL_SERVER_ERROR
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

from flask import Blueprint, Flask, current_app, jsonify
from flask_apispec import FlaskApiSpec
from sqlalchemy.exc import SQLAlchemyError

from src.apps import auth, user
from src.commons.configs.config import get_config
from src.commons.constants.message import ERROR_MESSSAGE
from src.commons.extensions import bcrypt, cache, cors, db, docs, mail, migrate
from src.commons.middlewares.exception import ApiException, error_template


def create_app(config_name):
    app = Flask(
        __name__.split(".", maxsplit=1)[0],
        template_folder="./static/templates",
        static_folder="static",
    )
    app.url_map.strict_slashes = False
    app.config.from_object(get_config(config_name))

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app: Flask):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    docs.init_app(app)
    configure_logging(app)
    # app.extensions["mail"].debug = 0


def register_blueprints(app: Flask):
    """Register Flask blueprints."""
    api_docs = docs if app.config.get("ENV") != "production" else None

    set_routes(
        app, api_docs=api_docs, blueprint=auth.auth_route, resources=auth.resources
    )
    set_routes(
        app, api_docs=api_docs, blueprint=user.user_route, resources=user.resources
    )

    origins = (
        ["*"]
        if app.config.get("ENV") != "production"
        else app.config.get("CORS_ORIGIN_WHITELIST", "*")
    )
    cors.init_app(app, origins=origins)


def register_errorhandlers(app: Flask):
    def errorhandler(error):
        response, code = error.to_json()
        current_app.logger.error(response.data)
        return response, code

    def errorhandler500(error):
        print(f"ERROR {error}")
        current_app.logger.error(error)
        res = error_template(
            data={"message": ERROR_MESSSAGE.SERVER_ERROR},
            status_code=INTERNAL_SERVER_ERROR,
        )
        return jsonify(res), INTERNAL_SERVER_ERROR

    app.errorhandler(INTERNAL_SERVER_ERROR)(errorhandler500)
    app.errorhandler(ApiException)(errorhandler)
    app.errorhandler(SQLAlchemyError)(errorhandler500)


def set_routes(
    app: Flask, blueprint: Blueprint, api_docs: FlaskApiSpec, resources: list
):
    for resource, route, name, methods in resources:
        blueprint.add_url_rule(route, view_func=resource.as_view(name), methods=methods)

    app.register_blueprint(blueprint)

    if api_docs is not None:
        for resource, route, name, methods in resources:
            api_docs.register(resource, blueprint=blueprint.name, endpoint=name)


def configure_logging(app: Flask):
    log_filename = datetime.datetime.now().strftime("app_%Y-%m-%d.log")
    log_file_path = os.path.join(app.config.get("LOG_DIR"), log_filename)

    if not os.path.exists(app.config.get("LOG_DIR")):
        os.makedirs(app.config.get("LOG_DIR"))

    file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1)
    file_handler.setLevel(app.config.get("LOG_LEVEL"))
    file_handler.setFormatter(Formatter(app.config.get("LOG_FORMAT")))
    app.logger.addHandler(file_handler)
