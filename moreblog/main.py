import morepath
from morepath.security import BasicAuthIdentityPolicy
import sqlalchemy
from more.transaction import transaction_app
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register
from werkzeug.serving import run_simple

from . import model

Session = scoped_session(sessionmaker())
register(Session)

class App(morepath.App):
    pass

@App.identity_policy()
def get_identity_policy():
    return BasicAuthIdentityPolicy()

@App.verify_identity()
def verify_identity(identity):
    return user_has_password(identity.username, identity.password)

def user_has_password(name, pw):
    if model.users[name].password == pw:
        return True
    else:
        return False

def main():
    engine = sqlalchemy.create_engine('sqlite:///morepath_sqlalchemy.db')
    Session.configure(bind=engine)
    model.Base.metadata.create_all(engine)
    model.Base.metadata.bind = engine

    morepath.autosetup()
    run_simple('localhost', 8080, App(), use_reloader=True)
