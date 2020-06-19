import json

class LoginInfo():
    """ 
    Private Login info for Clockify API
    Reads information from login_info.json file and returns keys as string

    """

    def __init__(self):
        self.info = json.load(open('login_info.json'))


    def get_api_key(self):
        return self.info['clockify-api-key']


    def get_workspace(self):
        return self.info['workspace-id']


    def get_user(self):
        return self.info['user-id']
