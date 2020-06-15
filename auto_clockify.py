import time
from win32gui import GetWindowText, GetForegroundWindow
import clockify
import json

""" 
    logic inspired by ssokolow's gist:
    https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8

"""


# variables
last_seen = {'xid': None, 'title': None, 'program': None}    
exec_interval = 1 # interval in seconds to check for window changes in main time.sleep loop
tags = clockify.get_tags() # list of tags from Clockify API


# receive window text and return program name
def get_selected_program(win_title: str):
    switcher = { # get specific windows title substrings and translate to used programs
        'CHROME': 'Web Browser',
        'VISUAL STUDIO CODE': 'VS Code',
        'POWER BI': 'Power BI',
        'KNIME': 'KNIME',
    }
    res = dict(filter(lambda item: item[0] in win_title.upper(), switcher.items())) # filter new dictionary with first occurrence of substring
    if len(res.keys()) > 0 and list(res.values())[0] is not None: # return value if available
        return list(res.values())[0]


def get_program_tag(win_title: str):
    filtered_tags = [tag for tag in tags if tag['name'].upper() in win_title.upper()]
    if filtered_tags:
        print(filtered_tags[0]['id'])
        print(filtered_tags[0]['name'])



if __name__ == '__main__':

    # initialize last_seen window and program with first available window after running script
    wnd = GetWindowText(GetForegroundWindow())
    last_seen['title'] = wnd
    last_seen['program'] = get_selected_program(wnd)

    while True:
        new_win_title = GetWindowText(GetForegroundWindow()) # get current window text

        if new_win_title != last_seen['title'] and new_win_title: # if it's valid and different from last window

            new_program = get_selected_program(new_win_title) # get new program from new window
            new_tag = get_program_tag(new_win_title)
            
            if new_program: # if new program requires clock switch
                last_seen['title'] = new_win_title
                print('call clockify API - ' + new_program)
                # print('call clockify API - ' + new_tag)
        time.sleep(exec_interval)

    
