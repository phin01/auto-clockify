import time
from win32gui import GetWindowText, GetForegroundWindow
import clockify
import atexit
import signal
import win32api

""" 
    logic inspired by ssokolow's gist:
    https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8

"""


# variables
last_seen = {'xid': None, 'title': None, 'program': None, 'tags': None}    
exec_interval = 1 # interval in seconds to check for window changes in main time.sleep loop
tags = clockify.get_tags() # list of tags from Clockify API
minimized = False # all windows minimized (stops time entries)
undefined_entry = False # untagged window (crate untagged time entry, including only window name, for manual tagging in clockify dashboard)


def get_window_tags(win_title: str) -> list:
    filtered_tags = [tag['id'] for tag in tags if tag['name'].upper() in win_title.upper()] # return list of tag IDs if tag name matches any part of window name
    if filtered_tags:
        return filtered_tags


def reset_last_seen(new_title=None, new_tags=None):
    last_seen['title'] = new_title
    last_seen['tags'] = new_tags


def handle_exit():
    clockify.stop_time_entry(clockify.get_time())


if __name__ == '__main__':

    # initialize last_seen window and program with first available window after running script
    wnd = GetWindowText(GetForegroundWindow())
    last_seen['title'] = wnd
    last_seen['tags'] = get_window_tags(wnd)

    while True:
        new_win_title = GetWindowText(GetForegroundWindow()) # get current window text
        new_win_tags = get_window_tags(new_win_title) # get current window tags

        if not new_win_title and not minimized: # stops current time entry if all windows are minimized
            minimized = True
            clockify.stop_time_entry(clockify.get_time())
            reset_last_seen()

        elif new_win_title and not new_win_tags and new_win_title != last_seen['title']: # create untagged time entry in case no tags are found
            minimized = False
            entry_time = clockify.get_time()
            clockify.stop_time_entry(entry_time)
            clockify.create_time_entry(entry_time, new_win_title)
            reset_last_seen(new_win_title)

        elif new_win_title and new_win_tags != last_seen['tags']: # create regular tagged entry
            minimized = False
            entry_time = clockify.get_time()
            clockify.stop_time_entry(entry_time)
            clockify.create_time_entry(entry_time, new_win_title, new_win_tags)
            reset_last_seen(new_win_title, new_win_tags)

        time.sleep(exec_interval)







    
