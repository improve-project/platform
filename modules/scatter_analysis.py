# coding=utf-8
__author__ = 'olovs'
"""An module for creating a scatter plot of two rehabilitation set features from a selection (or all) of rehabilitation sets
"""

from AnalysisPackage import analysismodule, moduleUtilities
import time
import datetime
import numpy as np
import sys
import json
from flask import jsonify
import logging

PARAM_DIAGRAM_X_AXIS_VARIABLE             = "X axis"
PARAM_DIAGRAM_Y_AXIS_VARIABLE             = "Y axis"

PARAM_REHAB_SET_SELECTION_GENDER          = "gender"
PARAM_REHAB_SET_SELECTION_BIRTH_YEAR      = "birthYear"
PARAM_REHAB_SET_SELECTION_WEIGHT          = "weight"
PARAM_REHAB_SET_SELECTION_HEIGHT          = "height"
PARAM_REHAB_SET_SELECTION_CONDITION       = "condition"
PARAM_REHAB_SET_SELECTION_PROGRESS        = "progress"
PARAM_REHAB_SET_SELECTION_EXERCISE        = "exercise"
PARAM_REHAB_SET_SELECTION_DURATION        = "duration days"
PARAM_REHAB_SET_SELECTION_NR_OF_EXERCISES = "number of exercises"

VARIABLE_BIRTH_YEAR                       = "birthYear"
VARIABLE_PROGRESS_INCR                    = "progress incr"
VARIABLE_PROGRESS                         = "progress"
VARIABLE_CONDITION                        = "condition"
VARIABLE_WEIGHT                           = "weight"
VARIABLE_HEIGHT                           = "height"
VARIABLE_GENDER                           = "gender"
VARIABLE_EXERCISE                         = "exercise"
VARIABLE_NR_OF_EXERCISES                  = "number of exercises"
VARIABLE_DURATION                         = "duration"

CATEGORY_REHAB_SET_SELECTION              = "Rehabilitation set selection"          

def getVariablesList():
        return  VARIABLE_GENDER + "," + VARIABLE_BIRTH_YEAR + "," + VARIABLE_WEIGHT + "," + VARIABLE_HEIGHT + "," + VARIABLE_CONDITION + "," + VARIABLE_DURATION + "," + VARIABLE_NR_OF_EXERCISES + "," + VARIABLE_PROGRESS_INCR + "," + VARIABLE_PROGRESS + "," + VARIABLE_EXERCISE


