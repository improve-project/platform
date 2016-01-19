#!/usr/bin/env python
# coding=utf-8

"""
Contains stuff that could help a programmer to write an analysismodule.

It contains example of configuration parameters with correct format.


"""
import json
import numpy as np
import logging

def moving_average(a, n=3):
	"""
	An implementation of a moving average filter (MA-filter).

	Filters a with windowlength n.
	Args:
		a ([float]): The list to filter.
		n (float): The windowlength. Default=3.
	Returns:
		([float]): A filtered version of a.
	"""
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

def sort_all_matrix_cols_by_col(matrix, colIndex):
	"""
	First sorts one column of the matrix and then sorts all other columns in the same order.

	Args:
		matrix ([[Number]]): The matrix to sort.
		colIndex (Number): The index of the column to sort, and then sort all other columns in the same way.
	Returns:
		[[Number]]: A sorted matrix.
	"""
	matrix = np.array(matrix)
	return matrix[matrix[:,colIndex].argsort()]

def genderFloat(gender):
	"""
	Transforms gender into a float. 

	Male -> 0
	Female -> 1
	Neither -> 2

	Args: 
		gender (String): The gender.
	Returns:
		(float): Number between 0 and 2.
	"""
	if gender == "Male":
		return 0
	elif gender == "Female":
		return 1
	else:
		return 2

def construct_results_object(results=[{}], model={}):
	"""
	Constructs a result object that is understandable to the analysisHandler.

	This also follows the format that is presented as a suggestion in the documentation.
	Args:
		results [{String}]: A list with JSON-formatted strings with results, preferably created with suitable help methods in this module.
		model {String}: A JSON-formatted string with a model.
	Returns:
		{String}: A JSON-formatted string that has a format that could be understood by the analysisHandler.
	"""
	return {"results": 
		{
			"results": results,
			"model": model
		},
		"status": "Ready"
	}

def construct_plotresult(title, plotDatas, priority, x_label, y_label):
	"""
	Constructs a result object for plots that follows the format presented as a suggestion in the documentation.

	Often the result from this method is later used in construct_results_object.
	Args:
		title (String): The name of this result.
		plotDatas (String): JSON-formatted string with data of this result. Preferably constructed by construct_single_plotdata.
		priority (Number): A suggestion for how important this result is.
		legend (String): A suggestion for a legend to use in the plot of this result.
		subtype (String): A suggestion for how to plot this result.
		plotID (String): A suggestion for an ID of this plot, to make it possible to plot several datasets in the same plot.
	Returns:
		{String}: A JSON-formatted string that has the format presented as a suggestion in the documentation. 
	"""
	return 	{
				"title": title,
				"type": "plot",
				"data": plotDatas, 
				"priority": priority,
				"x_label": x_label,
				"y_label": y_label
			}

def construct_single_plotdata(data, legend, subtype):
	"""
	Constructs a result object for plots that follows the format presented as a suggestion in the documentation.

	Often the result from this method is later used in construct_results_object.
	Args:
		data ([Number]): An array with the data to be plotted.
		legend (String): A suggestion for a legend to use in the plot of this result.
		subtype (String): A suggestion for how to plot this result.
	Returns:
		{String}: A JSON-formatted string that has the format presented as a suggestion in the documentation. 
	"""
	return 	{
		"data": data,
		"legend": legend,
		"subtype": subtype
	}
	
			
def construct_textresult(name, data, priority, ):
	"""
	Constructs a result object for texts that follows the format presented as a suggestion in the documentation.

	Often the result from this method is later used in construct_results_object.
	Args:
		name (String): The name of this result.
		data (String): A string with the result.
		priority (Number): A suggestion for how important this result is.
	Returns:
		{String}: A JSON-formatted string that has the format presented as a suggestion in the documentation. 
	"""

	return	{
				"name": name,
				"type": "text",
				"data":  data,
				"priority": priority
			}
			

