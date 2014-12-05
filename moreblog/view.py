from .main import App, redirect
from .model import Root, Collection, Post


@App.html(model=Root)
def show_posts(self, request):
    return '''\
<!DOCTYPE html>
<html>
<head>
<title>Moreblog</title>
 <script src="https://code.jquery.com/jquery-2.1.1.min.js" type="text/javascript"></script>
</head>
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

<script type="text/javascript">
posts = $.getJSON('/posts', function( data ) {
  var items = [];
  $.each( data.posts, function(key, val ) {
    items.push( "<div class='post' id='" + val.id + "'>"\
    + "<h2>" + val.title + "</h2>" \
    + "<p>" + val.content + "</p>" \
    + "</div>" );
  });

  $( "<div/>", {
    "class": "posts",
    html: items.join( "" )
  }).appendTo( "#content" );
});</script>

</body>
</html>
'''

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
