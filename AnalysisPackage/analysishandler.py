#!/usr/bin/env python
# coding=utf-8

__author__ = 'bjorne'
"""Handles all commands regarding analysis, i.e. get_available_analysis_modules and perform_analysis.

Uses JSON objects to represent the analysismodules, which are returned from get_available_analysis_modules(username, dbHandler), on the form:

{
	"analysismodules": 
	[ 
		{
			"name": "analysisModuleName", 
			"permission_level": "4",
			"description": "blablabla",
			"configParams": 
			[
				{
				"name": "exercise",
				"description": "The exercise to use in the analysis",
				"type": "enum",
				"default": ["value"],
				"range": "exercise_A, exercise_B",
				"required": true/false,
				"max_amount": 33, #negative value means arbitrary
				"min_amount": 5 #negative value means arbitrary
				}, {
				"name": "good name",
				"description": "descr...",
				"type": "int",
				"default": ["value"],
				"range": "0-100",
				"required": true/false,
				"max_amount": 33, #negative value means arbitrary
				"min_amount": 5 #negative value means arbitrary
				}
			]
		}
	]
}

The available types in configParams are:
enum, string, int, float, bool, exerciseID, dataID, deviceID, exerciseResultID, rehabilitationSetID, patientInformationID, patientConditionID, patientID, userID, userGropID, organizationID, analysisTaskID

The settings-object that are used as input in perform_analysis(username, moduleName, settings, dbHandler) is also an JSON object and it is on the form:
{
   "configParams": {"exerciseID": ["y7tt347fyre", "ignfu4bh"],
					"max_weight": [100]},
	"notification": {"none": "email@email.se"},
	"taskname": "The name of this task"
}


The analysisResult produced by the analysismodules are all on the following form:
{
	"results": 
		[
			{
				"name": "a name",
				"type": "plot",
				"data": [[1,3],[2,634],[3,33],[5,233]],
				"priority": 5  #How important is this result?,
				"subtype": "lines",
				"legend": "Legend to use"		
				"plotID": "id of the plot to make it possible to plot many things in same plot"	
			},
			{
				"name": "a name",
				"type": "plot",
				"data": [[1,3],[2,634],[3,33],[5,233]],
				"priority": 5  #How important is this result?,
				"subtype": "points",
				"legend": "Legend to use"		
				"plotID": "id of the plot to make it possible to plot many things in same plot"	
			},
			{
				"name": "a name",
				"type": "text",
				"data": "here is a result",
				"priority": 2
			},
			{
				"name": "a name",
				"type": "html",
				"data": "{htmlcode...}",
				"priority": 6,
				"subtype": "body" 
			}
		],
	"model": {...}
}

"""

import threading
import glob
import importlib
import time
import smtplib
import json
import inspect
import sys, traceback
import logging



"""
## Logging ##
- https://docs.python.org/2/howto/logging.html
- https://docs.python.org/2/howto/logging-cookbook.html

### Logging levels ###
- DEBUG
    + Detailed information, typically of interest only when diagnosing problems.
- INFO
    + Confirmation that things are working as expected.
- WARNING
    + An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’)
- ERROR
    + Due to a more serious problem, the software has not been able to perform some function.
- CRITICAL
    + A serious error, indicating that the program itself may be unable to continue running.
"""

# Logger functionality
logger = logging.getLogger('AnalysisHandler')  # Get Logger
logger.setLevel(logging.DEBUG)  # Set logging level

# Logging to file
logFileHandler = logging.FileHandler('analysishandler.log')  # Handler to log to file
logFileHandler.setLevel(logging.DEBUG)  # Set logging level

# Logging to Console
logConsoleHandler = logging.StreamHandler()  # Handler to log to console
logConsoleHandler.setLevel(logging.DEBUG)  # Set logging level

# Log formatter for handlers
logFileFormatter = logging.Formatter('%(asctime)s - %(filename)s on line %(lineno)-6d - %(levelname)-8s - %(message)s')
logConsoleFormatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)-8s - %(message)s')

# Add log formatter to log handlers
logFileHandler.setFormatter(logFileFormatter)
logConsoleHandler.setFormatter(logConsoleFormatter)

# Add log handlers to logger
logger.addHandler(logFileHandler)
logger.addHandler(logConsoleHandler)
# ************************************************************** #
# The following section to overwrite console log formatter
#class MyStreamHandler(logging.StreamHandler):
#    def handleError(self, record):
#        raise


#console = MyStreamHandler()
#logger.addHandler(console)
# ************************************************************** #

# To log things use
#  logger.debug('debug message')
#  logger.info('info message')
#  logger.warn('warn message')
#  logger.error('error message')
#  logger.critical('critical message')

# END OF LOGGER INIT
logger.debug("Debug: Logger Online")
logger.info("Info: Logger Online")
logger.warn("Warn: Logger Online")
logger.error("Error: Logger Online")
logger.critical("Critical: Logger Online")

# ************************************************************** #




