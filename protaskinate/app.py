"""protaskinate/app.py"""

import logging
import os

import click
from flask import Flask
from flask.cli import load_dotenv, with_appcontext
from sqlalchemy import text
from werkzeug.security import generate_password_hash

from protaskinate.routes import dashboard, login
from protaskinate.utils.database import db

load_dotenv(os.path.join(os.path.dirname(__file__), "../.secret_key.env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


def create_app():
    """ Create the Flask app """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/protaskinate")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(12).hex())
    app.config["PORT"] = os.environ.get("PORT", 5000)
    app.config["DEBUG"] = os.environ.get("DEBUG", False)

    logging.basicConfig(level=logging.DEBUG if app.config["DEBUG"] else logging.INFO)

    db.init_app(app)

    app.cli.add_command(create_schema)
    app.cli.add_command(populate_db)

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


@click.command("populate_db")
@with_appcontext
def populate_db():
    """ Populate the database with sample data """
    logging.info("Populating database")
    sql = """
    INSERT INTO users (username, password) VALUES (:username, :password);
    """
    with db.engine.connect() as conn:
        conn.execute(text(sql), {"username": "admin", "password": generate_password_hash("admin")})
        conn.commit()
