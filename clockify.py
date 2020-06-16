import requests
import login_info
import json
import time
import datetime

""" 
    Handle HTTP GET and POST requests for Clockify API

"""


# variables
API_URL = 'https://api.clockify.me/api/v1/' # clockify API root URL
API_KEY = login_info.get_api_key() # API key
WSPACE = login_info.get_workspace() # workspace ID

def get_tags():
    """ return list of tags from workspace as json list """
    URL = API_URL + 'workspaces/' + WSPACE + '/tags'
    headers = {'X-Api-Key': API_KEY }
    return requests.get(url=URL, headers=headers).json()


def get_time():
    """ return datetime.now() formatted as a string for API input """
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") # time string formatted according to Clockify API requirements


def create_time_entry():
    """ create new time entry using time and tags as input """ 





if __name__ == '__main__':
    print(get_time())