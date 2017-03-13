import os #loads operating system
import webapp2 #loads the webapplication
import jinja2 #does it matter which you import 1st?

import re #what does this mean?
from string import letters #read up on this
from google.appengine.ext import db #interpreted as import database from google app engine

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinjia_env = jinjia2.Environment(loader = jinjia2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params): #why was this placed first? why was self deleted?
    t = jinjia_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw)) #come back to this

    def write(self, *a, **kw): #why was order changed for write and render?
        self.response.out.write(*a, **kw)

class Rot13(BaseHandler):
    def get(self): #difference between get & post
        self.render('Rot13.html') #this is the Rot13 form here we created a new class for the inherited Handler

    def post(self):
        rot13 = '' # are we saying the Rot13 is a string?
        text = self.request.get('text') #get the text the user put in
        if text:
            rot13 = text.encode('rot13') #if statement encode what user puts in
        self.render('Rot13.html', text = rot13) #renders the encoded text on the form

class SignupPage(BaseHandler):
    def get(self):
        self.render("signupform.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username, email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That's not a valid password."
            have_error = True

        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."

        if have_error:
            self.render('signupform.html', **params)
        else:
            self.redirect('/hw1/welcomepage' + username)

#why can't I place the functions for the username, passwords, emails here it
#makes more logical sense to be here
#why isn't it indented all the way?

USER_RE = re.compile(r"^[a-zA-Z0_-]{3,20}$") #I understand now that we are using what we imported above
def valid_username(username):
    return username and USER_RE.match(username) #is this verifying that the username and the characters match?

PASS_RE = re.compile(r"^.{3,20}$")
def valid_username(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')#why only one quotation mark?
def valid_email(email): #we are defining a valid email function
    return not email or EMAIL_RE.match(email) # do not return either

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/hw1/signup')
            
app = webapp2.WSGIApplication([('/hw1/rot13', Rot13),
                                ('/hw1/signup', Signup),
                                ('/hw1/welcomepage', Welcome)], debug=True)
