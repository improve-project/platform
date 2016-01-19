# coding=utf-8
__author__ = 'olovs'
"""An module for creating a graph plotting a feature in a specific rehabilitation set as compared to the mean of the same feature in a selection (or all) of other rehabilitation sets
"""

from AnalysisPackage import analysismodule, moduleUtilities
import time
import datetime
import numpy as np
import sys
import json
from flask import jsonify
import logging

PARAM_DIAGRAM_REHABLITATION_SET           = "rehabilitation set"
PARAM_DIAGRAM_Y_AXIS_VARIABLE             = "feature"

PARAM_REHAB_SET_SELECTION_GENDER          = "gender"
PARAM_REHAB_SET_SELECTION_BIRTH_YEAR      = "birthYear"
PARAM_REHAB_SET_SELECTION_WEIGHT          = "weight"
PARAM_REHAB_SET_SELECTION_HEIGHT          = "height"
PARAM_REHAB_SET_SELECTION_CONDITION       = "condition"
PARAM_REHAB_SET_SELECTION_EXERCISE        = "exercise"
PARAM_REHAB_SET_SELECTION_DURATION        = "duration days"
PARAM_REHAB_SET_SELECTION_NR_OF_EXERCISES = "number of exercises"
PARAM_REHAB_SET_SELECTION_START_PROGRESS  = "start progress"

VARIABLE_PROGRESS                         = "progress"
VARIABLE_STABILITY                        = "stability"
VARIABLE_ACCURACY                         = "accuracy"
VARIABLE_RIABLOSITY                       = "riablosity"
VARIABLE_PRECISION                        = "precision"
VARIABLE_TARGET                           = "target (% of body weight)"
VARIABLE_PEAK_MEAN                        = "peakMean (% of body weight)"

CATEGORY_REHAB_SET_MAIN                   = "Set & feature"          
CATEGORY_REHAB_SET_SELECTION              = "Rehabilitation set selection"          

def getVariablesList():
        return  VARIABLE_PROGRESS + "," + VARIABLE_STABILITY + "," + VARIABLE_ACCURACY + "," + VARIABLE_RIABLOSITY + "," + VARIABLE_PRECISION + "," + VARIABLE_TARGET + "," + VARIABLE_PEAK_MEAN


