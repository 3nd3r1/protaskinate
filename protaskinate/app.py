"""protaskinate/app.py"""

import logging
import os

import click
from flask import Flask
from flask.cli import load_dotenv, with_appcontext
from sqlalchemy import text
from werkzeug.security import generate_password_hash

from protaskinate.routes import dashboard, login, logout, tasks, register
from protaskinate.utils.database import db
from protaskinate.utils.login_manager import lm

load_dotenv(os.path.join(os.path.dirname(__file__), "../.secret_key.env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


def create_app():
    """ Create the Flask app """
    app = Flask(__name__)

    # If DATABASE_URL or SECRET_KEY not set throw error
    if not os.environ.get("DATABASE_URL"):
        raise ValueError("DATABASE_URL environment variable is not set")
    if not os.environ.get("SECRET_KEY"):
        raise ValueError(("Please generate a secret_key with "
                          "`poetry run invoke generate-secret-key`"))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["PORT"] = os.environ.get("PORT", 5000)
    app.config["DEBUG"] = os.environ.get("DEBUG", False)

    logging.basicConfig(level=logging.DEBUG if app.config["DEBUG"] else logging.INFO)

    db.init_app(app)
    lm.init_app(app)

    app.cli.add_command(create_schema)
    app.cli.add_command(populate_db)

    with app.app_context():
        app.register_blueprint(dashboard.blueprint)
        app.register_blueprint(login.blueprint)
        app.register_blueprint(logout.blueprint)
        app.register_blueprint(tasks.blueprint)
        app.register_blueprint(register.blueprint)

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
    sql_users = """
    INSERT INTO users (username, password) VALUES (:username, :password);
    """
    sql_tasks = """
    INSERT INTO tasks (title, status, creator_id, created_at, priority) VALUES
    ('Task 1', 'open', 1, '2021-01-01', 'low'),
    ('Task 2', 'in_progress', 1, '2021-01-02', 'high'),
    ('Task 3', 'done', 1, '2021-01-03', 'very_high');
    """
    with db.engine.connect() as conn:
        conn.execute(text(sql_users),
                     {"username": "admin", "password": generate_password_hash("admin")})
        conn.execute(text(sql_tasks))
        conn.commit()
