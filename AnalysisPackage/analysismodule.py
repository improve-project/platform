__author__ = 'bjorne'

"""This is an abstract class for analysis modules. 

All subclasses must implement the analyse method, the description method, the permission_level method and the necessary_config_params method method.
"""
#What could be a better class and filename? moduleinterface?
#Should we use abc module??

class AnalysisModule(object):

	def analyse(self, username, configParams, dbHandler):
		"""This is where the analysis is suppose to happen. 

		This method is also responsible for extracting the necessary data from the 
		database but not for saving the data.

		Args:
			username (String): 
			configParams (String): JSON-formatted string on the form desribed in the analysishandler.
			dbHandler (database_handler): The place to extract the data from.
		Returns:
			result (String): JSON-formatted string On the form
			{"status": status (String),
			"result": result (String)}"""
		raise NotImplementedError(self.not_implemented_msg("analyse"))

	def necessary_config_params(self):
		"""Here the module defines which config parameters that is needed."""
		raise NotImplementedError(self.not_implemented_msg("necessary_config_params"))
		
	def description(self):
		"""Returns the description of the module"""
		raise NotImplementedError(self.not_implemented_msg("description"))

	def permission_level(self):
		"""Returns the permission level of the module"""
		raise NotImplementedError(self.not_implemented_msg("permission_level"))

	def not_implemented_msg(self, method):		
		return "Oh no! You forgot to implement the " + method + " method. Please implement this method."