class group_analysis(analysismodule.AnalysisModule):

        def filterRange(self, value, min, max, logger):
                  
                if value == "" or value == None:
                        return False
                elif int(value) >= int(min) and int(value) <= int(max):
                        return True
                else:
                        return False
                                
        def filterValue(self, value, cmpValue, logger):
            
                if str(cmpValue) == "Any" or str(cmpValue) == "":
                        return True
                elif str(value) == str(cmpValue):
                        return True
                else:
                        return False

        def divideDataValues(self, data, factor, logger):
                result = []
                for tuple in data:
                        value = tuple[1]/factor
                        result.append([tuple[0], value, "value=" + str(value)])
                return result

        def getExerciseResultParameterValue(self, exerciseData, parameter):
                if parameter == VARIABLE_PROGRESS:
                        return exerciseData.get("progress")
                elif parameter == VARIABLE_ACCURACY:
                        values = json.loads(exerciseData.get("values"))
                        return values.get("accuracy")
                elif parameter == VARIABLE_PRECISION:
                        values = json.loads(exerciseData.get("values"))
                        return values.get("precision")
                elif parameter == VARIABLE_RIABLOSITY:
                        values = json.loads(exerciseData.get("values"))
                        return values.get("riablosity_gained")
                elif parameter == VARIABLE_STABILITY:
                        values = json.loads(exerciseData.get("values"))
                        return values.get("stability")
                elif parameter == VARIABLE_TARGET:
                        values = json.loads(exerciseData.get("settings"))
                        return values.get("target")
                elif parameter == VARIABLE_PEAK_MEAN:
                        values = json.loads(exerciseData.get("values"))
                        return values.get("peakAverage")
                else:
                        return 0.0

        def getRehabilitationProgressStart(self, dbHandler, username, rehabSet):
                exerciseResultIdsStr = rehabSet.get("exerciseResultIDs")
                progress = 0
                if (exerciseResultIdsStr != ""):
                        exerciseResultIdsArr = exerciseResultIdsStr.split(";")
                        exerciseId = exerciseResultIdsArr[0]
                        exerciseResult = json.loads(dbHandler.get_exerciseresult(username, exerciseId))
                        if exerciseResult.get("status_code") == "200":
                                exerciseDataArr = exerciseResult.get("ExerciseResult")
                                exerciseData = exerciseDataArr[0]
                                progress = int(exerciseData.get("progress"))
                return progress

        def gatherExerciseResultDatas(self, dbHandler, username, rehabSet, parameter):
                data = []
                exerciseResultIdsStr = rehabSet.get("exerciseResultIDs")
                if (exerciseResultIdsStr != ""):
                        exerciseNumber = 1
                        exerciseResultIdsArr = exerciseResultIdsStr.split(";")
                        for exerciseId in exerciseResultIdsArr:
                                exerciseResult = json.loads(dbHandler.get_exerciseresult(username, exerciseId))
                                if exerciseResult.get("status_code") == "200":
                                        exerciseDataArr = exerciseResult.get("ExerciseResult")
                                        for exerciseData in exerciseDataArr:
                                                started = exerciseData.get("started")
                                                tuple = []
                                                tuple.append(exerciseNumber);
                                                value = self.getExerciseResultParameterValue(exerciseData, parameter)
                                                if value != None and value != "":
                                                        tuple.append(float(value))
                                                        tuple.append("value=" + str(value))
                                                        data.append(tuple)
                                                exerciseNumber = exerciseNumber + 1
                return data

	def analyse(self, username, configParams, dbHandler, logger):

		logger.info("Starting group analysis ... " + username)

		rehabSetId = configParams[PARAM_DIAGRAM_REHABLITATION_SET]
		varY = configParams[PARAM_DIAGRAM_Y_AXIS_VARIABLE]

                gender = configParams[PARAM_REHAB_SET_SELECTION_GENDER]
                birthYear = configParams[PARAM_REHAB_SET_SELECTION_BIRTH_YEAR]
                weight = configParams[PARAM_REHAB_SET_SELECTION_WEIGHT]
                height = configParams[PARAM_REHAB_SET_SELECTION_HEIGHT]
                condition = configParams[PARAM_REHAB_SET_SELECTION_CONDITION]
                exercise = configParams[PARAM_REHAB_SET_SELECTION_EXERCISE]
                duration = configParams[PARAM_REHAB_SET_SELECTION_DURATION]

                progressStart = configParams[PARAM_REHAB_SET_SELECTION_START_PROGRESS]

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

                progressStartMin = 0;
                progressStartMax = 100;

                if (progressStart != ""):
                        minusIndex = progressStart.find('-')
                        if (minusIndex != -1):
                                progressStartMin = int(progressStart[:minusIndex])
                                progressStartMax = int(progressStart[minusIndex+1:])
                        else:
                                progressStartMin = int(progressStart)
                                progressStartMax = int(progressStart)

                if (progressStartMin > progressStartMax):
                        tmp = progressStartMin
                        progressStartMin = progressStartMax
                        progressStartMax = tmp

                rehabSetResult = json.loads(dbHandler.list_rehabilitationsets(username))

                rehabSetDatas = []
                rehabsSetData = []

                if rehabSetResult.get("status_code") == "200":
                        rehabSetArray = rehabSetResult.get("RehabilitationSets")
			for rehabSet in rehabSetArray:
                                doFilter = True
                                patientInfoID = rehabSet.get("patientInformationID")
                                if rehabSetId == rehabSet.get("rehabilitationSetID"):
                                        doFilter = False
                                patientInfoResult = json.loads(dbHandler.get_patientinformation(username, patientInfoID))
                                rehabSetOk = True
                                progressStart = self.getRehabilitationProgressStart(dbHandler, username, rehabSet)
                                if doFilter and True != self.filterRange(progressStart, progressStartMin, progressStartMax, logger):
                                        continue
                                patientWeight = 0
                                if patientInfoResult.get("status_code") == "200":
                                        patientInfoArray = patientInfoResult.get("PatientInformation")
                                        for patientInfo in patientInfoArray:
                                                if doFilter and True != self.filterRange(int(patientInfo.get("birthYear")), birthYearMin, birthYearMax, logger):
                                                        rehabSetOk = False
                                                        break               
                                                patientWeight = int(patientInfo.get("bodyWeight"))
                                                if doFilter and True != self.filterRange(patientWeight, weightMin, weightMax, logger):
                                                        rehabSetOk = False
                                                        break                                        
                                                if doFilter and True != self.filterRange(int(patientInfo.get("bodyHeight")), heightMin, heightMax, logger):
                                                        rehabSetOk = False
                                                        break                                        
                                                if doFilter and True != self.filterValue(patientInfo.get("gender"), gender, logger):
                                                        rehabSetOk = False
                                                        break                                        
                                if True != rehabSetOk:
                                        continue

                                patientCondIDs = rehabSet.get("patientConditionIDs").split(";")
                                for patientCondID in patientCondIDs:
                                        patientCondResult = json.loads(dbHandler.get_patientcondition(username, patientCondID))
                                        if patientCondResult.get("status_code") == "200":
                                                patientCondArray = patientCondResult.get("PatientCondition")
                                                for patientCond in patientCondArray:
                                                        if doFilter and True != self.filterValue(patientCond.get("label"), condition, logger):
                                                                rehabSetOk = False
                                                                break                                        
                                if True != rehabSetOk:
                                        continue
                                
                                data = self.gatherExerciseResultDatas(dbHandler, username, rehabSet, varY)
                                if varY == VARIABLE_TARGET or varY == VARIABLE_PEAK_MEAN:
                                        data = self.divideDataValues(data, patientWeight/100.0, logger)

                                if rehabSetId == rehabSet.get("rehabilitationSetID"):
                                        rehabSetData = data
                                else:
                                        rehabSetDatas.append(data)

                else:
                        logger.debug("ERROR - Couldn't get rehab set list!");

                meanData = []
                exerciseNumber = 1
                doContinue = True
                while (doContinue):
                        valueTot = 0.0
                        rehabSetsTot = 0
                        for data in rehabSetDatas:
                                for tuple in data:
                                        if tuple[0] == exerciseNumber:
                                                valueTot = valueTot + tuple[1]
                                                rehabSetsTot = rehabSetsTot + 1
                                                break
                        if rehabSetsTot > 0:
                                valueMean = valueTot/rehabSetsTot
                                meanData.append([exerciseNumber, valueMean, "value=" + str(valueMean)])
                        else:
                                doContinue = False
                        exerciseNumber = exerciseNumber + 1

		plotData = []
		plotData.append(moduleUtilities.construct_single_plotdata(data=rehabSetData, legend="set", subtype="lines_and_points"))
		plotData.append(moduleUtilities.construct_single_plotdata(data=meanData, legend="mean", subtype="lines_and_points"))
		plotResult = [moduleUtilities.construct_plotresult(title="", plotDatas=plotData, priority=1, x_label="exercise", y_label=varY)]

		result = moduleUtilities.construct_results_object(plotResult)
		return result

	def necessary_config_params(self):
		return [ANALYSIS_REHAB_SET, 
                        ANALYSIS_VARIABLE_Y, 
                        ANALYSIS_SELECTION_BIRTH_YEAR, 
                        ANALYSIS_SELECTION_WEIGHT, 
                        ANALYSIS_SELECTION_GENDER, 
                        ANALYSIS_SELECTION_HEIGHT, 
                        ANALYSIS_SELECTION_EXERCISE,
                        ANALYSIS_SELECTION_CONDITION,
                        ANALYSIS_SELECTION_DURATION,
                        ANALYSIS_SELECTION_NR_OF_EXERCISES,
                        ANALYSIS_SELECTION_PROGRESS_START
                ]

	def description(self):
		description = "Compare a single rehabilitation set to others. Select the set and the feature, and optionally a selection of sets to compare."
		return description

	def permission_level(self):
		return 6

	def __init__(self):
		return

ANALYSIS_REHAB_SET = {
        "name": PARAM_DIAGRAM_REHABLITATION_SET,
        "category": CATEGORY_REHAB_SET_MAIN,
        "type": "rehabilitationSetID",
        "description": "The rehabilitation set to compare",
        "default": [""],
        "range": "",
        "required": True,
        "max_amount": -1,
        "min_amount": 0
}

ANALYSIS_VARIABLE_Y = {
        "name": PARAM_DIAGRAM_Y_AXIS_VARIABLE,
        "category": CATEGORY_REHAB_SET_MAIN,
        "type": "enum",
        "description": "The variable to view on the Y axis",
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

ANALYSIS_SELECTION_PROGRESS_START = {
        "name": PARAM_REHAB_SET_SELECTION_START_PROGRESS,
        "category": CATEGORY_REHAB_SET_SELECTION,
        "type": "int",
        "description": "Progess at start of rehabilitation",
        "default": [""],
        "range": "1-100",
        "required": False,
        "max_amount": -1,
        "min_amount": 0
}

