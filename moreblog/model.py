from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    )
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Root(object):
    pass


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
