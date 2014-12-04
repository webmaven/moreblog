from .main import App, Session
from .model import Root, Collection, Post

@App.html(model=Root)
def show_posts(self, request):
    return '''\
<html>
<body>
<h1>MoreBlog</h1>
<div id="content">
</div>
<div id="footer">
<form action="/posts" method="POST">
title: <input type="text" name="title"><br>
content: <input type="text" name="content"><br>
<input type="submit" value="Add!"><br>
</form>
</div>
</body>
</html>
'''

@App.json(model=Post)
def post_default(self,request):
    return {'id': self.id,
            'title': self.title,
            'content': self.content,
            'link': request.link(self)
            }

@App.json(model=Collection, request_method="GET")
def posts_default(self,request):
    session = Session()
    return {'posts': [post.id for post in session.query(Post)]}


@App.html(model=Collection, request_method='POST')
def collection_add_submit(self, request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    post = self.add(title=title, content=content)
    return "<p>Awesome %s</p>" % post.id
