# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuessWhatDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GuessWhatDialog(object):
    def setupUi(self, GuessWhatDialog):
        GuessWhatDialog.setObjectName("GuessWhatDialog")
        GuessWhatDialog.resize(400, 300)
        GuessWhatDialog.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(GuessWhatDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.NPC = QtWidgets.QLabel(GuessWhatDialog)
        self.NPC.setObjectName("NPC")
        self.horizontalLayout.addWidget(self.NPC)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(GuessWhatDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ScissorButton = QtWidgets.QPushButton(GuessWhatDialog)
        self.ScissorButton.setStyleSheet("background-color: transparent;\n"
"border: none;\n"
"background-repeat: none;")
        self.ScissorButton.setText("")
        self.ScissorButton.setObjectName("ScissorButton")
        self.horizontalLayout_2.addWidget(self.ScissorButton)
        self.StoneButton = QtWidgets.QPushButton(GuessWhatDialog)
        self.StoneButton.setStyleSheet("background-color: transparent;\n"
"border: none;\n"
"background-repeat: none;")
        self.StoneButton.setText("")
        self.StoneButton.setObjectName("StoneButton")
        self.horizontalLayout_2.addWidget(self.StoneButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.PaperButton = QtWidgets.QPushButton(GuessWhatDialog)
        self.PaperButton.setStyleSheet("background-color: transparent;\n"
"border: none;\n"
"background-repeat: none;")
        self.PaperButton.setText("")
        self.PaperButton.setObjectName("PaperButton")
        self.gridLayout.addWidget(self.PaperButton, 1, 0, 1, 1)

        self.retranslateUi(GuessWhatDialog)
        QtCore.QMetaObject.connectSlotsByName(GuessWhatDialog)

    def retranslateUi(self, GuessWhatDialog):
        _translate = QtCore.QCoreApplication.translate
        GuessWhatDialog.setWindowTitle(_translate("GuessWhatDialog", "Guess What ?"))
        self.NPC.setText(_translate("GuessWhatDialog", "ddddff"))

