from .main import App, Session
from .model import Root, Collection, Post

@App.path(model=Root, path='/')
def get_root():
    return Root()

@App.path(model=Post, path='posts/{id}',
          converters={'id': int})
def get_post(id):
    session = Session()
    post = session.query(Post).filter(Post.id == id).first()
    return post

@App.path(model=Collection, path='posts')
def get_posts():
    return Collection()
