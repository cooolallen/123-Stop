# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JudgeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_JudgeDialog(object):
    def setupUi(self, JudgeDialog):
        JudgeDialog.setObjectName("JudgeDialog")
        JudgeDialog.resize(329, 177)
        font = QtGui.QFont()
        font.setPointSize(16)
        JudgeDialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(JudgeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.LabelTitle = QtWidgets.QLabel(JudgeDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LabelTitle.setFont(font)
        self.LabelTitle.setObjectName("LabelTitle")
        self.gridLayout.addWidget(self.LabelTitle, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LabelNum = QtWidgets.QLabel(JudgeDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LabelNum.setFont(font)
        self.LabelNum.setObjectName("LabelNum")
        self.horizontalLayout.addWidget(self.LabelNum)
        self.LineEditGuess = QtWidgets.QLineEdit(JudgeDialog)
        self.LineEditGuess.setObjectName("LineEditGuess")
        self.horizontalLayout.addWidget(self.LineEditGuess)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LabelChance = QtWidgets.QLabel(JudgeDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LabelChance.setFont(font)
        self.LabelChance.setObjectName("LabelChance")
        self.horizontalLayout_2.addWidget(self.LabelChance)
        self.LabelChanceNum = QtWidgets.QLabel(JudgeDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LabelChanceNum.setFont(font)
        self.LabelChanceNum.setObjectName("LabelChanceNum")
        self.horizontalLayout_2.addWidget(self.LabelChanceNum)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.GuessButton = QtWidgets.QPushButton(JudgeDialog)
        self.GuessButton.setObjectName("GuessButton")
        self.horizontalLayout_3.addWidget(self.GuessButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.retranslateUi(JudgeDialog)
        QtCore.QMetaObject.connectSlotsByName(JudgeDialog)

    def retranslateUi(self, JudgeDialog):
        _translate = QtCore.QCoreApplication.translate
        JudgeDialog.setWindowTitle(_translate("JudgeDialog", "Did you catch that?"))
        self.LabelTitle.setText(_translate("JudgeDialog", "Did you catach that?"))
        self.LabelNum.setText(_translate("JudgeDialog", "Number:"))
        self.LabelChance.setText(_translate("JudgeDialog", "Chance :"))
        self.LabelChanceNum.setText(_translate("JudgeDialog", "3"))
        self.GuessButton.setText(_translate("JudgeDialog", "Guess"))

