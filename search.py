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

class Search(webapp2.RequestHandler) :
	def get(self) :
		self.response.headers['Content-Type'] = 'text/html'
		logout = users.create_logout_url('/')

		# generate a map that contains everything that we need to pass to the template
		template_values = {
			'logout' : logout		
		}

		# asking jinja to render the template files with the template values
		template = JINJA_ENVIRONMENT.get_template('search.html')
		self.response.write(template.render(template_values))

	def post(self) :
		self.response.headers['Content-Type'] = 'text/html'

		# If the user clicks on the Search Button
		if self.request.get('button') == 'Search' :
			geometryShader = self.request.get('checkbox_geometryShader')
			tesselationShader = self.request.get('checkbox_tesselationShader')
			shaderInt16 = self.request.get('checkbox_shaderInt16')
			sparseBinding = self.request.get('checkbox_sparseBinding')
			textureCompressionETC2 =  self.request.get('checkbox_textureCompressionETC2')
			vertexPipelineStoresAndAtomics = self.request.get('checkbox_vertexPipelineStoresAndAtomics')	

			result_of_querying= Gpu.query()
			
			# Displaying features for user to select from
			if geometryShader :
				result_of_querying = result_of_querying.filter(Gpu.geometryShader == 'True')
			if tesselationShader :
				result_of_querying = result_of_querying.filter(Gpu.tesselationShader == 'True')
			if shaderInt16 :
				result_of_querying = result_of_querying.filter(Gpu.shaderInt16 == 'True')
			if sparseBinding :
				result_of_querying = result_of_querying.filter(Gpu.sparseBinding == 'True')
			if textureCompressionETC2 :
				result_of_querying = result_of_querying.filter(Gpu.textureCompressionETC2 == 'True')
			if vertexPipelineStoresAndAtomics :
				result_of_querying = result_of_querying.filter(Gpu.vertexPipelineStoresAndAtomics == 'True')
			
			# Retrieving available GPUs based on the requested features
			result_of_querying = result_of_querying.fetch()

			# If there exists at least one GPU with the requested features
			if result_of_querying :
				logout = users.create_logout_url('/')
				message = ''

				# generate a map that contains everything that we need to pass to the template
				template_values = {
					'result_of_querying' : result_of_querying,
					'logout' : logout,
					'message' : message
				}	

				# asking jinja to render the template files with the template values
				template = JINJA_ENVIRONMENT.get_template('display.html')
				self.response.write(template.render(template_values))
			
			# If there are no GPUs with the requested features
			else : 
				result_of_querying = ''
				message = 'Sorry no GPU exists that supports the checked features'
				logout = users.create_logout_url('/')

				# generate a map that contains everything that we need to pass to the template
				template_values = {
					'result_of_querying' : result_of_querying,
					'message' : message,
					'logout' : logout
				}	

				# asking jinja to render the template files with the template values
				template = JINJA_ENVIRONMENT.get_template('display.html')
				self.response.write(template.render(template_values))
				
		# If the user clicks on the Cancel Button
		elif self.request.get('button') == 'Cancel' :
			self.redirect('/main')
