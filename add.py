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

class Add(webapp2.RequestHandler) :
	def get(self) :
		self.response.headers['Content-Type'] = 'text/html'
		logout = users.create_logout_url('/')
		error_message = ''

		# generate a map that contains everything that we need to pass to the template
		template_values = {
			'logout' : logout,
			'error_message' : error_message
		}

		# asking jinja to render the template files with the template values
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.write(template.render(template_values))

	def post(self) :
		self.response.headers['Content-Type'] = 'text/html'

		# If the user clicks on the Add button
		if self.request.get('button') == 'Add' :
			check = self.request.get('gpu_device')
			myuser_key = ndb.Key('Gpu',check)
			gpu = myuser_key.get()

			# Add the gpu if it doesn't already exists
			if gpu == None :
				gpu = Gpu(id=check)
				
				gpu.geometryShader = self.request.get('gpu_geometryShader')
				gpu.tesselationShader = self.request.get('gpu_tesselationShader')
				gpu.shaderInt16 = self.request.get('gpu_shaderInt16')
				gpu.sparseBinding = self.request.get('gpu_sparseBinding')
				gpu.textureCompressionETC2 =  self.request.get('gpu_textureCompressionETC2')
				gpu.vertexPipelineStoresAndAtomics = self.request.get('gpu_vertexPipelineStoresAndAtomics')
				gpu.put()

				self.redirect('/main')

			# If gpu exists
			else :
				logout = users.create_logout_url('/')
				error_message = 'A gpu with this name exists'

				# generate a map that contains everything that we need to pass to the template
				template_values = {
					'logout' : logout,
					'error_message' : error_message
				}

				# asking jinja to render the template files with the template values
				template = JINJA_ENVIRONMENT.get_template('add.html')
				self.response.write(template.render(template_values))

		# If the user clicks on the Cancel button
		elif self.request.get('button') == 'Cancel' :
			self.redirect('/main')
