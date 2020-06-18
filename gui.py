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
from AutoClockifyGUI import Ui_AutoClockifyGUI


class StatusWindow(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        ui_path = os.path.join(os.path.dirname(__file__), "AutoClockifyGUI\\form.ui")
        self.ui = uic.loadUi(ui_path, self)

        self.pushButton.clicked.connect(self.vai)


    def vai(self):
        print('vai')


    def closeEvent(self, event):
        event.ignore()
        self.hide()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Clockify AutoTracker')
        menu = QtWidgets.QMenu(parent)

        open_window = menu.addAction("Open Status Window")
        open_window.triggered.connect(self.show_status_window)
        open_window.setIcon(QtGui.QIcon("icon.png"))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon("icon.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)
        self.statusWindow = StatusWindow() # start status window, functions only show/hide it later


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


class Controller:

    def __init__(self):
        pass


    def show_tray(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.tray = SystemTrayIcon(QtGui.QIcon(icon_path))
        self.tray.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_tray()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()