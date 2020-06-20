import time
from win32gui import GetWindowText, GetForegroundWindow
from call_clockify import CallClockify
import threading

class AutoClockify():

    """ 
    logic inspired by ssokolow's gist:
    https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8

    Monitor changes from active window titles, gets tags registered in Clockify workspace and calls Clockify API as needed

    """

    def __init__(self):
        self.clockify = CallClockify() # object to handle all API calls to Clockify
        self.tags = self.clockify.get_tags() # list of tags from Clockify API
        self.last_seen = {'xid': None, 'title': None, 'program': None, 'tags': None}  # initializes list to hold previous window's info
        self.exec_interval = 1 # interval in seconds to check for window changes in main time.sleep loop
        self.minimized = False # all windows minimized (stops time entries)

        # initialize last_seen window and program with first available window after running script
        wnd = GetWindowText(GetForegroundWindow())
        self.last_seen['title'] = wnd
        self.last_seen['tags'] = self.get_window_tags(wnd)

        # self.start_loop()


    def get_window_tags(self, win_title: str) -> list:
        """ based on window title, get related tags from Clockify workspace tags """
        filtered_tags = [tag['id'] for tag in self.tags if tag['name'].upper() in win_title.upper()] # return list of tag IDs if tag name matches any part of window name
        if filtered_tags:
            return filtered_tags


    def reset_last_seen(self, new_title=None, new_tags=None):
        """ updates last_seen list with previous window title and tags """
        self.last_seen['title'] = new_title
        self.last_seen['tags'] = new_tags


    def handle_exit(self):
        """ stops current Clockify entry when program is closed """
        self.clockify.stop_time_entry(self.clockify.get_time())


    def update_entry(self, new_minimized: bool, new_win_title=None, new_win_tags=None):
        """ handle clockify entry requests:
            if minimized - only stop current time entry
            if not minimized - stop current time entry and start new one, with title and tags (if provided)

        """
        self.minimized = new_minimized
        entry_time = self.clockify.get_time()
        self.clockify.stop_time_entry(entry_time)
        self.reset_last_seen(new_win_title, new_win_tags)
        if not new_minimized:
            self.clockify.create_time_entry(entry_time, new_win_title, new_win_tags)


    def check_window_change(self):
        """
            check current window's title and tags
            compare to previous info stored in last_seen list and calls API if changes are needed
            this function will be called from systray in a separate thread loop every x seconds
        """
        new_win_title = GetWindowText(GetForegroundWindow()) # get current window text
        new_win_tags = self.get_window_tags(new_win_title) # get current window tags

        if not new_win_title and not self.minimized: # stops current time entry if all windows are minimized
            self.update_entry(True)

        elif new_win_title and not new_win_tags and new_win_title != self.last_seen['title']: # create untagged time entry in case no tags are found
            self.update_entry(False, new_win_title)

        elif new_win_title and new_win_tags != self.last_seen['tags']: # create regular tagged entry
            self.update_entry(False, new_win_title, new_win_tags)
