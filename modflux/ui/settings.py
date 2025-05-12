# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName("Settings")
        Settings.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.nexusAPIKeyLabel = QLabel(Settings)
        self.nexusAPIKeyLabel.setObjectName("nexusAPIKeyLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nexusAPIKeyLabel)

        self.nexusAPIKeyLineEdit = QLineEdit(Settings)
        self.nexusAPIKeyLineEdit.setObjectName("nexusAPIKeyLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nexusAPIKeyLineEdit)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        QMetaObject.connectSlotsByName(Settings)

    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(
            QCoreApplication.translate("Settings", "Settings", None)
        )
        self.nexusAPIKeyLabel.setText(
            QCoreApplication.translate("Settings", "Nexus API Key", None)
        )

    # retranslateUi
