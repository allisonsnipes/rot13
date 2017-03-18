import os #loads operating system
import webapp2 #loads the webapplication
import jinja2 #does it matter which you import 1st?

import re #used for upload to the re.compiler
from string import letters #read up on this
from google.appengine.ext import db #interpreted as import database from google app engine

template_dir = os.path.join(os.path.dirname(__file__), 'templates') #creates a directory within our folder called templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True) #loads jinja to our template folder, autoescape function

def render_str(template, **params): #why was this placed first? why was self deleted?
    t = jinja_env.get_template(template) #initializes t as a variable to get whatever we place in the template
    return t.render(params) #returns to us whatever parameters were saved on our template

class BaseHandler(webapp2.RequestHandler): #creating a BaseHandler that initializes the RequestHandler function
    def render(self, template, **kw): #defines the function render but need help understanding self, template, **kw part
        self.response.out.write(render_str(template, **kw)) #understanding?

    def write(self, *a, **kw): #why was order changed for write and render?
        self.response.out.write(*a, **kw)

class Rot13(BaseHandler): #creating a new class Rot13 that inherits the BaseHandler properties
    def get(self): #difference between get & post? Stackoverflow/googling not helpful
        self.render('Rot13.html') #this is the Rot13 form here we created a new class for the inherited Handler

    def post(self):
        rot13 = '' # are we initialing the rot13 variable as a string?
        text = self.request.get('text') #intializing text varaible to hold what user types in as text string
        if text:
            rot13 = text.encode('rot13') #if text then encode rot13 string
        self.render('Rot13.html', text = rot13) #renders the Rot13 form with encoded text

class SignupPage(BaseHandler): #initialing new class called SignupPage that inherits the BaseHandler properties
    def get(self):
        self.render("signupform.html") #renders the SignupPage form

    def post(self):
        have_error = False #initialing have_error variable as false
        username = self.request.get('username') #intializing username variable as what user types in as the username
        password = self.request.get('password') #intializing password variable as what user types in
        verify = self.request.get('verify') #intializing verify variable as what user types in
        email = self.request.get('email') #intializing email variable as what user types in

        params = dict(username = username, email = email) #initialing params (parameters?) dictionary as username and email variables
        #for this section i think below should be listed first for the re.compilers
        #as we are defining what is a valid email, username, and password seems backwards

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True #sets new variable status to true

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
            self.redirect('/')

app = webapp2.WSGIApplication([('/', SignupPage),
                                ('/rot13', Rot13),

                                ('/welcomepage', Welcome)], debug=True)
