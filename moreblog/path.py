from .main import App, Session
from .model import Post, Root
#from .collection import DocumentCollection

@App.path(model=Root, path='/')
def get_root():
    return Root()

@App.path(model=Post, path='posts/{id}',
          converters={'id': int})

def get_post(id):
    session = Session()
    return session.query(Post).filter(Post.id == id).first()
