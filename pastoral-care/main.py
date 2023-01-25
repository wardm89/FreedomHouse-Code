from base64 import b64encode
import os
import sys
import time
import traceback
import requests
from dotenv import load_dotenv
from utils import configure_logs, print_json, print_execution_time
from mpClient import MinistryPlatformClient, CareCase

load_dotenv()

path = os.getcwd()
log = configure_logs()
log.info("Current directory path: " + str(path))

def main():
    log.info("----------------STARTING SCRIPT------------------")
    os.environ["START_TIME"] = str(time.time())
    error = None
    MP_CLIENT = MinistryPlatformClient()
    
    # MP_CLIENT.print_table_names()
    try:
        care_cases = MP_CLIENT.get_care_cases()
        pastoral_care_request_forms = MP_CLIENT.get_pastoral_care_form_responses()
        new_pastoral_requests = []  
        # print_json(pastoral_care_request_forms)
        # print_json(care_cases)


        if len(pastoral_care_request_forms) == 0:
            log.warning("No Pastoral Care Request Forms created within the past 5 minutes.")
            log.info("Exiting script...")
            print_execution_time()
            return "Success", 200

        if len(care_cases) == 0:
            log.info("No Pastoral Care Request found. Now going to create one.")
            # Create based on all the forms since none were found
            for care_request in pastoral_care_request_forms:
                new_pastoral_requests.append(CareCase(care_request).get_care_case())

        else:
            log.info("Pastoral Care Request found. Determining if new one needs to be created.")
            
            for care_request in pastoral_care_request_forms:
                for case in care_cases:
                    if case['Title'] != CareCase.get_title(care_request) and case['Start_Date'] != care_request['Response_Date']:
                        new_pastoral_requests.append(CareCase(care_request).get_care_case())

        # print_json(new_pastoral_requests)

        if len(new_pastoral_requests) == 0:
            log.warning("No Pastoral Care Request Forms need to be created.")
            log.info("Exiting script...")
            print_execution_time()
            return "Success", 200
        
        MP_CLIENT.create_care_cases(new_pastoral_requests)

    except requests.RequestException as e:
        error = log_error(str(e), 400)
    except:
        # We don't want to return details of internal server errors for security reasons
        error = log_error("Internal Server Error. Check logs for details.", 500)
    finally:
        if error is not None:
            return error
        else:
            return "Success", 200
    


def log_error(error, status_code=500):
    exc_info = sys.exc_info()
    trace = traceback.format_exc()
    log.error("Error: \n"
                  "- type: {} \n"
                  "- value: {} \n"
                  "- traceback: {}".format(exc_info[0], exc_info[1], trace))

    return str(error), status_code

if __name__ == '__main__':
    """
    Set environment variable to indicate this is being ran in development and not production.
    """
    os.environ["ENV"] = "DEV"
    main()