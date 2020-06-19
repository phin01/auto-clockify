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
        self.WSPACE = loginInfo.get_workspace() # workspace ID
        self.USER = loginInfo.get_user() # Clockify user


    def get_tags(self) -> list:
        """ return list of tags from workspace """
        URL = self.API_URL + 'workspaces/' + self.WSPACE + '/tags'
        headers = {'X-Api-Key': self.API_KEY }
        return requests.get(url=URL, headers=headers).json()


    def get_time(self) -> str:
        """ return datetime.now() formatted as a string for API input """
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") # time string formatted according to Clockify API requirements
    

    def create_time_entry(self, time: str, title: str, tags=[]) -> bool:
        """ 
            create new time entry using time(str) and tags(list) as input
            return True if status_code is 201 from a successful request
        """
        URL = self.API_URL + 'workspaces/' + self.WSPACE + '/time-entries'
        headers = {'X-Api-Key': self.API_KEY, 'Content-Type': 'application/json'} 
        payload = {
            "start": time,
            "description": title,
            "tagIds": tags
        }
        r = requests.post(url=URL, headers=headers, json=payload)
        return r.status_code == 201 # success


    def stop_time_entry(self, time: str) -> bool:
        """ 
            stops currently running time entry, setting input time as end time
            returns True if status_code is 200 (successfully stopped) or 404 (no entry was running)
        """
        URL = self.API_URL + 'workspaces/' + self.WSPACE + '/user/' + self.USER + '/time-entries'
        headers = {'X-Api-Key': self.API_KEY, 'Content-Type': 'application/json'}
        payload = { 
            "end": time
        } 
        r = requests.patch(url=URL, headers=headers, json=payload)
        return r.status_code == 200 or r.status_code == 404 # successfully stopped or no running time entries to be stopped
