import os #loads operating system
import webapp2 #loads the webapplication
import jinja2 #does it matter which you import 1st?

import re #what does this mean?
from string import letters #read up on this
from google.appengine.ext import db #interpreted as import database from google app engine

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinjia_env = jinjia2.Environment(loader = jinjia2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(self, template, **params): #why was this placed first?
    t = jinjia_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def write(self, *a, **kw): #why was order changed for write to render?
        self.response.out.write(*a, **kw)

class MainPage(Handler):
    def get(self):
        self.render("Rot13.html")

class EncryptHandler(Handler)
    def get(self):
        self.render("Rot13.html")

def post(self):
    rottext = self.request.get("text")
    rottext = encrypt(rottext)
    self.render("Rot13.html", rottext = rottext)

app = webapp2.WSGIApplication([('/', MainPage),('/rot13', EncryptHandler)], debug=True)
