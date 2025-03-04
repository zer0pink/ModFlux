# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_settings.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLayout, QPlainTextEdit,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_GameSettings(object):
    def setupUi(self, GameSettings):
        if not GameSettings.objectName():
            GameSettings.setObjectName(u"GameSettings")
        GameSettings.resize(398, 297)
        self.verticalLayout = QVBoxLayout(GameSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.downloadPathBrowse = QToolButton(GameSettings)
        self.downloadPathBrowse.setObjectName(u"downloadPathBrowse")

        self.gridLayout.addWidget(self.downloadPathBrowse, 3, 2, 1, 1)

        self.gamePathBrowse = QToolButton(GameSettings)
        self.gamePathBrowse.setObjectName(u"gamePathBrowse")

        self.gridLayout.addWidget(self.gamePathBrowse, 2, 2, 1, 1)

        self.label = QLabel(GameSettings)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.modPathBrowse = QToolButton(GameSettings)
        self.modPathBrowse.setObjectName(u"modPathBrowse")

        self.gridLayout.addWidget(self.modPathBrowse, 4, 2, 1, 1)

        self.label_3 = QLabel(GameSettings)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.overwritePathBrowse = QToolButton(GameSettings)
        self.overwritePathBrowse.setObjectName(u"overwritePathBrowse")

        self.gridLayout.addWidget(self.overwritePathBrowse, 5, 2, 1, 1)

        self.label_4 = QLabel(GameSettings)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_6 = QLabel(GameSettings)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.workPathBrowse = QToolButton(GameSettings)
        self.workPathBrowse.setObjectName(u"workPathBrowse")

        self.gridLayout.addWidget(self.workPathBrowse, 6, 2, 1, 1)

        self.label_2 = QLabel(GameSettings)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.label_5 = QLabel(GameSettings)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.label_7 = QLabel(GameSettings)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.gameNameEdit = QPlainTextEdit(GameSettings)
        self.gameNameEdit.setObjectName(u"gameNameEdit")
        self.gameNameEdit.setMaximumSize(QSize(16777215, 30))
        self.gameNameEdit.setTabChangesFocus(True)

        self.gridLayout.addWidget(self.gameNameEdit, 0, 1, 1, 1)

        self.gameIdEdit = QPlainTextEdit(GameSettings)
        self.gameIdEdit.setObjectName(u"gameIdEdit")
        self.gameIdEdit.setMaximumSize(QSize(16777215, 30))
        self.gameIdEdit.setTabChangesFocus(True)

        self.gridLayout.addWidget(self.gameIdEdit, 1, 1, 1, 1)

        self.gamePathEdit = QPlainTextEdit(GameSettings)
        self.gamePathEdit.setObjectName(u"gamePathEdit")
        self.gamePathEdit.setMaximumSize(QSize(16777215, 30))
        self.gamePathEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gamePathEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gamePathEdit.setTabChangesFocus(True)
        self.gamePathEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.gridLayout.addWidget(self.gamePathEdit, 2, 1, 1, 1)

        self.downloadPathEdit = QPlainTextEdit(GameSettings)
        self.downloadPathEdit.setObjectName(u"downloadPathEdit")
        self.downloadPathEdit.setMaximumSize(QSize(16777215, 30))
        self.downloadPathEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.downloadPathEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.downloadPathEdit.setTabChangesFocus(True)
        self.downloadPathEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.gridLayout.addWidget(self.downloadPathEdit, 3, 1, 1, 1)

        self.modPathEdit = QPlainTextEdit(GameSettings)
        self.modPathEdit.setObjectName(u"modPathEdit")
        self.modPathEdit.setMaximumSize(QSize(16777215, 30))
        self.modPathEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.modPathEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.modPathEdit.setTabChangesFocus(True)
        self.modPathEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.gridLayout.addWidget(self.modPathEdit, 4, 1, 1, 1)

        self.overwritePathEdit = QPlainTextEdit(GameSettings)
        self.overwritePathEdit.setObjectName(u"overwritePathEdit")
        self.overwritePathEdit.setMaximumSize(QSize(16777215, 30))
        self.overwritePathEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.overwritePathEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.overwritePathEdit.setTabChangesFocus(True)
        self.overwritePathEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.gridLayout.addWidget(self.overwritePathEdit, 5, 1, 1, 1)

        self.workPathEdit = QPlainTextEdit(GameSettings)
        self.workPathEdit.setObjectName(u"workPathEdit")
        self.workPathEdit.setMaximumSize(QSize(16777215, 30))
        self.workPathEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.workPathEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.workPathEdit.setTabChangesFocus(True)
        self.workPathEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.gridLayout.addWidget(self.workPathEdit, 6, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(GameSettings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(GameSettings)
        self.buttonBox.accepted.connect(GameSettings.accept)
        self.buttonBox.rejected.connect(GameSettings.reject)

        QMetaObject.connectSlotsByName(GameSettings)
    # setupUi

    def retranslateUi(self, GameSettings):
        GameSettings.setWindowTitle(QCoreApplication.translate("GameSettings", u"Edige Game", None))
        self.downloadPathBrowse.setText(QCoreApplication.translate("GameSettings", u"...", None))
        self.gamePathBrowse.setText(QCoreApplication.translate("GameSettings", u"...", None))
        self.label.setText(QCoreApplication.translate("GameSettings", u"Game Path", None))
        self.modPathBrowse.setText(QCoreApplication.translate("GameSettings", u"...", None))
        self.label_3.setText(QCoreApplication.translate("GameSettings", u"Mod Path", None))
        self.overwritePathBrowse.setText(QCoreApplication.translate("GameSettings", u"...", None))
        self.label_4.setText(QCoreApplication.translate("GameSettings", u"Overwrite Path", None))
        self.label_6.setText(QCoreApplication.translate("GameSettings", u"Game Name", None))
        self.workPathBrowse.setText(QCoreApplication.translate("GameSettings", u"...", None))
        self.label_2.setText(QCoreApplication.translate("GameSettings", u"Download Path", None))
        self.label_5.setText(QCoreApplication.translate("GameSettings", u"Work Path", None))
        self.label_7.setText(QCoreApplication.translate("GameSettings", u"Game ID", None))
    # retranslateUi

