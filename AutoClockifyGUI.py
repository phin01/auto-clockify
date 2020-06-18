# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_AutoClockifyGUI(object):
    def setupUi(self, AutoClockifyGUI):
        if not AutoClockifyGUI.objectName():
            AutoClockifyGUI.setObjectName(u"AutoClockifyGUI")
        AutoClockifyGUI.resize(436, 330)
        self.pushButton = QPushButton(AutoClockifyGUI)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 100, 141, 81))

        self.retranslateUi(AutoClockifyGUI)

        QMetaObject.connectSlotsByName(AutoClockifyGUI)
    # setupUi

    def retranslateUi(self, AutoClockifyGUI):
        AutoClockifyGUI.setWindowTitle(QCoreApplication.translate("AutoClockifyGUI", u"AutoClockifyGUI", None))
        self.pushButton.setText(QCoreApplication.translate("AutoClockifyGUI", u"PushButton", None))
    # retranslateUi

