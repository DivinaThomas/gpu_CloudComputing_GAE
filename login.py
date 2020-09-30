import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from main import MainPage
from gpu import Gpu
from add import Add
from update import Update
from feature import Feature
from search import Search
from compare import Compare

# Setting up an environment for jinja
JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class Login(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		# Retrieving user details
		user = users.get_current_user()

		# If the user is logged in
		if user : 
			self.redirect('/main')

		# If the user is not logged in
		else :
			self.redirect(users.create_login_url(self.request.uri))

# Specifying the routing table
app = webapp2.WSGIApplication ([
	('/main',MainPage),
	('/update',Update),
	('/feature',Feature),
	('/add',Add),
	('/',Login),
	('/search',Search),
	('/compare',Compare),
], debug=True)	
