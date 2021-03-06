import os
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
    if 'db' not in g:
        # open a connection, save it to close when done
        DB_URL = os.environ.get('DATABASE_URL', None)
        if DB_URL:
            g.db = psycopg2.connect(DB_URL, sslmode='require')
        else:
            g.db = psycopg2.connect(
                f"dbname={current_app.config['DB_NAME']}" +
                f" user={current_app.config['DB_USER']}"
            )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close() # close the connection


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        cur = db.cursor()
        cur.execute(f.read())
        db.commit()
        cur.close()


def create_user(email, hash, role):
    db = get_db()
    cur = db.cursor()

    # commit the values in params to the database, update the database, and close it.
    cur.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", (email, hash, role))

    db.commit()
    cur.close()
    db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('create-user')
@with_appcontext
@click.option('--email', prompt='Email')
@click.option('--password', prompt='Password')
@click.option('--role', prompt='Role')
def create_user_command(email, password, role):
    """Create new User"""
    create_user(email, generate_password_hash(password), role)
    click.echo(f'Created new user. Email: {email} Password: {password} Role: {role}')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user_command)
