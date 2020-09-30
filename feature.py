import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from main import MainPage
from gpu import Gpu

# Setting up an environment for jinja
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class Feature(webapp2.RequestHandler) :
	def post(self) :
		# Displaying features of a particular GPU
		self.response.headers['Content-Type'] = 'text/html'
		this_id = self.request.get('hidden_link')
		myuser_key = ndb.Key('Gpu', this_id)
		gpu = myuser_key.get()
		logout = users.create_logout_url('/')

		# generate a map that contains everything that we need to pass to the template
		template_values = {
			'gpu' : gpu,
			'logout' : logout
		}

		# asking jinja to render the template files with the template values
		template = JINJA_ENVIRONMENT.get_template('feature.html')
		self.response.write(template.render(template_values))

		# If the user clicks on the Cancel button
		if self.request.get('button') == 'Cancel' :
			self.redirect('/main')
	
