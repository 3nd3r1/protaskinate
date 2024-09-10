"""protaskinate/app.py"""

import logging
import os

import click
from flask import Flask
from flask.cli import with_appcontext
from sqlalchemy import text

from protaskinate.routes import dashboard, login
from protaskinate.utils.database import db


def create_app():
    """ Create the Flask app """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/protaskinate")
    app.config["SECRET_KEY"] = os.urandom(12).hex()
    app.config["PORT"] = os.environ.get("PORT", 5000)
    app.config["DEBUG"] = os.environ.get("DEBUG", False)

    logging.basicConfig(level=logging.DEBUG if app.config["DEBUG"] else logging.INFO)

    db.init_app(app)

    app.cli.add_command(create_schema)

    with app.app_context():
        app.register_blueprint(dashboard.blueprint)
        app.register_blueprint(login.blueprint)

        @app.route("/ping")
        def ping():
            return "pong"

    return app


@click.command("create_schema")
@with_appcontext
def create_schema():
    """ Create the database schema """
    logging.info("Creating schema")
    with open("schema.sql", "r", encoding="utf-8") as fp:
        sql = fp.read()

    logging.debug("SQL: %s", sql)
    with db.engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
