import json
import os


class AutoClockifyConfig():
    """ 
    AutoClockify Configuration settings
    Private Login info for Clockify API
    Reads information from configs.json file and returns keys as string

    """

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "configs.json")
        self.info = json.load(open(json_path))


    def get_api_key(self):
        return self.info['clockify-api-key'] if self.info['clockify-api-key'] else False


    def get_workspace_name(self):
        return self.info['workspace-name'] if self.info['workspace-name'] else False


    def get_default_interval(self):
        return self.info['default-interval'] if self.info['default-interval'] else 60 # return 60 seconds in case default-interval can't be found


    def get_local_log_path(self):
        return self.info['local-log-path'] if self.info['local-log-path'] else False
