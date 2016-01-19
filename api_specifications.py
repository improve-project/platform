#!/usr/bin/env python
# coding=utf-8

import json
from flask import make_response, jsonify, request
from werkzeug.exceptions import abort
from api_logger import logger

__author__ = "Jani Yli-Kantola"
__credits__ = ["Jani Yli-Kantola", "Tommi Portti", "Harri Hirvonsalo", "Kari Liukkunen", "Björn Elmers", "Olov Ståhl"]
__license__ = ""
__status__ = "Development"


######### CONSTANTS

# Debug switches
RESPONSE_DEBUG = False


# 2XX Success Status codes for response validation
SUCCESS_STATUS_CODES = ['200', '201', '202', '203', '204', '205', '206']

"""
Username to use for testing purposes
"""
DEMO_USER = 'NotInUse'
#DEMO_USER = 'Evalan_u_1'
#DEMO_USER = 'Jani_test_user_username'

# Username for production use
production_user = ''

# Secret for DB reset
SECRET_CORRECT = "FqPon673GfQ"


## Error messages
ERROR_USING_DEFAULT_VALUE = ', Using default value'
ERROR_USING_USERS_OWN_ORGANIZATION = ", Using user's own organization"

#Request
ERROR_HEADERS_USERNAME_NOT_PRESENT = 'No username present in request headers.'
ERROR_HEADERS_USERNAME = "Can't make username available for API-endpoints"
ERROR_JSON_NOT_PRESENT = 'No json payload. Are yoy sure you are using Content-Type: application/json'
ERROR_JSON_NOT_VALID = 'Invalid JSON payload'

ERROR_JSON_FIELD_NOT_PRESENT = 'No field attribute present on json payload'
ERROR_JSON_VALUE_NOT_PRESENT = 'No value attribute present on json payload'

ERROR_JSON_NAME_NOT_PRESENT = 'No name attribute present on json payload'
ERROR_JSON_PERMISSION_LEVEL_NOT_PRESENT = 'No permission level attribute present on json payload'

ERROR_JSON_USER_IDS_NOT_PRESENT = 'No userIDs attribute present on json payload'
ERROR_JSON_ORGANIZATION_ID_NOT_PRESENT = 'No organizationID attribute present on json payload'
ERROR_JSON_PATIENT_IDS_NOT_PRESENT = 'No patientIDs attribute present on json payload'
ERROR_JSON_USER_TO_ATTACH_NOT_PRESENT = 'No attachable user id attribute present on json payload'
ERROR_JSON_ALLOWED_ORGANIZATION_IDS_NOT_PRESENT = 'No allowedOrganizations attribute present on json payload'
ERROR_JSON_ALLOWED_ORGANIZATIONS_NOT_PRESENT = 'No allowedOrganizations attribute present on json payload'
ERROR_JSON_REHABILITATION_SET_IDS_NOT_PRESENT = 'No rehabilitationSetID attribute present on json payload'

#User
ERROR_JSON_FIRSTNAME_NOT_PRESENT = 'No firstName attribute present on json payload'
ERROR_JSON_LASTNAME_NOT_PRESENT = 'No lastName attribute present on json payload'
ERROR_JSON_JOBTITLE_NOT_PRESENT = 'No jobTitle attribute present on json payload'
ERROR_JSON_USERNAME_NOT_PRESENT = 'No userName attribute present on json payload'
ERROR_JSON_PASSWORD_NOT_PRESENT = 'No password attribute present on json payload'

#PatientCondition
ERROR_JSON_LABEL_NOT_PRESENT = 'No label attribute present on json payload'
ERROR_JSON_DESCRIPTION_NOT_PRESENT = 'No description attribute present on json payload'
ERROR_JSON_OFFICAL_MEDICAL_CODE_NOT_PRESENT = 'No officialMedicalCode attribute present on json payload'

