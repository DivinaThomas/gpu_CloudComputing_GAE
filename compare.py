import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from gpu import Gpu

# Setting up an environment for jinja
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class Compare(webapp2.RequestHandler) :
	def get(self) :
		self.response.headers['Content-Type'] = 'text/html'
		result = Gpu.query().fetch();
		logout = users.create_logout_url('/')
		error_message = ''

		# generate a map that contains everything that we need to pass to the template
		template_values = {
			'logout' : logout,
			'result' : result,
			'error_message' : error_message 		
		}

		# asking jinja to render the template files with the template values
		template = JINJA_ENVIRONMENT.get_template('compare.html')
		self.response.write(template.render(template_values))
	
	def post(self) :
		self.response.headers['Content-Type'] = 'text/html'

		# If the user clicks on the Compare button
		if self.request.get('Button') == 'Compare' :
			logout = users.create_logout_url('/')
			result = Gpu.query().fetch();
			list_of_devices_checked = []

			# Counter to ensure the user compares at least 2 GPUs
			counter = 0

			# Storing the values selected by the user 
			for x in result :
				name = "checkbox_"+x.key.id()
				x_value = self.request.get(name)
				if x_value :
					counter = counter + 1
					myuser_key = ndb.Key('Gpu',x.key.id())
					gpu = myuser_key.get()
					list_of_devices_checked.append(gpu)
			
			# If the user has selected at least 2 GPUs to be compared
			if counter > 1 :

				# generate a map that contains everything that we need to pass to the template
				template_values = {
							'logout' : logout,
							'list_of_devices_checked' : list_of_devices_checked	
						}

				# asking jinja to render the template files with the template values
				template = JINJA_ENVIRONMENT.get_template('display_compare.html')
				self.response.write(template.render(template_values))
			
			# If the user has not selected at least 2 GPUs to be compared		
			else :
				error_message = 'Please select atleast two gpu devices'
				result = Gpu.query().fetch();
				logout = users.create_logout_url('/')

				# generate a map that contains everything that we need to pass to the template
				template_values = {
					'logout' : logout,
					'result' : result,
					'error_message' : error_message,		
				}

				# asking jinja to render the template files with the template values
				template = JINJA_ENVIRONMENT.get_template('compare.html')
				self.response.write(template.render(template_values))

		# If the user clicks on the Cancel button
		elif self.request.get('Button') == 'Cancel' :
			self.redirect('/main')
			
