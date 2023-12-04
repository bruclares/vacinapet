from flask import g
import psycopg2
# from psycopg2.extras import RealDictCursor
# from db import get_db


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host="localhost",
            database="vacina_pet",
            user='postgres',
            password='postgres'
        )
        # g.cursor = g.db.cursor(cursor_factory=RealDictCursor)
    return g.db


def close_db(e=None):
    cursor = g.pop('cursor', None)
    db = g.pop('db', None)

    if cursor is not None:
        cursor.close()

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)