from base64 import b64encode
from datetime import datetime, timedelta
import logging
import os
import pytz
import requests
from requests import HTTPError
from dotenv import load_dotenv
from utils import print_json, get_env_variable

load_dotenv()

log = logging.getLogger('pastoral_care_log')

class MinistryPlatformClient(object):
    """ 
    This is the Ministry Platform API client class. Its purpose is to handle all requests to and from the Ministry Platform
    """
    HISTORICAL_QUERY_MINUTES = 500

    def __init__(self):
        log.info("Initializing MP Client...")
        self.access_token = self.authenticate()
        self.api_url = get_env_variable('MP_API_URL')

        # Query anything newer than the historical minutes ago (newer than 5 minutes ago)
        self.query_time = (datetime.now(pytz.timezone('America/New_York')) - timedelta(minutes=self.HISTORICAL_QUERY_MINUTES)).strftime("%Y-%m-%dT%H:%M:%S")
        self.form_fields = self.get_form_fields()
        self.locations = self.get_locations()

    def authenticate(self):
        # Set the token endpoint
        url = get_env_variable('MP_CLIENT_URL')

        # Set the client ID and secret
        client_id = get_env_variable('MP_CLIENT_ID')
        client_secret = get_env_variable('MP_CLIENT_SECRET')

        # Create the headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + b64encode(f'{client_id}:{client_secret}'.encode()).decode()
        }

        # Set the request body
        data = {
            'grant_type': 'client_credentials',
            'scope': 'http://www.thinkministry.com/dataplatform/scopes/all'
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=data).json()
        access_token = response.get("access_token", '')
        if access_token == '':
            raise ValueError

        # print(access_token)

        return access_token

    def get_auth_headers(self):
        return {
            'Authorization': 'Bearer ' + self.access_token
        }

    def get_endpoint(self, endpoint, params = ''):
        # Make the GET request

        url = self.api_url + endpoint 
        log.debug("GET: {url}")
        # print(url)
        # print_json(params)
        try:
            response = requests.get(url, headers=self.get_auth_headers(), params=params).json()
            return response
        except Exception as e:
            log.error(f"GET request failed. Endpoing: {endpoint}")
            raise Exception(e) from e

    def post_endpoint(self, endpoint, json = ''):
        # Make the POST request

        url = self.api_url + endpoint
        log.debug("POST: {url}")
        try:
            response = requests.post(url, headers=self.get_auth_headers(), json=json).json()
            return response
        except Exception as e:
            log.error(f"POST request failed. Endpoing: {endpoint}")
            raise Exception(e) from e


    def create_care_cases(self, cases):
        log.info(f"Creating {len(cases)} Pastoral Care Request(s).")
        response = self.post_endpoint('/tables/Care_Cases', json=cases)
        print_json(response)
        return response


    def print_table_names(self):
        tables = self.get_endpoint('/tables')
        table_names = []
        for table in tables:
            table_names.append(table['Name'])
        print_json(table_names)
    
    def print_form_fields(self):
        form_fields = self.get_endpoint('/tables/Form_Fields')
        fields = []
        field_ids = []
        for field in form_fields:
            if field['Form_ID'] == 36:
                fields.append(field)
                field_ids.append(field['Form_Field_ID'])
        print_json(fields)

    def get_form_fields(self):
        form_query_params = {
            '$filter': f"Form_ID = 36"
        }
        form_fields = self.get_endpoint('/tables/Form_Fields', form_query_params)
        return form_fields    
        
    def get_locations(self):
        form_fields = self.get_endpoint('/tables/Locations')
        return form_fields

    def get_pastoral_care_form_responses(self):
        log.info(f"Getting Form Responses created after: {self.query_time}")

        form_query_params = {
            '$filter': f"Response_Date >= '{self.query_time}' AND Form_ID = 36"
        }
        answer_query_params = {
            '$filter': "Form_Field_ID IN(800,801,802,803,804,805,806,807,808)"
        }

        forms = self.get_endpoint('/tables/Form_Responses', form_query_params)
        form_answers = self.get_endpoint('/tables/Form_Response_Answers', answer_query_params)

        for form in forms:
            answers = []
            for answer in form_answers:
                if answer['Form_Response_ID'] == form['Form_Response_ID']:
                    if answer['Form_Field_ID'] == 801:
                        form['Location_ID'] = self.get_location_id(answer['Response'])
                    answer['Label'] = self.get_field_label(answer['Form_Field_ID'])
                    answers.append(answer)
            
            form['answers'] = answers
            form['contact'] = self.get_contact(form['Contact_ID'])
        return forms
    
    def get_care_cases(self):
        form_query_params = {
            '$filter': f"Start_Date >= '{self.query_time}'"
        }
        care_cases = self.get_endpoint( '/tables/Care_Cases', form_query_params)
        return care_cases
        
    def get_contact(self, contact_id):
        form_query_params = {
            '$filter': f"Contact_ID  = '{contact_id}'"
        }
        care_cases = self.get_endpoint( '/tables/Contacts', form_query_params)
        return care_cases
    
    def get_field_label(self, field_id):
        fields = {x['Form_Field_ID']: x['Field_Label'] for x in self.form_fields}
        return fields.get(field_id, '')
        
    def get_location_id(self, location_name):
        locations = {x['Location_Name']: x['Location_ID'] for x in self.locations}
        return locations.get(location_name, None)


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
