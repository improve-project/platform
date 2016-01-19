# coding=utf-8
__author__ = 'bjorne'
"""An module for analysis on data from Evalans SensiStep. 

Calculates the error between the peakvalues in an exerciseresult and the targetvalue. 
It produces a result for the chosen exerciseresult and another result with mean errors of several other exerciseresult. """

from AnalysisPackage import analysismodule, moduleUtilities
import time
import numpy as np
import sys
import json
from flask import jsonify
import logging

class peakerror_analysis(analysismodule.AnalysisModule):


	def analyse(self, username, configParams, dbHandler, logger):
		"""
		Calculates the error between the peak loadings and the target loading for the chosen session.

		The module then calculates the mean error and compare it to the mean error of all other available sessions.
		Args: 
			username (String): The username
			configParams (String): JSON string on the form:
				{
					"max_number_of_old_results": [5],
					"exerciseResultID": ["something"],
					"rehabilitationSetID": ["somethingelse"]}
				}
			dbHandler (DatabaseHandler): The databasehandler.
			logger (logger): The logging class.
		Returns:
			{
				"status": "Ready",
				"results": 
				[
					{
						"name": "currentErrors",
						"type": "plot",
						"data": [
							3.1,
							-8.2,
							0.6
						],
						"priority": 1,
						"legend": "currentErrors",
						"subtype": "lines",
						"plotID": "1"

					},
					{
						"name": "currentMeanError",
						"type": "plot",
						"data": 5.6,
						"priority": 1,
						"legend": "currentMeanError",
						"subtype": "lines",
						"plotID": "1"

					},
					{
						"name": "oldErrors",
						"type": "plot",
						"data": [
							3.6,
							-9.2,
							4.4
						],
						"priority": 1,
						"legend": "oldErrors",
						"subtype": "lines",
						"plotID": "1"
					},
					{
						"name": "oldMeanError",						
						"type": "plot",
						"data": 2.6,
						"priority": 1,
						"legend": "oldMeanError",
						"subtype": "lines",
						"plotID": "1"
					}
				]
			}
		"""

		logger.info("Starting analysis...")

		#Gather data
		currentExerciseResultID = configParams["exerciseResultID"][0]
		rehabilitationSetID = configParams["rehabilitationSetID"][0]

		oldDatasets = []

		logger.info("username: " + username)
		logger.info("currentExerciseResultID: " + currentExerciseResultID)
		logger.info("rehabilitationSetID: " + rehabilitationSetID)

		newExerciseResult = moduleUtilities.gather_exerciseresult(username, dbHandler, logger, currentExerciseResultID) #Maybe need to load?
		logger.debug("newExerciseResult: " + str(newExerciseResult))

		currentErrors = self._get_peak_errors_from_exercise_result(newExerciseResult, logger)
		currentMeanError = np.mean(currentErrors)

		rehabilitationSet = moduleUtilities.gather_rehabilitationset(username, dbHandler, logger, rehabilitationSetID)
		logger.debug("RehabilitationSet: " + str(rehabilitationSet))

		exerciseResultIDs = rehabilitationSet.get("exerciseResultIDs")
		exerciseResultIDs = exerciseResultIDs.split(";")
		logger.debug("exerciseResultIDs: " + str(exerciseResultIDs)) 

		numberOfOldResults = 0
		try: 
			maxNumberOfOldResults = int(configParams[moduleUtilities.MAX_NUMBER_OF_OLD_RESULTS["name"]][0])
		except Exception as e:
			logger.error(str(e))
			maxNumberOfOldResults = int(moduleUtilities.MAX_NUMBER_OF_OLD_RESULTS["default"][0])

		logger.info("maxNumberOfOldResults: " + str(maxNumberOfOldResults))

		oldExerciseResults = []
		for exerciseResultID in exerciseResultIDs:
			logger.debug("exerciseResultID: " + str(exerciseResultID))
			if (exerciseResultID == currentExerciseResultID): #Dont use same exerciseResult again
				continue
			elif (numberOfOldResults >= maxNumberOfOldResults):
				break
			else:
				oldExerciseResult = moduleUtilities.gather_exerciseresult(username, dbHandler, logger, exerciseResultID)

				if (json.loads(oldExerciseResult.get("values")).get("peaks")) is None:
					continue

				numberOfOldResults = numberOfOldResults + 1
				logger.debug("numberOfOldResults = " + str(numberOfOldResults))
				oldExerciseResults.append(oldExerciseResult)

		oldErrorMatrix = []
		for result in oldExerciseResults:
			oldErrorMatrix.append(self._get_peak_errors_from_exercise_result(result, logger))

		#transpose the oldErrorMatrix and calculate mean error for each peak
		oldErrorsTransposed = zip(*oldErrorMatrix)
		oldErrors = map(np.mean, oldErrorsTransposed)
		oldMeanError = np.mean(oldErrors)
		result = self._construct_result_object(currentErrors, currentMeanError, oldErrors, oldMeanError)	
		return result

		
	def _construct_result_object(self, currentErrors, currentMeanError, oldErrors, oldMeanError):
		currentErrors = map(lambda x,y: [x,y], list(xrange(len(currentErrors))),currentErrors)
		currentMeanError = [[0, currentMeanError], [len(currentErrors)-1, currentMeanError]]
		oldErrors = map(lambda x,y: [x,y], list(xrange(len(oldErrors))),oldErrors)
		oldMeanError = [[0, oldMeanError], [len(oldErrors)-1, oldMeanError]]

		plotData = []
		plotData.append(moduleUtilities.construct_single_plotdata(data=currentErrors, legend="currentErrors", subtype="lines"))
		plotData.append(moduleUtilities.construct_single_plotdata(data=currentMeanError, legend="currentMeanError", subtype="lines"))
		plotData.append(moduleUtilities.construct_single_plotdata(data=oldErrors, legend="oldErrors", subtype="lines"))
		plotData.append(moduleUtilities.construct_single_plotdata(data=oldMeanError, legend="oldMeanError", subtype="lines"))
		plotResult = [moduleUtilities.construct_plotresult(title="Peak errors", plotDatas=plotData, priority=1, x_label="Time", y_label="Weight (kg)")]

		return moduleUtilities.construct_results_object(plotResult)


	def _get_peaks_from_exercise_result(self, exerciseResult, logger):
		"""
		Extracts the peaks from an exerciseResult.

		Args:
			exerciseResult (String): A JSON-formatted string with an exerciseResult.
			logger (logger): The logging class.
		Returns:
			peaks ([float]): An array with all the peaks from the exerciseResult.
		"""
		values = json.loads(exerciseResult.get("values"))
		peakData = values.get("peaks")
		logger.debug("peakData: " + str(peakData))
		peaks = []
		for peak in peakData:
			peaks.append(float(peak[1]))	#removes timestamp
		logger.debug("peaks: " + str(peaks))
		return peaks



	def _get_peak_errors_from_exercise_result(self, exerciseResult, logger):
		"""
		Extracts the peakerrors from an exerciseResult.

		Args:
			exerciseResult (String): A JSON-formatted string with an exerciseResult.
			logger (logger): The logging class.
		Returns:
			error ([float]): An array with all the errors from the peaks in the exerciseResult.
		"""
		logger.debug("in _get_peak_errors_from_exercise_result...")

		settings = json.loads(exerciseResult.get("settings"))
		targetValue = float(settings["target"])
		peaks = self._get_peaks_from_exercise_result(exerciseResult, logger)
		errors = []
		for peak in peaks:
			errors.append(peak-targetValue)
		logger.debug("Errors: " + str(errors))
		return errors


	def necessary_config_params(self):
		return [moduleUtilities.MAX_NUMBER_OF_OLD_RESULTS, moduleUtilities.EXERCISE_RESULT_ID, moduleUtilities.REHABILITATIONSET_ID]

	def description(self):
		description = "An module for analysis on data from Evalans SensiStep. Calculates the error between the peakvalues in an exerciseresult and the targetvalue. It produces a result for the chosen exerciseresult and another result with mean errors of several other exerciseresult. "
		return description

	def permission_level(self):
		return 6

	def __init__(self):
		return

