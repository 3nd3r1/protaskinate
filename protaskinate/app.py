"""protaskinate/app.py"""

import logging
import os

import click
from flask import Flask
from flask.cli import load_dotenv, with_appcontext
from sqlalchemy import text
from werkzeug.security import generate_password_hash

from protaskinate.routes import dashboard, login, logout, project, register
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
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
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
        app.register_blueprint(register.blueprint)
        app.register_blueprint(project.blueprint)

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
    INSERT INTO users (username, password) VALUES
    ('admin', :admin_password),
    ('user', :user_password);
    """
    sql_projects = """
    INSERT INTO projects (name, creator_id, created_at, updated_at, description) VALUES
    ('Project 1', 1, '2021-01-01', '2021-01-03', 'Project 1 description'),
    ('Project 2', 1, '2021-01-02', '2021-01-03', 'Project 2 description'),
    ('Project 3', 1, '2021-01-03', '2021-01-03', 'Project 3 description');
    """
    sql_tasks = """
    INSERT INTO tasks (title, status, creator_id, created_at, updated_at, priority, project_id, description) VALUES
    ('Project 1 Task 1', 'open', 1, '2021-01-01', '2021-01-01', 'low', 1, 'Task 1 description'),
    ('Project 1 Task 2', 'in_progress', 1, '2021-01-02', '2021-01-02', 'high', 1, 'Task 2 description'),
    ('Project 1 Task 3', 'done', 2, '2021-01-03', '2021-01-03', 'very_high', 1, 'Task 3 description'),

    ('Project 2 Task 1', 'open', 1, '2021-01-01', '2021-01-01', 'low', 2, 'Task 1 description'),
    ('Project 2 Task 2', 'in_progress', 1, '2021-01-02', '2021-01-02', 'high', 2, 'Task 2 description'),
    ('Project 2 Task 3', 'done', 2, '2021-01-03', '2021-01-03', 'very_high', 2, 'Task 3 description'),

    ('Project 3 Task 1', 'open', 1, '2021-01-01', '2021-01-01', 'low', 3, 'Task 1 description'),
    ('Project 3 Task 2', 'in_progress', 1, '2021-01-02', '2021-01-02', 'high', 3, 'Task 2 description'),
    ('Project 3 Task 3', 'done', 2, '2021-01-03', '2021-01-03', 'very_high', 3, 'Task 3 description');
    """
    sql_comments = """
    INSERT INTO comments (task_id, creator_id, created_at, content) VALUES
    (1, 1, '2021-01-01', 'Comment 1'),
    (1, 2, '2021-01-02', 'Comment 2'),
    (1, 1, '2021-01-03', 'Comment 4'),
    (2, 1, '2021-01-04', 'Comment 3');
    """
    sql_user_projects = """
    INSERT INTO user_projects (user_id, project_id, role) VALUES
    (2, 2, 'reader'),
    (2, 3, 'writer');
    """


    with db.engine.connect() as conn:
        conn.execute(text(sql_users), {
            "admin_password": generate_password_hash("admin"),
            "user_password": generate_password_hash("user")})
        conn.execute(text(sql_projects))
        conn.execute(text(sql_tasks))
        conn.execute(text(sql_comments))
        conn.execute(text(sql_user_projects))
        conn.commit()