def construct_htmlresult(name, data, priority, subtype):
	"""
	Constructs a result object for html that follows the format presented as a suggestion in the documentation.

	Often the result from this method is later used in construct_results_object.
	Args:
		name (String): The name of this result.
		data (String): A string with html-code containing the result.
		priority (Number): A suggestion for how important this result is.
		subtype (String): A suggestion for a subtype of this html. That is preferably the container to put the htmlcode in, e.g. <div> or <body>.
	Returns:
		{String}: A JSON-formatted string that has the format presented as a suggestion in the documentation. 
	"""

	return	{
				"name": name,
				"type": "text",
				"data":  data,
				"priority": priority,
				"subtype": subtype
			}


def gather_exerciseresults_with_patient_informations_from_rehabilitationsets(username, dbHandler, logger, rehabilitationSetIDs=[]):
	"""
		Gathers all exercise results from rehabilitationSetIDs that are available for the user.

		If no value is given for rehabilitationSetIDs then the method will look through ALL available rehabilitationSets. 
		The patientInformation corresponding to each rehabilitationset will also be included in the result.

		Please note that if the format in the database changes then the format of the return will differ from whats presented below.

		Args:
			username (String): The userName
			dbHandler (database_handler): The databasehandler
			logger (logger): The logger
			rehabilitationSetIDs ([String]): An array with IDs for all rehabilitationSets the method should try to gather results from.
		Returns:
			exerciseResults ([String]): An array with JSON-formatted strings on the form:
				{u'dataIDs': u'dataset_1437662219.401022', 
				u'exerciseResultID': u'evalan_exerciseresultid_1437662219.430169', 
				u'settings': u'{"targetlower": "30.0", "targetupper": "50.0", "difficultyLevel": "5", "deviceID": "00:16:A4:08:BC:3C", "target": "45.0"}', 
				u'started': 1437662166, 
				'patientInformation': {u'upperBodyDominantSide': u'Right', 
									u'allowedOrganizations': u'Evalan_1', 
									u'gender': u'Male', 
									u'bodyHeight': 181.0, 
									u'patientInformationID': 
									u'bjorne_information', 
									u'birthYear': 1988, 
									u'lowerbodyDominantSide': 
									u'Right', u'bodyWeight': 75.0}, 
				u'exerciseID': u'Evalan_test_exercise', 
				u'allowedOrganizations': u'Evalan_1', 
				u'ended': 1437662213, 
				u'progress': u'', 
				u'values': u'{"peakAverage": "44.71875", 
							"target": "0", "peaksOver": "3.0", 
							"peaks": [[1437662168680, 46], [1437662169920, 45], [1437662202400, 48]], 
							"peakMax": "55.0", 
							"peakMin": "30.0", 
							"loadAverage": "12.718905", 
							"peaksUnder": "0.0", 
							"activeDuration": "0.0", 
							"peakCount": "32.0"}'}
	"""
	
	exerciseResults = []
	if (rehabilitationSetIDs is None) or (len(rehabilitationSetIDs) == 0):
		dbMsg = json.loads(dbHandler.list_rehabilitationsets(username))
		#logger.debug(dbMsg)
		if dbMsg.get("status_code") == "200":
			rehabilitationSets = dbMsg.get("RehabilitationSets")
		else:
			logger.debug(dbMsg)

	else:
		rehabilitationSets = []
		for ID in rehabilitationSetIDs:
			dbMsg = json.loads(dbHandler.get_rehabilitationset(username, ID))
			#logger.debug(dbMsg)
			if dbMsg.get("status_code") == "200":
				rehabilitationSets.append(dbMsg.get("RehabilitationSet")[0])
			else:
				logger.debug("for ID: " + str(ID) + " - " + str(dbMsg))

	logger.debug("rehabilitationSets: " + str(rehabilitationSets))
	exerciseResultIDs = []
	for rehabSet in rehabilitationSets:
		IDs = rehabSet.get("exerciseResultIDs")
		patientInformationID = rehabSet.get("patientInformationID")
		patientInformation = json.loads(dbHandler.get_patientinformation(username, patientInformationID))
		#logger.debug("patientInformation: " + str(patientInformation))
		if (patientInformation.get("status_code") == "200"):
			patientInformation = patientInformation.get("PatientInformation")[0]
		else:
			logger.debug(dbMsg)
			continue
		if IDs is None:
			continue
		else:
			exerciseResultIDs = IDs.split(";")
			for ID in exerciseResultIDs:
				dbMsg = json.loads(dbHandler.get_exerciseresult(username, ID))
				if dbMsg.get("status_code") == "200":
					exerciseResult = dbMsg.get("ExerciseResult")[0]
					exerciseResult["patientInformation"] = patientInformation
					exerciseResults.append(exerciseResult)
				else:
					logger.debug(dbMsg)

	logger.debug("exerciseResults: " + str(exerciseResults))

	return exerciseResults


