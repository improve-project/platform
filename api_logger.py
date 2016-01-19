#!/usr/bin/env python
# coding=utf-8

# http://stackoverflow.com/questions/21393758/unicodedecodeerror-ascii-codec-cant-decode-byte-0xe5-in-position-0-ordinal
import logging
#from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
from os import mkdir, path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = "Jani Yli-Kantola"
__credits__ = ["Jani Yli-Kantola", "Tommi Portti", "Harri Hirvonsalo", "Kari Liukkunen", "Björn Elmers", "Olov Ståhl"]
__license__ = ""
__status__ = "Development"

# TODO: Capture printouts of external modules
## About capturing and redirecting stdout
# https://wrongsideofmemphis.wordpress.com/2010/03/01/store-standard-output-on-a-variable-in-python/
# http://stackoverflow.com/questions/22822267/python-capture-print-output-of-another-module

LOG_PATH = './logs/'
LOG_FILE = LOG_PATH + 'restAPI.log'

if LOG_PATH != "./":
    try:
        mkdir(LOG_PATH)
        print("Creating LOG_PATH: '{}'.".format(LOG_PATH))
    except IOError:
        print("LOG_PATH: '{}' already exists.".format(LOG_PATH))
    except Exception as e:
        print("LOG_PATH: '{}' could not be created. Exception: {}.".format(LOG_PATH, repr(e)))

# Logger functionality
logger = logging.getLogger('RestAPI')  # Get Logger
logger.setLevel(logging.DEBUG)  # Set logging level
# Log levels
# ->  CRITICAL
# ->  ERROR
# ->  WARNING
# ->  INFO
# ->  DEBUG
# ->  NOTSET

# Logging to file
if 'vagrant' in path.abspath(__file__):
    # Log everything to one file when running vagrant
    # http://stackoverflow.com/questions/22852555/rotatingfilehandler-text-file-busy-in-windows
    # http://bugs.python.org/issue4749
    logFileHandler = logging.FileHandler(LOG_FILE)  # Handler to log to file
else:
    # To switch log file when it reaches specified file-size
    #bytes = 1024 * 1024 * 5  # 5 MB
    #logFileHandler = RotatingFileHandler(LOG_FILE, maxBytes=bytes, backupCount=5)

    # To switch log file based on time
    logFileHandler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7, utc=True)

# To set logging-level for logFileHandler
logFileHandler.setLevel(logging.DEBUG)  # Set logging level

# Logging to Console
logConsoleHandler = logging.StreamHandler()  # Handler to log to console
logConsoleHandler.setLevel(logging.DEBUG)  # Set logging level

# Log formatter for handlers
logFileFormatter = logging.Formatter('%(asctime)s - %(filename)-22s on line %(lineno)-6d - %(levelname)-10s - %(message)s')
logConsoleFormatter = logging.Formatter('%(asctime)s - %(filename)-22s - %(levelname)-10s - %(message)s')

# Add log formatter to log handlers
logFileHandler.setFormatter(logFileFormatter)
logConsoleHandler.setFormatter(logConsoleFormatter)

# Add log handlers to logger
logger.addHandler(logFileHandler)
logger.addHandler(logConsoleHandler)

logger.debug("****************")
