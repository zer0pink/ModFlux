# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QListView,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Games(object):
    def setupUi(self, Games):
        if not Games.objectName():
            Games.setObjectName(u"Games")
        Games.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Games)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gamesList = QListView(Games)
        self.gamesList.setObjectName(u"gamesList")

        self.horizontalLayout.addWidget(self.gamesList)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.openGameButton = QPushButton(Games)
        self.openGameButton.setObjectName(u"openGameButton")

        self.verticalLayout.addWidget(self.openGameButton)

        self.createGameButton = QPushButton(Games)
        self.createGameButton.setObjectName(u"createGameButton")

        self.verticalLayout.addWidget(self.createGameButton)

        self.deleteGameButton = QPushButton(Games)
        self.deleteGameButton.setObjectName(u"deleteGameButton")

        self.verticalLayout.addWidget(self.deleteGameButton)

        self.quitButton = QPushButton(Games)
        self.quitButton.setObjectName(u"quitButton")

        self.verticalLayout.addWidget(self.quitButton, 0, Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Games)
        self.quitButton.clicked.connect(Games.reject)
        self.openGameButton.clicked.connect(Games.accept)
        self.gamesList.doubleClicked.connect(Games.on_double_click)

        QMetaObject.connectSlotsByName(Games)
    # setupUi

    def retranslateUi(self, Games):
        Games.setWindowTitle(QCoreApplication.translate("Games", u"Games", None))
        self.openGameButton.setText(QCoreApplication.translate("Games", u"Open", None))
        self.createGameButton.setText(QCoreApplication.translate("Games", u"Create", None))
        self.deleteGameButton.setText(QCoreApplication.translate("Games", u"Delete", None))
        self.quitButton.setText(QCoreApplication.translate("Games", u"Quit", None))
    # retranslateUi