#RehabilitationSet
ERROR_JSON_PATIENT_ID_NOT_PRESENT = 'No patientID attribute present on json payload'
ERROR_JSON_PATIENTINFORMATION_ID_NOT_PRESENT = 'No patientInformationID attribute present on json payload'
ERROR_JSON_PATIENTCONDITION_IDS_NOT_PRESENT = 'No patientConditionIDs attribute present on json payload'
ERROR_JSON_EXERCISERESULT_IDS_NOT_PRESENT = 'No exerciseResultID attribute present on json payload'

#PatientInformation
ERROR_JSON_BODY_WEIGHT_NOT_PRESENT = 'No bodyWeight attribute present on json payload'
ERROR_JSON_BODY_HEIGHT_NOT_PRESENT = 'No bodyHeight attribute present on json payload'
ERROR_JSON_UPPER_BODY_DOMINANT_SIDE_NOT_PRESENT = 'No upperBodyDominantSide attribute present on json payload'
ERROR_JSON_LOWER_BODY_DOMINANT_SIDE_NOT_PRESENT = 'No lowerBodyDominantSide attribute present on json payload'
ERROR_JSON_BIRTH_YEAR_NOT_PRESENT = 'No birthYear attribute present on json payload'
ERROR_JSON_GENDER_NOT_PRESENT = 'No gender attribute present on json payload'

#DEVICE
ERROR_JSON_DEVICE_NAME_NOT_PRESENT = 'No name attribute present on json payload'
ERROR_JSON_DEVICE_TYPE_NOT_PRESENT = 'No type attribute present on json payload'
ERROR_JSON_DEVICE_DESCRIPTION_NOT_PRESENT = 'No description attribute present on json payload'
ERROR_JSON_DEVICE_AXIS_COUNT_NOT_PRESENT = 'No axisCount attribute present on json payload'
ERROR_JSON_DEVICE_VALUE_UNIT_NOT_PRESENT = 'No valueUnit attribute present on json payload'
ERROR_JSON_DEVICE_VALUE_UNIT_ABB_NOT_PRESENT  = 'No valueUnitAbbreviation attribute present on json payload'
ERROR_JSON_DEVICE_DEFAULT_VALUE_NOT_PRESENT = 'No defaultValue attribute present on json payload'
ERROR_JSON_DEVICE_MAXIMUM_VALUE_NOT_PRESENT = 'No maximumValue attribute present on json payload'
ERROR_JSON_DEVICE_MININIMUM_VALUE_NOT_PRESENT = 'No minimumValue attribute present on json payload'

#ExerciseResult
ERROR_JSON_EXERCISE_ID_NOT_PRESENT = 'No exerciseID attribute present on json payload'
ERROR_JSON_EXERCISERESULT_DEVICE_ID_NOT_PRESENT = 'No deviceID attribute present on json payload'
ERROR_JSON_EXERCISERESULT_DATA_NOT_PRESENT = 'No dataSamples attribute present on json payload'
ERROR_JSON_EXERCISERESULT_STARTED_NOT_PRESENT = 'No started attribute present on json payload'
ERROR_JSON_EXERCISERESULT_ENDED_NOT_PRESENT = 'No ended attribute present on json payload'
ERROR_JSON_EXERCISERESULT_SETTINGS_NOT_PRESENT = 'No settings attribute present on json payload'
ERROR_JSON_EXERCISERESULT_VALUES_NOT_PRESENT = 'No values attribute present on json payload'
ERROR_JSON_EXERCISERESULT_PROGRESS_NOT_PRESENT = 'No progress attribute present on json payload'
ERROR_JSON_DATA_IDS_NOT_PRESENT = 'No dataID attribute present on json payload'

#Data
ERROR_JSON_DEVICE_ID_NOT_PRESENT = 'No deviceID attribute present on json payload'
ERROR_JSON_SAMPLES_NOT_PRESENT = 'No samples attribute present on json payload'

#Exercise
ERROR_JSON_EXERCISE_NAME_NOT_PRESENT = 'No name attribute present on json payload'
ERROR_JSON_EXERCISE_DESCRIPTION_NOT_PRESENT = 'No description attribute present on json payload'
ERROR_JSON_EXERCISE_SETTINGS_PRESENT = 'No settings attribute present on json payload'

