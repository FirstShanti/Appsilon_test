import logging
import click
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from .index import MovieIndexView
from flask.cli import with_appcontext

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, indexview=MovieIndexView)
migrate = Migrate(app, db)

# from sqlalchemy.engine import Engine
# from sqlalchemy import event

#Only include this for SQLLite constraints
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     # Will force sqllite contraint foreign keys
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

@click.command(name='retrive_update_wiki_data')
@with_appcontext
def retrive_update_wiki_data():
    from .utils import create_update_data
    create_update_data(db)

app.cli.add_command(retrive_update_wiki_data)

from . import views
