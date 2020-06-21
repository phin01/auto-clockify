import requests
import datetime
from login_info import LoginInfo


class CallClockify():
    """ 
    Handle HTTP requests for Clockify API

    """

    def __init__(self):
        self.API_URL = 'https://api.clockify.me/api/v1/' # clockify API root URL

        loginInfo = LoginInfo()
        self.API_KEY = loginInfo.get_api_key() # API key
        self.WSPACENAME = loginInfo.get_workspace_name() # workspace name

        self.WSPACE = None
        self.USER = None
        self.check_login_info() # sets user ID and workspace ID


    def get_tags(self) -> list:
        """ return list of tags from workspace """
        URL = self.API_URL + 'workspaces/' + str(self.WSPACE) + '/tags'
        headers = {'X-Api-Key': str(self.API_KEY) }
        try:
            r = requests.get(url=URL, headers=headers)
            return r.json() if r.status_code == 200 else False # return json list of tags if request goes through with no problems, otherwise False
        except:
            return False


    def get_time(self) -> str:
        """ return datetime.now() formatted as a string for API input """
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") # time string formatted according to Clockify API requirements
    

    def create_time_entry(self, time: str, title: str, tags=[]) -> bool:
        """ 
            create new time entry using time(str) and tags(list) as input
            return True if status_code is 201 from a successful request
        """
        URL = self.API_URL + 'workspaces/' + str(self.WSPACE) + '/time-entries'
        headers = {'X-Api-Key': str(self.API_KEY), 'Content-Type': 'application/json'} 
        payload = {
            "start": time,
            "description": title,
            "tagIds": tags
        }
        try:
            r = requests.post(url=URL, headers=headers, json=payload)
            return r.status_code == 201 # success
        except:
            return False


    def stop_time_entry(self, time: str) -> bool:
        """ 
            stops currently running time entry, setting input time as end time
            returns True if status_code is 200 (successfully stopped) or 404 (no entry was running)
        """
        URL = self.API_URL + 'workspaces/' + str(self.WSPACE) + '/user/' + str(self.USER) + '/time-entries'
        headers = {'X-Api-Key': str(self.API_KEY), 'Content-Type': 'application/json'}
        payload = { 
            "end": time
        } 
        try:
            r = requests.patch(url=URL, headers=headers, json=payload)
            return r.status_code == 200 or r.status_code == 404 # successfully stopped or no running time entries to be stopped
        except:
            return False


    def check_login_info(self) -> bool:
        """ 
            based on api-key and workspace name provided in login_info.json file,
            attempt to find user ID and workspace ID from clockify API
            sets variables and return True if found, returns False if either can't be found
        """
        URL = self.API_URL + 'user'
        headers = {'X-Api-Key': self.API_KEY }
        try:
            r = requests.get(url=URL, headers=headers)
            if r.status_code == 200:
                self.USER = r.json()['id'] # sets user ID
                URL = self.API_URL + 'workspaces'
                r = requests.get(url=URL, headers=headers)
                if r.status_code == 200:
                    wspace = [wspace['id'] for wspace in r.json() if wspace['name'].upper() in self.WSPACENAME.upper()]
                    self.WSPACE = wspace[0] if wspace else 'False' # sets workspace ID

            return False if not self.USER or not self.WSPACE else True
        except:
            return False
