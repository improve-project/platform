#!/usr/bin/env python
# coding=utf-8

import os
import sys
from imp import reload
from flask import Flask, make_response, jsonify, request, send_from_directory, abort, json
from werkzeug.exceptions import BadRequest
from api_logger import logger
import api_specifications
import database_handler
from AnalysisPackage import analysishandler

# http://stackoverflow.com/questions/21393758/unicodedecodeerror-ascii-codec-cant-decode-byte-0xe5-in-position-0-ordinal
reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = "Jani Yli-Kantola"
__credits__ = ["Jani Yli-Kantola", "Tommi Portti", "Harri Hirvonsalo", "Kari Liukkunen", "Björn Elmers", "Olov Ståhl"]
__license__ = ""
__status__ = "Development"

# Flask App
app = Flask(__name__)
logger.debug('app = Flask(' + __name__ + ')')

database = database_handler.DatabaseHandler()


# Before Request
logger.debug('@app.before_request')
@app.before_request
def before_request():
    # Request basic logging
    logger.debug('**********************')
    logger.debug('New request')

    logger.info(request.method + ' to ' + request.url)
    logger.info('request.remote_addr: ' + request.remote_addr)
    logger.debug('Headers')
    for header in request.headers:
        logger.debug(repr(header).replace("('", "--> ").replace("', u'", ": ").replace("')", ""))

    logger.debug('Request Data (length: ' + str(len(request.data)) + ') \n' + request.data)

    # Username check
    username_from_headers = ""
    username_from_headers = request.headers.get('username')
    logger.debug('username_from_headers as ' + repr(type(username_from_headers)) + ': ' + repr(username_from_headers))

    if type(username_from_headers) is unicode:
        logger.debug('username_from_headers: ' + username_from_headers)
    elif (('/api/v1.0/system/documentation' in request.url) or ('/dashboard' in request.url) or ('/static/' in request.url) or ('favicon.ico' in request.url) or ('/performance' in request.url)):
        logger.debug('Accessing /api/v1.0/system/documentation without username')
    else:
        abort(400, api_specifications.ERROR_HEADERS_USERNAME_NOT_PRESENT)

    if request.endpoint == 'patients' and request.method == 'POST':
        logger.info('JSON payload not required, skipping valid JSON test.')
    elif request.method == 'POST' or request.method == 'PUT':
        try:
            json.loads(json.dumps(request.json))
        except Exception as argument:
            abort(400,
                  api_specifications.ERROR_JSON_NOT_VALID + ': ' + repr(argument).replace("u'", "").replace("'", ""))

    logger.info('Function to call:  ' + repr(request.endpoint) + '()')

#
# Error handlers
logger.debug("Defining error handlers for HTML status codes")
# 4XX Client Errors
@app.errorhandler(400)
def error_400(error):
    """
    HTML Status code 400 - Bad Request
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 400")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '400', 'requestStatus': 'Bad Request', 'content': return_content}), 400)


@app.errorhandler(401)
def error_401(error):
    """
    HTML Status code 401 - Unauthorized
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 401")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '401', 'requestStatus': 'Unauthorized', 'content': return_content}), 401)


@app.errorhandler(403)
def error_403(error):
    """
    HTML Status code 403 - Forbidden
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 403")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(jsonify({'requestStatusCode': '403', 'requestStatus': 'Forbidden', 'content': return_content}), 403)


@app.errorhandler(404)
def error_404(error):
    """
    HTML Status code 404 - Not found
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 404")
    logger.debug(request.method + ' request to: ' + request.url + ' From: ' + request.remote_addr)
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(jsonify({'requestStatusCode': '404', 'requestStatus': 'Not found', 'content': return_content}), 404)


@app.errorhandler(405)
def error_405(error):
    """
    HTML Status code 405 - Method Not Allowed
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 405")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '405', 'requestStatus': 'Method Not Allowed', 'content': return_content}), 405)


@app.errorhandler(406)
def error_406(error):
    """
    HTML Status code 406 - Not Acceptable
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 406")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '406', 'requestStatus': 'Not Acceptable', 'content': return_content}), 406)


@app.errorhandler(408)
def error_408(error):
    """
    HTML Status code 408 - Request Timeout
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 408")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '408', 'requestStatus': 'Request Timeout', 'content': return_content}), 408)


@app.errorhandler(409)
def error_409(error):
    """
    HTML Status code 409 - Conflict
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 409")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(jsonify({'requestStatusCode': '409', 'requestStatus': 'Conflict', 'content': return_content}), 409)


@app.errorhandler(413)
def error_413(error):
    """
    HTML Status code 413 - Payload Too Large
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 413")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '413', 'requestStatus': 'Payload Too Large', 'content': return_content}), 413)


@app.errorhandler(414)
def error_414(error):
    """
    HTML Status code 414 - URI Too Long
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 414")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '414', 'requestStatus': 'URI Too Long', 'content': return_content}), 414)


@app.errorhandler(415)
def error_415(error):
    """
    HTML Status code 415 - Unsupported Media Type
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 415")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '415', 'requestStatus': 'Unsupported Media Type', 'content': return_content}), 415)


@app.errorhandler(426)
def error_426(error):
    """
    HTML Status code 426 - Upgrade Required
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 426")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '426', 'requestStatus': 'Upgrade Required', 'content': return_content}), 426)


@app.errorhandler(429)
def error_429(error):
    """
    HTML Status code 429 - Too Many Requests
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 429")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '429', 'requestStatus': 'Too Many Requests', 'content': return_content}), 429)


@app.errorhandler(431)
def error_431(error):
    """
    HTML Status code 431 - Request Header Fields Too Large
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 431")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(jsonify(
        {'requestStatusCode': '431', 'requestStatus': 'Request Header Fields Too Large', 'content': return_content}), 431)


# 5XX Server Errors
@app.errorhandler(500)
def error_500(error):
    """
    HTML Status code 500 - Internal Server Error
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.warn('Error StatusCode: 500')
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error_description}

    return make_response(
        jsonify({'requestStatusCode': '500', 'requestStatus': 'Internal Server Error', 'content': return_content}), 500)


@app.errorhandler(501)
def error_501(error):
    """
    HTML Status code 501 - Not Implemented
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 501")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '501', 'requestStatus': 'Not Implemented', 'content': return_content}), 501)


