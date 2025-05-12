# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QMenu,
    QMenuBar,
    QPushButton,
    QStatusBar,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(915, 909)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filterModList = QLineEdit(self.centralwidget)
        self.filterModList.setObjectName("filterModList")

        self.verticalLayout_2.addWidget(self.filterModList)

        self.tableMods = QTableView(self.centralwidget)
        self.tableMods.setObjectName("tableMods")
        self.tableMods.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.verticalLayout_2.addWidget(self.tableMods)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonActivate = QPushButton(self.centralwidget)
        self.buttonActivate.setObjectName("buttonActivate")

        self.verticalLayout.addWidget(self.buttonActivate)

        self.buttonDownload = QPushButton(self.centralwidget)
        self.buttonDownload.setObjectName("buttonDownload")

        self.verticalLayout.addWidget(self.buttonDownload)

        self.buttonImport = QPushButton(self.centralwidget)
        self.buttonImport.setObjectName("buttonImport")

        self.verticalLayout.addWidget(self.buttonImport)

        self.buttonSettings = QPushButton(self.centralwidget)
        self.buttonSettings.setObjectName("buttonSettings")

        self.verticalLayout.addWidget(self.buttonSettings)

        self.buttonQuit = QPushButton(self.centralwidget)
        self.buttonQuit.setObjectName("buttonQuit")

        self.verticalLayout.addWidget(self.buttonQuit, 0, Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 80)
        self.horizontalLayout.setStretch(1, 20)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 915, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.buttonActivate.clicked.connect(MainWindow.handleMount)
        self.buttonDownload.clicked.connect(MainWindow.download)
        self.buttonImport.clicked.connect(MainWindow.importMod)
        self.buttonSettings.clicked.connect(MainWindow.settings)
        self.buttonQuit.clicked.connect(MainWindow.quit)
        self.tableMods.doubleClicked.connect(MainWindow.handleTableDoubleClick)
        self.tableMods.customContextMenuRequested.connect(MainWindow.contextMenu)
        self.filterModList.textEdited.connect(MainWindow.updateModListFilter)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionExit.setText(QCoreApplication.translate("MainWindow", "Exit", None))
        self.filterModList.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Filter...", None)
        )
        self.buttonActivate.setText(
            QCoreApplication.translate("MainWindow", "Activate", None)
        )
        self.buttonDownload.setText(
            QCoreApplication.translate("MainWindow", "Download", None)
        )
        self.buttonImport.setText(
            QCoreApplication.translate("MainWindow", "Import", None)
        )
        self.buttonSettings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )
        self.buttonQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", "About", None))

    # retranslateUi
