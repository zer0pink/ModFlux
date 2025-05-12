# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import QHBoxLayout, QListView, QPushButton, QVBoxLayout


class Ui_Games(object):
    def setupUi(self, Games):
        if not Games.objectName():
            Games.setObjectName("Games")
        Games.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Games)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gamesList = QListView(Games)
        self.gamesList.setObjectName("gamesList")

        self.horizontalLayout.addWidget(self.gamesList)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.openGameButton = QPushButton(Games)
        self.openGameButton.setObjectName("openGameButton")

        self.verticalLayout.addWidget(self.openGameButton)

        self.createGameButton = QPushButton(Games)
        self.createGameButton.setObjectName("createGameButton")

        self.verticalLayout.addWidget(self.createGameButton)

        self.deleteGameButton = QPushButton(Games)
        self.deleteGameButton.setObjectName("deleteGameButton")

        self.verticalLayout.addWidget(self.deleteGameButton)

        self.quitButton = QPushButton(Games)
        self.quitButton.setObjectName("quitButton")

        self.verticalLayout.addWidget(self.quitButton, 0, Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Games)
        self.quitButton.clicked.connect(Games.reject)
        self.openGameButton.clicked.connect(Games.accept)
        self.gamesList.doubleClicked.connect(Games.on_double_click)

        QMetaObject.connectSlotsByName(Games)

    # setupUi

    def retranslateUi(self, Games):
        Games.setWindowTitle(QCoreApplication.translate("Games", "Games", None))
        self.openGameButton.setText(QCoreApplication.translate("Games", "Open", None))
        self.createGameButton.setText(
            QCoreApplication.translate("Games", "Create", None)
        )
        self.deleteGameButton.setText(
            QCoreApplication.translate("Games", "Delete", None)
        )
        self.quitButton.setText(QCoreApplication.translate("Games", "Quit", None))

    # retranslateUi