class scatter_analysis(analysismodule.AnalysisModule):

        def getRehabSetAttribute(self, rehabSet, attr):
                if attr == VARIABLE_GENDER:
                        return rehabSet['gender']
                elif attr == VARIABLE_WEIGHT:
                        return rehabSet['weight']
                elif attr == VARIABLE_HEIGHT:
                        return rehabSet['height']
                elif attr == VARIABLE_BIRTH_YEAR:
                        return rehabSet['birthYear']
                elif attr == VARIABLE_DURATION:
                        return rehabSet['duration']
                elif attr == VARIABLE_NR_OF_EXERCISES:
                        return rehabSet['nrOfExercises']
                elif attr == VARIABLE_PROGRESS_INCR:
                        return rehabSet['progressIncr']
                elif attr == VARIABLE_PROGRESS:
                        return rehabSet['progress']
                elif attr == VARIABLE_CONDITION:
                        return rehabSet['condition']
                elif attr == VARIABLE_EXERCISE:
                        return rehabSet['exercise']
                else:
                        return 0

        def createRehabSet(self, rehabSetId):
                return {"id": rehabSetId}

        def filterRange(self, rehabSets, attr, min, max, logger):
                result = []
                for rehabSet in rehabSets:
                        if attr in rehabSet and rehabSet[attr] >= min and rehabSet[attr] <= max:
                                result.append(rehabSet)
                                
                return result

        def filterValue(self, rehabSets, attr, value, logger):
                result = []
                for rehabSet in rehabSets:
                        if str(value) == "Any" or str(value) == "" or rehabSet[attr] == value:
                                result.append(rehabSet)
                                
                return result

	def analyse(self, username, configParams, dbHandler, logger):

		logger.info("Starting analysis scatter... " + username)

		varX = configParams[PARAM_DIAGRAM_X_AXIS_VARIABLE]
		varY = configParams[PARAM_DIAGRAM_Y_AXIS_VARIABLE]

                gender = configParams[PARAM_REHAB_SET_SELECTION_GENDER]
                birthYear = configParams[PARAM_REHAB_SET_SELECTION_BIRTH_YEAR]
                weight = configParams[PARAM_REHAB_SET_SELECTION_WEIGHT]
                height = configParams[PARAM_REHAB_SET_SELECTION_HEIGHT]
                progress = configParams[PARAM_REHAB_SET_SELECTION_PROGRESS]
                condition = configParams[PARAM_REHAB_SET_SELECTION_CONDITION]
                exercise = configParams[PARAM_REHAB_SET_SELECTION_EXERCISE]
                duration = configParams[PARAM_REHAB_SET_SELECTION_DURATION]

                birthYearMin = 1900;
                birthYearMax = 2015;

                if (birthYear != ""):
                        minusIndex = birthYear.find('-')
                        if (minusIndex != -1):
                                birthYearMin = int(birthYear[:minusIndex])
                                birthYearMax = int(birthYear[minusIndex+1:])
                        else:
                                birthYearMin = int(birthYear)
                                birthYearMax = int(birthYear)

                if (birthYearMin > birthYearMax):
                        tmp = birthYearMin
                        birthYearMin = birthYearMax
                        birthYearMax = tmp

                weightMin = 0;
                weightMax = 200;

                if (weight != ""):
                        minusIndex = weight.find('-')
                        if (minusIndex != -1):
                                weightMin = int(weight[:minusIndex])
                                weightMax = int(weight[minusIndex+1:])
                        else:
                                weightMin = int(weight)
                                weightMax = int(weight)

                if (weightMin > weightMax):
                        tmp = weightMin
                        weightMin = weightMax
                        weightMax = tmp

                heightMin = 0;
                heightMax = 250;

                if (height != ""):
                        minusIndex = height.find('-')
                        if (minusIndex != -1):
                                heightMin = int(height[:minusIndex])
                                heightMax = int(height[minusIndex+1:])
                        else:
                                heightMin = int(height)
                                heightMax = int(height)

                if (heightMin > heightMax):
                        tmp = heightMin
                        heightMin = heightMax
                        heightMax = tmp

                progressMin = 0;
                progressMax = 100;

                if (progress != ""):
                        minusIndex = progress.find('-')
                        if (minusIndex != -1):
                                progressMin = int(progress[:minusIndex])
                                progressMax = int(progress[minusIndex+1:])
                        else:
                                progressMin = int(progress)
                                progressMax = int(progress)

                if (progressMin > progressMax):
                        tmp = progressMin
                        progressMin = progressMax
                        progressMax = tmp

                durationMin = 0;
                durationMax = 10000;

                if (duration != ""):
                        minusIndex = duration.find('-')
                        if (minusIndex != -1):
                                durationMin = int(duration[:minusIndex])
                                durationMax = int(duration[minusIndex+1:])
                        else:
                                durationMin = int(duration)
                                durationMax = int(duration)

                if (durationMin > durationMax):
                        tmp = durationMin
                        durationMin = durationMax
                        durationMax = tmp

                rehabSetResult = json.loads(dbHandler.list_rehabilitationsets(username))

                rehabSets = []

                if rehabSetResult.get("status_code") == "200":
                        rehabSetArray = rehabSetResult.get("RehabilitationSets")
			for rehabSet in rehabSetArray:
                                rehabSetId = rehabSet.get("rehabilitationSetID")
                                _rehabSet = self.createRehabSet(rehabSetId)
                                rehabSets.append(_rehabSet)
                                patientInfoID = rehabSet.get("patientInformationID")
                                patientInfoResult = json.loads(dbHandler.get_patientinformation(username, patientInfoID))
                                if patientInfoResult.get("status_code") == "200":
                                        patientInfoArray = patientInfoResult.get("PatientInformation")
                                        for patientInfo in patientInfoArray:
                                                _rehabSet['gender'] = patientInfo.get("gender")
                                                _rehabSet['height'] = int(patientInfo.get("bodyHeight"))
                                                _rehabSet['weight'] = int(patientInfo.get("bodyWeight"))
                                                _rehabSet['birthYear'] = int(patientInfo.get("birthYear"))
                                patientCondIDs = rehabSet.get("patientConditionIDs").split(";")
                                for patientCondID in patientCondIDs:
                                        patientCondResult = json.loads(dbHandler.get_patientcondition(username, patientCondID))
                                        if patientCondResult.get("status_code") == "200":
                                                patientCondArray = patientCondResult.get("PatientCondition")
                                                for patientCond in patientCondArray:
                                                        _rehabSet['condition'] = patientCond.get("label")
                                exerciseCount = 0
                                _rehabSet['nrOfExercises'] = 0
                                _rehabSet['progressIncr'] = 0
                                _rehabSet['duration'] = 0
                                exerciseResultIdsStr = rehabSet.get("exerciseResultIDs")
                                if (exerciseResultIdsStr != ""):
                                        latestExerciseTime = 0
                                        earliestProgress = 0;
                                        latestProgress = 0;
                                        earliestExerciseTime = 0
                                        exerciseResultIdsArr = exerciseResultIdsStr.split(";")
                                        _rehabSet['nrOfExercises'] = len(exerciseResultIdsArr)
                                        for exerciseId in exerciseResultIdsArr:
                                                exerciseResult = json.loads(dbHandler.get_exerciseresult(username, exerciseId))
                                                if exerciseResult.get("status_code") == "200":
                                                        exerciseDataArr = exerciseResult.get("ExerciseResult")
                                                        for exerciseData in exerciseDataArr:
                                                                _rehabSet['exercise'] = exerciseData.get("exerciseID")
                                                                started = exerciseData.get("started")
                                                                if 0 == latestExerciseTime or int(started) > latestExerciseTime:
                                                                        latestExerciseTime = int(started)
                                                                        progress = exerciseData.get("progress")
                                                                        if progress != None and progress != "":
                                                                                latestProgress = int(progress)
                                                                                _rehabSet['progress'] = int(progress)
                                                                if 0 == earliestExerciseTime or int(started) < earliestExerciseTime:
                                                                        earliestExerciseTime = int(started)
                                                                        earliestProgress = int(exerciseData.get("progress"))
                                        _rehabSet['duration'] = (latestExerciseTime - earliestExerciseTime)/(60*60*24)
                                        _rehabSet['progressIncr'] = (latestProgress - earliestProgress)
                    
                else:
                        logger.debug("ERROR - Couldn't get rehab set list!");

                rehabSets = self.filterRange(rehabSets, 'birthYear', birthYearMin, birthYearMax, logger)
                rehabSets = self.filterRange(rehabSets, 'weight', weightMin, weightMax, logger)
                rehabSets = self.filterRange(rehabSets, 'height', heightMin, heightMax, logger)
                rehabSets = self.filterRange(rehabSets, 'progress', progressMin, progressMax, logger)
                rehabSets = self.filterRange(rehabSets, 'duration', durationMin, durationMax, logger)

                rehabSets = self.filterValue(rehabSets, 'gender', gender, logger)
                rehabSets = self.filterValue(rehabSets, 'condition', condition, logger)
                rehabSets = self.filterValue(rehabSets, 'exercise', exercise, logger)

                variableData = []

                for rehabSet in rehabSets:

                        data = []
                        data.append(self.getRehabSetAttribute(rehabSet, varX))
                        data.append(self.getRehabSetAttribute(rehabSet, varY))
                        data.append(rehabSet['id'] + "<br>" + str(rehabSet['gender']) + "<br>" + str(rehabSet['birthYear']) + " / " + str(rehabSet['weight']) + " kg / " + str(rehabSet['height']) + " cm<br>" + rehabSet['condition'] + "<br>" + str(rehabSet['duration']) + " days / " + str(rehabSet['nrOfExercises']) + " exercises<br>" + str(rehabSet['progress']) + " / " + str(rehabSet['progressIncr']) + " incr")
                        variableData.append(data)

		plotData = []
		plotData.append(moduleUtilities.construct_single_plotdata(data=variableData, legend="", subtype="points"))
		plotResult = [moduleUtilities.construct_plotresult(title="", plotDatas=plotData, priority=1, x_label=varX, y_label=varY)]

		result = moduleUtilities.construct_results_object(plotResult)
		return result

	def necessary_config_params(self):
		return [ANALYSIS_VARIABLE_X, 
                        ANALYSIS_VARIABLE_Y, 
                        ANALYSIS_SELECTION_BIRTH_YEAR, 
                        ANALYSIS_SELECTION_WEIGHT, 
                        ANALYSIS_SELECTION_GENDER, 
                        ANALYSIS_SELECTION_HEIGHT, 
                        ANALYSIS_SELECTION_PROGRESS,
                        ANALYSIS_SELECTION_EXERCISE,
                        ANALYSIS_SELECTION_CONDITION,
                        ANALYSIS_SELECTION_DURATION,
                        ANALYSIS_SELECTION_NR_OF_EXERCISES
                ]

	def description(self):
		description = "Collect and plot features from a selection of rehabilitation sets. Select scatter plot axis variables, and optionally a rehabilitation set selection."
		return description

	def permission_level(self):
		return 6

	def __init__(self):
		return

