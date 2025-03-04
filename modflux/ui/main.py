# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(915, 909)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableMods = QTableView(self.centralwidget)
        self.tableMods.setObjectName(u"tableMods")
        self.tableMods.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.horizontalLayout.addWidget(self.tableMods)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonActivate = QPushButton(self.centralwidget)
        self.buttonActivate.setObjectName(u"buttonActivate")

        self.verticalLayout.addWidget(self.buttonActivate)

        self.buttonDownload = QPushButton(self.centralwidget)
        self.buttonDownload.setObjectName(u"buttonDownload")

        self.verticalLayout.addWidget(self.buttonDownload)

        self.buttonImport = QPushButton(self.centralwidget)
        self.buttonImport.setObjectName(u"buttonImport")

        self.verticalLayout.addWidget(self.buttonImport)

        self.buttonSettings = QPushButton(self.centralwidget)
        self.buttonSettings.setObjectName(u"buttonSettings")

        self.verticalLayout.addWidget(self.buttonSettings)

        self.buttonQuit = QPushButton(self.centralwidget)
        self.buttonQuit.setObjectName(u"buttonQuit")

        self.verticalLayout.addWidget(self.buttonQuit, 0, Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 80)
        self.horizontalLayout.setStretch(1, 20)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 915, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
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

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.buttonActivate.setText(QCoreApplication.translate("MainWindow", u"Activate", None))
        self.buttonDownload.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.buttonImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.buttonSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.buttonQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

