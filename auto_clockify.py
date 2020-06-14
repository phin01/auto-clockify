import time
from win32gui import GetWindowText, GetForegroundWindow

""" 
    logic inspired by ssokolow's gist:
    https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8

"""


last_seen = {'xid': None, 'title': None}  # type: Dict[str, Any]

exec_interval = 1

def wnd_changed(new_wnd: str):
    last_seen['title'] = new_wnd
    print('changed')




if __name__ == '__main__':

    # initialize last_seen window with first available window after running script
    wnd = GetWindowText(GetForegroundWindow())
    last_seen['title'] = wnd

    while True:

        new_wnd = GetWindowText(GetForegroundWindow())
        if new_wnd != last_seen['title']:
            wnd_changed(new_wnd)

        time.sleep(exec_interval)

    