modulesFolder = 'modules'	#The name of the folder containing the analysismodules
threadList = []
analysisPermissionLevel = 7
analysisUsername = "Evalan_analysis_user" #This username is only used when calling methods regarding analysisTasks in the database

#Analysis task statuses
STATUS_RUNNING = "Running"
STATUS_READY = "Ready"
STATUS_FAILED = "Failed"

def _get_file_name_from_path(path):  
	"""Extracts the filename from the relative path

	Assuming the path is on the form folder/fileName.extension
	Args:
		path (String): the path on the form folder/fileName.extension
	Returns:
		(String): The fileName without extension
	""" 
	return path.split('/')[1].split('.')[0]

def _get_available_analysis_modules(username, dbHandler):
	"""Finds all modules in the modulesFolder and their necessary configuration parameters.

	Only includes the modules if the user is has correct permissionlevel.
	Args:
		username (String): The username.
		dbHandler (DatabaseHandler): The databasehandler.
	Returns:
		modules (JSON): A JSON object on the form described at the top of this document. 

	"""

	logger.debug("In _get_available_analysis_modules")
	files = glob.glob(modulesFolder + "/*.py")
	modules = []

	for fileName in files:	
		if (fileName != modulesFolder + "/__init__.py"): #removes the __init__ file
			name = _get_file_name_from_path(fileName)
			
			try:
				moduleClass = _get_analysis_module_class(name)	
				modulePermissionLevel = moduleClass.permission_level()
				userPermissionLevel = dbHandler.get_usergroup_by_username(username)
				if  userPermissionLevel >= modulePermissionLevel:
					continue

				description = moduleClass.description()
				params = moduleClass.necessary_config_params()
				
			except Exception as e:
				msg = "There was an error in module: " + str(name) + str(e) + " - "
				logger.error(msg)
				continue
						
			modules.append({"name": name, "description": description, "permission_level": modulePermissionLevel, "configParams": params})
	
	return modules

def _get_analysis_module_class(moduleName):		#In this version we're assuming that each module only contains one class
	"""Imports the analysis module and returns the modules class with the same name.

	Args:
		moduleName (String): The name of the module.
	Returns:
		moduleClass (Class): The class of the module.
	Raises: 
		Exception if modulename doesn't exists or if module doesn't contain a class with modulename.
	"""
	logger.debug("in _get_analysis_module_class")
	module = importlib.import_module(modulesFolder + "." + moduleName)
	moduleClass = None
	for name, obj in inspect.getmembers(module):
		logger.debug(name)
		if inspect.isclass(obj) and (name == moduleName):	#Assumes that the module only contains one class
			logger.debug("found a class-attr")
			moduleClass = getattr(module, name)()
	if moduleClass is None:
		raise NameError
	return moduleClass



def _start_analysis_thread(username, moduleName, moduleClass, settings, dbHandler):
	"""The method that actually starts the analysisthread.

	Saves the thread in a list, thread_list, so it can be accessed later, isn't used at the moment.
	Args:
		username (String): The username.
		moduleName (String): The name of the module to use.
		moduleClass (Class): The class of the module to use.
		settings (String): JSON-formatted string with settings for the chosen analysismodule on the form specified at the top.
		dbHandler (DatabaseHandler): The databasehandler.
	Returns:
		analysisTaskID (String): The ID of the created task.
	Raises:
		Exception if database is unable to create an analysisTask. Probably due to bad input.

	"""
	logger.debug("in _start_analysis_thread")
	started = time.time()*1000
	databaseMsg = ""
	try:
		logger.debug("Username: " + str(username))
		databaseMsg = json.loads(dbHandler.create_analysistask(username=username, allowedOrganizations=dbHandler.get_usergroup_by_username(username).organizationID, taskname=settings["taskname"], analysisModule=moduleName, status=STATUS_RUNNING, notification=json.dumps(settings["notification"]), configurationParameters=json.dumps(settings["configParams"]), started=started))
		logger.debug("Created analysisTask. Msg from database: " + str(databaseMsg))
		analysisTaskID = databaseMsg["TaskID"]
	except Exception, Argument:
		Argument.message = Argument.message + ". Database msg: " + str(databaseMsg)
		raise

	t = threading.Thread(target=_analysis_thread, args=(username, moduleClass, settings, dbHandler, analysisTaskID,))
	threadList.append(t)	#To make the thread accessible
	t.start()
	logger.info("Analysisthread started")

	return databaseMsg