@app.errorhandler(503)
def error_503(error):
    """
    HTML Status code 503 - Service Unavailable
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 503")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '503', 'requestStatus': 'Service Unavailable', 'content': return_content}), 503)


@app.errorhandler(505)
def error_505(error):
    """
    HTML Status code 505 - HTTP Version Not Supported
    """

    try:
        error_description = repr(error.description)
    except Exception:
        error_description = repr(error)

    logger.info("Error StatusCode: 505")
    logger.debug('Error description: ' + error_description)

    return_content = {'message': error.description}

    return make_response(
        jsonify({'requestStatusCode': '505', 'requestStatus': 'HTTP Version Not Supported', 'content': return_content}), 505)


logger.debug("Defined error handlers for HTML status codes")
#
# End of Error handlers



# API endpoints
# INDEX
logger.debug("/ | GET")
@app.route('/', methods=['GET'])
def index():
    """
    App Root
    Response: 403
    """
    response = make_response('Forbidden', 403)
    return response

# RESET DATABASE CONNECTIONS
logger.debug("/api/v1.0/system/DBreset/<string:secret> | GET")
@app.route('/api/v1.0/system/DBreset/<string:secret>', methods=['GET'])
def db_reset(secret):
    """
    GET: Reset database connections
        URL
        - `secret` Secret key
    """
    if 'DBreset' not in request.url:
        logger.info("##")
        logger.info('Internal call of db_reset(secret)')

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = ""

    if secret == api_specifications.SECRET_CORRECT:
        try:
            logger.debug('database.reset(' + secret + ')')
            db_response = database.reset()
            logger.debug('Database Query Returned: ' + repr(db_response))

            return_content = 'As you wish!'

        except Exception as argument:
            return_content = "I would like to, but I just can't do it!"
            status = 500
            logger.debug('Exception with Argument: ' + repr(argument).replace("(u'", " | ").replace("',)", ""))
    else:
        return_content = "I won't do it for you!"
        status = 403

    # TODO: Should response generation also follow if'DBreset' not in request.url
    logger.debug('Status: ' + str(status) + ', Return Content: ' + repr(return_content))
    response = make_response(jsonify({'content': return_content}), int(status))
    response.headers['Content-Type'] = 'application/json'
    logger.debug('Response: ' + repr(response))

    if 'DBreset' not in request.url:
        logger.info("##")

    return response

# UI / DASHBOARD
logger.debug("/dashboard | GET")
@app.route('/dashboard')
def dashboard():
    """
    GET: Demo UI for the Platform
    """
    return app.send_static_file('dashboard.html')


# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ************************************************************** #

# For Organizations
logger.debug("/api/v1.0/data/organizations | GET, POST")
@app.route('/api/v1.0/data/organizations', methods=['GET', 'POST'])
def organizations():
    """
    GET: Returns list of organizations

    POST: Creates an organization
        PAYLOAD
        - `name` Name of the organization

    RESPONSE ATTRIBUTES
        - 'organizationID' Organization ID
        - 'name' Name of the organization
        - 'userIDs' Users of the organization
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []
    db_response = ''

    # GET to list all organizations
    if request.method == 'GET':
        try:
            logger.debug('database.list_organizations(username=' + username + ')')
            db_response = database.list_organizations(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST to create organization
    if request.method == 'POST':

        new_organization_name = 'Not determined'

        # Validate request127
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'name' not in request.json:
            abort(400, api_specifications.ERROR_JSON_NAME_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_organization_name = request.json['name']

        # Database Query
        try:
            logger.debug('database.create_organization(username=' + username + ', name=' + new_organization_name + ')')
            db_response = database.create_organization(username, new_organization_name)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For organization
logger.debug("/api/v1.0/data/organizations/<string:organization_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/organizations/<string:organization_id>', methods=['GET', 'PUT', 'DELETE'])
def organizations_id(organization_id):
    """
    GET: Returns the organization by ID
        URL
        - `organizationID` ID for the organization

    PUT: Updates the organization by ID
        URL
        - `organizationID` ID for the organization
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the organization by ID
        URL
        - `organizationID` ID for the organization

    RESPONSE ATTRIBUTES
        - 'organizationID' Organization ID
        - 'name' Name of the organization
        - 'userIDs' Users of the organization
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET to retrieve organization by ID
    if request.method == 'GET':
        try:
            logger.debug('database.get_organization(username=' + username + ', organization_id=' + organization_id + ')')
            db_response = database.get_organization(username, organization_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update organization identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_organization(username=' + username + ', organizationID=' + organization_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_organization(username, organization_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove organization identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_organization(username=' + username + ', organization_id=' + organization_id + ')')
            db_response = database.delete_organization(username, organization_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# Users in organization
logger.debug("/api/v1.0/data/organizations/<string:organization_id>/users | POST")
@app.route('/api/v1.0/data/organizations/<string:organization_id>/users', methods=['POST'])
def organizations_id_users(organization_id):
    """
    POST: Adds users to the organization
        URL
        - `organizationID` ID for the organization
        PAYLOAD
        - `userIDs` UserID to add

    RESPONSE ATTRIBUTES
        - 'organizationID' Organization ID
        - 'userIDs' Users of the organization
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add user to organization identified by organizationID
    if request.method == 'POST':

        user_id_to_add = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'userIDs' not in request.json:
            abort(400, api_specifications.ERROR_JSON_USER_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: Check that only one userID is provided (Multiple IDs can be provided as CSV)
            user_id_to_add = request.json['userID']

        # Database Query
        try:
            logger.debug('database.add_user_to_organization(username=' + username + ', organizationID=' + organization_id + ', userID=' + user_id_to_add + ')')
            db_response = database.add_user_to_organization(username, organization_id, user_id_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# User in organization
logger.debug("/api/v1.0/data/organizations/<string:organization_id>/users/<string:user_id> | DELETE")
@app.route('/api/v1.0/data/organizations/<string:organization_id>/users/<string:user_id>', methods=['DELETE'])
def organizations_id_users_id(organization_id, user_id):
    """
    DELETE: Removes the user from the organization
        URL
        - `organizationID` ID of the organization
        - `userID` ID of the user

    RESPONSE ATTRIBUTES
        - 'organizationID' Organization ID
        - 'userIDs' Users of the organization
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove user from organization identified by organizationID
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug('database.remove_user_from_organization(username=' + username + ', organizationID=' + organization_id + ', userID=' + user_id + ')')
            db_response = database.remove_user_from_organization(username, organization_id, user_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of Organizations
# ************************************************************** #
# UserGroups
# For all
logger.debug("/api/v1.0/data/groups | GET, POST")
@app.route('/api/v1.0/data/groups', methods=['GET', 'POST'])
def groups():
    """
    GET: Returns list of user groups

    POST: Creates a user group
        PAYLOAD
        - `name` Name for the new organization
        - `permissionLevel` Permission level of the organization
        - `userIDs` UserID to add to the user group

    RESPONSE ATTRIBUTES
        - 'userGroupID' User group ID
        - 'name' Name of the group
        - `permissionLevel` Permission level of the organization
        - 'organizationID ' Users of the organization
        - 'userIDs' Users of the organization
    """
    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_usergroups(username=' + username + ')')
            db_response = database.list_usergroups(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST
    if request.method == 'POST':

        new_group_name = 'Not determined'
        new_group_permission_level = 8.0  # Permission level for non active group
        new_organization_id = database.__organizationID_by_username__(username)
        new_user_id_list = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'name' not in request.json:
            abort(400, api_specifications.ERROR_JSON_NAME_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_group_name = request.json['name']

            if 'permissionLevel' in request.json:
                new_group_permission_level = request.json['permissionLevel']
            else:
                logger.debug(api_specifications.ERROR_JSON_PERMISSION_LEVEL_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'organizationID' in request.json:
                new_organization_id = request.json['organizationID']
            else:
                logger.debug(api_specifications.ERROR_JSON_PERMISSION_LEVEL_NOT_PRESENT + api_specifications.ERROR_USING_USERS_OWN_ORGANIZATION)

            if 'userIDs' in request.json:
                new_user_id_list = request.json['userIDs']
            else:
                logger.debug(api_specifications.ERROR_JSON_USER_IDS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

        # Database Query
        try:
            logger.debug('database.create_usergroup(username=' + username + ', name=' + new_group_name + ', permissionLevel=' + str(new_group_permission_level) + ', organizationID=' + str(new_organization_id) + ', userIDs=' + repr(new_user_id_list).replace("u'", "").replace("'", "") + ')')
            db_response = database.create_usergroup(username, new_group_name, new_group_permission_level, new_organization_id, new_user_id_list)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/groups/<string:group_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/groups/<string:group_id>', methods=['GET', 'PUT', 'DELETE'])
def group_id(group_id):
    """
    GET: Returns the user group by ID
        URL
        - `userGroupID` ID for the user group

    POST: Updates the user group by ID
        URL
        - `userGroupID` ID for the user group
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the user group by ID
        URL
        - `userGroupID` ID for the user group

    RESPONSE ATTRIBUTES
        - 'userGroupID' User group ID
        - 'name' Name of the group
        - `permissionLevel` Permission level of the organization
        - 'organizationID ' Users of the organization
        - 'userIDs' Users of the organization
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_usergroup(username=' + username + ', group_id=' + group_id + ')')
            db_response = database.get_usergroup(username, group_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update userGroup identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_usergroup(username=' + username + ', userGroupID=' + group_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_usergroup(username, group_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove userGroup identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_usergroup(username=' + username + ', userGroupID=' + group_id + ')')
            db_response = database.delete_usergroup(username, group_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# Users in userGroups
logger.debug("/api/v1.0/data/groups/<string:group_id>/users | POST")
@app.route('/api/v1.0/data/groups/<string:group_id>/users', methods=['POST'])
def group_id_users(group_id):
    """
    POST: Adds users to the user group
        URL
        - `userGroupID` ID for the user group
        PAYLOAD
        - `userIDs` UserID to add

    RESPONSE ATTRIBUTES
        - 'userGroupID' user group ID
        - 'userIDs' Users of the user group
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add users to userGroup identified by groupID
    if request.method == 'POST':

        user_ids_to_add = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'userIDs' not in request.json:
            abort(400, api_specifications.ERROR_JSON_USER_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: If userIDs is a JSON list, convert to CSV
            user_ids_to_add = request.json['userIDs']

        # Database Query
        try:
            logger.debug('database.add_user_to_usergroup(username=' + username + ', userGroupID=' + group_id + ', userID=' + user_ids_to_add + ')')
            db_response = database.add_user_to_usergroup(username, group_id, user_ids_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# User in userGroup
logger.debug("/api/v1.0/data/groups/<string:group_id>/users/<string:user_id> | DELETE")
@app.route('/api/v1.0/data/groups/<string:group_id>/users/<string:user_id>', methods=['DELETE'])
def group_id_users_id(group_id, user_id):
    """
    DELETE: Removes the user from the user group
        URL
        - `userGroupID` ID of the user group
        - `userID` ID for the user

    RESPONSE ATTRIBUTES
        - 'userGroupID' User group ID
        - 'userIDs' Users of the user group
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove user from userGroup identified by groupID
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug( 'database.remove_user_from_usergroup(username=' + username + ', UserGroupID=' + group_id + ', userID=' + user_id + ')')
            db_response = database.remove_user_from_usergroup(username, group_id, user_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of UserGroups
# ************************************************************** #
# Users
# For all
# TODO: Endpoint/Query-string-style-method for searching users with database.get_users(self, username, field, value)
logger.debug("/api/v1.0/data/users | GET, POST")
@app.route('/api/v1.0/data/users', methods=['GET', 'POST'])
def users():
    """
    GET: Returns list of users

    POST: Creates an user
        PAYLOAD
        - `lastName` User’s last name
        - `firstName` User’s first name
        - `jobTitle` User’s job title
        - `userName` User’s username
        - `password` User’s password
        - `patientIDs` PatientID to link with user - OPTIONAL
        - `organizationID` OrganizationID to witch new user should belong, defaults to creators own organization - OPTIONAL

    RESPONSE ATTRIBUTES
        - `userID` User ID
        - `lastName` User’s last name
        - `firstName` User’s first name
        - `jobTitle` User’s job title
        - `userName` User’s username
        - `password` User’s password
        - `accessToken` User’s access token
        - `patientIDs` List of patients that belong to user
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    # return_content = "Under construction!"
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_users(username=' + username + ')')
            db_response = database.list_users(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST
    if request.method == 'POST':

        new_organization_id = database.__organizationID_by_username__(username)
        new_first_name = 'Not determined'
        new_last_name = 'Not determined'
        new_username = 'Not determined'
        new_password = 'Not determined'
        new_job_title = 'Not determined'
        new_patient_ids = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'firstName' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIRSTNAME_NOT_PRESENT)
        elif 'lastName' not in request.json:
            abort(400, api_specifications.ERROR_JSON_LASTNAME_NOT_PRESENT)
        elif 'jobTitle' not in request.json:
            abort(400, api_specifications.ERROR_JSON_JOBTITLE_NOT_PRESENT)
        elif 'userName' not in request.json:
            abort(400, api_specifications.ERROR_JSON_USERNAME_NOT_PRESENT)
        elif 'password' not in request.json:
            abort(400, api_specifications.ERROR_JSON_PASSWORD_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_first_name = request.json['firstName']
            new_last_name = request.json['lastName']
            new_job_title = request.json['jobTitle']
            new_username = request.json['userName']
            new_password = request.json['password']

            if 'patientIDs' in request.json:
                new_patient_ids = request.json['patientIDs']
            else:
                logger.debug(api_specifications.ERROR_JSON_PATIENT_IDS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'organizationID' in request.json:
                new_organization_id = request.json['organizationID']
            else:
                logger.debug(api_specifications.ERROR_JSON_PATIENT_IDS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

        # Database Query
        try:
            logger.debug('database.create_user(username=' + username + ', organizationID=' + new_organization_id + ', firstName=' + new_first_name + ', lastName=' + new_last_name + ', newUsername=' + new_username + ', password=' + new_password + ', jobTitle=' + new_job_title + ', patientIDs=' + new_patient_ids + ')')
            db_response = database.create_user(username, new_organization_id, new_first_name, new_last_name, new_username, new_password, new_job_title, new_patient_ids)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # TODO: How should status codes be handled when multiple queries will be executed?
        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

        # Database Query #2
        try:
            new_user_id = db_response['UserID']

            logger.debug('database.add_user_to_organization(username=' + username + ', organizationID=' + new_organization_id + ', userID=' + new_user_id + ')')
            db_response = database.add_user_to_organization(username, new_organization_id, new_user_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/users/<string:user_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_id(user_id):
    """
    GET: Returns the user by ID
        URL
        - `organizationID` ID for the user

    POST: Updates the organization by ID
        URL
        - `organizationID` ID for the user
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the organization by ID
        URL
        - `organizationID` ID for the user

    RESPONSE ATTRIBUTES
    - 'organizationID' User ID
    - 'name' Name of the user
    - 'userIDs' Users of the user
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_user(username=' + username + ', user_id=' + user_id + ')')
            db_response = database.get_user(username, user_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update user identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_user(username=' + username + ', userID=' + user_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_user(username, user_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove user identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_user(username=' + username + ', userID=' + user_id + ')')
            db_response = database.delete_user(username, user_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# Patients for user
logger.debug("/api/v1.0/data/users/<string:user_id>/patients | POST")
@app.route('/api/v1.0/data/users/<string:user_id>/patients', methods=['POST'])
def users_id_patients(user_id):
    """
    POST: Adds patient to the user
        URL
        - `userID` ID for the user
        PAYLOAD
        - `patientIDs` PatientID

    RESPONSE ATTRIBUTES
    - 'UserID' User ID
    - 'userIDs' Patients IDs
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add patients to user
    if request.method == 'POST':

        patient_id_to_add = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'patientIDs' not in request.json:
            abort(400, api_specifications.ERROR_JSON_PATIENT_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: Check that only one patientID is provided (Multiple can be provided as CSV)
            patient_id_to_add = request.json['patientIDs']

        # Database Query
        try:
            logger.debug('database.add_patient_to_user(username=' + username + ', userID=' + user_id + ', patientID=' + patient_id_to_add + ')')
            db_response = database.add_patient_to_user(username, user_id, patient_id_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/users/<string:user_id>/patients/<string:patient_id> | DELETE")
@app.route('/api/v1.0/data/users/<string:user_id>/patients/<string:patient_id>', methods=['DELETE'])
def users_id_patients_id(user_id, patient_id):
    """
    DELETE: Removes the patient from the user
        URL
        - `UserID` ID of the user
        - `PatientID` ID of the patient

    RESPONSE ATTRIBUTES
        - `UserID` ID of the user
        - `PatientID` ID of the patient
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove patient from user
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug('database.remove_patient_from_user(username=' + username + ', userID=' + user_id + ', patientID=' + patient_id + ')')
            db_response = database.remove_patient_from_user(username, user_id, patient_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of Users
# ************************************************************** #
# Patients
# For all
logger.debug("/api/v1.0/data/patients | GET, POST")
@app.route('/api/v1.0/data/patients', methods=['GET', 'POST'])
def patients():
    """
    GET: Returns list of patients

    POST: Creates an patient
        PAYLOAD
        - `name` Name of the patient

    RESPONSE ATTRIBUTES
        - `patientID` Patient ID
        - `extID` External ID to hide actual Patient ID
        - `rehabilitationSets` Array containing Patient IDs and External IDs of patients
        - `allowedOrganizations` List of organizations that have access to patients information
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []
    db_response = ''

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_patients(username=' + username + ')')
            db_response = database.list_patients(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST
    if request.method == 'POST':

        new_allowed_organizations = database.__organizationID_by_username__(username)
        user_to_attach_to_patient = database.__userID_by_username__(username)
        new_rehabilitation_sets = ''

        # Validate request
        # TODO: Because none of attributes are not mandatory posting without payload should be possible
        # TODO: Because Flask is not directly allowing POSTing without payload, should HTTP Method be changed?

        try:
            request.json
        except BadRequest:
            logger.debug('No JSON-payload, continuing anyway')
        else:
            # Attributes to parameters
            if 'allowedOrganizations' in request.json:
                new_allowed_organizations = request.json['allowedOrganizations']
            else:
                logger.debug(api_specifications.ERROR_JSON_ALLOWED_ORGANIZATIONS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'rehabilitationSets' in request.json:
                new_rehabilitation_sets = request.json['rehabilitationSets']
            else:
                logger.debug(api_specifications.ERROR_JSON_REHABILITATION_SET_IDS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'userToAttachToPatient' in request.json:
                user_to_attach_to_patient = request.json['userToAttachToPatient']
            else:
                logger.debug(api_specifications.ERROR_JSON_USER_TO_ATTACH_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

        # Database Query
        try:
            logger.debug('database.create_patient(username=' + username + ', allowedOrganizations=' + new_allowed_organizations + ', rehabilitationSets=' + new_rehabilitation_sets + ')')
            db_response = database.create_patient(username, new_allowed_organizations, new_rehabilitation_sets)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

        # Database Query #2
        try:
            new_patient_id = db_response['PatientID']

            logger.debug('database.add_patient_to_user(username=' + username + ', userID=' + user_to_attach_to_patient + ', patientID=' + new_patient_id + ')')
            db_response = database.add_patient_to_user(username, user_to_attach_to_patient, new_patient_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/patients/<string:patient_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/patients/<string:patient_id>', methods=['GET', 'PUT', 'DELETE'])
def patients_id(patient_id):
    """
    GET: Returns the patient by ID
        URL
        - `patientID` ID for the patient

    POST: Updates the patient by ID
        URL
        - `patientID` ID for the patient
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the patient by ID
        URL
        - `patientID` ID for the patient

    RESPONSE ATTRIBUTES
        - `patientID` Patient ID
        - `extID` External ID to hide actual Patient ID
        - `rehabilitationSets` Array containing Patient IDs and External IDs of patients
        - `allowedOrganizations` List of organizations that have access to patients information
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_patient(username=' + username + ', patientID=' + patient_id + ')')
            db_response = database.get_patient(username, patient_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update organization identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_patient(username=' + username + ', patientID=' + patient_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_patient(username, patient_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove organization identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_patient(username=' + username + ', patientID=' + patient_id + ')')
            db_response = database.delete_patient(username, patient_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/patients/<string:patient_id>/organizations | POST")
@app.route('/api/v1.0/data/patients/<string:patient_id>/organizations', methods=['POST'])
def patients_id_organizations(patient_id):
    """
    POST: Adds organizations to the patient
        URL
        - `patientID` ID for the patient
        PAYLOAD
        - `organizationID` ID for the organization

    RESPONSE ATTRIBUTES
        - 'patientID' Patient ID
        - 'organizationID' Organization ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add user to organization identified by organizationID
    if request.method == 'POST':

        organization_id_to_add = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'allowedOrganizations' not in request.json:
            abort(400, api_specifications.ERROR_JSON_ALLOWED_ORGANIZATION_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: Check that only one userID is provided (Multiple can be provided as CSV)
            organization_id_to_add = request.json['allowedOrganizations']

        # Database Query
        try:
            logger.debug('database.add_allowed_organization_to_patient(username=' + username + ', patientID=' + patient_id + ', organizationID=' + organization_id_to_add + ')')
            db_response = database.add_allowed_organization_to_patient(username, patient_id, organization_id_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/patients/<string:patient_id>/organizations/<string:organization_id> | DELETE")
@app.route('/api/v1.0/data/patients/<string:patient_id>/organizations/<string:organization_id>', methods=['DELETE'])
def patients_id_organizations_id(patient_id, organization_id):
    """
    DELETE: Removes the organization from the patient
        URL
        - `patientID` ID of the patient
        - `organizationID` ID of the organization

    RESPONSE ATTRIBUTES
        - `patientID` ID of the patient
        - `organizationID` ID of the organization
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove user from organization identified by organizationID
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug('database.remove_allowed_organization_from_patient(username=' + username + ', patientID=' + patient_id + ', organizationID=' + organization_id + ')')
            db_response = database.remove_allowed_organization_from_patient(username, patient_id, organization_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/patients/<string:patient_id>/rehabilitationSets | POST")
@app.route('/api/v1.0/data/patients/<string:patient_id>/rehabilitationSets', methods=['POST'])
def patients_id_rehabilitationsets(patient_id):
    """
    POST: Adds rehabilitation sets to the patient
        URL
        - `patientID` ID for the patient
        PAYLOAD
        - `rehabilitationSetID` ID for the rehabilitation set

    RESPONSE ATTRIBUTES
        - 'patientID' Patient ID
        - 'rehabilitationSetID' rehabilitationSet ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add user to organization identified by organizationID
    if request.method == 'POST':

        rehabilitationset_id_to_add = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'rehabilitationSetIDs' not in request.json:
            abort(400, api_specifications.ERROR_JSON_REHABILITATION_SET_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: Check that only one userID is provided, (Multiple can be provided as CSV)
            rehabilitationset_id_to_add = request.json['rehabilitationSetIDs']

        # Database Query
        try:
            logger.debug('database.add_rehabilitation_set_to_patient(username=' + username + ', patientID=' + patient_id + ', rehabilitationSetID=' + rehabilitationset_id_to_add + ')')
            db_response = database.add_rehabilitation_set_to_patient(username, patient_id, rehabilitationset_id_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/patients/<string:patient_id>/rehabilitationSets/<string:rehabilitation_set_id> | DELETE")
@app.route('/api/v1.0/data/patients/<string:patient_id>/rehabilitationSets/<string:rehabilitation_set_id>', methods=['DELETE'])
def patients_id_rehabilitationsets_id(patient_id, rehabilitation_set_id):
    """
    DELETE: Removes the rehabilitation set from the patient
        URL
        - 'patientID' Patient ID
        - 'rehabilitationSetID' rehabilitationSet ID

    RESPONSE ATTRIBUTES
        - 'patientID' Patient ID
        - 'rehabilitationSetID' rehabilitationSet ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove user from organization identified by organizationID
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug('database.remove_rehabilitation_set_from_patient(username=' + username + ', patientID=' + patient_id + ', rehabilitationSetID=' + rehabilitation_set_id + ')')
            db_response = database.remove_rehabilitation_set_from_patient(username, patient_id, rehabilitation_set_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of Patients
# ************************************************************** #
# RehabilitationSets
# For all
logger.debug("/api/v1.0/data/rehabilitationSets | GET, POST")
@app.route('/api/v1.0/data/rehabilitationSets', methods=['GET', 'POST'])
def rehabilitationsets():
    """
    GET: Returns list of rehabilitationSets

    POST: Creates a rehabilitationSet and adds created rehabilitationSet to patient
        PAYLOAD
        - `patientID` Patient ID
        - `patientInformationID` Patient Information ID
        - `patientConditionIDs` PatientCondition ID - OPTIONAL
        - `exerciseResultIDs` ExerciseResult ID - OPTIONAL

    RESPONSE ATTRIBUTES
        - `rehabilitationSetID` Rehabilitation Set ID
        - `patientInformationID` Patient Information ID
        - `patientConditionIDs` List containing PatientCondition IDs
        - `allowedOrganizations` List of Organization IDs
        - `exerciseResultIDs` List of ExerciseResult IDs
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_rehabilitationsets(username=' + username + ')')
            db_response = database.list_rehabilitationsets(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST
    # TODO: POST -method should also be able to handle patientCondition and patientInformation creation
    if request.method == 'POST':

        new_organization_to_attach = database.__organizationID_by_username__(username)
        new_patient_information_id = ''
        new_patient_condition_ids = ''
        new_exercise_result_ids = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'patientID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_PATIENT_ID_NOT_PRESENT)
        elif 'patientInformationID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_PATIENTINFORMATION_ID_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_patient_information_id = request.json['patientInformationID']
            patient_id_to_attach = request.json['patientID']

            if 'patientConditionIDs' in request.json:
                new_patient_condition_ids = request.json['patientConditionIDs']
            else:
                logger.debug(api_specifications.ERROR_JSON_PATIENTCONDITION_IDS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'exerciseResultIDs' in request.json:
                new_exercise_result_ids = request.json['exerciseResultIDs']
            else:
                logger.debug(api_specifications.ERROR_JSON_EXERCISERESULT_IDS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'allowedOrganizations' in request.json:
                new_organization_to_attach = request.json['allowedOrganizations']
            else:
                logger.debug(api_specifications.ERROR_JSON_ALLOWED_ORGANIZATIONS_NOT_PRESENT + api_specifications.ERROR_USING_USERS_OWN_ORGANIZATION)

        # Database Query
        try:
            logger.debug('database.create_rehabilitationset(username=' + username + ', allowedOrganizations=' + new_organization_to_attach + ', patientConditionIDs=' + new_patient_condition_ids + ', patientInformationID=' + new_patient_information_id + ', exerciseResultIDs=' + new_exercise_result_ids + ')')
            db_response = database.create_rehabilitationset(username=username, allowedOrganizations=new_organization_to_attach, patientConditionIDs=new_patient_condition_ids, patientInformationID=new_patient_information_id, exerciseResultIDs=new_exercise_result_ids)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

        # Database Query #2
        try:
            new_rehabilitationset_id = db_response['RehabilitationSetID']

            logger.debug('database.add_rehabilitation_set_to_patient(username=' + username + ', patientID=' + patient_id_to_attach + ', rehabilitationSetID=' + new_rehabilitationset_id + ')')
            db_response = database.add_rehabilitation_set_to_patient(username, patient_id_to_attach, new_rehabilitationset_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitationset_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitationset_id>', methods=['GET', 'PUT', 'DELETE'])
def rehabilitationsets_id(rehabilitationset_id):
    """
    GET: Returns the rehabilitationSet by ID
        URL
        - `patientID` ID for the rehabilitationSet

    POST: Updates the rehabilitationSet by ID
        URL
        - `patientID` ID for the rehabilitationSet
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the rehabilitationSet by ID
        URL
        - `patientID` ID for the rehabilitationSet

    RESPONSE ATTRIBUTES
        - `rehabilitationSetID` Rehabilitation Set ID
        - `patientInformationID` Patient Information ID
        - `patientConditionIDs` List containing PatientCondition IDs
        - `allowedOrganizations` List of allowed Organization IDs
        - `exerciseResultIDs` List of allowed ExerciseResult IDs
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_rehabilitationset(username=' + username + ', rehabilitationSetID=' + rehabilitationset_id + ')')
            db_response = database.get_rehabilitationset(username, rehabilitationset_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update organization identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_rehabilitationset(username=' + username + ', patientConditionID=' + rehabilitationset_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_rehabilitationset(username, rehabilitationset_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove organization identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_rehabilitationset(username=' + username + ', patientConditionID=' + rehabilitationset_id + ')')
            db_response = database.delete_rehabilitationset(username, rehabilitationset_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitationset_id>/manage/exerciseResults | POST")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitationset_id>/manage/exerciseResults', methods=['POST'])
def rehabilitationsets_id_exerciseresults(rehabilitationset_id):
    """
    POST: Appends exerciseResult to the rehabilitationSet
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        PAYLOAD
        - `exerciseResultID` ID for the ExerciseResult

    RESPONSE ATTRIBUTES
        - `rehabilitationSetID` Rehabilitation Set ID
        - `ExerciseResultID` Exercise Result ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add patients to user
    if request.method == 'POST':

        exerciseresult_id_to_add = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'exerciseResultID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: Check that only one patientID is provided (Multiple can be provided as CSV)
            exerciseresult_id_to_add = request.json['exerciseResultID']

        # Database Query
        try:
            logger.debug('database.add_exerciseresult_to_rehabilitationset(username=' + username + ', rehabilitationSetID=' + rehabilitationset_id + ', exerciseResultID=' + exerciseresult_id_to_add + ')')
            db_response = database.add_exerciseresult_to_rehabilitationset(username, rehabilitationset_id, exerciseresult_id_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitationset_id>/manage/exerciseResults/<string:exerciseresult_id> | DELETE")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitationset_id>/manage/exerciseResults/<string:exerciseresult_id>', methods=['DELETE'])
def rehabilitationsets_id_exerciseresults_id(rehabilitationset_id, exerciseresult_id):
    """
    DELETE: Removes exerciseResult from rehabilitationSet
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `exerciseResultID` ID for the ExerciseResult

    RESPONSE ATTRIBUTES
        - `rehabilitationSetID` Rehabilitation Set ID
        - `ExerciseResultID` Exercise Result ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove patient from user
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug('database.remove_exerciseresult_from_rehabilitationset(username=' + username + ', rehabilitationSetID=' + rehabilitationset_id + ', exerciseResultID=' + exerciseresult_id + ')')
            db_response = database.remove_exerciseresult_from_rehabilitationset(username, rehabilitationset_id, exerciseresult_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of RehabilitationSets
# ************************************************************** #
# Patient Infromation
logger.debug("/api/v1.0/data/rehabilitationSets/patientInformation | POST")
@app.route('/api/v1.0/data/rehabilitationSets/patientInformation', methods=['POST'])
def patientinformation():
    # def patientinformation(rehabilitation_set_id):
    """
    POST: Creates a patientInformation
        PAYLOAD
        - `bodyWeight` Weight of patient at time when rehabilitation was started
        - `bodyHeight` Height of patient at time when rehabilitation was started
        - `upperBodyDominantSide` Dominant side of upper body | ENUM[Right, Left]
        - `lowerBodyDominantSide` Dominant side of lower body | ENUM[Right, Left]
        - `gender` Gender of the patient | ENUM[Male, Female, None], defaults to None
        - `birthYear` Birth year of the patient

    RESPONSE ATTRIBUTES
        - `patientInformationID` patientInformation ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []
    db_response = ''

    # POST to create organization
    if request.method == 'POST':

        new_organization_to_attach = database.__organizationID_by_username__(username)
        new_body_weight = '0'
        new_body_height = '0'
        new_upper_body_dominant_side = ''
        new_lower_body_dominant_side = ''
        new_gender = 'None'
        new_birth_year = '0'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'bodyWeight' not in request.json:
            abort(400, api_specifications.ERROR_JSON_BODY_WEIGHT_NOT_PRESENT)
        elif 'bodyHeight' not in request.json:
            abort(400, api_specifications.ERROR_JSON_BODY_HEIGHT_NOT_PRESENT)
        elif 'upperBodyDominantSide' not in request.json:
            abort(400, api_specifications.ERROR_JSON_UPPER_BODY_DOMINANT_SIDE_NOT_PRESENT)
        elif 'lowerBodyDominantSide' not in request.json:
            abort(400, api_specifications.ERROR_JSON_LOWER_BODY_DOMINANT_SIDE_NOT_PRESENT)
        elif 'birthYear' not in request.json:
            abort(400, api_specifications.ERROR_JSON_BIRTH_YEAR_NOT_PRESENT)
        elif 'gender' not in request.json:
            abort(400, api_specifications.ERROR_JSON_GENDER_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_body_weight = request.json['bodyWeight']
            new_body_height = request.json['bodyHeight']
            new_upper_body_dominant_side = request.json['upperBodyDominantSide']
            new_lower_body_dominant_side = request.json['lowerBodyDominantSide']
            new_gender = request.json['gender']
            new_birth_year = request.json['birthYear']

            if 'allowedOrganizations' in request.json:
                new_organization_to_attach = request.json['allowedOrganizations']
            else:
                logger.debug(api_specifications.ERROR_JSON_ALLOWED_ORGANIZATIONS_NOT_PRESENT + api_specifications.ERROR_USING_USERS_OWN_ORGANIZATION)

        # Database Query
        try:
            logger.debug('database.create_patientinformation(username=' + username + ', allowedOrganizations=' + new_organization_to_attach + ', bodyWeight=' + new_body_weight + ', bodyHeight=' + new_body_height + ', upperBodyDominantSide=' + new_upper_body_dominant_side + ', lowerBodyDominantSide=' + new_lower_body_dominant_side + ', birthYear=' + new_birth_year + ', gender=' + new_gender + ')')
            db_response = database.create_patientinformation(username, new_organization_to_attach, new_body_weight, new_body_height, new_upper_body_dominant_side, new_lower_body_dominant_side, new_birth_year, new_gender)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# PatientInformation
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/patientInformation/<string:patient_information_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/patientInformation/<string:patient_information_id>', methods=['GET', 'PUT', 'DELETE'])
def patientinformation_id(rehabilitation_set_id, patient_information_id):
    """
    GET: Returns the patientInformation by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `PatientInformationID` ID for the patientInformation

    POST: Updates the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `PatientInformationID` ID for the patientInformation
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `PatientInformationID` ID for the patientInformation

    RESPONSE ATTRIBUTES
        - `patientInformationID` patientInformation ID
        - `bodyHeight` Height of patient at time when rehabilitation was started
        - `upperBodyDominantSide` Dominant side of upper body | ENUM[Right, Left]
        - `lowerBodyDominantSide` Dominant side of lower body | ENUM[Right, Left]
        - `gender` Gender of the patient | ENUM[Male, Female, None], defaults to None
        - `birthYear` Birth year of the patient
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_patientinformation(username=' + username + ', patientInformationID=' + patient_information_id + ')')
            db_response = database.get_patientinformation(username, patient_information_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update organization identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_patientinformation(username=' + username + ', patientInformationID=' + patient_information_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_patientinformation(username, patient_information_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove organization identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_patientinformation(username=' + username + ', patientInformationID=' + patient_information_id + ')')
            db_response = database.delete_patientinformation(username, patient_information_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End fo Patient Infromation
# ************************************************************** #
# PatientCondition
logger.debug("/api/v1.0/data/rehabilitationSets/patientConditions | POST")
@app.route('/api/v1.0/data/rehabilitationSets/patientConditions', methods=['POST'])
def patientconditions():
    # def patientconditions(rehabilitation_set_id):
    """
    POST: Creates a PatientCondition
        PAYLOAD
        - `label` Short title/description of condition
        - `description` Longer description of condition - OPTIONAL
        - `officialMedicalCode` ICD-10 classification code - OPTIONAL

    RESPONSE ATTRIBUTES
        - `PatientConditionID` PatientCondition ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []
    db_response = ''

    # POST to create organization
    if request.method == 'POST':

        new_organization_to_attach = database.__organizationID_by_username__(username)
        new_label = ''
        new_description = ''
        new_official_medical_code = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'label' not in request.json:
            abort(400, api_specifications.ERROR_JSON_LABEL_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_label = request.json['label']

            if 'allowedOrganizations' in request.json:
                new_organization_to_attach = request.json['allowedOrganizations']
            else:
                logger.debug(api_specifications.ERROR_JSON_ALLOWED_ORGANIZATIONS_NOT_PRESENT + api_specifications.ERROR_USING_USERS_OWN_ORGANIZATION)

            if 'description' in request.json:
                new_description = request.json['description']
            else:
                logger.debug(api_specifications.ERROR_JSON_DESCRIPTION_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

            if 'officialMedicalCode' in request.json:
                new_official_medical_code = request.json['officialMedicalCode']
            else:
                logger.debug(api_specifications.ERROR_JSON_OFFICAL_MEDICAL_CODE_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

        # Database Query
        try:
            logger.debug('database.create_patientcondition(username=' + username + ', allowedOrganizations=' + new_organization_to_attach + ', label=' + new_label + ', description=' + new_description + ', officialMedicalCode=' + new_official_medical_code + ')')
            db_response = database.create_patientcondition(username, new_organization_to_attach, new_label, new_description, new_official_medical_code)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# PatientCondition
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/patientConditions/<string:patient_condition_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/patientConditions/<string:patient_condition_id>', methods=['GET', 'PUT', 'DELETE'])
def patientconditions_id(rehabilitation_set_id, patient_condition_id):
    """
    GET: Returns the PatientCondition by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `PatientConditionID` ID for the PatientCondition

    POST: Updates the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `PatientConditionID` ID for the PatientCondition
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `PatientConditionID` ID for the PatientCondition

    RESPONSE ATTRIBUTES
        - `PatientConditionID` PatientCondition ID
        - `label` Short title/description of condition
        - `description` Longer description of condition
        - `officialMedicalCode` ICD-10 classification code
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_patientcondition(username=' + username + ', patientConditionID=' + patient_condition_id + ')')
            db_response = database.get_patientcondition(username, patient_condition_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update organization identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_patientcondition(username=' + username + ', patientConditionID=' + patient_condition_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_patientcondition(username, patient_condition_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove organization identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_patientcondition(username=' + username + ', patientConditionID=' + patient_condition_id + ')')
            db_response = database.delete_patientcondition(username, patient_condition_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of PatientCondition
# ************************************************************** #
# ExerciseResults
# For all
#  TODO: list_exerciseresults_by_exercise(username, exerciseID)
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults | POST")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults', methods=['POST'])
def exerciseresults(rehabilitation_set_id):
    """
    POST: Creates an exerciseResult
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        PAYLOAD
        - `exerciseID` Exercise ID to bind to ExerciseResult
        - `deviceID` Device ID to bind to ExerciseResult
        - `dataSamples` Data samples of the exercise (as JSON)
        - `started` Unix time (Epoch time)
        - `ended` Unix time (Epoch time)
        - `settings` Settings that were used during exercise (as JSON)
        - `values` Pre-calculated values like average, minimum and maximum values. Content can be device/sensor specific (as JSON)
        - `progress` Progress of the exercise - OPTIONAL


    RESPONSE ATTRIBUTES
        - `rehabilitationSetID` Rehabilitation Set ID
        - `exerciseResultID` Exercise Result ID
        - `dataID` Data ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []
    # db_parameters = {}
    # db_responses = {}
    # db_response = ''
    # data_id_list = []
    # data_id_list_str = ''

    # POST
    if request.method == 'POST':

        new_organization_id = database.__organizationID_by_username__(username)
        new_exercise_id = ''
        new_device_id = ''
        new_data_samples = ''
        new_started = ''
        new_ended = ''
        new_settings = ''
        new_values = ''
        new_progress = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'exerciseID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISE_ID_NOT_PRESENT)
        elif 'deviceID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_DEVICE_ID_NOT_PRESENT)
        elif 'dataSamples' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_DATA_NOT_PRESENT)
        elif 'started' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_STARTED_NOT_PRESENT)
        elif 'ended' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_ENDED_NOT_PRESENT)
        elif 'settings' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_SETTINGS_NOT_PRESENT)
        elif 'values' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISERESULT_VALUES_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_exercise_id = request.json['exerciseID']
            new_device_id = request.json['deviceID']
            new_started = request.json['started']
            new_ended = request.json['ended']

            try:
                new_data_samples = request.json['dataSamples']
                logger.debug("dataSamples as " + repr(type(new_data_samples)))
                if isinstance(new_data_samples, dict):
                    new_data_samples = json.dumps(new_data_samples)
                    logger.debug("dataSamples converted to str")
                elif isinstance(new_data_samples, list):
                    new_data_samples = json.dumps(new_data_samples)
                    logger.debug("dataSamples converted to str")
                elif isinstance(new_data_samples, str) or isinstance(new_data_samples, unicode):
                    logger.debug("dataSamples: no conversion")
            except Exception as argument:
                abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

            try:
                new_settings = request.json['settings']
                logger.debug("settings as " + repr(type(new_settings)))
                if isinstance(new_settings, dict):
                    new_settings = json.dumps(new_settings)
                    logger.debug("settings converted to str")
                elif isinstance(new_settings, list):
                    new_settings = json.dumps(new_settings)
                    logger.debug("settings converted to str")
                elif isinstance(new_settings, str) or isinstance(new_settings, unicode):
                    logger.debug("settings: no conversion")
            except Exception as argument:
                abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

            try:
                new_values = request.json['values']
                logger.debug("values as " + repr(type(new_values)))
                if isinstance(new_values, dict):
                    new_values = json.dumps(new_values)
                    logger.debug("values converted to str")
                elif isinstance(new_values, list):
                    new_values = json.dumps(new_values)
                    logger.debug("values converted to str")
                elif isinstance(new_values, str) or isinstance(new_values, unicode):
                    logger.debug("values: no conversion")
            except Exception as argument:
                abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

            if 'progress' in request.json:
                new_progress = request.json['progress']
                logger.debug("progress as " + repr(type(new_progress)))
                if isinstance(new_progress, dict):
                    new_progress = json.dumps(new_progress)
                    logger.debug("progress converted to str")
                elif isinstance(new_progress, list):
                    new_progress = json.dumps(new_progress)
                    logger.debug("progress converted to str")
                elif isinstance(new_progress, str) or isinstance(new_progress, unicode):
                    logger.debug("progress: no conversion")
            else:
                logger.debug(api_specifications.ERROR_JSON_EXERCISERESULT_PROGRESS_NOT_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

        # Database Query
        try:
            logger.debug('database.create_data(allowedOrganizations=' + new_organization_id + ', username=' + username + ', deviceID=' + new_device_id + ', samples=' + new_data_samples + ')')
            db_response = database.create_data(new_organization_id, username, new_device_id, new_data_samples)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # TODO: How should status codes be handled when multiple queries will be executed?
        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

        # Database Query #2
        try:
            new_data_id = db_response['dataID']

            logger.debug('database.create_exerciseresult(username=' + username + ', exerciseID=' + new_exercise_id + ', dataIDs=' + new_data_id + ', allowedOrganizations=' + new_organization_id + ', started=' + new_started + ', ended=' + new_ended + ', settings=' + new_settings + ', values=' + new_values + ', progress=' + new_progress + ')')
            db_response = database.create_exerciseresult(username, new_exercise_id, new_data_id, new_organization_id, new_started, new_ended, new_settings, new_values, new_progress)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Database response to return content
        return_content.append(db_response)

        # Database Query #3
        try:
            new_exerciseresult_id = db_response['ExerciseResultID']

            logger.debug('database.create_exerciseresult(username=' + username + ', rehabilitationSetID=' + rehabilitation_set_id + ', userID=' + new_exerciseresult_id + ')')
            db_response = database.add_exerciseresult_to_rehabilitationset(username, rehabilitation_set_id, new_exerciseresult_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Database response to return content
        return_content.append(db_response)

    # Response
    # TODO: Not completely following Swagger API-documentation
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id> | GET, PUT")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>', methods=['GET', 'PUT'])
def exerciseresults_id(rehabilitation_set_id, exercise_result_id):
    """
    GET: Returns the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `exerciseResultID` ID for the ExerciseResult

    POST: Updates the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `exerciseResultID` ID for the ExerciseResult
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the patient by ID
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `exerciseResultID` ID for the ExerciseResult

    RESPONSE ATTRIBUTES
        - `exerciseResultID` ExerciseResult ID
        - `exerciseID` Exercise ID
        - `dataIDs` DataIDs related to ExerciseResult
        - `dataSamples` Data samples of the exercise (as JSON)
        - `started` Unix time (Epoch time)
        - `ended` Unix time (Epoch time)
        - `settings` Settings that were used during exercise (as JSON)
        - `values` Pre-calculated values like average, minimum and maximum values. Content can be device/sensor specific (as JSON)
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_exerciseresult(username=' + username + ', exerciseResultID=' + exercise_result_id + ')')
            db_response = database.get_exerciseresult(username, exercise_result_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update user identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_exerciseresult(username=' + username + ', exerciseResultID=' + exercise_result_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_exerciseresult(username, exercise_result_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/appendDataID | POST")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/appendDataID', methods=['POST'])
def exerciseresults_id_append_data_id(rehabilitation_set_id, exercise_result_id):
    """
    POST: Appends dataset to the exerciseResult
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `exerciseResultID` ID for the ExerciseResult
        PAYLOAD
        - `dataID` data ID to append to the ExerciseResult


    RESPONSE ATTRIBUTES
        - `DataID` Data ID
        - `ExerciseResultID` Exercise Result ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST to add patients to user
    if request.method == 'POST':

        data_id_to_add = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'dataID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DATA_IDS_NOT_PRESENT)
        else:
            # Attributes to parameters
            # TODO: Check that only one patientID is provided (Multiple can be provided as CSV)
            data_id_to_add = request.json['dataID']

        # Database Query
        try:
            logger.debug('database.add_data_to_exerciseresult(username=' + username + ', exerciseResultID=' + exercise_result_id + ', dataID=' + data_id_to_add + ')')
            db_response = database.add_data_to_exerciseresult(username, exercise_result_id, data_id_to_add)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/removeDataID/<string:data_id> | DELETE")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/removeDataID/<string:data_id>', methods=['DELETE'])
def exerciseresults_id_remove_data_id(rehabilitation_set_id, exercise_result_id, data_id):
    """
    DELETE: Removes dataset from exerciseResult
        URL
        - `rehabilitationSetID` ID for the rehabilitationSet
        - `exerciseResultID` ID for the ExerciseResult
        - `dataID` data ID to remove from ExerciseResult


    RESPONSE ATTRIBUTES
        - `DataID` Rehabilitation Set ID
        - `ExerciseResultID` Exercise Result ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # DELETE to remove patient from user
    if request.method == 'DELETE':

        # Database Query
        try:
            logger.debug('database.remove_dataid_from_exerciseresult(username=' + username + ', exerciseResultID=' + exercise_result_id + ', dataID=' + data_id + ')')
            db_response = database.remove_dataid_from_exerciseresult(username, exercise_result_id, data_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of ExerciseResults
# ************************************************************** #
# Data
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/data | POST")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/data', methods=['POST'])
def datas(rehabilitation_set_id, exercise_result_id):
    """
    POST: Creates an data entry
        PAYLOAD
        - `deviceID` Device ID
        - `samples` Samples of data entry (as JSON)

    RESPONSE ATTRIBUTES
        - 'dataID' Data entry ID
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # POST
    if request.method == 'POST':

        allowed_organization_id = database.__organizationID_by_username__(username)
        new_device_id = ''
        new_samples = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'deviceID' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_ID_NOT_PRESENT)
        elif 'samples' not in request.json:
            abort(400, api_specifications.ERROR_JSON_SAMPLES_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_device_id = request.json['deviceID']
            try:
                new_samples = json.dumps(request.json['samples'])
            except Exception as argument:
                abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database Query
        try:
            logger.debug('database.create_data(allowedOrganizations=' + allowed_organization_id + ', username=' + username + ', deviceID=' + new_device_id + ', samples=' + new_samples + ')')
            db_response = database.create_data(allowed_organization_id, username, new_device_id, new_samples)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # TODO: How should status codes be handled when multiple queries will be executed?
        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/data/<string:data_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/rehabilitationSets/<string:rehabilitation_set_id>/exerciseResults/<string:exercise_result_id>/data/<string:data_id>', methods=['GET', 'PUT', 'DELETE'])
def datas_id(rehabilitation_set_id, exercise_result_id, data_id):
    """
    GET: Returns the data entry by ID
        URL
        - `patientID` ID for the data entry

    POST: Updates the data entry by ID
        URL
        - `patientID` ID for the data entry
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the data entry by ID
        URL
        - `patientID` ID for the data entry

    RESPONSE ATTRIBUTES
        - `dataID` Data ID
        - `deviceID` Device ID
        - `samples` Samples of data entry
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_data(username=' + username + ', dataID=' + data_id + ')')
            db_response = database.get_data(username, data_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update user identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_data(username=' + username + ', dataID=' + data_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_data(username, data_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove user identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_data(username=' + username + ', dataID=' + data_id + ')')
            db_response = database.delete_data(username, data_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# TODO: Manage allowedOrganizations
# End of Data
# ************************************************************** #
# Exercise
# For all
logger.debug("/api/v1.0/data/exercises | GET, POST")
@app.route('/api/v1.0/data/exercises', methods=['GET', 'POST'])
def exercises():
    """
    GET: Returns list of exercises

    POST: Creates an exercise
        PAYLOAD
        - `name` Name of the exercise
        - `description` Description of the exercise
        - `settings` Settings of the exercise (as JSON)

    RESPONSE ATTRIBUTES
        - `exerciseID` Exercise ID
        - `name` Name of the exercise
        - `description` Description of the exercise
        - `settings` Settings of the exercise (as JSON)
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_exercises(username=' + username + ')')
            db_response = database.list_exercises(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST
    if request.method == 'POST':

        allowed_organization_id = database.__organizationID_by_username__(username)
        new_name = ''
        new_description = ''
        new_settings = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'name' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISE_NAME_NOT_PRESENT)
        elif 'description' not in request.json:
            abort(400, api_specifications.ERROR_JSON_EXERCISE_DESCRIPTION_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_name = request.json['name']
            new_description = request.json['description']

            if 'settings' in request.json:
                new_settings = request.json['settings']
            else:
                logger.debug(api_specifications.ERROR_JSON_EXERCISE_SETTINGS_PRESENT + api_specifications.ERROR_USING_DEFAULT_VALUE)

        # Database Query
        try:
            logger.debug('database.create_exercise(username=' + username + ', allowedOrganizations=' + allowed_organization_id + ', name=' + new_name + ', description=' + new_description + ', settings=' + new_settings + ')')
            db_response = database.create_exercise(username, allowed_organization_id, new_name, new_description, new_settings)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # TODO: How should status codes be handled when multiple queries will be executed?
        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/exercises/<string:exercise_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/exercises/<string:exercise_id>', methods=['GET', 'PUT', 'DELETE'])
def exercises_id(exercise_id):
    """
    GET: Returns the exercise by ID
        URL
        - `exerciseID` ID for the exercise

    POST: Updates the exercise by ID
        URL
        - `exerciseID` ID for the exercise
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the exercise by ID
        URL
        - `exerciseID` ID for the exercise

    RESPONSE ATTRIBUTES
        - `exerciseID` Exercise ID
        - `name` Name of the exercise
        - `description` Description of the exercise
        - `settings` Settings of the exercise (as JSON)
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_exercise(username=' + username + ', exerciseID=' + exercise_id + ')')
            db_response = database.get_exercise(username, exercise_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update user identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_exercise(username=' + username + ', exerciseID=' + exercise_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_exercise(username, exercise_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove user identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_exercise(username=' + username + ', exerciseID=' + exercise_id + ')')
            db_response = database.delete_exercise(username, exercise_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of Exercise
# ************************************************************** #
# Devices
# For all
logger.debug("/api/v1.0/data/devices | GET, POST")
@app.route('/api/v1.0/data/devices', methods=['GET', 'POST'])
def devices():
    """
    GET: Returns list of devices

    POST: Creates an device
        PAYLOAD
        - `name` Name of the device
        - `type` Type of the device
        - `description` Description of the device
        - `axisCount` Number of axes that produce data
        - `valueUnit` Unit of produced data
        - `valueUnitAbbreviation` Abbreviation of the unit
        - `defaultValue` Default value of data
        - `maximumValue` Maximum value of data
        - `minimumValue` Minimum value of data

    RESPONSE ATTRIBUTES
        - `deviceID` Device ID
        - `name` Name of the device
        - `type` Type of the device
        - `description` Description of the device
        - `axisCount` Number of axes that produce data
        - `valueUnit` Unit of produced data
        - `valueUnitAbbreviation` Abbreviation of the unit
        - `defaultValue` JSON array of default values of data for each axis
        - `maximumValue` Maximum value of data
        - `minimumValue` Minimum value of data
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_devices(username=' + username + ')')
            db_response = database.list_devices(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # POST
    if request.method == 'POST':

        allowed_organization_id = database.__organizationID_by_username__(username)
        new_name = ''
        new_type = ''
        new_description = ''
        new_axis_count = ''
        new_value_unit = ''
        new_value_unit_abbreviation = ''
        new_default_value = ''
        new_maximum_value = ''
        new_minimum_value = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'name' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_NAME_NOT_PRESENT)
        elif 'type' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_TYPE_NOT_PRESENT)
        elif 'description' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_DESCRIPTION_NOT_PRESENT)
        elif 'axisCount' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_AXIS_COUNT_NOT_PRESENT)
        elif 'valueUnit' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_VALUE_UNIT_NOT_PRESENT)
        elif 'valueUnitAbbreviation' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_VALUE_UNIT_ABB_NOT_PRESENT)
        elif 'defaultValue' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_DEFAULT_VALUE_NOT_PRESENT)
        elif 'maximumValue' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_MAXIMUM_VALUE_NOT_PRESENT)
        elif 'minimumValue' not in request.json:
            abort(400, api_specifications.ERROR_JSON_DEVICE_MININIMUM_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            new_name = request.json['name']
            new_type = request.json['type']
            new_description = request.json['description']
            # TODO: Should following attribute be parsed somehow ( isInteger?? )
            new_axis_count = request.json['axisCount']
            new_value_unit = request.json['valueUnit']
            new_value_unit_abbreviation = request.json['valueUnitAbbreviation']
            # TODO: Should following attributes be parsed somehow ( isDouble?? )
            new_default_value = request.json['defaultValue']
            new_maximum_value = request.json['maximumValue']
            new_minimum_value = request.json['minimumValue']

        # Database Query
        try:
            logger.debug('database.create_device(username=' + username + ', allowedOrganizations=' + allowed_organization_id + ', name=' + new_name + ', type=' + new_type + ', description=' + new_description + ', axisCount=' + new_axis_count + ', valueUnit=' + new_value_unit + ', valueUnitAbbreviation=' + new_value_unit_abbreviation + ', defaultValue=' + new_default_value + ', maximumValue=' + new_maximum_value + ', minimumValue=' + new_minimum_value + ')')
            db_response = database.create_device(username, allowed_organization_id, new_name, new_type, new_description, new_axis_count, new_value_unit, new_value_unit_abbreviation, new_default_value, new_maximum_value, new_minimum_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# For one
logger.debug("/api/v1.0/data/devices/<string:device_id> | GET, PUT, DELETE")
@app.route('/api/v1.0/data/devices/<string:device_id>', methods=['GET', 'PUT', 'DELETE'])
def devices_id(device_id):
    """
    GET: Returns the device by ID
        URL
        - `deviceID` ID for the device

    POST: Updates the device by ID
        URL
        - `deviceID` ID for the device
        PAYLOAD
        - `field` Field name to update
        - `value` New value for filed to update

    DELETE: Removes the device by ID
        URL
        - `deviceID` ID for the device

    RESPONSE ATTRIBUTES
        - `deviceID` Device ID
        - `name` Name of the device
        - `type` Type of the device
        - `description` Description of the device
        - `axisCount` Number of axes that produce data
        - `valueUnit` Unit of produced data
        - `valueUnitAbbreviation` Abbreviation of the unit
        - `defaultValue` Default value of data
        - `maximumValue` Maximum value of data
        - `minimumValue` Minimum value of data
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_device(username=' + username + ', deviceID=' + device_id + ')')
            db_response = database.get_device(username, device_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # PUT to update user identified by ID
    if request.method == 'PUT':

        field_to_update = 'Not determined'
        update_with_value = 'Not determined'

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)
        elif 'field' not in request.json:
            abort(400, api_specifications.ERROR_JSON_FIELD_NOT_PRESENT)
        elif 'value' not in request.json:
            abort(400, api_specifications.ERROR_JSON_VALUE_NOT_PRESENT)
        else:
            # Attributes to parameters
            field_to_update = request.json['field']
            update_with_value = request.json['value']

        # Database Query
        try:
            logger.debug('database.update_device(username=' + username + ', deviceID=' + device_id + ', field=' + field_to_update + ', value=' + update_with_value + ')')
            db_response = database.update_device(username, device_id, field_to_update, update_with_value)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # DELETE to remove user identified by ID
    if request.method == 'DELETE':
        try:
            logger.debug('database.delete_device(username=' + username + ', deviceID=' + device_id + ')')
            db_response = database.delete_device(username, device_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# TODO: Manage allowedOrganizations (add / remove)

# End of Devices
# ************************************************************** #
# Analysis
logger.debug("Defining analysis_tasks()")
@app.route('/api/v1.0/analysis/analysisTasks', methods=['GET'])
def analysis_tasks():
    """
    GET: Returns list of analysisTasks

    RESPONSE ATTRIBUTES
        - `AnalysisTasks` List of analysis tasks
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.list_analysistasks(username=' + username + ')')
            db_response = database.list_analysistasks(username)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("Defining analysis_task(analysis_task_id)")
@app.route('/api/v1.0/analysis/analysisTasks/<string:analysis_task_id>', methods=['GET'])
def analysis_task(analysis_task_id):
    """
    GET: Returns the analysisTask by ID
        URL
        - `analysistaskID` ID for the analysisTask

    RESPONSE ATTRIBUTES
        - `configParams` The config parameters used in task
        - `notification` The notification method used in task
        - `taskName` The name of the task
        - `username` The user who initiated the task
        - `moduleName` The module who runs/runned the task
        - `status` When the task started
        - `started` When the task started as Unix time (Epoch time)
        - `ended` When the task ended as Unix time (Epoch time)
        - `analysisResult` The result of the task
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':
        try:
            logger.debug('database.get_analysistask(username=' + username + ', analysis_task_id=' + analysis_task_id + ')')
            db_response = database.get_analysistask(username, analysis_task_id)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response validation
        db_response = api_specifications.validate_db_response(db_response)

        # Set status code of the response
        if 'status_code' in db_response:
            status = db_response['status_code']

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of Analysis Tasks


# Analysis Modules
logger.debug("Defining analysis_modules()")
@app.route('/api/v1.0/analysis/analysisModules', methods=['GET'])
def analysis_modules():
    """
    GET: Returns list of analysisModules

    RESPONSE ATTRIBUTES
        - `analysisModules` Array of all available analysismodules
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    # GET
    if request.method == 'GET':

        try:
            logger.debug('analysishandler.get_available_analysis_modules(username=' + username + ', database=DatabaseHandler)')
            return_content = analysishandler.get_available_analysis_modules(username, database)
            logger.debug('Return: ' + repr(return_content))

        except Exception as argument:
            return_content = {'Argument': repr(argument)}
            logger.debug('Exception with Argument: ' + repr(argument).replace("(u'", " | ").replace("',)", ""))
            status = 500

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response


logger.debug("Defining analysis_module_start(analysis_module_name)")
@app.route('/api/v1.0/analysis/analysisModules/<string:analysis_module_name>/start', methods=['POST'])
def analysis_module_start(analysis_module_name):
    """
    POST: Start analysisModule
        URL
        - `analysis_module_name` Name of the module that should perform the analysis
        PAYLOAD
        - `Settings` Settings for the analysis

    RESPONSE ATTRIBUTES
        - `status` Notification to show to user
    """

    # Init variables
    username = request.headers.get('username')
    status = 200
    return_content = []

    if request.method == 'POST':

        new_settings = ''

        # Validate request
        if not request.json:
            abort(400, api_specifications.ERROR_JSON_NOT_PRESENT)

        else:
            try:
                new_settings = json.dumps(request.json)
            except Exception as argument:
                abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database Query
        try:
            logger.debug('analysishandler.perform_analysis(username=' + username + ', moduleName=' + analysis_module_name + ', settings=' + new_settings + ', dbHandler=DatabaseHandler)')
            db_response = analysishandler.perform_analysis(username, analysis_module_name, request.json, database)
            logger.debug('Database Query Returned: ' + repr(db_response))

        except Exception as argument:
            logger.debug('Abort with: 500, ' + api_specifications.ERROR_DB_QUERY_FAILED)
            abort(500, api_specifications.ERROR_DB_QUERY_FAILED + ': ' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response decoding
        try:
            db_response = json.loads(db_response)
            db_response = json.dumps(db_response)
        except Exception as argument:
            abort(500, api_specifications.ERROR_DB_JSON_DECODE + ': 3' + repr(argument).replace("u'", "").replace("'", ""))

        # Database response to return content
        return_content.append(db_response)

    # Response
    response = api_specifications.generate_response(return_content, status)
    return response

# End of Analysis
# ************************************************************** #

if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0", port=8080, threaded=False)
