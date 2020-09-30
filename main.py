import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from gpu import Gpu
import os

# Setting up an environment for jinja
JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class MainPage(webapp2.RequestHandler):
	def get(self):
		# Retrieving information to display when the main page is loaded
		self.response.headers['Content-Type'] = 'text/html'
		result = Gpu.query().fetch();
		logout = users.create_logout_url('/')
		
		# generate a map that contains everything that we need to pass to the template
		template_values = {
			'result' : result,
			'logout' : logout
		}

		# asking jinja to render the template files with the template values
		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))
	
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		# If the user clicks on the delete button
		if self.request.get('button') == 'Delete' :
			check = self.request.get('hidden_id')
			myuser_key = ndb.Key('Gpu', check)
			myuser_key.delete()

			result = Gpu.query().fetch();
			logout = users.create_logout_url('/')

			# generate a map that contains everything that we need to pass to the template
			template_values = {
					'result' : result,
					'logout' : logout
			}

			# asking jinja to render the template files with the template values
			template = JINJA_ENVIRONMENT.get_template('main.html')
			self.response.write(template.render(template_values))
		
		else :
			result = Gpu.query().fetch();
			logout = users.create_logout_url('/')

			# generate a map that contains everything that we need to pass to the template
			template_values = {
					'result' : result,
					'logout' : logout
			}

			# asking jinja to render the template files with the template values
			template = JINJA_ENVIRONMENT.get_template('main.html')
			self.response.write(template.render(template_values))
		