def _analysis_thread(username, moduleClass, settings, dbHandler, analysisTaskID):
	""" This is the thread that runs the analysis of the chosen module.

	Args:
		username (String): The username.
		moduleClass (Class): The class of the module to use.
		settings (String): JSON-formatted string with settings for the chosen analysismodule on the form specified at the top.
		dbHandler (DatabaseHandler): The databasehandler.
		analysisTaskID (String): The ID in the database of the created task.
	 """
	logger.debug("in _analysis_thread")
	result = {}
	try:
		settings["configParams"]["thisAnalysisTaskID"] = analysisTaskID #Including taskID in settings to make it possible for the module to accessing itself, maybe for scheduling or other purposes
		result = moduleClass.analyse(username, settings["configParams"], dbHandler, logger)
		
		msg = "Status on '" + settings["taskname"] + "'' is: " + str(result.get("status")) + ".\n"
		logger.info(msg)
		ended = time.time()*1000

		logger.info("analysisTaskID = " + analysisTaskID)
		dbMessage = dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="analysisResult", value=json.dumps(result.get("results")))
		logger.info("Update result: " + dbMessage)
		dbMessage = dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="status", value=STATUS_READY)
		logger.info("Update status: " + dbMessage)
		dbMessage = dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="ended", value=ended)
		logger.info("Update ended: " + dbMessage)
	except Exception, Argument:	
		msg = traceback.format_exc()
		logger.error(msg)
		ended = time.time()*1000		
		dbMessage = dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="status", value=STATUS_FAILED)
		logger.info("Update status: " + dbMessage)
		dbMessage = dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="ended", value=ended)
		logger.info("Update ended: " + dbMessage)
	
	#notify user
	sender = "eit.rehab.platform@gmail.com"
	password = "eitrehabplatform"
	for key in settings["notification"]:	#should implement other notificationsmethod here, i.e. sms
		if key == "email":
			_email_user(sender,settings["notification"]["email"],password,"Analysisstatus", msg)
		elif key == "none":
			logger.info("No notification requested")
			continue
		else:
			logger.info("notification-method " + key + " not implemented")
	print "Result: " + str(result.get("results")) + "\n"
	logger.info("Result: " + str(result.get("results")))

def _email_user(sender, receiver, password, subj, msg):
	"""Sends an email to the user, e.g. with a notification that the analysis is ready and possibly where to find it.

	Args:
		sender (String): The email to send from.
		receiver (String): The email to send to.
		password (String): The password of the sender.
		subj (String): The subject of the email.
		msg (String): The message of the email.

	Raises:
		SMTPException: If email couldn't be sent.

	"""
	logger.debug("in _email_user")
	receiver = [receiver]
	message = 'Subject: %s\n\n%s' % (subj, msg)

	try:    
		session = smtplib.SMTP('smtp.gmail.com',587)
		session.ehlo()
		session.starttls()
		session.ehlo()
		session.login(sender,password)
		session.sendmail(sender,receiver,message)
		session.quit()
		logger.info("message sent!")
	except smtplib.SMTPException:
		logger.error("Could not send email.\n" + traceback.format_exc())
		




def get_available_analysis_modules(username, dbHandler):
	"""Checks the modules folder for all available analysis modules.

	If the user is unauthorized to do this an error message will return,

	Args:
		username (String): The username.
		dbHandler (DatabaseHandler): The databasehandler.
	Returns:
		(String): A JSON-formatted respone string. It is either
		a) A status message 200 and all the available analysisModules.
    	b) A status message 401, meaning that the User doesn't have the right to see available analysisModules.
    	c) A status message 500, meaning something went wrong.	
	"""
	
	try:
		logger.debug("in get_available_analysis_modules")
		logger.debug("username: " + str(username))
		if dbHandler.__permissionLevel_by_username__(username) > analysisPermissionLevel:
			return json.dumps({'status_code': '401', 'msg': 'User not allowed to do this.'})

		analysisModules = _get_available_analysis_modules(username, dbHandler)
		return json.dumps({'status_code': '200', 'analysisModules': analysisModules})
	except Exception, Argument:	
		errorMsg = {'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message}
		msg = traceback.format_exc()
		logger.error(msg)
		return json.dumps(errorMsg)
		

def perform_analysis(username, moduleName, settings, dbHandler):
	"""The method for starting an analysis.

	Args:
		username (String): The username.
		moduleName (String): The name of the analysismodule that should perform the analysis.
		settings (String): A JSON-formatted string with the settings for to use for the analysis.
		dbHandler (DatabaseHandler): The database handler.
	Returns:
		msg (String): A JSON-formatted respone string. It is either
		a) A status message 201 and the analysisTaskID of the created analysisTask
    	b) A status message 401, meaning that the User doesn't have the right to create this analysisTask.
    	c) A status message 500, meaning something went wrong.	"""
	logger.debug("in perform_analysis")
	logger.debug("username: " + str(username))
	try:
		permissionlevel = dbHandler.get_usergroup_by_username(username).permissionLevel
		logger.debug("permissionlevel: " + str(permissionlevel))

		moduleClass = _get_analysis_module_class(moduleName)
		modulePermissionlevel = moduleClass.permission_level()
		logger.debug("modulePermissionlevel: " + str(modulePermissionlevel))

		if permissionlevel > modulePermissionlevel:
			return json.dumps({'status_code': '401', 'msg': 'User not allowed to run this analysis.'})
		databaseMsg = _start_analysis_thread(username, moduleName, moduleClass, settings, dbHandler)
		return json.dumps(databaseMsg)
	except Exception, Argument:	
		errorMsg = {'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message}
		msg = traceback.format_exc()
		logger.error(msg)
		return json.dumps(errorMsg)



