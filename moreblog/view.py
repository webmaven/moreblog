from .main import App, Session
from .model import Post, Root

@App.html(model=Root)
def show_posts(self, request):
    return '''\
<html>
<body>
<form action="/add_submit" method="POST">
title: <input type="text" name="title"><br>
content: <input type="text" name="content"><br>
<input type="submit" value="Add!"><br>
</form>
</body>
</html>
'''
