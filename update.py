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

class Update(webapp2.RequestHandler) :
	def get(self) :
		self.response.headers['Content-Type'] = 'text/html'
		gpu = ''
		logout = users.create_logout_url('/')

		# generate a map that contains everything that we need to pass to the template
		template_values = {
			'gpu' : gpu,
			'logout' : logout
		}

		# asking jinja to render the template files with the template values
		template = JINJA_ENVIRONMENT.get_template('update.html')
		self.response.write(template.render(template_values))

	def post(self) :
		self.response.headers['Content-Type'] = 'text/html'

		# If the user clicks on the Update button
		if self.request.get('button') == 'Update' :
			check= self.request.get('hidden_id')
			myuser_key = ndb.Key('Gpu',check)

			gpu = myuser_key.get()

			# updates the feature values changed by the user
			gpu.geometryShader = self.request.get('gpu_geometryShader')
			gpu.tesselationShader = self.request.get('gpu_tesselationShader')
			gpu.shaderInt16 = self.request.get('gpu_shaderInt16')
			gpu.sparseBinding = self.request.get('gpu_sparseBinding')
			gpu.textureCompressionETC2 = self.request.get('gpu_textureCompressionETC2')
			gpu.vertexPipelineStoresAndAtomics = self.request.get('gpu_vertexPipelineStoresAndAtomics')
			gpu.put()

			self.redirect('/main')

		# If the user clicks on the Cancel button
		elif self.request.get('button') == 'Cancel' :
			self.redirect('/main')

		# If the user clicks on the Edit button
		elif self.request.get('button') == 'Edit' :
			# Taking the user to the edit page while passing the current feature values of the GPU
			check = self.request.get('hidden_value')
			myuser_key = ndb.Key('Gpu',check)
			logout = users.create_logout_url('/')
			
			gpu = myuser_key.get()

			# generate a map that contains everything that we need to pass to the template
			template_values = {
				'gpu' : gpu,
				'logout' : logout
			}

			# asking jinja to render the template files with the template values
			template = JINJA_ENVIRONMENT.get_template('update.html')
			self.response.write(template.render(template_values))
			