#Database
ERROR_DB_PREFIX = 'Database Error: '
ERROR_DB_QUERY_FAILED = ERROR_DB_PREFIX + 'Query failed'
ERROR_DB_JSON_DECODE = ERROR_DB_PREFIX + "JSON from database handler couldn't be decoded"
ERROR_DB_NO_STATUS_CODE = ERROR_DB_PREFIX + 'No status code in db query response'
ERROR_DB_NO_CONTAINER = ERROR_DB_PREFIX + 'Could not find correct container from db_response. Using db_response[msg] instead'
ERROR_DB_STATUS_500 = ERROR_DB_PREFIX + 'Database returned 500 as status code'

DB_RESET = 'Resetting database connections with db_reset(secret=' + SECRET_CORRECT + ')'


#Response
ERROR_RESPONSE_JSON_PARSE = "Return_content handler couldn't be parsed to valid JSON"

######### END OF CONSTANTS



### FUNCTIONS

# Generate response
def generate_response(return_content_par, status_par):

    if RESPONSE_DEBUG:
        logger.debug("1")

    logger.info('generate_response(return_content, status)')

    if RESPONSE_DEBUG:
        logger.debug("2")

    return_content = return_content_par

    if RESPONSE_DEBUG:
        logger.debug("3")
        logger.debug(repr(return_content))

    try:
        if RESPONSE_DEBUG:
            logger.debug("4")
            logger.debug(repr(return_content))

        return_content = json.dumps(return_content_par).replace("\"[", "[").replace("]\"", "]").replace('\\', '').replace("\"{", "{").replace("}\"", "}")
    except Exception as argument:
        if RESPONSE_DEBUG:
            logger.debug("5")
            logger.debug(repr(return_content))
        abort(500, ERROR_RESPONSE_JSON_PARSE + ' json.dumps(): ' + repr(argument).replace("u'", "").replace("'", ""))

    try:
        if RESPONSE_DEBUG:
            logger.debug("6")
            logger.debug(repr(return_content))
        return_content = json.loads(return_content)
        if RESPONSE_DEBUG:
            logger.debug("7")
            logger.debug(repr(return_content))
    except Exception as argument:
        if RESPONSE_DEBUG:
            logger.debug("8")
            logger.debug(repr(return_content))
        abort(500, ERROR_RESPONSE_JSON_PARSE + ' json.loads(): ' + repr(argument).replace("u'", "").replace("'", ""))

    #Log response content
    if RESPONSE_DEBUG:
        logger.debug("9")
        logger.debug(repr(return_content))
    logger.debug('Response Status: ' + str(status_par) + ', Content: ' + repr(return_content))

    # Because 204 has no body content
    if status_par == '204':
        response = make_response()
        response.status_code = 204
    else:
        response = make_response(jsonify({'requestURL': request.url, 'requestMethod': request.method, 'requestStatusCode': status_par, 'content': return_content}))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = int(status_par)

    logger.debug('Response: ' + repr(response))
    return response


def validate_db_response(db_response_par):

    logger.debug("validate_db_response(db_response_par)")

    if 'status_code' in db_response_par:
        status = db_response_par['status_code']

        if status not in SUCCESS_STATUS_CODES:
            # Generate error message
            error_message = ERROR_DB_PREFIX
            if 'msg' in db_response_par:
                error_message += db_response_par['msg']

            if 'ErrorText' in db_response_par:
                error_message += ', ErrorText: ' + db_response_par['ErrorText'].replace('\"', '')

            # Abort with statusCode and errorMessage
            logger.debug('Abort with: ' + str(status) + ', ' + error_message)
            abort(int(status), str(error_message))
    else:
        abort(500, ERROR_DB_NO_STATUS_CODE)

    logger.debug("validate_db_response(db_response_par): OK")

    return db_response_par

