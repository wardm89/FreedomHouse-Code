class CareCase():
    def __init__(self, pastoral_care_request):
        self.title = CareCase.get_title(pastoral_care_request)
        self.description = CareCase.get_description(pastoral_care_request)
        self.household_id = pastoral_care_request['contact'][0]['Household_ID'] # "Household Record" 2 is Inactive | 206 Laurel Crest Dr | Kannapolis
        self.contact_id = pastoral_care_request['Contact_ID'] # "People Record" 2 Is the Default Contact ID 
        self.start_date = pastoral_care_request['Response_Date']
        self.end_date = None
        self.care_case_type_id = 13
        self.location_id = pastoral_care_request['Location_ID']
        self.case_manager = 6 # "Administration User Record" 6 is ***Unassigned, Contact
        self.share_with_group_leaders = False
        self.program_id = None

    def get_care_case(self):
        return  {
        "Title": self.title,
        "Description": self.description,
        "Household_ID": self.household_id,
        "Contact_ID": self.contact_id,
        "Start_Date": self.start_date,
        "End_Date": self.end_date,
        "Care_Case_Type_ID": self.care_case_type_id,
        "Location_ID": self.location_id,
        "Case_Manager": self.case_manager,
        "Share_With_Group_Leaders": self.share_with_group_leaders,
        "Program_ID": self.program_id
    }

    @staticmethod
    def get_title(pastoral_care_request):
        return pastoral_care_request['answers'][0]['Response'] + ' ' + pastoral_care_request['answers'][3]['Response']

    @staticmethod
    def get_description(pastoral_care_request):
        desc = f"Recipient: {pastoral_care_request['answers'][0]['Response']}"
        desc = desc + "\n" + f"Circumstance: {pastoral_care_request['answers'][3]['Response']}"
        desc = desc + "\n"
        desc = desc + "\n" + f"Campus: {pastoral_care_request['answers'][1]['Response']}"
        desc = desc + "\n" + f"Care recipient is a: {pastoral_care_request['answers'][2]['Response']}"
        desc = desc + "\n"
        desc = desc + "\n" + f"Please describe the need. {pastoral_care_request['answers'][4]['Response']}"
        desc = desc + "\n" + f"When and how did you become aware of the need? {pastoral_care_request['answers'][5]['Response']}"
        desc = desc + "\n" + f"What has been done? {pastoral_care_request['answers'][6]['Response']}"
        desc = desc + "\n"
        desc = desc + "\n" + f"Please share Contact Number and any other information to assist with follow up care. {pastoral_care_request['answers'][7]['Response']}"
        desc = desc + "\n\n"
        desc = desc + "\n" + f"Created via webhook from Form_Response_ID {pastoral_care_request['Form_Response_ID']}"
        return desc
