#!/usr/bin/env python3


"""
Name: System Tray Application
Author :  Rajiv Sharma
Developer Website : www.hqvfx.com
Developer Email   : rajiv@hqvfx.com
Date Started : 07 July 2019
Date Modified :
Description : Desktop client for Stdio Line Production pipeline
Download Application from : www.hqvfx.com/downloads
Source Code Website : www.github.com/hqvfx
Free Video Tutorials : www.youtube.com/vfxpipeline
Copyright (c) 2018, HQVFX(www.hqvfx.com) . All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of HQVFX(www.hqvfx.com) nor the names of any
      other contributors to this software may be used to endorse or
      promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


"""
    Multiple windows logic based on MalloyDelacroix's gist:
    https://gist.github.com/MalloyDelacroix/2c509d6bcad35c7e35b1851dfc32d161

"""


import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
import os
from auto_clockify import AutoClockify
from configs import AutoClockifyConfig
import threading
import time


class StatusWindow(QtWidgets.QWidget):

    def __init__(self, parent, default_interval):
        """ 
            status window contains buttons to start/stop tracking thread, counters for failed/successful calls to API
            and current tracking thread status (active or inactive)
            user can customize window change check interval before starting thread (default interval received from config.json file)
        """
        QtWidgets.QWidget.__init__(self)
        ui_path = os.path.join(os.path.dirname(__file__), "AutoClockifyGUI\\form.ui")
        self.ui = uic.loadUi(ui_path, self)

        self.btnStartTracker.clicked.connect(self.start_tracker) # start tracker button routine
        self.btnStopTracker.clicked.connect(self.stop_tracker) # stop tracker button routine

        self.spinBoxInterval.setValue(default_interval) # set spinbox value as default interval from config.json file

        self.sysTray = parent # systray parent object that will run start/stop functions


    def update_status_label(self, color: str, text: str):
        """ update text and color of status label in status window """
        self.lblStatus.setStyleSheet('color: ' + color)
        self.lblStatus.setText(text)


    def set_button_status(self, start_button: bool, stop_button: bool):
        """ enable or disable buttons used to start/stop tracking thread """
        self.btnStartTracker.setEnabled(start_button)
        self.btnStopTracker.setEnabled(stop_button)
    
    
    def start_tracker(self):
        """ 
            starts tracking thread using spinbox value as time interval
            resets status label
            toggles start/stop thread buttons
        """
        self.sysTray.start_thread(self.spinBoxInterval.value())
        self.update_status_label('green', 'ACTIVE')
        self.set_button_status(False, True)


    def stop_tracker(self):
        """ 
            stops tracking thread
            resets status label
            toggles start/stop thread buttons
        """
        self.sysTray.stop_thread()
        self.update_status_label('black', 'Inactive')
        self.set_button_status(True, False)
        


    def update_counters(self, successful_updates, update_errors):
        """ updates counter labels with number of successful and failed time entry calls to API """
        self.lblSuccessCount.setText(str(successful_updates))
        self.lblErrorCount.setText(str(update_errors))


    def closeEvent(self, event):
        """ override close event for status window to only hide it (program should be closed from systray) """
        event.ignore()
        self.hide()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Clockify AutoTracker - Disabled')
        menu = QtWidgets.QMenu(parent)
        configs = AutoClockifyConfig()

        self.clockify = AutoClockify() # start Clockify tracker, actual tracking to be called later
        self.should_stop = threading.Event() # threading event to monitor tracker start/stop
        
        self.exec_interval = configs.get_default_interval()
        self.statusWindow = StatusWindow(self, self.exec_interval) # start status window, functions only show/hide it later

        self.successful_updates = 0
        self.update_errors = 0
        
        # menu options
        open_window = menu.addAction("Open Status Window")
        open_window.triggered.connect(self.show_status_window)
        open_window.setIcon(QtGui.QIcon("icon.png"))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(self.close_systray)
        exit_.setIcon(QtGui.QIcon("icon.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)
        

    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.show_status_window()


    def show_status_window(self):
        self.statusWindow.show()


    def tracking_thread(self, should_stop):
        """ 
            runs auto tracker check_window_change on separate thread 
            thread will run in a loop every x seconds according to self.exec_interval variable
            thread will stop once should_stop thread event is set
        """
        self.clockify.check_window_change()
        while should_stop.is_set():
            return_code = self.clockify.check_window_change() # returns -1 if error, 1 if successful and 0 if no changes needed
            print(return_code)
            if return_code != 0:
                self.toggle_icon_tooltip(True, return_code)
                if return_code == 1:
                    self.successful_updates += 1
                else:
                    self.update_errors += 1
                self.statusWindow.update_counters(self.successful_updates, self.update_errors)
            time.sleep(self.exec_interval)


    def toggle_icon_tooltip(self, active: bool, error_code=0):
        """ 
            systray icon and tooltip represent tracker's status
            when starting/stopping tracker, both should be updated according to bool parameter
        """
        if error_code == -1:
            icon_status = 'error'
        else:
            icon_status = 'enabled' if active else 'disabled'

        icon_path = os.path.join(os.path.dirname(__file__), 'icon_' + icon_status + '.png')
        self.setIcon(QtGui.QIcon(icon_path))
        self.setToolTip(f'Clockify AutoTracker - ' + icon_status.title())


    def start_thread(self, exec_interval: int):
        """ resets should_stop thread to execution interval and starts tracking thread """
        self.exec_interval = exec_interval
        self.should_stop.set()

        thread = threading.Thread(target=self.tracking_thread, args=(self.should_stop,))
        thread.start()
        self.toggle_icon_tooltip(True)


    def stop_thread(self):
        """ stop tracking thread, including any possible currently running time entries """
        self.clockify.handle_exit() 
        self.should_stop.clear()
        self.toggle_icon_tooltip(False)


    def close_systray(self):
        """ closes systray and tracking thread """
        self.hide()
        self.statusWindow.hide()
        self.stop_thread() 
        self.clockify = None
        sys.exit()


class Controller:

    def __init__(self):
        pass


    def show_tray(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon_disabled.png")
        self.tray = SystemTrayIcon(QtGui.QIcon(icon_path))
        self.tray.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_tray()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()