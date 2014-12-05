import morepath
from more.static import StaticApp
from morepath import redirect
import sqlalchemy
from more.transaction import transaction_app
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register
from werkzeug.serving import run_simple

from . import model

Session = scoped_session(sessionmaker())
register(Session)

class App(StaticApp):
    pass


def main():
    engine = sqlalchemy.create_engine('sqlite:///morepath_sqlalchemy.db')
    Session.configure(bind=engine)
    model.Base.metadata.create_all(engine)
    model.Base.metadata.bind = engine

    morepath.autosetup()
    run_simple('localhost', 8080, App(), use_reloader=True)
