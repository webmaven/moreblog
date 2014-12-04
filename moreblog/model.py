from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    )
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import register

Base = declarative_base()

Session = scoped_session(sessionmaker())
register(Session)

class Root(object):
    pass

class Collection(object):
    @classmethod
    def get_posts(cls):
        pass

    def add(self, title, content):
        session = Session()
        post = Post(title=title, content=content)
        session.add(post)
        session.flush()
        return post



class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    content = Column(Text)



class User(object):
     def __init__(self, username, fullname, email, password):
         self.username = username
         self.fullname = fullname
         self.email = email
         self.password = password

users = {}
def add_user(user):
     users[user.username] = user

admin = User('admin', 'Admin User', 'admin@example.com', 'admin')

add_user(admin)
