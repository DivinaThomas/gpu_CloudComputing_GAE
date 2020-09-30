from google.appengine.ext import ndb

# Defining GPU properties
class Gpu(ndb.Model):
	geometryShader = ndb.StringProperty()
	tesselationShader = ndb.StringProperty()
	shaderInt16 = ndb.StringProperty()
	sparseBinding = ndb.StringProperty()
	textureCompressionETC2 = ndb.StringProperty()
	vertexPipelineStoresAndAtomics = ndb.StringProperty()


