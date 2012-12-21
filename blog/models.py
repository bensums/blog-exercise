from google.appengine.ext import db

class BlogPost(db.Model):
    author = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
