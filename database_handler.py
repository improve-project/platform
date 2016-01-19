# coding=utf-8
#__author__ = "Tommi Portti"

import time
import json
from models.AnalysisClass import AnalysisClass
from models.DeviceClass import DeviceClass
from models.ExerciseClass import ExerciseClass
from models.OrganizationClass import OrganizationClass
from models.PatientClass import PatientClass
from models.PatientConditionClass import PatientConditionClass
from models.PatientInformationClass import PatientInformationClass
from models.RehabilitationSetClass import RehabilitationSetClass
from models.UserGroupClass import UserGroupClass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.ExerciseResultClass import ExerciseResultClass
from models.UserClass import UserClass
from models.DataClass import DataClass



## The library-class responsible for all database related actions
class DatabaseHandler:



    ##The constructor.
    #The constructor initializes the database-connections that are needed for the operations
    def __init__(self):


        with open('databases.conf') as data_file:
            self.databaseData = json.load(data_file)

        self.userEngine = create_engine(
            'mysql+mysqldb://' + self.databaseData["user"]["username"] + ':' + self.databaseData["user"]["password"] + '@' +
            self.databaseData["user"]["server"] + '/' + self.databaseData["user"]["database"] + '', echo=True)

        self.patientEngine = create_engine(
            'mysql+mysqldb://' + self.databaseData["patient"]["username"] + ':' + self.databaseData["patient"][
                "password"] + '@' + self.databaseData["patient"]["server"] + '/' + self.databaseData["patient"][
                "database"] + '', echo=True)
        self.exerciseEngine = create_engine(
            'mysql+mysqldb://' + self.databaseData["exercise"]["username"] + ':' + self.databaseData["exercise"][
                "password"] + '@' + self.databaseData["exercise"]["server"] + '/' + self.databaseData["exercise"][
                "database"] + '', echo=True)

        self.sensorEngine = create_engine(
            'mysql+mysqldb://' + self.databaseData["sensor"]["username"] + ':' + self.databaseData["sensor"][
                "password"] + '@' + self.databaseData["sensor"]["server"] + '/' + self.databaseData["sensor"][
                "database"] + '', echo=True)

        self.analysisEngine = create_engine(
            'mysql+mysqldb://' + self.databaseData["analysis"]["username"] + ':' + self.databaseData["analysis"][
                "password"] + '@' + self.databaseData["analysis"]["server"] + '/' + self.databaseData["analysis"][
                "database"] + '', echo=True)


        self.userSession = sessionmaker(bind=self.userEngine)
        self.userSession = self.userSession()

        self.patientSession = sessionmaker(bind=self.patientEngine)
        self.patientSession = self.patientSession()

        self.exerciseSession = sessionmaker(bind=self.exerciseEngine)
        self.exerciseSession = self.exerciseSession()

        self.sensorSession = sessionmaker(bind=self.sensorEngine)
        self.sensorSession = self.sensorSession()

        self.analysisSession = sessionmaker(bind=self.analysisEngine)
        self.analysisSession = self.analysisSession()

    ##Find out if Organizations is allowed to access the Device by deviceID
    #Find out if an organizationID is contained within the allowedOrganizations of a Device identified by the deviceID
    #@param deviceID - The ID of the Data.
    #@param organizationID - The ID of the Organization to find.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __allowedOrganizations_in_deviceID__(self, deviceID, organizationID):
        try:
            device_query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID == deviceID).filter(DeviceClass.allowedOrganizations.contains(organizationID))
            self.sensorSession.commit()
            if len(device_query.all()) > 0:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.sensorSession.rollback()
            return "false"

    ##Find out if Organizations is allowed to access the Data by dataID
    #Find out if an organizationID is contained within the allowedOrganizations of a Data identified by the dataID
    #@param dataID - The ID of the Data.
    #@param organizationID - The ID of the Organization to find.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __allowedOrganizations_in_dataID__(self, dataID, organizationID):
        try:
            data_query = self.sensorSession.query(DataClass).filter(DataClass.dataID == dataID).filter(DataClass.allowedOrganizations.contains(organizationID))
            self.sensorSession.commit()
            if len(data_query.all()) >  0 :
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.sensorSession.rollback()
            return "false"

    ##Find out if Organizations is allowed to access the ExerciseResult by exerciseResultID
    #Find out if an organizationID is contained within the allowedOrganizations of a ExerciseResult identified by the exerciseResultID
    #@param exerciseResultID - The ID of the ExerciseResult.
    #@param organizationID - The ID of the Organization to find.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __allowedOrganization_in_exerciseResultID__(self, exerciseResultID, organizationID):
        try:
            exerciseresult_query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID == exerciseResultID).filter(ExerciseResultClass.allowedOrganizations.contains( organizationID))
            self.exerciseSession.commit()
            if len(exerciseresult_query.all()) >0:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.exerciseSession.rollback()
            return "false"

    ##Find out if Organizations is allowed to access the RehabilitationSet by rehabilitationSetID
    #Find out if an organizationID is contained within the allowedOrganizations of a RehabilitationSet identified by the rehabilitationSetID
    #@param rehabilitationSetID - The ID of the RehabilitationSet.
    #@param organizationID - The ID of the Organization to find.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __allowedOrganization_in_rehabilitationSetID__(self, rehabilitationSetID, organizationID):
        try:
            rehabilitationset_query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID == rehabilitationSetID).filter(RehabilitationSetClass.allowedOrganizations.contains(organizationID))
            self.exerciseSession.commit()
            if len(rehabilitationset_query.all()) >0:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.exerciseSession.rollback()
            return "false"

    ##Find out if Organizations is allowed to access the PatientInformation by patientInformationID
    #Find out if an organizationID is contained within the allowedOrganizations of a PatientInformation identified by the patientInformationID
    #@param patientInformationID - The ID of the PatientInformation.
    #@param organizationID - The ID of the Organization to find.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __allowedOrganization_in_patientInformationID__(self, patientInformationID, organizationID):
        try:
            patientinformation_query = self.exerciseSession.query(PatientInformationClass).filter(PatientInformationClass.patientInformationID == patientInformationID).filter(PatientInformationClass.allowedOrganizations.contains(organizationID))
            self.exerciseSession.commit()
            if len(patientinformation_query.all()) >0:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.exerciseSession.rollback()
            return "false"


    ##Find out if Organizations is allowed to access the PatientCondition by patientConditionID
    #Find out if an organizationID is contained within the allowedOrganizations of a PatientCondition identified by the patientConditionID
    #@param patientConditionID - The ID of the PatientCondition.
    #@param organizationID - The ID of the Organization to find.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __allowedOrganization_in_patientConditionID__(self, patientConditionID, organizationID):
        try:
            patientcondition_query = self.exerciseSession.query(PatientConditionClass).filter(PatientConditionClass.patientConditionID == patientConditionID).filter(PatientConditionClass.allowedOrganizations.contains(organizationID))
            self.exerciseSession.commit()
            if len(patientcondition_query.all()) >0:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.exerciseSession.rollback()
            return "false"

    ##Get a list of Organizations allowed to access the Patient by patientID
    #Get a list of Organizations allowed to access the Patient by patientID
    #@param patientID - The ID of the Patient.
    #@return A CSV-formatted response string containing allowed Organizations
    def __allowedOrganizations_by_patientID__(self, patientID):
        try:
            organization_query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
            organization = organization_query.one()
            self.patientSession.commit()
            return organization.allowedOrganizations
        except Exception , Argument:
            self.patientSession.rollback()
            return ""

    ##Get a list of Organizations allowed to access the ExerciseResult by exerciseResultID
    #Get a list of Organizations allowed to access the ExerciseResult by exerciseResultID
    #@param exerciseResultID - The ID of the ExerciseResult.
    #@return A CSV-formatted response string containing allowed Organizations
    def __allowedOrganizations_by_exerciseResultID(self, exerciseResultID):
        try:
            organization_query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID == exerciseResultID)
            organization = organization_query.one()
            self.exerciseSession.commit()
            return organization.allowedOrganizations
        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""

    ##Get a list of Organizations allowed to access the Exercise by exerciseID
    #Get a list of Organizations allowed to access the Exercise by exerciseID
    #@param exerciseID - The ID of the Exercise.
    #@return A CSV-formatted response string containing allowed Organizations
    def __allowedOrganizations_by_exerciseID(self, exerciseID):
        try:
            organization_query = self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID == exerciseID)
            organization = organization_query.one()
            self.exerciseSession.commit()
            return organization.allowedOrganizations
        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""

    ##Get a list of Organizations allowed to access the Device by deviceID
    #Get a list of Organizations allowed to access the Device by deviceID
    #@param deviceID - The ID of the Device.
    #@return A CSV-formatted response string containing allowed Organizations
    def __allowedOrganizations_by_deviceID(self, deviceID):
        try:
            organization_query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID == deviceID)
            organization = organization_query.one()
            self.sensorSession.commit()
            return organization.allowedOrganizations
        except Exception , Argument:
            self.sensorSession.rollback()
            return ""

    ##Get a list of Organizations allowed to access the Data by dataID
    #Get a list of Organizations allowed to access the Data by dataID
    #@param dataID - The ID of the Data.
    #@return A CSV-formatted response string containing allowed Organizations
    def __allowedOrganizations_by_dataID(self, dataID):
        try:
            organization_query = self.sensorSession.query(DataClass).filter(DataClass.dataID == dataID)
            organization = organization_query.one()
            self.sensorSession.commit()
            return organization.allowedOrganizations
        except Exception , Argument:
            self.sensorSession.rollback()
            return ""

    ##Get a list of Organizations allowed to access the Data by dataID
    #Get a list of Organizations allowed to access the Data by dataID
    #@param dataID - The ID of the Data.
    #@return A CSV-formatted response string containing allowed Organizations
    def __allowedOrganizations_by_analysisTaskID(self, analysisTaskID):
        try:
            organization_query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID == analysisTaskID)
            organization = organization_query.one()
            self.analysisSession.commit()
            return organization.allowedOrganizations
        except Exception , Argument:
            self.analysisSession.rollback()
            return ""


    ##Get the organizationID of the User by username
    #Get the organizationID of the User by username
    #@param username - The username of the User.
    #@return A response string containing the organizationID
    def __organizationID_by_username__(self, username):
        try:
            user_query = self.userSession.query(UserClass).filter(UserClass.userName == username)
            self.userSession.commit()
            return user_query.one().organizationID
        except Exception , Argument:
            self.userSession.rollback()
            return ""


    ##Get the organizationID of the UserGroup by userGroupID
    #Get the organizationID of the UserGroup by userGroupID
    #@param userGroupID - The ID of the UserGroup.
    #@return A response string containing the organizationID
    def __organizationID_by_UserGroup__(self, userGroupID):
        try:
            organization_query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID == userGroupID)
            self.userSession.commit()
            return organization_query.one().organizationID
        except Exception , Argument:
            self.userSession.rollback()
            return ""

    ##Check if UserGroup belongs to a specific Organization
    #Check if UserGroup belongs to a specific Organization
    #@param organizationID - The ID of the Organization
    #@param userGroupID - The ID of the UserGroup.
    #@return A response string. It is either
    # a) "true" if the organizationID is contained in the allowedOrganization
    # b) "false" if the organizationID is not contained in the allowedOrganization
    def __userGroup_in_Organization__(self, organizationID, userGroupID):
        try:
            usergroup_query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID == userGroupID)
            self.userSession.commit()
            if usergroup_query.one().organizationID == organizationID:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.userSession.rollback()
            return ""

    ##Get the userID of the User by username
    #Get the userID of the User by username
    #@param username - The username of the User.
    #@return A response string containing the userID
    def __userID_by_username__(self, username):
        try:
            id_query = self.userSession.query(UserClass).filter(UserClass.userName == username)
            user = id_query.one()
            self.userSession.commit()
            return user.userID
        except Exception , Argument:
            self.userSession.rollback()
            return ""


    ##Get the username of the User by userID
    #Get the username of the User by userID
    #@param userID - The ID of the User.
    #@return A response string containing the username
    def __username_by_userID__(self, userID):
        try:
            username_query = self.userSession.query(UserClass).filter(UserClass.userID == userID)
            user = username_query.one()
            self.userSession.commit()
            return user.userName
        except Exception , Argument:
            self.userSession.rollback()
            return ""

    ##Get the username of the User by patientID
    #Get the username of the User by patientID
    #@param patientID - The ID of the Patient.
    #@return A response string containing the userID, to whom the Patient belongs to
    def __userID_by_patientID(self, patientID):
        try:
            username_query = self.userSession.query(UserClass).filter(UserClass.patientIDs.contains(patientID))
            user = username_query.one()
            self.userSession.commit()
            return user.userID
        except Exception , Argument:
            self.userSession.rollback()
            return ""


    ##Get the permissionLevel of the User by username
    #Get the permissionLevel of the User by username
    #@param username - The username of the User.
    #@return A response string containing the permissionLevel
    def __permissionLevel_by_username__(self, username):
        try:
            id_query = self.userSession.query(UserClass).filter(UserClass.userName == username)
            user = id_query.one()
            group_query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userIDs.contains(user.userID))
            self.userSession.commit()
            return group_query.one().permissionLevel
        except Exception , Argument:
            print Argument.message
            self.userSession.rollback()
            return "8"


    ##Get the userGroupID of the User by username
    #Get the userGroupID of the User by username
    #@param username - The username of the User.
    #@return A response string containing the userGroupID
    def __userGroupID_by_username__(self, username):
        try:
            id_query = self.userSession.query(UserClass).filter(UserClass.userName == username)
            user = id_query.one()
            group_query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userIDs.contains(user.userID))
            self.userSession.commit()
            return group_query.one().userGroupID

        except Exception , Argument:
            self.userSession.rollback()
            return ""

    ##Check if Patient belongs to a specific User
    #Check if Patient belongs to a specific User
    #@param username - The username of the User
    #@param patientID - The ID of the Patient.
    #@return A response string. It is either
    # a) "true" if the patientID is contained in the User
    # b) "false" if the patientID is not contained in the User
    def __Patient_in_User__(self, username, patientID):
        try:
            patient_query = self.userSession.query(UserClass).filter(UserClass.userID == self.__userID_by_username__(username))
            self.userSession.commit()
            if patientID in patient_query.one().patientIDs:
                return "true"
            else:
                return "false"
        except Exception , Argument:
            self.userSession.rollback()
            return ""


    ##Search for PatientID containing RehabilitationSet
    #Search for PatientID containing RehabilitationSet
    #@param rehabilitationSetID - ID of the RehabilitationSet
    #@return A response string. It is either
    # a) rehabilitationSetID if the ID is found.
    # b) "" if the RehabilitationSet is not found.
    def __PatientID_by_RehabilitationSet(self, rehabilitationSetID):
        try:
            patient_query = self.patientSession.query(PatientClass).filter(PatientClass.rehabilitationSets.contains(rehabilitationSetID))
            self.patientSession.commit()
            if len(patient_query.one()) == 1:
                return patient_query.one().patientID
            elif len(patient_query.one()) != 1:
                return ""

        except Exception , Argument:
            self.patientSession.rollback()
            return ""

    ##Search for RehabilitationSet containing PatientCondition
    #Search for RehabilitationSet containing PatientCondition
    #@param patientConditionID - ID of the PatientCondition
    #@return A response string. It is either
    # a) patientConditionID if the ID is found.
    # b) "" if the RehabilitationSet is not found.
    def __RehabilitationSetID_by_PatientCondition(self, patientConditionID):
        try:
            rehab_query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.patientConditionIDs.contains(patientConditionID))
            self.exerciseSession.commit()
            if len(rehab_query.one()) == 1:
                return rehab_query.one().rehabilitationSetID
            elif len(rehab_query.one()) != 1:
                return ""

        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""

    ##Search for RehabilitationSet containing PatientInformation
    #Search for RehabilitationSet containing PatientInformation
    #@param patientInformationID - ID of the PatientInformation
    #@return A response string. It is either
    # a) patientInformationID if the ID is found.
    # b) "" if the RehabilitationSet is not found.
    def __RehabilitationSetID_by_PatientInformation(self, patientInformationID):
        try:
            rehab_query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.patientInformationID.contains(patientInformationID))
            self.exerciseSession.commit()
            if len(rehab_query.one()) == 1:
                return rehab_query.one().rehabilitationSetID
            elif len(rehab_query.one()) != 1:
                return ""

        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""


    ##Search for RehabilitationSet containing ExerciseResult
    #Search for RehabilitationSet containing ExerciseResult
    #@param exerciseResultID - ID of the ExerciseResult
    #@return A response string. It is either
    # a) exerciseResultID if the ID is found.
    # b) "" if the RehabilitationSet is not found.
    def __RehabilitationSetID_by_ExerciseResult(self, exerciseResultID):
        try:
            rehab_query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.exerciseResultIDs.contains(exerciseResultID))
            self.exerciseSession.commit()
            if len(rehab_query.one()) == 1:
                return rehab_query.one().rehabilitationSetID
            elif len(rehab_query.one()) != 1:
                return ""

        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""

    ##Search for ExerciseResult containing Data
    #Search for ExerciseResult containing Data
    #@param dataID - ID of the Data
    #@return A response string. It is either
    # a) exerciseResultID if the ID is found.
    # b) "" if the ExerciseResult is not found.
    def __ExerciseResultID_by_Data(self, dataID):
        try:
            exercise_query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.dataIDs.contains(dataID))
            self.exerciseSession.commit()
            if len(exercise_query.one()) == 1:
                return exercise_query.one().exerciseResultID
            elif len(exercise_query.one()) != 1:
                return ""

        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""

    ##Search for ExerciseResult containing Exercise
    #SSearch for ExerciseResult containing Exercise
    #@param exerciseID - ID of the Exercise
    #@return A response string. It is either
    # a) exerciseResultID if the ID is found.
    # b) "" if the RehabilitationSet is not found.
    def __ExerciseResultID_by_Exercise(self, exerciseID):
        try:
            exercise_query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseID.contains(exerciseID))
            self.exerciseSession.commit()
            if exerciseID in exercise_query.one() :
                return exercise_query.one().exerciseResultID
            else:
                return ""

        except Exception , Argument:
            self.exerciseSession.rollback()
            return ""

    ##Search for Data containing Device
    #Search for Data containing Device
    #@param deviceID - ID of the Device
    #@return A response string. It is either
    # a) dataID if the ID is found.
    # b) "" if the Data is not found.
    def __DataID_by_Device(self, deviceID):
        try:
            exercise_query = self.sensorSession.query(DataClass).filter(DataClass.deviceID.contains(deviceID))
            self.sensorSession.commit()
            if deviceID in exercise_query.one() :
                return exercise_query.one().dataID
            else:
                return ""

        except Exception , Argument:
            self.sensorSession.rollback()
            return ""


    ##Used for re-initializing the database connections.
    #If a database connection for some reason fails, using the reset-function one can kill the database sessions and restart them.
    def reset(self):

        self.userSession = ""
        self.userSession = sessionmaker(bind=self.userEngine)
        self.userSession = self.userSession()

        self.patientSession = ""
        self.patientSession = sessionmaker(bind=self.patientEngine)
        self.patientSession = self.patientSession()

        self.exerciseSession = ""
        self.exerciseSession = sessionmaker(bind=self.exerciseEngine)
        self.exerciseSession = self.exerciseSession()

        self.sensorSession = ""
        self.sensorSession = sessionmaker(bind=self.sensorEngine)
        self.sensorSession = self.sensorSession()

        self.analysisSession = ""
        self.analysisSession = sessionmaker(bind=self.analysisEngine)
        self.analysisSession = self.analysisSession()

    ##Retrieve a JSON-formatted list of Organizations
    #Users can only fetch organizations where they are members of. System administrators are allowed to get all organizations in the system.
    #@param username(String) - the username of the user who is fetching the Organizations-list. The username is used to check if user is allowed to list the Organizations.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of Organizations
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_organizations(self, username):

        try:
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText+=',"Organizations":['
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(OrganizationClass)
            else:
                query = self.userSession.query(OrganizationClass).filter(OrganizationClass.userIDs.contains( self.__userID_by_username__(username)))
            self.userSession.commit()
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                rowcount -= 1
                jsonText += json.dumps(item.tojson())
                if rowcount != 0:
                    jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific Organization from the database
    #Get a specific Organization from the database
    #@param username(String) - The username of the User who is getting the organization. The username is used to check if user is allowed to get the organization.
    #@param organizationID(String) - The organizationID of the Organization to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A JSON of Organization
    # b) A status massage 401, meaning that the User is not allowed to access the Organization
    # c) A status message 404, meaning that the organizationID doesn't exist
    # c) A status message 500, meaning something went wrong.
    def get_organization(self, username, organizationID):
        try:
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Organization":['
            query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID == organizationID)
            self.userSession.commit()
            if username in query.one().userIDs or self.__permissionLevel_by_username__(username)  == 0: # or self.__permissionLevel_by_username__(username)  == 7:
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0:
                            jsonText += ","
                jsonText+= "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'Forbidden.'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Create a new Organization to the database
    #Create an new Organization to the database
    #@param username(String) - The username of the User who is creating the new Organization. The username is used to check if User is allowed to create the Organization.
    #@param name(String) - The name of the new Organization
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the OrganizationID of the created Organization
    # b) A status message 401, meaning that the User doesn't have the right to create an Organization
    # b) A status message 500, meaning something went wrong.
    def create_organization(self, username, name, userIDs="", userGroupIDs =""):
        if self.__permissionLevel_by_username__(username)  < 1:
            organizationID = "organization_" + "{:.6f}".format(time.time())
            try:
                new_record = OrganizationClass(organizationID, name, userIDs, userGroupIDs)
                self.userSession.add(new_record)
                self.userSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'Organization created', 'OrganizationID:': organizationID})

            except Exception ,Argument:
                self.userSession.rollback()
                return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})
        else:
             return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create an Organization'})


    ##Update a specific aspect of a single Organization in the database
    #Update a specific aspect of a single Organization in the database
    #@param username(String) - The username of the User who is updating the Organization. The username is used to check if User is allowed to update the Organization.
    #@param organizationID(String) - The ID of the Organization
    #@param field(String) - The field's name you want to update in the Organization
    #@param value(String) - The value you want to insert in the 'field' in Organization
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning that the User doesn't have the required rights to update the Organization
    # c) A status message 404, meaning the organizationID does not correspond to any Organization.
    # d) A status message 500, meaning something went wrong.
    def update_organization(self, username, organizationID, field, value):
        if (self.__permissionLevel_by_username__(username) < 2 and self.__organizationID_by_username__(username) == organizationID) or self.__permissionLevel_by_username__(username) == 0:
            try:
                query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID == organizationID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was updated'})
                if self.__permissionLevel_by_username__(username) > 0 and field=="UserGroupIDs":
                    self.userSession.rollback()
                    return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update this apect of the Organization'})
                else:
                    query.update({getattr(OrganizationClass, field):value})
                    self.userSession.commit()

                return json.dumps({'status_code': '200', 'msg': 'Success'})

            except Exception , Argument:
                self.userSession.rollback()
                return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})
        else:
             return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the Organization'})

    ##Delete a specific Organization from the database
    #Delete a specific Organization from the database
    #@param username(String) - The username of the User who is deleting the Organization. The username is used to check if User is allowed to delete the Organization.
    #@param organizationID(String) - The ID of the Organization
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning that the User is not allowed to remove the Organization.
    # b) A status message 404, meaning the organizationID does not correspond to any Organization.
    # c) A status message 500, meaning something went wrong.
    def delete_organization(self, username, organizationID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 :
                 query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID == organizationID)
                 rowcount = len(query.all())
                 if rowcount == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                 self.userSession.delete(query.one())
                 self.userSession.commit()
                 return json.dumps({'status_code': '200', 'msg': 'Organization deleted', 'OrganizationID': organizationID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the Organization'})
        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})



    ##Add user to an Organization
    #Add user to an Organization
    #@param username(String) - The username of the User adding the User to the Organization. Used to check if the user is allowed to edit the Organization
    #@param organizationID(String) - The OrganizationID of the Organization the User is to be added
    #@param userID(String) - The ID of the User to be added.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add a User to the Organization
    # c) A status message 404, meaning the Organization was not found
    # b) A status message 500, meaning something went wrong, details in message.
    def add_user_to_organization(self, username, organizationID, userID):
        try:
            if (self.__permissionLevel_by_username__(username) < 2  and self.__organizationID_by_username__(username) == organizationID) or self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID==organizationID)
                if len(query.all()) == 1:
                    userIDs = query.one().userIDs
                    userIDs_split = userIDs.split(";")
                    if userID in userIDs_split:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'User already in the Organization', 'UserID' : userID})
                    else:
                        if len(userIDs) == 0:
                            userIDs = userID
                        else:
                            userIDs += ";"+userID
                        userIDs = ''.join(userIDs)
                        self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID==organizationID).update({OrganizationClass.userIDs: userIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'User added', 'OrganizationID' : organizationID, 'UserID:':userID})
                elif len(query.all()) == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for OrganizationID'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed add a User to the Organization'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove User from an Organization
    #Remove User from an Organization
    #@param username(String) - The username of the User removing the User from the Organization. Used to check if the user is allowed to edit the Organization
    #@param organizationID(String) - The OrganizationID of the Organization the User is to be removed from
    #@param userID(String) - The ID of the User to be removed.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning that the User is not allowed to remove a User form the Organization
    # c) A status message 404, meaning that the Organization wasn't found.
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_user_from_organization(self, username, organizationID, userID):
        try:
            if (self.__permissionLevel_by_username__(username) < 2  and self.__organizationID_by_username__(username) == organizationID) or self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID == organizationID)
                if len(query.all()) == 1:
                    userIDs = query.one().userIDs
                    userIDs_split = userIDs.split(";")
                    if userID in userIDs_split:
                        userIDs_split.remove(userID)
                        userIDs = ';'.join(map(str, userIDs_split))
                        self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID==organizationID).update({OrganizationClass.userIDs: userIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'User removed'})

                    else:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'User not in the organization', 'OrganizationID' : organizationID, 'UserID': userID})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for OrganizationID', 'OrganizationID' : organizationID})
            else:
                 return json.dumps({'status_code': '401', 'msg': 'You are not allowed remove a User from the Organization'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add UserGroup to an Organization
    #Add UserGroup to an Organization
    #@param username(String) - The username of the User adding the User to the Organization. Used to check if the user is allowed to edit the Organization
    #@param organizationID(String) - The OrganizationID of the Organization the User is to be added
    #@param userGroupID(String) - The ID of the UserGroup to be added.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add a UserGroup to the Organization
    # c) A status message 404, meaning the Organization was not found
    # b) A status message 500, meaning something went wrong, details in message.
    def add_userGroup_to_organization(self, username, organizationID, userGroupID):
        try:
            if (self.__permissionLevel_by_username__(username) < 2  and self.__organizationID_by_username__(username) == organizationID) or self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID==organizationID)
                if len(query.all()) == 1:
                    userGroupIDs = query.one().userGroupIDs
                    userGroupIDs_split = userGroupIDs.split(";")
                    if userGroupID in userGroupIDs_split:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'UserGroup already in the Organization', 'UserGroupID' : userGroupID})
                    else:
                        if len(userGroupIDs) == 0:
                            userGroupIDs = userGroupID
                        else:
                            userGroupIDs += ";" + userGroupID
                        userGroupIDs = ';'.join(userGroupIDs)
                        self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID==organizationID).update({OrganizationClass.userGroupIDs: userGroupIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'UserGroup added', 'OrganizationID' : organizationID, 'UserGroupID:':userGroupID})
                elif len(query.all()) == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for OrganizationID'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed add a UserGroup to the Organization'})

        except Exception, Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove UserGroup from an Organization
    #Remove UserGroup from an Organization
    #@param username(String) - The username of the User removing the User from the Organization. Used to check if the user is allowed to edit the Organization
    #@param organizationID(String) - The OrganizationID of the Organization the UserGroup is to be removed from
    #@param userGroupID(String) - The ID of the UserGroup to be removed.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning that the User is not allowed to remove a User form the Organization
    # c) A status message 404, meaning that the Organization wasn't found.
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_userGroup_from_organization(self, username, organizationID, userGroupID):
        try:
            if (self.__permissionLevel_by_username__(username) < 2  and self.__organizationID_by_username__(username) == organizationID) or self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID == organizationID)
                if len(query.all()) == 1:
                    userGroupIDs = query.one().userGroupIDs
                    userGroupIDs_split = userGroupIDs.split(";")
                    if userGroupID in userGroupIDs_split:
                        userGroupIDs_split.remove(userGroupID)
                        userGroupIDs = ';'.join(map(str, userGroupIDs_split))
                        self.userSession.query(OrganizationClass).filter(OrganizationClass.organizationID==organizationID).update({OrganizationClass.userGroupIDs: userGroupIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'UserGroup removed'})

                    else:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'UserGroup not in the Organization', 'OrganizationID' : organizationID, 'UserGroupID': userGroupID})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for OrganizationID', 'OrganizationID' : organizationID})
            else:
                 return json.dumps({'status_code': '401', 'msg': 'You are not allowed remove a User from the Organization'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Retrieve a JSON-formatted list of UserGroups
    #Retrieve a JSON-formatted list of UserGroups.
    #@param username(String) - the username of the user who is fetching the UserGroups-list. The username is used to check if used is allowed to list the UserGroups.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of UserGroups
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_usergroups(self, username):
        try:
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"UserGroups":['
            if self.__permissionLevel_by_username__(username) < 1:
                query = self.userSession.query(UserGroupClass)
            else:
                query = self.userSession.query(UserGroupClass).filter(UserGroupClass.organizationID == self.__organizationID_by_username__(username))
            self.userSession.commit()
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0:
                        jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred',  'ErrorText':Argument.message})

    ##Get a specific UserGroup from the database
    #Get a specific UserGroup from the database
    #@param username(String) - the username of the user who is getting the UserGroup. The username is used to check if used is allowed to get the UserGroup.
    #@param userGroupID(String) - The userGroupID of the UserGroup to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the UserGroup
    # b) A status message 404, meaning that the UserGroup doesn't exist
    # c) A status message 500, meaning something went wrong.
    def get_usergroup(self, username, userGroupID):
        try:
            if self.__permissionLevel_by_username__(username) <2 or ( self.__userGroup_in_Organization__(self.__organizationID_by_username__(username), userGroupID) == "true"):
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"UserGroup":['
                query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID == userGroupID)
                self.userSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0:
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the UserGroup'})
        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Get the UserGroup of the User by username
    #Get the UserGroup of the User by username
    #@param username - The username of the User.
    #@return A response string containing the userGroupID
    def get_usergroup_by_username(self, username):
        try:
            id_query = self.userSession.query(UserClass).filter(UserClass.userName == username)
            user = id_query.one()
            group_query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userIDs.contains(user.userID))
            self.userSession.commit()
            return group_query.one()

        except Exception , Argument:
            self.userSession.rollback()
            return ""


    ##Create a new UserGroup to the database
    #Create an new UserGroup to the database
    #@param username(String) - The username of the User who is creating the new UserGroup. The username is used to check if User is allowed to create the UserGroup.
    #@param name(String) - The name of the new UserGroup
    #@param permissionLevel(Double) - The permissionLevel describing the rights of the users within that group. !NOTE! This level cannot be higher than the User's who is creating it.
    #@param userIDs(String)(voluntary) - A CSV String of userIDs separated by ; to be added to this UserGroup
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the UserGroupID of the created UserGroup
    # b) A status message 500, meaning something went wrong.
    def create_usergroup(self, username, name, permissionLevel, organizationID, userIDs = ""):
        userGroupID = "usergroup_" + "{:.6f}".format(time.time())
        try:
            if (self.__organizationID_by_username__(username) == organizationID and self.__permissionLevel_by_username__(username) ==1) or self.__permissionLevel_by_username__(username) == 0 :
                new_record = UserGroupClass(userGroupID, name, permissionLevel, organizationID, userIDs )
                self.userSession.add(new_record)
                self.userSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'UserGroup created', 'UserGroupID:': userGroupID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the UserGroup'})

        except Exception ,Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single UserGroup in the database
    #Update a specific aspect of a single UserGroup in the database
    #@param username(String) - The username of the User who is updating the UserGroup. The username is used to check if User is allowed to update the UserGroup.
    #@param userGroupID(String) - The ID of the UserGroup
    #@param field(String) - The field's name you want to update in the UserGroup
    #@param value(String) - The value you want to insert in the 'field' in UserGroup
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 404, meaning the userGroupID does not correspond to any UserGroup.
    # c) A status message 500, meaning something went wrong.
    def update_usergroup(self, username, userGroupID, field, value):
        try:
            if self.__permissionLevel_by_username__(username) == 0 :
                query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID == userGroupID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was updated'})
                query.update({getattr(UserGroupClass, field):value})
                self.userSession.commit()

                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the UserGroup'})
        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Delete a specific UserGroup from the database
    #Delete a specific UserGroup from the database
    #@param username(String) - The username of the User who is deleting the UserGroup. The username is used to check if User is allowed to delete the UserGroup.
    #@param userGroupID(String) - The ID of the UserGroup
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 404, meaning the userGroupID does not correspond to any UserGroup.
    # c) A status message 500, meaning something went wrong.
    def delete_usergroup(self, username, userGroupID):
        try:
            if (self.__organizationID_by_username__(username) == self.__organizationID_by_UserGroup__(userGroupID) and self.__permissionLevel_by_username__(username) == 1) or self.__permissionLevel_by_username__(username) == 0 :
                query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID == userGroupID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_userGroup_from_organization(username, self.__organizationID_by_UserGroup__(userGroupID), userGroupID)
                self.userSession.delete(query.one())
                self.userSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'UserGroup deleted', 'UserGroupID': userGroupID})

            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the UserGroup'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add user to a UserGroup
    #Add user to a UserGroup
    #@param username(String) - The username of the User adding the User to the UserGroup. Used to check if the user is allowed to edit the UserGroup
    #@param userGroupID(String) - The UserGroupID of the UserGroup the User is to be added to
    #@param userID(String) - The ID of the User to be added.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 500, meaning something went wrong, details in message.
    def add_user_to_usergroup(self, username, userGroupID, userID):
        try:
            if (self.__organizationID_by_username__(username) == self.__organizationID_by_UserGroup__(userGroupID) and self.__permissionLevel_by_username__(username) == 1) or self.__permissionLevel_by_username__(username) == 0 :
                query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID == userGroupID)
                if len(query.all()) == 1:
                    userIDs = query.one().userIDs
                    userIDs_split = userIDs.split(";")
                    if userID in userIDs_split:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'User already in the UserGroup', 'UserID' : userID})

                    else:
                        if len(userIDs) == 0:
                            userIDs = userID
                        else:
                            userIDs += ";"+userID

                        #userIDs = ';'.join(map(str, userIDs))
                        self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID==userGroupID).update({UserGroupClass.userIDs: userIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'User added', 'UserGroupID' : userGroupID, 'UserID':userID})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for UserGroup', 'UserGroupID' : userGroupID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add Users to the UserGroup'})
        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove a user from a UserGroup
    #Remove a user from a UserGroup
    #@param username(String) - The username of the User removing the User from the UserGroup. Used to check if the user is allowed to edit the UserGroup
    #@param userGroupID(String) - The UserGroupID of the UserGroup the User is to be removed from
    #@param userID(String) - The ID of the User to be removed.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 404, meaning that the User or the UserGroup was not found.
    # c) A status message 500, meaning something went wrong, details in message.
    def remove_user_from_usergroup(self, username, userGroupID, userID):
        try:
            if (self.__organizationID_by_username__(username) == self.__organizationID_by_UserGroup__(userGroupID) and self.__permissionLevel_by_username__(username) == 1)  or self.__permissionLevel_by_username__(username) == 0 :
                query = self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID==userGroupID)
                if len(query.all()) == 1:
                    userIDs = query.one().userIDs
                    userIDs_split = userIDs.split(";")
                    if userID in userIDs_split:
                        userIDs_split.remove(userID)
                        userIDs = ';'.join(map(str, userIDs_split))
                        self.userSession.query(UserGroupClass).filter(UserGroupClass.userGroupID==userGroupID).update({UserGroupClass.userIDs: userIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'User removed', 'UserGroup' : userGroupID, 'UserID:':userID})
                    else:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'User not in the UserGroup', 'UserGroup' : userGroupID, 'UserID': userID})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for UserGroupID', 'UserGroup' : userGroupID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove Users from the UserGroup'})
        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Retrieve a JSON-formatted list of Users
    #Retrieve a JSON-formatted list of Users.
    #@param username(String) - the username of the user who is fetching the Users-list. The username is used to check if User is allowed to list the Users.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of Users
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_users(self, username):
        try:
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(UserClass)
            else:
                query = self.userSession.query(UserClass).filter(UserClass.organizationID == self.__organizationID_by_username__(username))
            self.userSession.commit()
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Users":['
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0:
                        jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Find a specific User by a given value from a given field
    #Find a specific User by a given value from a given field
    #@param username(String) - Username of the User who is searching for Users. The username is used to check if User is allowed to search for users.
    #@param field(String) - The field to search by
    #@param value(String) - The value to be matched to the field
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the User
    # b) A status message 404, meaning that the User(s) wasn't / weren't found
    # c) A status message 500, meaning something went wrong.
    def find_users(self, username, field, value):
        try:
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(UserClass).filter(getattr(UserClass, field)==value)
            else:
                query = self.userSession.query(UserClass).filter(UserClass.organizationID == self.__organizationID_by_username__(username)).filter(getattr(UserClass, field)==value)
            self.userSession.commit()
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Users":['

            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0:
                        jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific User from the database
    #Get a specific User from the database
    #@param username(String) - the username of the user who is getting the User. The username is used to check if used is allowed to get the User.
    #@param userID(String) - The userID of the User to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the User
    # b) A status message 401, meaning the User is not allowed to view the User
    # c) A status message 404, meaning that the User doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_user(self, username, userID):
        try:
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.userSession.query(UserClass).filter(UserClass.userID == userID)
            elif self.__organizationID_by_username__(username) == self.__organizationID_by_username__(self.__username_by_userID__(userID)):
                query = self.userSession.query(UserClass).filter(UserClass.organizationID == self.__organizationID_by_username__(username)).filter(UserClass.userID == userID)
            else:
                self.userSession.rollback()
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to view this User'})
            self.userSession.commit()
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"User":['
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0:
                        jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred',  'ErrorText':Argument.message})


    ##Create a new User to the database
    #Create an new User to the database
    #@param username(String) - The username of the User who is creating the new User. The username is used to check if User is allowed to create the User.
    #@param firstName(String) - First name of the new User
    #@param lastName(String) - Last name of the new User
    #@param newUsername(String) - The username of the new User
    #@param password(String) - The password of the new user, it is passed as cleartext, but it's encrypted when put into database.
    #@param jobTitle(String) - Title of the User.
    #@param patientIDs(String)(voluntary) - Possible
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the UserID of the created User
    # b) A status message 401, meaning the User is not allowed to create this User
    # c) A status message 500, meaning something went wrong.
    def create_user(self, username, organizationID, firstName, lastName, newUsername, password, jobTitle, patientIDs=""):
        userID = "user_" + "{:.6f}".format(time.time())
        try:
            if self.__permissionLevel_by_username__(username) == 0 or (self.__organizationID_by_username__(username) == organizationID and self.__permissionLevel_by_username__(username) == 1):
                new_record = UserClass(userID, organizationID, firstName, lastName, newUsername, password, "", jobTitle, patientIDs )
                self.userSession.add(new_record)
                self.userSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'User created', 'UserID': userID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create this new User'})

        except Exception ,Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Delete a specific User from the database
    #Delete a specific User from the database
    #@param username(String) - The username of the User who is deleting the User. The username is used to check if User is allowed to delete the User.
    #@param userID(String) - The ID of the User
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to remove the User
    # c) A status message 404, meaning the userID does not correspond to any User.
    # d) A status message 500, meaning something went wrong.
    def delete_user(self, username, userID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or (self.__organizationID_by_username__(username) == self.__organizationID_by_username__(self.__username_by_userID__(userID)) and self.__permissionLevel_by_username__(username) == 1):
                query = self.userSession.query(UserClass).filter(UserClass.userID == userID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_user_from_organization(username,self.__organizationID_by_username__(self.__username_by_userID__(userID)), userID )
                self.remove_user_from_usergroup(username, self.__userGroupID_by_username__(self.__username_by_userID__(userID)), userID)
                self.userSession.delete(query.one())
                self.userSession.commit()

                return json.dumps({'status_code': '200', 'msg': 'User deleted', 'UserID': userID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete this User'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single User in the database
    #Update a specific aspect of a single User in the database
    #@param username(String) - The username of the User who is updating the User. The username is used to check if User is allowed to update the User.
    #@param userID(String) - The ID of the User
    #@param field(String) - The field's name you want to update in the User
    #@param value(String) - The value you want to insert in the 'field' in User
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the Users isn't allowed to update the User or a specific field.
    # b) A status message 404, meaning the userID does not correspond to any User.
    # c) A status message 500, meaning something went wrong.
    def update_user(self, username, userID, field, value):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or (self.__organizationID_by_username__(username) == self.__organizationID_by_username__(self.__username_by_userID__(userID)) and self.__permissionLevel_by_username__(username) <2):
                query = self.userSession.query(UserClass).filter(UserClass.userID == userID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                if(field == "organizationID" and value != self.__organizationID_by_username__(username) ) and self.__permissionLevel_by_username__(username)>0 :
                    self.userSession.rollback()
                    return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update this aspect of the User'})

                query.update({getattr(UserClass, field):value})
                self.userSession.commit()

                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update this User'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add Patient to a User
    #Add Patient to a User
    #@param username(String) - The username of the User adding the Patient to the User. Used to check if the user is allowed to edit the User
    #@param userID(String) - The UserID of the User the Patient is to be added to
    #@param patientID(String) - The ID of the Patient to be added.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add the Patient to the User
    # c) A status message 404, meaning that the User was not found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_patient_to_user(self, username, userID, patientID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or (self.__organizationID_by_username__(username) == self.__organizationID_by_username__(self.__username_by_userID__(userID)) and self.__permissionLevel_by_username__(username) <2 and (self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID))):
                query = self.userSession.query(UserClass).filter(UserClass.userID==userID)
                if len(query.all()) == 1:
                    patientIDs = query.one().patientIDs
                    patientIDs_split = patientIDs.split(";")
                    if userID in patientIDs_split:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Patient already in the user', 'UserID' : userID, 'PatientID':patientID})
                    else:
                        if len(patientIDs) == 0:
                            patientIDs = patientID
                        else:
                            patientIDs += ";"+patientID

                        patientIDs = ''.join(patientIDs)
                        self.userSession.query(UserClass).filter(UserClass.userID==userID).update({UserClass.patientIDs: patientIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Patient added', 'UserID' : userID, 'PatientID:':patientID})
                elif len(query.all()) == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': "User wasn't found", 'UserID' : userID})
                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for User', 'UserID' : userID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add this Patient to this User'})

        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove a Patient from a User
    #Remove a Patient from a User
    #@param username(String) - The username of the User removing the Patient from the User. Used to check if the user is allowed to edit the User
    #@param userID(String) - The UserID of the User the Patient is to be removed from
    #@param patientID(String) - The ID of the Patient to be removed.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove the Patient from the User
    # c) A status message 404, meaning the User or the Patient wasn't found from the User
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_patient_from_user(self, username, userID, patientID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or (self.__organizationID_by_username__(username) == self.__organizationID_by_username__(self.__username_by_userID__(userID)) and self.__permissionLevel_by_username__(username) == 1):
                query = self.userSession.query(UserClass).filter(UserClass.userID==userID)
                if len(query.all()) == 1:
                    patientIDs = query.one().patientIDs
                    patientIDs_split = patientIDs.split(";")
                    if patientID in patientIDs_split:
                        patientIDs_split.remove(patientID)
                        patientIDs = ';'.join(map(str, patientIDs_split))
                        self.userSession.query(UserClass).filter(UserClass.userID==userID).update({UserClass.patientIDs: patientIDs})
                        self.userSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Patient removed', 'UserID' : userID, 'PatientID:':patientID})
                    else:
                        self.userSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Patient not in user', 'User' : userID, 'PatientID': patientID})
                elif len(query.all()) == 0:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'User not found', 'User': userID})

                else:
                    self.userSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for User', 'User' : userID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove this Patient from this User'})
        except Exception , Argument:
            self.userSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Retrieve a JSON-formatted list of Patients
    #Retrieve a JSON-formatted list of Patients.
    #@param username(String) - the username of the user who is fetching the Patients-list. The username is used to check if used is allowed to list the Patients.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of Patients
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_patients(self, username):
        try:
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.patientSession.query(PatientClass)
            else:
                query = self.patientSession.query(PatientClass).filter(PatientClass.allowedOrganizations.ilike(self.__organizationID_by_username__(username)))
            self.patientSession.commit()
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Patients":['
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0:
                        jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Create a new Patient to the database
    #Create an new Patient to the database
    #@param username(String) - The username of the User who is creating the new Patient. The username is used to check if User is allowed to create the Patient.
    #@param allowedOrganizations(String) - The CSV-formatted String of organizationIDs that are allowed to access the Patient, the separator is ;
    #@param rehabilitationSets(String)(voluntary) - The CSV-formatted String of rehabilitationSetIDs that belong to the Patient, the separator is ;
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the PatientID of the created Patient
    # b) A status message 401, meaning the User is not allowed to create the Patient
    # c) A status message 500, meaning something went wrong.
    def create_patient(self, username, allowedOrganizations, rehabilitationSets = ""):
        patientID = "patient_" + "{:.6f}".format(time.time())
        try:
            if self.__permissionLevel_by_username__(username) == 0 or (self.__organizationID_by_username__(username) in allowedOrganizations and self.__permissionLevel_by_username__(username) <5) :
                new_record = PatientClass(patientID, allowedOrganizations, rehabilitationSets)
                self.patientSession.add(new_record)
                self.patientSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'Patient created', 'PatientID': patientID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create this Patient'})
        except Exception ,Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific Patient from the database
    #Get a specific Patient from the database
    #@param username(String) - the username of the user who is getting the Patient. The username is used to check if used is allowed to get the Patient.
    #@param patientID(String) - The patientID of the Patient to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the Patient
    # b) A status message 401, meaning the User isn't allowed to get the Patient
    # c) A status message 404, meaning that the Patient doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_patient(self, username, patientID):
        try:
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
            elif self.__permissionLevel_by_username__(username) <5 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID):
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID).filter(PatientClass.allowedOrganizations.contains(self.__organizationID_by_username__(username)))
            else:
                self.patientSession.rollback()
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get this Patient'})
            self.patientSession.commit()
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Patient":['
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0:
                        jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##Update a specific aspect of a single Patient in the database
    #Update a specific aspect of a single Patient in the database
    #@param username(String) - The username of the User who is updating the Patient. The username is used to check if User is allowed to update the Patient.
    #@param patientID(String) - The ID of the Patient
    #@param field(String) - The field's name you want to update in the Patient
    #@param value(String) - The value you want to insert in the 'field' in Patient
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the Patient
    # b) A status message 404, meaning the patientID does not correspond to any Patient.
    # c) A status message 500, meaning something went wrong.
    def update_patient(self, username, patientID, field, value):
        try:
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
            elif self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID):
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
            elif self.__Patient_in_User__(username,patientID) == "true" and self.__permissionLevel_by_username__(username)<4 :
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update this Patient'})

            rowcount = len(query.all())
            if rowcount == 0:
                self.patientSession.rollback()
                return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
            query.update({getattr(PatientClass, field):value})
            self.patientSession.commit()

            return json.dumps({'status_code': '200', 'msg': 'Success'})

        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Delete a specific Patient from the database
    #Delete a specific Patient from the database
    #@param username(String) - The username of the User who is deleting the Patient. The username is used to check if User is allowed to delete the Patient.
    #@param patientID(String) - The ID of the Patient
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to remove the Patient
    # c) A status message 404, meaning the patientID does not correspond to any Patient.
    # d) A status message 500, meaning something went wrong.
    def delete_patient(self, username, patientID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or ( self.__permissionLevel_by_username__(username) == 1 and self.__organizationID_by_username__(username) in  self.__allowedOrganizations_by_patientID__(patientID)):
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_patient_from_user(username, self.__userID_by_patientID(patientID), patientID)
                self.patientSession.delete(query.one())
                self.patientSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Patient deleted', 'PatientID': patientID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete this Patient'})

        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add allowed Organization to a Patient
    #Add allowed Organization to a Patient
    #@param username(String) - The username of the User adding the Organization to the Patient. Used to check if the User is allowed to edit the Patient
    #@param patientID(String) - The ID of the Patient to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this Patient
    # c) A status message 404, meaning the Patient wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_patient(self, username, patientID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID==patientID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.patientSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'PatientID':patientID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        organizationIDs = ''.join(organizationIDs)
                        self.patientSession.query(PatientClass).filter(PatientClass.patientID==patientID).update({PatientClass.allowedOrganizations: organizationIDs})
                        self.patientSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'PatientID:':patientID})
                elif len(query.all()) == 0:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Patient not found'})

                else:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Patient', 'PatientID' : patientID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this Patient'})

        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from a Patient
    #Remove allowed Organization from a Patient
    #@param username(String) - The username of the User removing the Organization from the Patient. Used to check if the User is allowed to edit the Patient
    #@param patientID(String) - The ID of the Patient from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove the Organization from the Patient
    # b) A status message 404, meaning the Organization within the Patient or the Patient wasn't found
    # b) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_patient(self, username, patientID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
                if len(query.all()) == 0:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        patientIDs = ';'.join(organizationIDs_split)
                        self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID).update({PatientClass.allowedOrganizations: patientIDs})
                        self.patientSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.patientSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in Patient'})
                else:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Patient'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this Patient'})

        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add RehabilitationSet to a Patient
    #Add RehabilitationSet to a Patient
    #@param username(String) - The username of the User adding the RehabilitationSet to the Patient. Used to check if the User is allowed to edit the Patient
    #@param patientID(String) - The ID of the Patient to which the RehabilitationSet is added to.
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to add a RehabilitationSet to the Patient
    # c) A status message 404, meaning the Patient wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_rehabilitation_set_to_patient(self, username, patientID, rehabilitationSetID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or ( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID)):
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID==patientID)
                if len(query.all()) == 1:
                    rehabilitationSetIDs = query.one().rehabilitationSets
                    rehabilitationSetIDs_split = rehabilitationSetIDs.split(";")
                    if rehabilitationSetID in rehabilitationSetIDs_split:
                        self.patientSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'RehabilitationSet already exists within the Patient'})

                    else:
                        if len(rehabilitationSetIDs) == 0:
                            rehabilitationSetIDs = rehabilitationSetID
                        else:
                            rehabilitationSetIDs += ";"+rehabilitationSetID

                        rehabilitationSetIDs = ''.join(rehabilitationSetIDs)
                        self.patientSession.query(PatientClass).filter(PatientClass.patientID==patientID).update({PatientClass.rehabilitationSets: rehabilitationSetIDs})
                        self.patientSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'RehabilitationSet added'})
                elif len(query.all()) == 0:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Patient not found'})
                else:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Patient'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add a RehabilitationSet to the Patient '})
        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove a RehabilitationSet from a Patient
    #Remove a RehabilitationSet from a Patient
    #@param username(String) - The username of the User removing the RehabilitationSet from the Patient. Used to check if the User is allowed to edit the Patient
    #@param patientID(String) - The ID of the Patient from which the RehabilitationSet is removed from.
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to remove the RehabilitationSet from the Patient
    # b) A status message 404, meaning the Patient or RehabilitationSet wasn't found
    # c) A status message 500, meaning something went wrong, details in message.
    def remove_rehabilitation_set_from_patient(self, username, patientID, rehabilitationSetID):
        try:
            if self.__permissionLevel_by_username__(username) == 0 or ( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_patientID__(patientID)):
                query = self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID)
                if len(query.all()) == 1:
                    rehabilitationSetIDs = query.one().rehabilitationSets
                    rehabilitationSetIDs_split = rehabilitationSetIDs.split(";")
                    if rehabilitationSetID in rehabilitationSetIDs:
                        rehabilitationSetIDs_split.remove(rehabilitationSetID)
                        patientIDs = ';'.join(rehabilitationSetIDs_split)
                        self.patientSession.query(PatientClass).filter(PatientClass.patientID == patientID).update({PatientClass.rehabilitationSets: patientIDs})
                        self.patientSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'RehabilitationSet removed'})
                    else:
                        self.patientSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'RehabilitationSet not in Patient'})
                elif len(query.all()) == 0:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Patient not found'})
                else:
                    self.patientSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Patient'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove a RehabilitationSet from the Patient'})
        except Exception , Argument:
            self.patientSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Create a new PatientCondition to the database
    #Create an new PatientCondition to the database
    #@param username(String) - The username of the User who is creating the new PatientCondition. The username is used to check if User is allowed to create the PatientCondition.
    #@param label(String) - Label that tells what is the current condition
    #@param description(String) - A more detailed description of the condition of the Patient
    #@param officialMedicalCode(String)(voluntary) - An official medicalcode, if such exists
    #@param allowedOrganization(String) - The organization where this condition belongs to
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the PatientConditionID of the created PatientCondition
    # b) A status message 401, meaning the User isn't allowed to create a PatientCondition
    # b) A status message 500, meaning something went wrong.
    def create_patientcondition(self, username, allowedOrganizations, label, description, officialMedicalCode=""):
        patientConditionID = "patientCondition_" + "{:.6f}".format(time.time())
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in allowedOrganizations) or self.__permissionLevel_by_username__(username) ==0:
                #if self.__permissionLevel_by_username__(username) == 0 or ( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in self.__allowedOrganization_in_patientConditionID__(patientConditionID, allowedOrganizations)):
                new_record = PatientConditionClass(patientConditionID, allowedOrganizations, label, description, officialMedicalCode)
                self.exerciseSession.add(new_record)
                self.exerciseSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'PatientCondition created', 'PatientConditionID:': patientConditionID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create a PatientCondition'})

        except Exception ,Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific PatientCondition from the database
    #Get a specific PatientCondition from the database
    #@param username(String) - the username of the user who is getting the PatientCondition. The username is used to check if used is allowed to get the PatientCondition.
    #@param patientID(String) - The patientConditionID of the PatientCondition to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the PatientCondition
    # b) A status message 401, meaning that User is not allowed to get the PatientCondition
    # c) A status message 404, meaning that the PatientCondition doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_patientcondition(self, username, patientConditionID):
        try:
            if (self.__allowedOrganization_in_patientConditionID__(patientConditionID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) < 5) or self.__permissionLevel_by_username__(username) == 0 :
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"PatientCondition":['
                query = self.exerciseSession.query(PatientConditionClass).filter(PatientConditionClass.patientConditionID == patientConditionID)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0:
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the PatientCondition'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##Delete a specific PatientCondition from the database
    #Delete a specific PatientCondition from the database
    #@param username(String) - The username of the User who is deleting the PatientCondition. The username is used to check if User is allowed to delete the PatientCondition.
    #@param patientConditionID(String) - The ID of the PatientCondition
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to delete the PatientCondition
    # b) A status message 404, meaning the patientConditiontID does not correspond to any PatientCondition.
    # c) A status message 500, meaning something went wrong.
    def delete_patientcondition(self, username, patientConditionID):
        try:
            if (self.__allowedOrganization_in_patientConditionID__(patientConditionID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) < 5) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(PatientConditionClass).filter(PatientConditionClass.patientConditionID == patientConditionID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_patientcondition_from_rehabilitationset(username, self.__RehabilitationSetID_by_PatientCondition(patientConditionID), patientConditionID )
                self.exerciseSession.delete(query.one())
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'PatientCondition deleted', 'PatientConditionID': patientConditionID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the PatientCondition'})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single PatientCondition in the database
    #Update a specific aspect of a single PatientCondition in the database
    #@param username(String) - The username of the User who is updating the PatientCondition. The username is used to check if User is allowed to update the PatientCondition.
    #@param patientConditionID(String) - The ID of the PatientCondition
    #@param field(String) - The field's name you want to update in the PatientCondition
    #@param value(String) - The value you want to insert in the 'field' in PatientCondition
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to update the PatientCondition
    # b) A status message 404, meaning the patientConditionID does not correspond to any PatientCondition.
    # c) A status message 500, meaning something went wrong.
    def update_patientcondition(self, username, patientConditionID, field, value):
        try:
            if (self.__allowedOrganization_in_patientConditionID__(patientConditionID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) < 5) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(PatientConditionClass).filter(PatientConditionClass.patientConditionID == patientConditionID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(PatientConditionClass, field):value})
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the PatientCondition'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Create a new PatientInformation to the database
    #Create an new PatientInformation to the database
    #@param username(String) - The username of the User who is creating the new PatientInformation. The username is used to check if User is allowed to create the PatientInformation.
    #@param bodyWeight(Double) - Weight of the Patient
    #@param bodyHeight(Double) - Height of the Patient
    #@param upperBodyDominantSide (ENUM [Right, Left]) - Dominant side of the upper body (Righthanded vs. Lefthanded)
    #@param lowerBodyDominantSide (ENUM [Right, Left]) - Dominant side of the lower body
    #@param birthYear(Integer) - Birthyear of the Patient
    #@param gender (ENUM [Male, Female, Indeterminate]) - Gender of the Patient
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the PatientInformationID of the created PatientInformation'
    # b) A status message 401, meaning the User is not allowed to create the PatientIndformation
    # c) A status message 500, meaning something went wrong.
    def create_patientinformation(self, username, allowedOrganizations, bodyWeight, bodyHeight, upperBodyDominantSide, lowerBodyDominantSide, birthYear, gender):
        patientInformationID = "patientInformation" + "{:.6f}".format(time.time())
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in allowedOrganizations) or self.__permissionLevel_by_username__(username) ==0:
                new_record = PatientInformationClass(patientInformationID, allowedOrganizations, bodyWeight, bodyHeight, upperBodyDominantSide, lowerBodyDominantSide, birthYear, gender)
                self.exerciseSession.add(new_record)
                self.exerciseSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'PatientInformation created', 'PatientInformationID': patientInformationID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the PatientInformation'})

        except Exception ,Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific PatientInformation from the database
    #Get a specific PatientInformation from the database
    #@param username(String) - the username of the user who is getting the PatientInformation. The username is used to check if used is allowed to get the PatientInformation.
    #@param patientInformationID(String) - The patientInformationID of the PatientInformation to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the PatientInformation
    # b) A status message 401, meaning that the User isn't allowed to get the PatientInformation
    # c) A status message 404, meaning that the PatientInformation doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_patientinformation(self, username, patientInformationID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_patientInformationID__(patientInformationID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :

                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"PatientInformation":['
                query = self.exerciseSession.query(PatientInformationClass).filter(PatientInformationClass.patientInformationID == patientInformationID)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0:
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the PatientInformation'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##Delete a specific PatientInformation from the database
    #Delete a specific PatientInformation from the database
    #@param username(String) - The username of the User who is deleting the PatientInformation. The username is used to check if User is allowed to delete the PatientInformation.
    #@param patientInformationID(String) - The ID of the PatientInformation
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to delete the PatientInformation
    # c) A status message 404, meaning the patientInformationID does not correspond to any PatientInformation.
    # d) A status message 500, meaning something went wrong.
    def delete_patientinformation(self, username, patientInformationID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_patientInformationID__(patientInformationID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(PatientInformationClass).filter(PatientInformationClass.patientInformationID == patientInformationID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_patientinformation_from_rehabilitationset(username, self.__RehabilitationSetID_by_PatientInformation(patientInformationID), patientInformationID)
                self.exerciseSession.delete(query.one())
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'PatientInformation deleted', 'PatientInformationID': patientInformationID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the PatientInformation'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single PatientInformation in the database
    #Update a specific aspect of a single PatientInformation in the database
    #@param username(String) - The username of the User who is updating the PatientInformation. The username is used to check if User is allowed to update the PatientInformation.
    #@param patientInformationID(String) - The ID of the PatientInformation
    #@param field(String) - The field's name you want to update in the PatientInformation
    #@param value(String) - The value you want to insert in the 'field' in PatientInformation
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the PatientInformation
    # b) A status message 404, meaning the patientInformationID does not correspond to any PatientInformation.
    # c) A status message 500, meaning something went wrong.
    def update_patientinformation(self, username, patientInformationID, field, value):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_patientInformationID__(patientInformationID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(PatientInformationClass).filter(PatientInformationClass.patientInformationID == patientInformationID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(PatientInformationClass, field):value})
                self.exerciseSession.commit()

                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the PatientInformation'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Retrieve a JSON-formatted list of RehabilitationSets
    #Retrieve a JSON-formatted list of RehabilitationSets.
    #@param username(String) - the username of the user who is fetching the RehabilitationSets-list. The username is used to check if used is allowed to list the RehabilitationSets.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of RehabilitationSets
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_rehabilitationsets(self, username):
        try:
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"RehabilitationSets":['
            if self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(RehabilitationSetClass)
            else:
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.allowedOrganizations.contains(self.__organizationID_by_username__(username)))
            self.exerciseSession.commit()
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0 :
                       jsonText += ","
            jsonText += "]}"
            return jsonText

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##Create a new RehabilitationSet to the database
    #Create an new RehabilitationSet to the database
    #@param username(String) - The username of the User who is creating the new RehabilitationSet. The username is used to check if User is allowed to create the RehabilitationSet.
    #@param patientConditionIDs(String) - A CSV-formatted String of patientConditionIDs that belong to this RehabilitationSet
    #@param patientInformationID(String) - The patientInformationID that belongs to the PatientInformation belonging to the RehabilitationSet
    #@param exerciseResultIDs(String)(voluntary) - A CSV-formatted String of exerciseResultIDs that belong to this RehabilitationSet
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the RehabilitationSetID of the created RehabilitationSet
    # b) A status message 401, meaning the User isn't allowed to create a RehabilitationSet
    # c) A status message 500, meaning something went wrong.
    def create_rehabilitationset(self, username, allowedOrganizations, patientConditionIDs, patientInformationID, exerciseResultIDs=""):
        rehabilitationSetID = "rehabilitationSetID" + "{:.6f}".format(time.time())
        try:
            if (self.__permissionLevel_by_username__(username) <4 and  self.__organizationID_by_username__(username) in allowedOrganizations) or self.__permissionLevel_by_username__(username) ==0 :
                new_record = RehabilitationSetClass(rehabilitationSetID, allowedOrganizations, exerciseResultIDs, patientConditionIDs, patientInformationID)
                self.exerciseSession.add(new_record)
                self.exerciseSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'RehabilitationSet created', 'RehabilitationSetID': rehabilitationSetID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the RehabilitationSet'})

        except Exception ,Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific RehabilitationSet from the database
    #Get a specific RehabilitationSet from the database
    #@param username(String) - the username of the user who is getting the RehabilitationSet. The username is used to check if used is allowed to get the RehabilitationSet.
    #@param rehabilitationSetID(String) - The rehabilitationSetID of the RehabilitationSet to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the RehabilitationSet
    # b) A status message 401, meaning the User isn't allowed to get the RehabilitationSet
    # b) A status message 404, meaning that the RehabilitationSet doesn't exist
    # c) A status message 500, meaning something went wrong.
    def get_rehabilitationset(self, username, rehabilitationSetID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"RehabilitationSet":['
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID == rehabilitationSetID)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##Update a specific aspect of a single RehabilitationSet in the database
    #Update a specific aspect of a single RehabilitationSet in the database
    #@param username(String) - The username of the User who is updating the RehabilitationSet. The username is used to check if User is allowed to update the RehabilitationSet.
    #@param rehabilitationSetID(String) - The ID of the RehabilitationSet
    #@param field(String) - The field's name you want to update in the RehabilitationSet
    #@param value(String) - The value you want to insert in the 'field' in RehabilitationSet
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the RehabilitationSet
    # b) A status message 404, meaning the rehabilitationSetID does not correspond to any RehabilitationSet.
    # c) A status message 500, meaning something went wrong.
    def update_rehabilitationset(self, username, rehabilitationSetID, field, value):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID == rehabilitationSetID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(RehabilitationSetClass, field):value})
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add allowed Organization to a RehabilitationSet
    #Add allowed Organization to a RehabilitationSet
    #@param username(String) - The username of the User adding the Organization to the Patient. Used to check if the User is allowed to edit the Patient
    #@param rehabilitationSetID(String) - The ID of the RehabilitationSet to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this RehabilitationSet
    # c) A status message 404, meaning the RehabilitationSet wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_rehabilitationSet(self, username, rehabilitationSetID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'RehabilitationSetID':rehabilitationSetID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.allowedOrganizations: organizationIDs})
                        conditions_split = query.one().patientConditionIDs.split(";")
                        for item in conditions_split:
                            self.exerciseSession.query(PatientConditionClass).filter(PatientConditionClass.patientConditionID == item).update({PatientConditionClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.query(PatientInformationClass).filter(PatientInformationClass.patientInformationID == query.one().patientInformationID).update({PatientInformationClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'RehabilitationSetID:':rehabilitationSetID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'RehabilitationSet not found'})

                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for RehabilitationSet', 'RehabilitationSetID' : rehabilitationSetID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from a RehabilitationSet
    #Remove allowed Organization from a RehabilitationSet
    #@param username(String) - The username of the User removing the Organization from the Patient. Used to check if the User is allowed to edit the Patient
    #@param patientID(String) - The ID of the Patient from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove the Organization from the RehabilitationSet
    # b) A status message 404, meaning the Organization within the RehabilitationSet or the RehabilitationSet wasn't found
    # b) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_rehabilitationSet(self, username, rehabilitationSetID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID == rehabilitationSetID)
                if len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'RehabilitationSet not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        organizationIDs = ';'.join(organizationIDs_split)
                        conditions_split = query.one().patientConditionIDs.split(";")
                        for item in conditions_split:
                            self.exerciseSession.query(PatientConditionClass).filter(PatientConditionClass.patientConditionID == item).update({PatientConditionClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.query(PatientInformationClass).filter(PatientInformationClass.patientInformationID == query.one().patientInformationID).update({PatientInformationClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID == rehabilitationSetID).update({RehabilitationSetClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in RehabilitationSet'})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for RehabilitationSet'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Delete a specific RehabilitationSet from the database
    #Delete a specific RehabilitationSet from the database
    #@param username(String) - The username of the User who is deleting the RehabilitationSet. The username is used to check if User is allowed to delete the RehabilitationSet.
    #@param rehabilitationSetID(String) - The ID of the RehabilitationSet
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 404, meaning the rehabilitationSetID does not correspond to any RehabilitationSet.
    # c) A status message 500, meaning something went wrong.
    def delete_rehabilitationset(self, username, rehabilitationSetID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID == rehabilitationSetID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_rehabilitation_set_from_patient(username, self.__PatientID_by_RehabilitationSet(rehabilitationSetID), rehabilitationSetID)
                self.exerciseSession.delete(query.one())
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'RehabilitationSet deleted', 'RehabilitationSetID': rehabilitationSetID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add an ExerciseResult to a RehabilitationSet
    #Add an ExerciseResult to a RehabilitationSet
    #@param username(String) - The username of the user adding the ExerciseResult to the RehabilitationSet. Username is used to check if the user has the right to edit the RehabilitationSet
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet that the ExerciseResult is added to
    #@param exerciseResultID(String) - The ExerciseResultID to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to add the ExerciseResult to the RehabilitationSet
    # c) A status message 500, meaning something went wrong, details in the errormessage
    def add_exerciseresult_to_rehabilitationset(self, username, rehabilitationSetID, exerciseResultID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    resultIDs = query.one().exerciseResultIDs
                    resultIDs_split = resultIDs.split(";")
                    if exerciseResultID in resultIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'ExerciseResultID already exists in the current RehabilitationSet', 'RehabilitationSetID' : rehabilitationSetID})

                    else:
                        if len(resultIDs) == 0:
                            resultIDs = exerciseResultID
                        else:
                            resultIDs += ";"+exerciseResultID

                        resultIDs = ''.join(resultIDs)
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.exerciseResultIDs: resultIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'ExerciseResultID added', 'RehabilitationSetID' : rehabilitationSetID, 'ExerciseResultID:':exerciseResultID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an ExerciseResult to the RehabilitationSet'})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove an ExerciseResult from a RehabilitationSet
    #Remove an ExerciseResult from a RehabilitationSet
    #@param username(String) - The username of the user removing the ExerciseResult from the RehabilitationSet. Username is used to check if the user has the right to edit the RehabilitationSet
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet that the ExerciseResult is removed from
    #@param exerciseResultID(String) - The ExerciseResultID to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to remove the PatientCondition from the RehabilitationSet
    # c) A status message 404, meaning the RehabilitationSet or Exerciseresult wasn't found.
    # d) A status message 500, meaning something went wrong, details in the errormessage
    def remove_exerciseresult_from_rehabilitationset(self, username, rehabilitationSetID, exerciseResultID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    resultIDs = query.one().exerciseResultIDs
                    resultIDs_split = resultIDs.split(";")
                    if exerciseResultID in resultIDs_split:
                        resultIDs_split.remove(exerciseResultID)
                        resultIDs = ';'.join(map(str, resultIDs_split))
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.exerciseResultIDs: resultIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'ExerciseResultID removed', 'RehabilitationSetID' : rehabilitationSetID, 'ExerciseResultID:':exerciseResultID})

                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'ExerciseResultID not found in RehabilitationSet, nothing was removed', 'RehabilitationSetID' : rehabilitationSetID, 'ExerciseResultID': exerciseResultID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an ExerciseResult from the RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Add an PatientCondition to a RehabilitationSet
    #Add an PatientCondition to a RehabilitationSet
    #@param username(String) - The username of the user adding the PatientCondition to the RehabilitationSet. Username is used to check if the user has the right to edit the RehabilitationSet
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet that the PatientCondition is added to
    #@param patientConditionID(String) - The PatientConditionID to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to add the PatientCondition to the RehabilitationSet
    # c) A status message 404, meaning the RehabilitationSet wasn't found
    # b) A status message 500, meaning something went wrong, details in the errormessage
    def add_patientcondition_to_rehabilitationset(self, username, rehabilitationSetID, patientConditionID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    resultIDs = query.one().patientConditionIDs
                    resultIDs_split = resultIDs.split(";")
                    if patientConditionID in resultIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'PatientConditionID already exists in the current RehabilitationSet'})

                    else:
                        if len(resultIDs) == 0:
                            resultIDs = patientConditionID
                        else:
                            resultIDs += ";"+patientConditionID

                        resultIDs = ''.join(resultIDs)
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.patientConditionIDs: resultIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'PatientConditionID added', 'RehabilitationSetID' : rehabilitationSetID, 'PatientConditionID:':patientConditionID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Rehabilitationset was not found', 'RehabilitationSetID' : rehabilitationSetID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for RehabilitationSetID', 'RehabilitationSetID' : rehabilitationSetID})
            else:
                self.exerciseSession.rollback()
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an PatientConditionID to the RehabilitationSet'})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove a PatientCondition from a RehabilitationSet
    #Remove a PatientCondition from a RehabilitationSet
    #@param username(String) - The username of the user removing the PatientCondition from the RehabilitationSet. Username is used to check if the user has the right to edit the RehabilitationSet
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet that the PatientCondition is removed from
    #@param patientConditionID(String) - The PatientCondition to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to remove the PatientCondition from the RehabilitationSet
    # c) A status message 404, meaning the RehabilitationSet or PatientCondition wasn't found.
    # d) A status message 500, meaning something went wrong, details in the errormessage
    def remove_patientcondition_from_rehabilitationset(self, username, rehabilitationSetID, patientConditionID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    resultIDs = query.one().patientConditionIDs
                    resultIDs_split = resultIDs.split(";")
                    if patientConditionID in resultIDs_split:
                        resultIDs_split.remove(patientConditionID)
                        resultIDs = ';'.join(map(str, resultIDs_split))
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.patientConditionIDs: resultIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'ExerciseResultID removed', 'RehabilitationSetID' : rehabilitationSetID, 'PatientConditionID:':patientConditionID})

                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'PatientConditionID not found in RehabilitationSet, nothing was removed', 'RehabilitationSetID' : rehabilitationSetID, 'PatientConditionID': patientConditionID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Rehabilitationset was not found', 'RehabilitationSetID' : rehabilitationSetID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for RehabilitationSetID', 'RehabilitationSetID' : rehabilitationSetID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an ExerciseResult from the RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Add a PatientInformation to a RehabilitationSet
    #Add a PatientInformation to a RehabilitationSet
    #@param username(String) - The username of the user adding the PatientInformation to the RehabilitationSet. Username is used to check if the user has the right to edit the RehabilitationSet
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet that the PatientInformation is added to
    #@param patientInformationID(String) - The PatientInformationID to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to add the PatientInformation to the RehabilitationSet
    # c) A status message 404, meaning the RehabilitationSet wasn't found
    # b) A status message 500, meaning something went wrong, details in the errormessage
    def add_patientinformation_to_rehabilitationset(self, username, rehabilitationSetID, patientInformationID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    resultIDs = query.one().patientInformationID
                    resultIDs_split = resultIDs.split(";")
                    if patientInformationID in resultIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'PatientInformationID already exists in the current RehabilitationSet'})

                    else:
                        if len(resultIDs) == 0:
                            resultIDs = patientInformationID
                        else:
                            self.exerciseSession.rollback()
                            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':'You can only have one PatientInformation in RehabilitationSet'})

                            #resultIDs += ";"+patientInformationID

                        resultIDs = ''.join(resultIDs)
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.patientInformationID: resultIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'PatientInformationID added', 'RehabilitationSetID' : rehabilitationSetID, 'PatientInformationID:':patientInformationID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Rehabilitationset was not found', 'RehabilitationSetID' : rehabilitationSetID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for RehabilitationSetID', 'RehabilitationSetID' : rehabilitationSetID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an PatientInformationID to the RehabilitationSet'})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove a PatientInformation from a RehabilitationSet
    #Remove a PatientInformation from a RehabilitationSet
    #@param username(String) - The username of the user removing the PatientInformation from the RehabilitationSet. Username is used to check if the user has the right to edit the RehabilitationSet
    #@param rehabilitationSetID(String) - The RehabilitationSetID of the RehabilitationSet that the PatientInformation is removed from
    #@param patientInformationID(String) - The PatientInformation to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to remove the PatientInformation from the RehabilitationSet
    # c) A status message 404, meaning the RehabilitationSet or PatientInformation wasn't found.
    # d) A status message 500, meaning something went wrong, details in the errormessage
    def remove_patientinformation_from_rehabilitationset(self, username, rehabilitationSetID, patientInformationID):
        try:
            if (self.__permissionLevel_by_username__(username) <4 and self.__allowedOrganization_in_rehabilitationSetID__(rehabilitationSetID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) ==0 :
                query = self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID)
                if len(query.all()) == 1:
                    resultIDs = query.one().patientInformationID
                    resultIDs_split = resultIDs.split(";")
                    if patientInformationID in resultIDs_split:
                        resultIDs_split.remove(patientInformationID)
                        resultIDs = ';'.join(map(str, resultIDs_split))
                        self.exerciseSession.query(RehabilitationSetClass).filter(RehabilitationSetClass.rehabilitationSetID==rehabilitationSetID).update({RehabilitationSetClass.patientInformationID: resultIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'ExerciseResultID removed', 'RehabilitationSetID' : rehabilitationSetID, 'PatientInformationID:':patientInformationID})

                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'PatientConditionID not found in RehabilitationSet, nothing was removed', 'RehabilitationSetID' : rehabilitationSetID, 'PatientInformationID': patientInformationID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Rehabilitationset was not found', 'RehabilitationSetID' : rehabilitationSetID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for RehabilitationSetID', 'RehabilitationSetID' : rehabilitationSetID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an ExerciseResult from the RehabilitationSet'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})



    ##Create a new ExerciseResult to the database
    #Create an new ExerciseResult to the database
    #@param username(String) - The username of the User who is creating the new ExerciseResult. The username is used to check if User is allowed to create the ExerciseResult.
    #@param exerciseID - The ID of the Exercise this Exerciseresult is a result of
    #@param dataIDs -The corresponding dataIDs
    #@param started - When was the Exercise started (EPOC)
    #@param ended - When was the Exercise finished (EPOC)
    #@param settings - Possible settings in JSON-formatted string
    #@param values - The data-values associated with the result.
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the RehabilitationSetID of the created RehabilitationSet
    # b) A status message 401, meaning the User isn't allowed to create the ExerciseResult
    # c) A status message 500, meaning something went wrong.
    def create_exerciseresult(self, username, exerciseID, dataIDs, allowedOrganizations, started, ended, settings, values, progress =""):
        exerciseResultID = "exerciseresult_" + "{:.6f}".format(time.time())
        try:
            if (self.__permissionLevel_by_username__(username) < 4 and self.__organizationID_by_username__(username) in allowedOrganizations) or self.__permissionLevel_by_username__(username) == 0:
                new_record = ExerciseResultClass(exerciseResultID, exerciseID, dataIDs, allowedOrganizations, started, ended, settings, values, progress)
                self.exerciseSession.add(new_record)
                self.exerciseSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'ExerciseResult created', 'ExerciseResultID': exerciseResultID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the ExerciseResult '})
        except Exception ,Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##List all ExerciseResults by Exercise
    #List all ExerciseResults by Exercise
    #@param username(String) - The username of the User who is listing the ExerciseResults. The username is used to check if User is allowed to list the ExerciseResults.
    #@param exerciseID - The ID of the Exercise yhr ExerciseResults are sorted by.    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and the list of ExerciseResults
    # b) A status message 204, meaning the query resulted in 0 results.
    # c) A status message 401, meaning the User isn't allowed to list the ExerciseResults
    # d) A status message 500, meaning something went wrong.
    def  list_exerciseresults_by_exercise(self, username, exerciseID):
        try:
            if self.__permissionLevel_by_username__(username) < 6:
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"ExerciseResults":['
                if self.__permissionLevel_by_username__(username) == 0:
                    query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseID == exerciseID)
                else:
                    query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseID == exerciseID).filter(self.__organizationID_by_username__(username) in ExerciseResultClass.allowedOrganizations )
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the ExerciseResults '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred',  'ErrorText':Argument.message})

    ##Update a specific aspect of a single ExerciseResult in the database
    #Update a specific aspect of a single ExerciseResult in the database
    #@param username(String) - The username of the User who is updating the ExerciseResult. The username is used to check if User is allowed to update the ExerciseResult.
    #@param exerciseResultID(String) - The ID of the ExerciseResult
    #@param field(String) - The field's name you want to update in the ExerciseResult
    #@param value(String) - The value you want to insert in the 'field' in ExerciseResult
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the ExerciseResult
    # c) A status message 404, meaning the exerciseResultID does not correspond to any ExerciseResult.
    # d) A status message 500, meaning something went wrong.
    def update_exerciseresult(self, username, exerciseResultID, field, value):
        try:
            if (self.__permissionLevel_by_username__(username) < 4 and self.__allowedOrganization_in_exerciseResultID__(exerciseResultID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0 :
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID == exerciseResultID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(ExerciseResultClass, field):value})
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the ExerciseResult '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific ExerciseResult from the database
    #Get a specific ExerciseResult from the database
    #@param username(String) - the username of the user who is getting the ExerciseResult. The username is used to check if used is allowed to get the ExerciseResult.
    #@param exerciseResultID(String) - The exerciseResultID of the ExerciseResult to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the ExerciseResult
    # b) A status message 401, meaning that the User isn't allowed to get the ExerciseResult
    # c) A status message 404, meaning that the ExerciseResult doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_exerciseresult(self, username, exerciseResultID):
        try:
            if (self.__permissionLevel_by_username__(username) < 6 and self.__allowedOrganization_in_exerciseResultID__(exerciseResultID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0 :
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"ExerciseResult":['
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID == exerciseResultID)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the ExerciseResult '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText ':Argument.message})

    ##Delete a specific ExerciseResult from the database
    #Delete a specific ExerciseResult from the database
    #@param username(String) - The username of the User who is deleting the ExerciseResult. The username is used to check if User is allowed to delete the ExerciseResult.
    #@param exerciseResultID(String) - The ID of the ExerciseResult
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to delete the ExerciseResult
    # b) A status message 404, meaning the exerciseResultID does not correspond to any ExerciseResult.
    # c) A status message 500, meaning something went wrong.
    def delete_exerciseresult(self, username, exerciseResultID):
        try:
            if (self.__permissionLevel_by_username__(username) < 4 and self.__allowedOrganization_in_exerciseResultID__(exerciseResultID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0 :
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID == exerciseResultID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                elif rowcount == 1:
                    self.remove_exerciseresult_from_rehabilitationset(username,self.__RehabilitationSetID_by_ExerciseResult(exerciseResultID), exerciseResultID)
                    self.exerciseSession.delete(query.one())
                    self.exerciseSession.commit()
                    return json.dumps({'status_code': '200', 'msg': 'ExerciseResult deleted', 'ExerciseResultID': exerciseResultID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExerciseResultID'})

            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the ExerciseResult '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})



    ##Add a Data to an ExerciseResult
    #Add a Data to an ExerciseResult
    #@param username(String) - The username of the user adding the Data to the ExerciseResult. Username is used to check if the user has the right to edit the ExerciseResult
    #@param exerciseResultID(String) - The ExerciseResultID of the ExerciseResult to which the Data is added to
    #@param dataID(String) - The DataID to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to add Data to the ExerciseResult
    # c) A status message 404, meaning the ExerciseResult wasn't found
    # d) A status message 500, meaning something went wrong, details in the errormessage
    def add_data_to_exerciseresult(self, username, exerciseResultID, dataID):
        try:
            if (self.__permissionLevel_by_username__(username) < 4 and self.__allowedOrganization_in_exerciseResultID__(exerciseResultID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0 :
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'ExerciseResult wasnt found'})

                elif rowcount == 1:
                    dataIDs = query.one().dataIDs
                    dataIDs_split = dataIDs.split(";")
                    if dataID in dataIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'DataID already exists in the current ExerciseResult', 'ExerciseResultID' : exerciseResultID, 'DataID': dataID})

                    else:
                        if len(dataIDs) == 0:
                            resultIDs = exerciseResultID
                        else:
                            dataIDs += ";"+dataID

                        dataIDs = ''.join(dataIDs)
                        self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID).update({ExerciseResultClass.dataIDs: dataIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'DataID added', 'DataID' : dataID, 'ExerciseResultID:':exerciseResultID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExercoseResultID'})

            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add the Data to the ExerciseResult '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove a Data from an ExerciseResult
    #Remove a Data from an ExerciseResult
    #@param username(String) - The username of the user removing the Data from the ExerciseResult. Username is used to check if the user has the right to edit the ExerciseResult
    #@param exerciseResultID(String) - The ExerciseResultID of the ExerciseResult from which the Data is removed from
    #@param dataID(String) - The DataID of the Data to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to add Data to ExerciseResult
    # c) A status message 404, meanint the Data or the ExerciseResult wasn't found.
    # d) A status message 500, meaning something went wrong, details in the errormessage
    def remove_dataid_from_exerciseresult(self, username, exerciseResultID, dataID):
        try:
            if (self.__permissionLevel_by_username__(username) < 4 and self.__allowedOrganization_in_exerciseResultID__(exerciseResultID, self.__organizationID_by_username__(username)) == "true") or self.__permissionLevel_by_username__(username) == 0 :
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID == exerciseResultID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'ExerciseResult wasnt found'})
                elif rowcount == 1:
                    dataIDs = query.one().dataIDs
                    dataIDs_split = dataIDs.split(";")
                    if dataID in dataIDs_split:
                        dataIDs_split.remove(dataID)
                        dataIDs = ';'.join(dataIDs_split)
                        self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID).update({ExerciseResultClass.dataIDs: dataIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'DataID removed', 'ExerciseResultID' : exerciseResultID, 'DataID:':dataID})

                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'DataID not found in ExerciseResult, nothing was removed', 'ExerciseResultID' : exerciseResultID, 'DataID': dataID})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExercoseResultID'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove the Data from the ExerciseResult '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Add allowed Organization to an ExerciseResult
    #Add allowed Organization to an ExerciseResult
    #@param username(String) - The username of the User adding the Organization to the ExerciseResult. Used to check if the User is allowed to edit the ExerciseResult
    #@param exerciseResultID(String) - The ID of the ExerciseResult to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this ExerciseResult
    # c) A status message 404, meaning the ExerciseResult wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_exerciseresult(self, username, exerciseResultID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_exerciseResultID(exerciseResultID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'ExerciseResultID':exerciseResultID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        organizationIDs = ''.join(organizationIDs)
                        self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID).update({ExerciseResultClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'ExerciseResultID:':exerciseResultID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'ExerciseResult not found'})

                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExerciseResult', 'ExerciseResultID' : exerciseResultID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this ExerciseResult'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from an ExerciseResult
    #Remove allowed Organization from an ExerciseResult
    #@param username(String) - The username of the User adding the Organization to the Patient. Used to check if the User is allowed to edit the ExerciseResult
    #@param exerciseResultID(String) - The ID of the ExerciseResult from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove an Organization from this ExerciseResult
    # c) A status message 404, meaning the ExerciseResult wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_exerciseresult(self, username, exerciseResultID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_exerciseResultID(exerciseResultID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID)
                if len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        organizationIDs = ';'.join(organizationIDs_split)
                        self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID).update({ExerciseResultClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in ExerciseResult'})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExerciseResult'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this ExerciseResult'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add Exercise to an ExerciseResult
    #Add Exercise to an ExerciseResult
    #@param username(String) - The username of the User adding the Exercise to the ExerciseResult. Used to check if the User is allowed to edit the ExerciseResult
    #@param exerciseResultID(String) - The ID of the ExerciseResult to which the Exercise is added to.
    #@param exerciseID(String) - The exerciseID of the Exercise to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Exercise to this ExerciseResult
    # c) A status message 404, meaning the ExerciseResult wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_exercise_to_exerciseresult(self, username, exerciseResultID, exerciseID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_exerciseResultID(exerciseResultID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID)
                if len(query.all()) == 1:
                    exerciseIDs = query.one().exerciseID
                    exerciseIDs_split = exerciseIDs.split(";")
                    if exerciseID in exerciseIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'ExerciseResultID':exerciseResultID})

                    else:
                        if len(exerciseIDs) == 0:
                            exerciseIDs = exerciseID
                        else:
                            #organizationIDs += ";"+organizationID
                            self.exerciseSession.rollback()
                            return json.dumps({'status_code': '500', 'msg': 'You can only have one Exercise in ExerciseResult'})


                        exerciseIDs = ''.join(exerciseIDs)
                        self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID).update({ExerciseResultClass.exerciseID: exerciseIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Exercise added', 'ExerciseID' : exerciseIDs, 'ExerciseResultID:':exerciseResultID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'ExerciseResult not found'})

                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExerciseResult', 'ExerciseResultID' : exerciseResultID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Exercise to this ExerciseResult'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove an Exercise from an ExerciseResult
    #Remove an Exercise  from an ExerciseResult
    #@param username(String) - The username of the User adding the Exercise to the ExerciseResult. Used to check if the User is allowed to edit the ExerciseResult
    #@param exerciseResultID(String) - The ID of the ExerciseResult from which the Exercise is removed from.
    #@param exerciseID(String) - The ExerciseID of the Exercise to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove an Exercise from this ExerciseResult
    # c) A status message 404, meaning the ExerciseResult wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_exercise_from_exerciseresult(self, username, exerciseResultID, exerciseID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_exerciseResultID(exerciseResultID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID)
                if len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    exerciseIDs = query.one().exerciseID
                    exerciseIDs_split = exerciseIDs.split(";")
                    if exerciseID in exerciseIDs:
                        exerciseIDs.remove(exerciseID)
                        exerciseIDs = ';'.join(exerciseIDs_split)
                        self.exerciseSession.query(ExerciseResultClass).filter(ExerciseResultClass.exerciseResultID==exerciseResultID).update({ExerciseResultClass.exerciseID: exerciseIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Exercise removed'})
                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Exercise not in ExerciseResult'})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for ExerciseResult'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Exercise from this ExerciseResult'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})




    ##Retrieve a JSON-formatted list of Devices
    #Retrieve a JSON-formatted list of Devices.
    #@param username(String) - the username of the user who is fetching the Devices-list. The username is used to check if used is allowed to list the Devices.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of Devices
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_devices(self, username):
        try:
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Devices":['
            if self.__permissionLevel_by_username__(username) < 4:
                query = self.sensorSession.query(DeviceClass)
            else:
                query = self.sensorSession.query(DeviceClass).filter(DeviceClass.allowedOrganizations.contains(self.__organizationID_by_username__(username)))
            self.sensorSession.commit()
            rowcount = len(query.all())
            if rowcount == 0:
                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0 :
                        jsonText += ","
            jsonText += "]}"
            return jsonText
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Create a new Device to the database
    #Create an new Device to the database
    #@param username(String) - The username of the User who is creating the new Device. The username is used to check if User is allowed to create the Device.
    #@param allowedOrganizations - OrganizationIDs of the Organizations whose users are allowed to use the Device
    #@param name(String) - Name of the sensor device
    #@param type(String) - Type of the sensor
    #@param description(String)- Description of the device
    #@param axisCount(Integer) - How many axises of measurement are there? (One would expect 1-3)
    #@param valueUnit(String) - The unit of measurement (Kilograms, newtons, kilometers per hour...)
    #@param valueUnitAbbreviation(String) - How do you abbreviate the unit of measurement (kg, N, km/h)
    #@param defaultValue(Double) - What is the default value of the measurement, if there is no imput
    #@param maximumValue(Double) - What is the maximum value that can be measured
    #@param minimumValue(Double) - What is the miminimum value that can be measured (Can also be the minimum detection threshold)
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the DeviceID of the created Device
    # b) A status message 401, meaning the User isnt't allowed to create the Device
    # c) A status message 500, meaning something went wrong.
    def create_device(self, username, allowedOrganizations, name, type, description, axisCount, valueUnit, valueUnitAbbreviation, defaultValue, maximumValue, minimumValue):
        deviceID = "device_" + "{:.6f}".format(time.time())
        try:
            if (self.__organizationID_by_username__(username) in allowedOrganizations and self.__permissionLevel_by_username__(username) <4) or self.__permissionLevel_by_username__(username) == 0 :
                new_record = DeviceClass(deviceID, allowedOrganizations, name, type, description, axisCount, valueUnit, valueUnitAbbreviation, defaultValue, maximumValue, minimumValue)
                self.sensorSession.add(new_record)
                self.sensorSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'Device created', 'DeviceID': deviceID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the Device '})

        except Exception ,Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorType': Argument.args, 'ErrorText':Argument.message})

    ##Get a specific Device from the database
    #Get a specific Device from the database
    #@param username(String) - the username of the user who is getting the Device. The username is used to check if used is allowed to get the Device.
    #@param deviceID(String) - The DeviceID of the Device to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the Device
    # b) A status message 401, meaning the User isn't allowed to get the Device
    # c) A status message 404, meaning that the Device doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_device(self, username, deviceID):
        try:
            if (self.__allowedOrganizations_in_deviceID__(deviceID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) <6) or self.__permissionLevel_by_username__(username) == 0 :
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"Device":['
                query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID == deviceID)
                self.sensorSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the Device '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single Device in the database
    #Update a specific aspect of a single Device in the database
    #@param username(String) - The username of the User who is updating the Device. The username is used to check if User is allowed to update the Device.
    #@param deviceID(String) - The ID of the Device
    #@param field(String) - The field's name you want to update in the Device
    #@param value(String) - The value you want to insert in the 'field' in Device
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the Device
    # c) A status message 404, meaning the deviceID does not correspond to any Device.
    # d) A status message 500, meaning something went wrong.
    def update_device(self, username, deviceID, field, value):
        try:
            if (self.__allowedOrganizations_in_deviceID__(deviceID, self.__organizationID_by_username__(username))=="true" and self.__permissionLevel_by_username__(username) <4) or self.__permissionLevel_by_username__(username) == 0 :
                query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID == deviceID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(DeviceClass, field):value})
                self.sensorSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the Device '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Delete a specific Device from the database
    #Delete a specific Device from the database
    #@param username(String) - The username of the User who is deleting the Device. The username is used to check if User is allowed to delete the Device.
    #@param deviceID(String) - The ID of the Device
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to delete the Device
    # b) A status message 404, meaning the deviceID does not correspond to any Device.
    # c) A status message 500, meaning something went wrong.
    def delete_device(self, username, deviceID):
        try:
            if (self.__allowedOrganizations_in_deviceID__(deviceID, self.__organizationID_by_username__(username))=="true" and self.__permissionLevel_by_username__(username) <4) or self.__permissionLevel_by_username__(username) == 0 :
                query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID == deviceID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                while self.__DataID_by_Device(deviceID) != "":
                    self.remove_device_from_data(username, self.__DataID_by_Device(deviceID), deviceID)
                self.sensorSession.delete(query.one())
                self.sensorSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Device deleted', 'DeviceID': deviceID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the Device '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add allowed Organization to a Device
    #Add allowed Organization to a Device
    #@param username(String) - The username of the User adding the Organization to the Device. Used to check if the User is allowed to edit the Device
    #@param deviceID(String) - The ID of the Device to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this Device
    # c) A status message 404, meaning the Device wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_device(self, username, deviceID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_deviceID(deviceID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID==deviceID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.sensorSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'DeviceID':deviceID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        organizationIDs = ''.join(organizationIDs)
                        self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID==deviceID).update({DeviceClass.allowedOrganizations: organizationIDs})
                        self.sensorSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'DeviceID:':deviceID})
                elif len(query.all()) == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Device not found'})

                else:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Device', 'DeviceID' : deviceID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this Device'})

        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from a Device
    #Remove allowed Organization from a Device
    #@param username(String) - The username of the User adding the Organization to the Device. Used to check if the User is allowed to edit the Device
    #@param deviceID(String) - The ID of the Device from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove an Organization from this Device
    # c) A status message 404, meaning the Device wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_device(self, username, deviceID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_deviceID(deviceID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID==deviceID)
                if len(query.all()) == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        organizationIDs = ';'.join(organizationIDs_split)
                        self.sensorSession.query(DeviceClass).filter(DeviceClass.deviceID==deviceID).update({DeviceClass.allowedOrganizations: organizationIDs})
                        self.sensorSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.sensorSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in Device'})
                else:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Device'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this Device'})

        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Create a new Data to the database
    #Create an new Data to the database
    #@param username(String) - The username of the User who is creating the new Data. The username is used to check if User is allowed to create the Data.
    #@param deviceID(String) - The ID of the device that is associated with the samples
    #@param samples(String) - Data-samples in JSON-formatted String
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the DataID of the created Data
    # b) A status message 401, meaning the User isn't allowed to create the Data
    # c) A status message 500, meaning something went wrong.
    def create_data(self,allowedOrganizations, username, deviceID, samples):
        dataID = "dataset_" + "{:.6f}".format(time.time())
        try:
            if (self.__organizationID_by_username__(username) in allowedOrganizations and self.__permissionLevel_by_username__(username) <4) or self.__permissionLevel_by_username__(username) == 0 :
                new_record = DataClass(dataID, deviceID, allowedOrganizations,  samples)
                self.sensorSession.add(new_record)
                self.sensorSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'Data created', 'dataID': dataID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the Data '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific Data from the database
    #Get a specific Data from the database
    #@param username(String) - the username of the user who is getting the Data. The username is used to check if used is allowed to get the Data.
    #@param dataID(String) - The DataID of the Data to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the Data
    # b) A status message 401, meaning the User isn't allowed to get the Data
    # c) A status message 404, meaning that the Data doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_data(self, username, dataID):
        try:
            if (self.__allowedOrganizations_in_dataID__(dataID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) <6) or self.__permissionLevel_by_username__(username) == 0 :
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"Data":['
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID == dataID)
                self.sensorSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the Data '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single Data in the database
    #Update a specific aspect of a single Data in the database
    #@param username(String) - The username of the User who is updating the Data. The username is used to check if User is allowed to update the Data.
    #@param dataID(String) - The ID of the Data
    #@param field(String) - The field's name you want to update in the Data
    #@param value(String) - The value you want to insert in the 'field' in Data
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the Data
    # c) A status message 404, meaning the dataID does not correspond to any Data.
    # d) A status message 500, meaning something went wrong.
    def update_data(self, username, dataID, field, value):
        try:
            if (self.__allowedOrganizations_in_dataID__(dataID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) <4) or self.__permissionLevel_by_username__(username) == 0 :
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID == dataID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(DataClass, field):value})
                self.sensorSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the Data '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Delete a specific Data from the database
    #Delete a specific Data from the database
    #@param username(String) - The username of the User who is deleting the Data. The username is used to check if User is allowed to delete the Data.
    #@param dataID(String) - The ID of the Data
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to delete the Data
    # c) A status message 404, meaning the dataID does not correspond to any Data.
    # d) A status message 500, meaning something went wrong.
    def delete_data(self, username, dataID):
        try:
            if (self.__allowedOrganizations_in_dataID__(dataID, self.__organizationID_by_username__(username)) == "true" and self.__permissionLevel_by_username__(username) <4) or self.__permissionLevel_by_username__(username) == 0 :
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID == dataID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                self.remove_dataid_from_exerciseresult(username, self.__ExerciseResultID_by_Data(dataID), dataID )
                self.sensorSession.delete(query.one())
                self.sensorSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Data deleted', 'DataID': dataID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the Data '})
        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add allowed Organization to a Data
    #Add allowed Organization to a Data
    #@param username(String) - The username of the User adding the Organization to the Data. Used to check if the User is allowed to edit the Data
    #@param dataID(String) - The ID of the Data to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this Data
    # c) A status message 404, meaning the Data wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_data(self, username, dataID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_dataID(dataID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.sensorSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'DataID':dataID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        organizationIDs = ''.join(organizationIDs)
                        self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID).update({DataClass.allowedOrganizations: organizationIDs})
                        self.sensorSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'DataID:':dataID})
                elif len(query.all()) == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Data not found'})

                else:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Data', 'DataID' : dataID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this Data'})

        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from a Data
    #Remove allowed Organization from a Data
    #@param username(String) - The username of the User remove the Organization from the Data. Used to check if the User is allowed to edit the Data
    #@param dataID(String) - The ID of the Data from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove an Organization from this Data
    # c) A status message 404, meaning the Data wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_data(self, username, dataID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_dataID(dataID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID)
                if len(query.all()) == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        organizationIDs = ';'.join(organizationIDs_split)
                        self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID).update({DataClass.allowedOrganizations: organizationIDs})
                        self.sensorSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.sensorSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in Data'})
                else:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Data'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this Data'})

        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add Device to a Data
    #Add Device to a Data
    #@param username(String) - The username of the User adding the Device to the Data. Used to check if the User is allowed to edit the Data
    #@param dataID(String) - The ID of the Data to which the Device is added to.
    #@param deviceID(String) - The DeviceID of the Device to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Device to this Data
    # c) A status message 404, meaning the Data wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_device_to_data(self, username, dataID, deviceID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_dataID(dataID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID)
                if len(query.all()) == 1:
                    deviceIDs = query.one().deviceID
                    deviceIDs_split = deviceIDs.split(";")
                    if deviceID in deviceIDs_split:
                        self.sensorSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Device is already in Data'})

                    else:
                        if len(deviceIDs) == 0:
                            deviceIDs = deviceID
                        else:
                            #organizationIDs += ";"+organizationID
                            return json.dumps({'status_code': '500', 'msg': 'You can only have one Device in Data'})


                        deviceIDs = ''.join(deviceIDs)
                        self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID).update({DataClass.deviceID: deviceIDs})
                        self.sensorSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Device added', 'DeviceID' : deviceIDs, 'DataID:':dataID})
                elif len(query.all()) == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Data not found'})

                else:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Data', 'DataID' : dataID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add a Device to this Data'})

        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove Device from a Data
    #Remove Device from a Data
    #@param username(String) - The username of the User removing the Device to the Data. Used to check if the User is allowed to edit the Data
    #@param dataID(String) - The ID of the Data from which the Organization is removed from.
    #@param deviceID(String) - The DeviceID of the Device to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove a Device from this Data
    # c) A status message 404, meaning the Data wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_device_from_data(self, username, dataID, deviceID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_dataID(dataID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID)
                if len(query.all()) == 0:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Data not found'})

                elif len(query.all()) == 1:
                    deviceIDs = query.one().deviceID
                    deviceIDs_split = deviceIDs.split(";")
                    if deviceID in deviceIDs:
                        deviceIDs_split.remove(deviceID)
                        deviceIDs = ';'.join(deviceIDs_split)
                        self.sensorSession.query(DataClass).filter(DataClass.dataID==dataID).update({DataClass.deviceID: deviceIDs})
                        self.sensorSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Device removed'})
                    else:
                        self.sensorSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Device not in Data'})
                else:
                    self.sensorSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Data'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove a Device from this Data'})

        except Exception , Argument:
            self.sensorSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

     ##Create a new Exercise to the database
    #Create an new Exercise to the database
    #@param username(String) - The username of the User who is creating the new Exercise. The username is used to check if User is allowed to create the Exercise.
    #@param name(String) - Name of the Exercise
    #@param description(String) - Description of the Exercise
    #@param settings(String) - A JSON-formatted string of settings that describe the exercise.
    #@return A JSON-formatted response string. It is either
    # a) A status message 201 and the ExerciseID of the created Exercise
    # b) A status message 401, meaning the User isn't allowed to create the Exercise
    # c) A status message 500, meaning something went wrong.
    def create_exercise(self, username, allowedOrganizations, name, description, settings):
        exerciseID = "exercise_" + "{:.6f}".format(time.time())
        try:
            if self.__permissionLevel_by_username__(username) < 4:
                new_record = ExerciseClass(exerciseID, allowedOrganizations, name, description, settings)
                self.exerciseSession.add(new_record)
                self.exerciseSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'Exercise created', 'ExerciseID': exerciseID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to create the Exercise '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific Exercise from the database
    #Get a specific Exercise from the database
    #@param username(String) - the username of the user who is getting the Exercise. The username is used to check if used is allowed to get the Exercise.
    #@param exerciseID(String) - The ExerciseID of the Exercise to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the Exercise
    # b) A status message 401, meaning the User isn't allowed to get the Exercise
    # c) A status message 404, meaning that the Exercise doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_exercise(self, username, exerciseID):
        try:
            if self.__permissionLevel_by_username__(username) < 6:
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"Exercise":['
                query = self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID == exerciseID)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the Exercise '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Retrieve a JSON-formatted list of Exercises
    #Retrieve a JSON-formatted list of Exercises.
    #@param username(String) - the username of the user who is fetching the Exercises-list. The username is used to check if used is allowed to list the Exercises.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of Exercises
    # b) A status message 401, meaning the User isn't allowed to list Exercises
    # c) A status message 204, meaning there is nothing to show
    # d) A status message 500, meaning something went wrong.
    def list_exercises(self, username):
        try:
            if self.__permissionLevel_by_username__(username) < 6:
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"Exercises":['
                query = self.exerciseSession.query(ExerciseClass)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to get the Exercise '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred',  'ErrorText':Argument.message})

    ##Update a specific aspect of a single Exercise in the database
    #Update a specific aspect of a single Exercise in the database
    #@param username(String) - The username of the User who is updating the Exercise. The username is used to check if User is allowed to update the Exercise.
    #@param exerciseID(String) - The ID of the Exercise
    #@param field(String) - The field's name you want to update in the Exercise
    #@param value(String) - The value you want to insert in the 'field' in Exercise
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User isn't allowed to update the Exercise
    # c) A status message 404, meaning the exerciseID does not correspond to any Exercise.
    # d) A status message 500, meaning something went wrong.
    def update_exercise(self, username, exerciseID, field, value):
        try:
            if self.__permissionLevel_by_username__(username) < 4:
                query = self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID == exerciseID)
                self.exerciseSession.commit()
                rowcount = len(query.all())
                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(ExerciseClass, field):value})
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to update the Exercise '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

   ##Delete a specific Exercise from the database
    #Delete a specific Exercise from the database
    #@param username(String) - The username of the User who is deleting the Exercise. The username is used to check if User is allowed to delete the Exercise.
    #@param exerciseID(String) - The ID of the Exercise
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 404, meaning the exerciseID does not correspond to any Exercise.
    # c) A status message 500, meaning something went wrong.
    def delete_exercise(self, username, exerciseID):
        try:
            if self.__permissionLevel_by_username__(username) < 4:
                query = self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID == exerciseID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results, nothing was deleted'})
                while self.__ExerciseResultID_by_Exercise(exerciseID) != "":
                    self.remove_exercise_from_exerciseresult(username, self.__ExerciseResultID_by_Exercise(exerciseID), exerciseID)
                self.exerciseSession.delete(query.one())
                self.exerciseSession.commit()
                return json.dumps({'status_code': '200', 'msg': 'Data deleted', 'ExerciseID': exerciseID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to delete the Exercise '})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Add allowed Organization to an Exercise
    #Add allowed Organization to an Exercise
    #@param username(String) - The username of the User adding the Organization to the Exercise. Used to check if the User is allowed to edit the Exercise
    #@param exercise(String) - The ID of the Exercise to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this Exercise
    # c) A status message 404, meaning the Exercise wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_exercise(self, username, exerciseID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_exerciseID(exerciseID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID==exerciseID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'ExerciseID':exerciseID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        organizationIDs = ''.join(organizationIDs)
                        self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID==exerciseID).update({ExerciseClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'ExerciseID:':exerciseID})
                elif len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Exercise not found'})

                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Exercise', 'ExerciseID' : exerciseID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this ExerciseResult'})

        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from an Exercise
    #Remove allowed Organization from an Exercise
    #@param username(String) - The username of the User adding the Organization to the Exercise. Used to check if the User is allowed to edit the Exercise
    #@param exerciseID(String) - The ID of the Exercise from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove an Organization from this Exercise
    # c) A status message 404, meaning the Exercise wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_exercise(self, username, exerciseID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_exerciseID(exerciseID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID==exerciseID)
                if len(query.all()) == 0:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        organizationIDs = ';'.join(organizationIDs_split)
                        self.exerciseSession.query(ExerciseClass).filter(ExerciseClass.exerciseID==exerciseID).update({ExerciseClass.allowedOrganizations: organizationIDs})
                        self.exerciseSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.exerciseSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in Exercise'})
                else:
                    self.exerciseSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for Exercise'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this Exercise'})
        except Exception , Argument:
            self.exerciseSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Create a new AnalysisTask to the database
    #Create an new AnalysisTask to the database
    #@param username(String) - The username of the User who is creating the new AnalysisTask. The username is used to check if User is allowed to create the AnalysisTask.
    #@param taskname(String) - Name of the AnalysisTask
    #@param analysisModule(String) - The analysis module belonging to the analysis
    #@param status(String) - Status of the analysis
    #@param notification(String) - Notifications
    #@param configurationParameters(String) - Configuration parameters in JSON-format
    #@param started(Integer) - Starttime (EPOC)
    #@param ended(Integer)(voluntary) - Endtime (EPOC)
    #@param analysisResult(String)(voluntary) - Results of the analysis in JSON format
    # a) A status message 201 and the TaskID of the created AnalysisTask
    # b) A status message 401, meaning the User is not allowed to create the AnalysisTask
    # d) A status message 500, meaning something went wrong.
    def create_analysistask(self, username, allowedOrganizations, taskname, analysisModule, status, notification, configurationParameters, started, ended=0, analysisResult=""):
        analysisTaskID = "analysistask_" + "{:.6f}".format(time.time())
        try:
            if( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in allowedOrganizations) or self.__permissionLevel_by_username__(username) == 0:
                new_record = AnalysisClass(analysisTaskID, allowedOrganizations, username, taskname, analysisModule, analysisResult, status, notification, configurationParameters, started, ended)
                self.analysisSession.add(new_record)
                self.analysisSession.commit()
                return json.dumps({'status_code': '201', 'msg': 'Analysis-job creater', 'TaskID': analysisTaskID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'User not allowed to create the AnalysisTask'})

        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

   ##Delete a specific AnalysisTask from the database
    #Delete a specific AnalysisTask from the database
    #@param username(String) - The username of the User who is deleting the AnalysisTask. The username is used to check if User is allowed to delete the AnalysisTask.
    #@param analysisTaskID(String) - The ID of the AnalysisTask
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the user is not allowed to delete an AnalysisTask
    # c) A status message 404, meaning the analysisTaskID does not correspond to any AnalysisTask.
    # d) A status message 500, meaning something went wrong.
    def delete_analysistask(self, username, analysisTaskID):
        try:
            if( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_analysisTaskID(analysisTaskID)) or self.__permissionLevel_by_username__(username) == 0:

                query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID == analysisTaskID)
                if len(query.all()) == 1:
                    self.analysisSession.delete(query.one())
                    self.analysisSession.commit()
                elif len(query.all()) >1:
                    self.analysisSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Too many results for AnalysisTask'})

                return json.dumps({'status_code': '200', 'msg': 'Analysis-job deleted', 'TaskID': analysisTaskID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'User not allowed to delete the AnalysisTask'})

        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Retrieve a JSON-formatted list of AnalysisTasks
    #Retrieve a JSON-formatted list of AnalysisTasks.
    #@param username(String) - the username of the user who is fetching the AnalysisTasks-list. The username is used to check if used is allowed to list the AnalysisTasks.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and A JSON of AnalysisTasks
    # b) A status message 204, meaning there is nothing to show
    # c) A status message 500, meaning something went wrong.
    def list_analysistasks(self, username):
        try:
            if(self.__permissionLevel_by_username__(username) == 0):
                query = self.analysisSession.query(AnalysisClass)
            else:
                query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.allowedOrganizations.ilike(self.__organizationID_by_username__(username)))
            self.analysisSession.commit()
            jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
            jsonText = jsonText.strip('}')
            jsonText += ',"Analyses":['
            rowcount = len(query.all())
            if rowcount == 0:

                return json.dumps({'status_code': '204', 'msg': 'Query resulted in 0 results'})
            for item in query:
                    rowcount -= 1
                    jsonText += json.dumps(item.tojson())
                    if rowcount != 0 :
                        jsonText += ","
            jsonText += "]}"

            return jsonText
        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Get a specific AnalysisTask from the database
    #Get a specific AnalysisTask from the database
    #@param username(String) - the username of the user who is getting the AnalysisTask. The username is used to check if used is allowed to get the AnalysisTask.
    #@param analysisTaskID(String) - The AnalysisTaskID of the AnalysisTask to be fetched.
    #@return A JSON-formatted response string. It is either
    # a) A status message 200 and a JSON of the AnalysisTask
    # b) A status message 401, meaning the User is not allowed to get the AnalysisTask
    # c) A status message 404, meaning that the AnalysisTask doesn't exist
    # d) A status message 500, meaning something went wrong.
    def get_analysistask(self, username, analysisTaskID):
        try:
            if( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_analysisTaskID(analysisTaskID)) or self.__permissionLevel_by_username__(username) == 0:
                jsonText = json.dumps({'status_code': '200', 'msg': 'Success'})
                jsonText = jsonText.strip('}')
                jsonText += ',"Analysis":['
                query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID == analysisTaskID)
                self.analysisSession.commit()
                rowcount = len(query.all())

                if rowcount == 0:
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                for item in query:
                        rowcount -= 1
                        jsonText += json.dumps(item.tojson())
                        if rowcount != 0 :
                            jsonText += ","
                jsonText += "]}"
                return jsonText
            else:
                return json.dumps({'status_code': '401', 'msg': 'User not allowed to get AnalysisTask'})

        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Update a specific aspect of a single AnalysisTask in the database
    #Update a specific aspect of a single AnalysisTask in the database
    #@param username(String) - The username of the User who is updating the AnalysisTask. The username is used to check if User is allowed to update the AnalysisTask.
    #@param analysisTaskID(String) - The ID of the AnalysisTask
    #@param field(String) - The field's name you want to update in the AnalysisTask
    #@param value(String) - The value you want to insert in the 'field' in AnalysisTask
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to update the AnalysisTask
    # c) A status message 404, meaning the analysisTaskID does not correspond to any AnalysisTask.
    # d) A status message 500, meaning something went wrong.
    def update_analysistask(self, username, analysisTaskID, field, value):
        try:
            if( self.__permissionLevel_by_username__(username) <4 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_analysisTaskID(analysisTaskID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID == analysisTaskID)
                rowcount = len(query.all())
                if rowcount == 0:
                    self.analysisSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Query resulted in 0 results'})
                query.update({getattr(AnalysisClass, field):value})
                self.analysisSession.commit()

                return json.dumps({'status_code': '200', 'msg': 'Success'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'User not allowed to update AnalysisTask'})

        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})


    ##Add allowed Organization to an AnalysisTask
    #Add allowed Organization to an AnalysisTask
    #@param username(String) - The username of the User adding the Organization to the AnalysisTask. Used to check if the User is allowed to edit the AnalysisTask
    #@param analysisTaskID(String) - The ID of the AnalysisTask to which the Organization is added to.
    #@param organizationID(String) - The OrganizationID of the Organization to be added
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to add an Organization to this AnalysisTask
    # c) A status message 404, meaning the AnalysisTask wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def add_allowed_organization_to_analysistask(self, username, analysisTaskID, organizationID):
        print "Allowed in task: " + self.__allowedOrganizations_by_analysisTaskID(analysisTaskID)
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_analysisTaskID(analysisTaskID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID==analysisTaskID)
                if len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs_split:
                        self.analysisSession.rollback()
                        return json.dumps({'status_code': '500', 'msg': 'Organization is already allowed', 'OrganizationID' : organizationID, 'AnalysisTaskID':analysisTaskID})

                    else:
                        if len(organizationIDs) == 0:
                            organizationIDs = organizationID
                        else:
                            organizationIDs += ";"+organizationID

                        organizationIDs = ''.join(organizationIDs)
                        self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID == analysisTaskID).update({AnalysisClass.allowedOrganizations: organizationIDs})
                        self.analysisSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization added', 'OrganizationID' : organizationIDs, 'AnalysisTaskID:':analysisTaskID})
                elif len(query.all()) == 0:
                    self.analysisSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'ExerciseResult not found'})

                else:
                    self.analysisSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for AnalysisTask', 'AnalysisTaskID' : analysisTaskID})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to add an Organization to this AnalysisTask'})

        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})

    ##Remove allowed Organization from an AnalysisTask
    #Remove allowed Organization from an AnalysisTask
    #@param username(String) - The username of the User adding the Organization to the AnalysisTask. Used to check if the User is allowed to edit the AnalysisTask
    #@param analysisTaskID(String) - The ID of the AnalysisTask from which the Organization is removed from.
    #@param organizationID(String) - The OrganizationID of the Organization to be removed
    #@return A JSON-formatted response string. It is either
    # a) A status message 200, meaning everything went as expected.
    # b) A status message 401, meaning the User is not allowed to remove an Organization from this AnalysisTask
    # c) A status message 404, meaning the AnalysisTask wasn't found
    # d) A status message 500, meaning something went wrong, details in message.
    def remove_allowed_organization_from_analysistask(self, username, analysisTaskID, organizationID):
        try:
            if( self.__permissionLevel_by_username__(username) <2 and self.__organizationID_by_username__(username) in self.__allowedOrganizations_by_analysisTaskID(analysisTaskID)) or self.__permissionLevel_by_username__(username) == 0:
                query = self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID==analysisTaskID)
                if len(query.all()) == 0:
                    self.analysisSession.rollback()
                    return json.dumps({'status_code': '404', 'msg': 'Organization not found'})

                elif len(query.all()) == 1:
                    organizationIDs = query.one().allowedOrganizations
                    organizationIDs_split = organizationIDs.split(";")
                    if organizationID in organizationIDs:
                        organizationIDs_split.remove(organizationID)
                        organizationIDs = ';'.join(organizationIDs_split)
                        self.analysisSession.query(AnalysisClass).filter(AnalysisClass.analysistaskID==analysisTaskID).update({AnalysisClass.allowedOrganizations: organizationIDs})
                        self.analysisSession.commit()
                        return json.dumps({'status_code': '200', 'msg': 'Organization removed'})
                    else:
                        self.analysisSession.rollback()
                        return json.dumps({'status_code': '404', 'msg': 'Organization not in AnalysisTask'})
                else:
                    self.analysisSession.rollback()
                    return json.dumps({'status_code': '500', 'msg': 'Multiple results for AnalysisTask'})
            else:
                return json.dumps({'status_code': '401', 'msg': 'You are not allowed to remove an Organization from this AnalysisTask'})

        except Exception , Argument:
            self.analysisSession.rollback()
            return json.dumps({'status_code': '500', 'msg': 'An error occurred', 'ErrorText':Argument.message})
