class CareCase():
    def __init__(self, pastoral_care_request):
        self.title = CareCase.get_title(pastoral_care_request)
        self.description = pastoral_care_request['answers'][4]['Response']
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