ANALYSIS_VARIABLE_X = {
        "name": PARAM_DIAGRAM_X_AXIS_VARIABLE,
        "category": "Diagram",
        "type": "enum",
        "description": "The variable to use on the X axis",
        "default": [""],
        "range": getVariablesList(),
        "required": True,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_VARIABLE_Y = {
        "name": PARAM_DIAGRAM_Y_AXIS_VARIABLE,
        "category": "Diagram",
        "type": "enum",
        "description": "The variable to use on the Y axis",
        "default": [""],
        "range": getVariablesList(),
        "required": True,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_BIRTH_YEAR = {
        "name": PARAM_REHAB_SET_SELECTION_BIRTH_YEAR,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Range of patient birth year",
        "default": [""],
        "range": "0-100",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_WEIGHT = {
        "name": PARAM_REHAB_SET_SELECTION_WEIGHT,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Range of patient weight",
        "default": [""],
        "range": "0-150",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_HEIGHT = {
        "name": PARAM_REHAB_SET_SELECTION_HEIGHT,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Range of patient height",
        "default": [""],
        "range": "0-200",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_PROGRESS = {
        "name": PARAM_REHAB_SET_SELECTION_PROGRESS,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Range of patient progress",
        "default": [""],
        "range": "0-100",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_GENDER = {
        "name": PARAM_REHAB_SET_SELECTION_GENDER,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "enum",
        "description": "Patient gender",
        "default": [""],
        "range": "Male, Female",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_CONDITION = {
        "name": PARAM_REHAB_SET_SELECTION_CONDITION,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "enum",
        "description": "Patient condition",
        "default": [""],
        "range": ", Hip, Knee, Foot, Back, Elbow",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_EXERCISE = {
        "name": PARAM_REHAB_SET_SELECTION_EXERCISE,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "exerciseID",
        "description": "Patient exercise",
        "default": [""],
        "range": "",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_DURATION = {
        "name": PARAM_REHAB_SET_SELECTION_DURATION,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Range of days in treatment",
        "default": [""],
        "range": "1-1000",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_SELECTION_NR_OF_EXERCISES = {
        "name": PARAM_REHAB_SET_SELECTION_NR_OF_EXERCISES,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Range of number of exercises",
        "default": [""],
        "range": "1-1000",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}
