"""tasks.py"""

import os
import sys

from invoke.tasks import task


@task
def debug(ctx):
    """Run the project in debug mode."""
    if sys.platform.startswith("win"):
        ctx.run("py protaskinate/index.py")
    else:
        ctx.run("python3 protaskinate/index.py")


@task
def create_schema(ctx):
    """Create the database schema."""
    ctx.run("flask create_schema")


@task
def populate_db(ctx):
    """Populate the database with sample data."""
    print("Populating database")
    ctx.run("flask populate_db")


@task
def generate_secret_key(ctx):
    """Create a secret key."""
    if os.path.exists(".secret_key.env"):
        print("File already exists - skipping generation")
    else:
        secret_key = os.urandom(12).hex()
        ctx.run("echo 'SECRET_KEY="+secret_key+"' > .secret_key.env")
        print("Secret key generated")

@task
def lint(ctx):
    """Run pylint on the project."""
    ctx.run("pylint protaskinate", warn=True)


@task
def unit_test(ctx):
    """Run unit tests"""
    ctx.run("pytest tests/unit")


@task
def coverage_report(ctx):
    """Run unit tests and create a coverage report"""
    ctx.run("pytest --cov-report xml --cov protaskinate tests/unit")