def gather_exerciseresult(username, dbHandler, logger, exerciseResultID):
	"""
		Gathers an exercise result from the database.

		Args:
			username (String): The userName
			dbHandler (database_handler): The databasehandler
			logger (logger): The logger
			exerciseResultID (String): The ID of an exerciseResult.
		Returns:
			exerciseResult (String): An JSON-formatted string with an exerciseResult from the database.
	"""
	
	exerciseResult = {}
	if (exerciseResultID is None): 
		logger.debug("exerciseResultID=None")
	else:
		dbMsg = json.loads(dbHandler.get_exerciseresult(username, exerciseResultID))
		#logger.debug(dbMsg)
		if dbMsg.get("status_code") == "200":
			exerciseResult = dbMsg.get("ExerciseResult")[0]
		else:
			logger.debug("for ID: " + str(exerciseResultID) + " - " + str(dbMsg))
	logger.debug("exerciseResult: " + str(exerciseResult))
	return exerciseResult

def gather_rehabilitationset(username, dbHandler, logger, rehabilitationSetID):
	"""
		Gathers a rehabilitationSet from the database.

		Args:
			username (String): The userName
			dbHandler (database_handler): The databasehandler
			logger (logger): The logger
			rehabilitationSetID (String): The ID of the rehabilitationSet to get. 
		Returns:
			rehabilitationSet (String): A JSON-formatted string with a rehabilitationSet with the same format as in the database.
	"""
	
	rehabilitationSet = {}
	if (rehabilitationSetID is None): 
		logger.debug("rehabilitationSet=None")
	else:
		dbMsg = json.loads(dbHandler.get_rehabilitationset(username, rehabilitationSetID))
		#logger.debug(dbMsg)
		if dbMsg.get("status_code") == "200":
			rehabilitationSet = dbMsg.get("RehabilitationSet")[0]
		else:
			logger.debug("for ID: " + str(rehabilitationSetID) + " - " + str(dbMsg))
	return rehabilitationSet


def meanError(peaks, target):
	"""
	Calculates the average absolute error of the peaks from the target.

	Uses RMS.
	Args:
		peaks ([[float, float]]): The peaks together with their timestamps.
		target (string): The target value.
	Returns:
		meanError (float): The mean absolute error.
	"""
	target = float(target)
	return np.sqrt(np.mean(np.square(map(lambda x: ((float(x[1])-target)), peaks))))


MAX_NUMBER_OF_OLD_RESULTS = {"name": "max_number_of_old_results",
"type": "int",
"description": "The maximum number of old results to include in the analysis.",
"default": [1000000],
"range": "0-",
"required": False,
"max_amount": -1,
"min_amount": 0} 

MIN_AGE = {"name": "min_age",
"type": "int",
"description": "The minimum age of patients to include in the analysis.",
"default": [0],
"range": "0-200",
"required": False,
"max_amount": -1,
"min_amount": 0} 

