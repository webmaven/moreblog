from .main import App, redirect
from .model import Root, Collection, Post


@App.chameleon(model=Root)
def show_posts(self, request):
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
    post = self.add(title=title, content=content)
    return redirect('/')
