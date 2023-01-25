import json
import logging
import os
import time

def configure_logs():
    print("Configuring logs...")

    log = logging.getLogger('pastoral_care_log')
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - Line #%(lineno)s - %(message)s')

    if not log.hasHandlers():
        ##### If you want to have a error log file when running LOCALLY you can uncomment this.
        # # Need to make the file like this one time because FileHandler does not make directories when creating log files
        # os.makedirs('temp', exist_ok=True)
        # file_handler = logging.FileHandler('temp/error_log.log')
        # file_handler.setLevel(logging.ERROR)
        # file_handler.setFormatter(formatter)
        # log.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        log.addHandler(stream_handler)

    return log

def print_json(data):
    json_formatted_str = json.dumps(data, indent=2)
    print(json_formatted_str)

def get_env_variable(key):
    """Gets the environment variables and raises and error if they are not there.
    Args:
        key (str): Environment variable key name.
    Raises:
        ValueError:
    Returns:
        str: The environment variable's value.
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing {key} from environment.")

    return value

def print_execution_time():
    """Logs the total execution time for the script.
    """
    log = logging.getLogger('pastoral_care_log')
    start_time = float(os.getenv("START_TIME", 0))
    difference = round(time.time() - start_time, 2)
    # Yes I know it's not a critical error. This will just separate it.
    log.critical(f"Execution time... {difference} seconds") 