MAX_AGE = {"name": "max_age",
"type": "int",
"description": "The maximum age of patients to include in the analysis.",
"default": ["Default value"],
"range": "0-200",
"required": False,
"max_amount": -1,
"min_amount": 0}

MIN_WEIGHT = {"name": "min_weight",
"type": "int",
"description": "The minimum weight of patients to include in the analysis.",
"default": ["Default value"],
"range": "0-",
"required": False,
"max_amount": -1,
"min_amount": 0} 

MAX_WEIGHT = {"name": "max_weight",
"type": "int",
"description": "The maximum weight of patients to include in the analysis.",
"default": ["Default value"],
"range": "0-",
"required": False,
"max_amount": -1,
"min_amount": 0}

MIN_BMI = {"name": "min_bmi",
"type": "int",
"description": "The minimum BMI of patients to include in the analysis.",
"default": ["Default value"],
"range": "0-",
"required": False,
"max_amount": -1,
"min_amount": 0} 

MAX_BMI = {"name": "max_bmi",
"type": "int",
"description": "The maximum BMI of patients to include in the analysis.",
"default": ["Default value"],
"range": "0-",
"required": False,
"max_amount": -1,
"min_amount": 0}

START_DATE = {"name": "start_date",
"type": "int",
"description": "The start date of results to include in the analysis.",
"default": ["Default value"],
"range": "something",
"required": False,
"max_amount": -1,
"min_amount": 0}

END_DATE = {"name": "max_weight",
"type": "int",
"description": "The end date of results to include in the analysis.",
"default": ["Default value"],
"range": "something",
"required": False,
"max_amount": -1,
"min_amount": 0}

GENDER = {"name": "gender",
"type": "enum",
"description": "The gender of the patients to include in the analysis.",
"default": ["Default value"],
"range": "male, female, other",
"required": False,
"max_amount": -1,
"min_amount": 0}

SMOKER = {"name": "smoker",
"type": "bool",
"description": "The smoking habits of the patients to include in the analysis.",
"default": ["Default value"],
"range": "never, sometimes, often, every day",
"required": False,
"max_amount": -1,
"min_amount": 0}

ORGANIZATION_ID = {"name": "organizationID",
"type": "organizationID",
"description": "The id of the organization(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}		

USERGROUP_ID = {"name": "usergroupID",
"type": "usergroupID",
"description": "The id of the usergroup(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}

USER_ID = {"name": "userID",
"type": "userID",
"description": "The id of the user(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}		

PATIENT_ID = {"name": "patientID",
"type": "patientID",
"description": "The id of the patient(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}

REHABILITATIONSET_ID = {"name": "rehabilitationSetID",
"type": "rehabilitationSetID",
"description": "The id of the rehabilitationset(s) to use for the analysis.",
"default": [""],
"range": "",
"required": True,
"max_amount": -1,
"min_amount": 0}

EXERCISE_RESULT_ID = {"name": "exerciseResultID",
"type": "exerciseResultID",
"description": "The id of the exercise result(s) to use for the analysis.",
"default": ["Default value"],
"range": "",
"required": True,
"max_amount": -1,
"min_amount": 0}

EXERCISE_ID = {"name": "exerciseID",
"type": "exerciseID",
"description": "The id of the exercise(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}

DEVICE_ID = {"name": "deviceID",
"type": "deviceID",
"description": "The id of the device(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}

ANALYSIS_TASK_ID = {"name": "analysisTaskID",
"type": "analysisTaskID",
"description": "The id of the analysisTask(s) to use for the analysis.",
"default": ["Default value"],
"range": "something, somethingelse",
"required": False,
"max_amount": -1,
"min_amount": 0}

USELESS_PARAMETER = {"name": "uselessParameter",
"type": "String",
"description": "This parameter is useless and will never be used.",
"default": ["Whats the point?"],
"range": "something",
"required": False,
"max_amount": -1,
"min_amount": 0}
