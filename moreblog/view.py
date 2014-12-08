import os

from .main import App, redirect
from .model import Root, Collection, Post
import bowerstatic

bower = bowerstatic.Bower()


components = bower.components(
    'app', os.path.join(os.path.dirname(__file__), 'bower_components'))


#local = bower.local_components('local', components)


#local.component(os.path.join(os.path.dirname(__file__), 'jquery'),
                #version=None)


@App.static_components()
def get_static_components():
    #return local
    return components

@App.chameleon(model=Root)
def show_posts(self, request):
    request.include('jquery')
    request.include('bootstrap')
    return {
         'template': 'base.pt'
     }

@App.json(model=Post, request_method="GET")
def post_default(self,request):
    return {"id": self.id}

@App.json(model=Collection, request_method="GET")
def posts_default(self,request):
    return {'posts': self.get_posts() }


@App.html(model=Collection, request_method='POST')
def collection_add_submit(self, request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    self.add(title=title, content=content)
    return redirect('/')
