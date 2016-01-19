__author__ = 'bjorne'
"""An example of an analysismodule"""
from AnalysisPackage import analysismodule, moduleUtilities
import time


class analysismodule_A(analysismodule.AnalysisModule):
	def count_letters(self, word):
		return len(word) - word.count(' ')

	def analyse(self, username, settings, dbHandler):
		print "I'm implemented! Starting analysis..."
		time.sleep(2)
		data = dbHandler.get_exerciseresult(username, settings["configParams"]["exerciseResult"])
		
		letters = len(data) - data.count(" ")
		return {"status": "\nAnalysis done!", "result": {"message": data, "number of letters": letters}}

	def necessary_config_params(self):
		return [moduleUtilities.MIN_AGE,
				moduleUtilities.MAX_AGE,
				moduleUtilities.EXERCISE_RESULT,
				moduleUtilities.EXERCISE]

	def description(self):
		return "I count the number of letters in the string returned from the database_handlers get_exerciseresult-method. I still need config parameters though, but just in a testing (and annoying) purpose."

	def permission_level(self):
		return 5

	def required_parameters(self):
		return {}
		
	def __init__(self):
		return
