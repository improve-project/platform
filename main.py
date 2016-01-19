__author__ = 'tommipor'
import time
import database_handler

def main():
        dbHandler = database_handler.DatabaseHandler()
        ended=time.time()*1000
        STATUS_READY = "Ready"
        username="Evalan_u_1"
        result = {'oldMeanError': 0.0, 'oldErrors': [-3.0, 3.0, 0.0, 0.0], 'currentMeanError': 0.0, 'currentErrors': [-3.0, 3.0, 0.0, 0.0]}
        analysisTaskID = "analysistask_1435306425.698266"

        #database.create_user(";", "Jani", "Yli-Kantola", "Jani", "a password", "Nurse", "")
        #database.create_user(self, username, firstName, lastName, newUsername, password, jobTitle, ):
        #database.create_exerciseresult("user", "ss", "ws","dr","","","","")
        #database.create_data("none", "this be dataid", "this be deviceid", "sample; sample; sample; sample; sample;sample")
        #database.add_exerciseresult("","Evalan_rehab_test", "1sd23s9")
        #print database.list_analysistasks("user", "analysistask_1", "notification", "modified")
        #print dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="analysisResult", value=str(result))
        #print dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="status", value=STATUS_READY)
        #print dbHandler.update_analysistask(username=username, analysisTaskID=analysisTaskID, field="ended", value=ended)
        #print dbHandler.list_analysistasks("Tommi")
        #dbHandler.__get_organization_rights__("Evalan_u_1","Evalan_1" )
        #dbHandler.__Patient_in_User__("Evalan_u_1","Evalan_test_patient")
        #print dbHandler.__permissionLevel_by_username__("Evalan_u_1")
        #print dbHandler.list_usergroups("Evalan_u_1")
        #print dbHandler.__userGroupID_by_username__("Evalan_u_1")
        #print dbHandler.__organizationID_by_username__("Evalan_u_1")
        #print dbHandler.get_usergroup("Jani_test_user_username", "usergroup1436188340.516476" )
        #print dbHandler.create_analysistask("Evalan_u_1", "Test task", "","","","","")
        #print dbHandler.update_usergroup(username="Jani_test_user_username", userGroupID="usergroup1438691764.082977", field="name", value="Tes_group_34")
        #print dbHandler.list_rehabilitationsets("Evalan_u_1")
        #print dbHandler.__organizationID_by_username__("Evalan_u_1")
        #print dbHandler.__permissionLevel_by_username__("Evalan_u_1")
        #print dbHandler.add_user_to_usergroup(username="Jani_test_user_username", userGroupID="usergroup1438693886.170913", userID="user_id_1")
        #print dbHandler.add_user_to_usergroup(username="Jani_test_user_username", userGroupID="usergroup1438693886.170913", userID="user_id_8")
        #print dbHandler.remove_user_from_usergroup(username="Jani_test_user_username", userGroupID="usergroup1438693886.170913", userID="user_id_7")
        #print dbHandler.get_user("Jani_test_user_username", "user_1438773019.000986" )
        #print dbHandler.update_user(username="Jani_test_user_username", userID="user_1438776975.655928", field="firstName", value="firstANDsecond")
        #print dbHandler.delete_user("Jani_test_user_username" , "user_1438778823.524638" )
        #print dbHandler.add_patient_to_user(username="Jani_test_user_username", userID="user_1438779915.942370", patientID="patient_E" )
        #print dbHandler.list_patients("Jani_test_user_username")
        #print dbHandler.get_patient(username="Jani_test_user_username", patientID="patient_1438864828.349008")
        #print dbHandler.add_allowed_organization_to_patient(username="Jani_test_user_username", patientID="patient_1438864828.349008", organizationID="firma")
        #print dbHandler.create_patientcondition(username="Jani_test_user_username", allowedOrganizations="organization_1438603110.140505", label="Otsikko", description="Kuvaus", officialMedicalCode="A-152")
        #print dbHandler.delete_patientinformation("Jani_test_user_username", "patientInformation1438944139.254825")
        #print dbHandler.add_allowed_organization_to_rehabilitationSet("Jani_test_user_username",  "rehabilitationSetID1439291490.190416", "loltest" )
        #print dbHandler.remove_allowed_organization_from_rehabilitationSet("Jani_test_user_username", "rehabilitationSetID1439291490.190416", "loltest")
        #print dbHandler.add_allowed_organization_to_patient("Jani_test_user_username", "testi-id", "testilol")
        #print dbHandler.remove_allowed_organization_from_patient("Jani_test_user_username", "testi-id", "testilol")
        #print dbHandler.add_allowed_organization_to_exerciseresult("Evalan_u_1", "evalan_exerciseresultid_1435325732.364940", "testilol")
        #print dbHandler.remove_allowed_organization_from_exerciseresult("Evalan_u_1", "evalan_exerciseresultid_1435325732.364940", "testilol")
        #print dbHandler.add_allowed_organization_to_exercise("Evalan_u_1", "Evalan_test_exercise", "testilol")
        #print dbHandler.remove_allowed_organization_from_exercise("Evalan_u_1", "Evalan_test_exercise", "testilol")
        #print dbHandler.add_allowed_organization_to_device("Evalan_u_1", "Evalan_test_device", "testilol")
        #print dbHandler.remove_allowed_organization_from_device("Evalan_u_1", "Evalan_test_device", "testilol")
        #print dbHandler.add_allowed_organization_to_data("Evalan_u_1", "dataset_1435325732.339890", "testilol")
        #print  dbHandler.remove_allowed_organization_from_data("Evalan_u_1", "dataset_1435325732.339890", "testilol")
        #print dbHandler.add_allowed_organization_to_analysistask("Evalan_u_1", "analysistask_1439470035.342530", "testilol")
        #print dbHandler.remove_allowed_organization_from_analysistask("Evalan_u_1", "analysistask_1439470035.342530", "testilol")
        #print dbHandler.create_analysistask("Evalan_u_1", "Evalan_1;hopoti", "Tommis test task", "analysisModule", "status", "notification", "configurationParameters", 0, 0, analysisResult="")
        #print dbHandler.delete_analysistask("Evalan_u_1", "analysistask_1439798745.107000" )
        #print dbHandler.create_patient("Evalan_u_1", "Evalan_1", "")
        #print dbHandler.delete_patient("Evalan_u_1", "patient_1439804212.542000" )
        #print dbHandler.list_analysistasks(username="Evalan_u_1")
        #print dbHandler.get_usergroup_by_username(username).organizationID
        print dbHandler.__organizationID_by_username__("Evalan_u_1")
main()