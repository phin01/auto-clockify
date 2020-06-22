import json
import os


class LoginInfo():
    """ 
    Private Login info for Clockify API
    Reads information from login_info.json file and returns keys as string

    """

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.info = json.load(open(json_path))


    def get_api_key(self):
        return self.info['clockify-api-key'] if self.info['clockify-api-key'] else False


    def get_workspace_name(self):
        return self.info['workspace-name'] if self.info['workspace-name'] else False
