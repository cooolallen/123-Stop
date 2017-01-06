from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QAudioOutput, QAudioFormat
import csv
import os
import sys
import cv2

import random_comp as rand


from ui_MainWindow import Ui_MainWindow
from ui_GuessWhatDialog import Ui_GuessWhatDialog
from ui_MessageDialog import Ui_MessageDialog
from ui_JudgeDialog import Ui_JudgeDialog
from ui_Table import Ui_Table

class MainWindow(QMainWindow):
    def __init__(self,mode1_fun,mode2_fun,parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.guessDialog = None
        self.mode1_fun = mode1_fun
        self.mode2_fun = mode2_fun
        self.ui.verticalLayout_2.setStretch(0,200)#100
        self.table = Table(self)
        self.playerName = ""
        self.show()

        # Connection
        self.ui.PlayButton.clicked.connect(self.showGuess)
        self.ui.ScoreButton.clicked.connect(self.showTable)
        self.ui.lineEdit.editingFinished.connect(self.setNewUser)

    def showGuess(self):
        self.playerName = self.ui.lineEdit.text()
        if self.playerName == '':
            QMessageBox.warning(self,'User Name Input','Please enter your name!!')
        else:
            self.guessDialog = GuessWhatDialog(self)

    def showTable(self):
        self.table.show_event()

    def setNewUser(self):
        self.playerName = self.ui.lineEdit.text()

    def mode1_trigger(self):
        self.mode1_fun()

    def mode2_trigger(self):
        self.mode2_fun()

class GuessWhatDialog(QDialog):
        def __init__(self,parent=None):
            super(GuessWhatDialog, self).__init__(parent)
            self.ui = Ui_GuessWhatDialog()
            self.ui.setupUi(self)
            self.result = []
            self.comp = []
            self.timer = QtCore.QTimer()
            self.message = []
            self.parent = parent

            self.ui.ScissorButton.setIcon(QIcon("./figures/scissor.png"))
            self.ui.ScissorButton.setIconSize(QtCore.QSize(130, 130))
            self.ui.PaperButton.setIcon(QIcon("./figures/paper.png"))
            self.ui.PaperButton.setIconSize(QtCore.QSize(130, 130))
            self.ui.StoneButton.setIcon(QIcon("./figures/stone.png"))
            self.ui.StoneButton.setIconSize(QtCore.QSize(130, 130))
            self.ui.NPC.setPixmap(QPixmap("./figures/question.png"))
            self.show()

            # Connection
            self.ui.ScissorButton.clicked.connect(self.scissorClicked)
            self.ui.ScissorButton.pressed.connect(self.scissorPressed)
            self.ui.ScissorButton.released.connect(self.scissorReleased)
            self.ui.PaperButton.clicked.connect(self.paperClicked)
            self.ui.PaperButton.pressed.connect(self.paperPressed)
            self.ui.PaperButton.released.connect(self.paperReleased)
            self.ui.StoneButton.clicked.connect(self.stoneClicked)
            self.ui.StoneButton.pressed.connect(self.stonePressed)
            self.ui.StoneButton.released.connect(self.stoneReleased)

        def scissorClicked(self):
            self.result, self.comp = rand.game_random('scissor')
            self.npcAttack()

        def scissorPressed(self):
            self.ui.ScissorButton.setIcon(QIcon("./figures/scissor_pressed.png"))

        def scissorReleased(self):
            self.ui.ScissorButton.setIcon(QIcon("./figures/scissor.png"))

        def paperClicked(self):
            self.result, self.comp = rand.game_random('paper')
            self.npcAttack()

        def paperPressed(self):
            self.ui.PaperButton.setIcon(QIcon("./figures/paper_pressed.png"))

        def paperReleased(self):
            self.ui.PaperButton.setIcon(QIcon("./figures/paper.png"))

        def stoneClicked(self):
            self.result, self.comp = rand.game_random('stone')
            self.npcAttack()

        def stonePressed(self):
            self.ui.StoneButton.setIcon(QIcon("./figures/stone_pressed.png"))

        def stoneReleased(self):
            self.ui.StoneButton.setIcon(QIcon("./figures/stone.png"))


        def npcAttack(self):
            if(self.comp=='scissor'):#
                self.ui.NPC.setPixmap(QPixmap("./figures/scissor_npc.png"))
            elif(self.comp=='paper'):
                self.ui.NPC.setPixmap(QPixmap("./figures/paper_npc.png"))
            else:#
                self.ui.NPC.setPixmap(QPixmap("./figures/stone_npc.png"))

            if(self.result=='lose'):#Lose
                print('you lost')
            elif(self.result=='win'):#Win
                print('you win')
            else:#Fair
                print('you fair')

            self.message = MessageDialog(self.result, self)
            self.timer_start(1000)

        def timer_start(self,ms):
            if(self.result!='fair'):
                self.timer.start(ms)
                self.timer.timeout.connect(self.window_close)
            else:
                self.timer.start(ms)
                self.timer.timeout.connect(self.message_close)

        def message_close(self):
            self.timer.stop()
            self.message.close()
            self.timer.timeout.disconnect(self.message_close)
            self.activateWindow()

        def window_close(self):
            self.timer.stop()
            # self.timer.timeout.disconnect(self.window_close)
            self.close()
            self.message.close()
            if(self.result=='win'):
                self.parent.mode1_trigger()
            else:
                self.parent.mode2_trigger()

class MessageDialog(QDialog):
    def __init__(self,state,parent=None):
        super(MessageDialog, self).__init__(parent)
        self.ui = Ui_MessageDialog()
        self.setGeometry(850,150,50,50)
        self.ui.setupUi(self)
        self.state = state
        self.setPicture()
        self.geometry()
        self.show()

    def setPicture(self):
        if(self.state=='lose'):
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/lose.png"))
        elif(self.state=='win'):
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/win.png"))
        elif(self.state=='fair'):#Fair
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/fair.png"))
        elif(self.state=='back'):
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/back.png"))
        elif(self.state=='start'):
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/start.png"))
        elif(self.state=='move'):
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/move.png"))
        elif(self.state=='freeze'):
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/freeze.png"))

class JudgeDialog(QDialog):
    def __init__(self,num,parent=None):
        super(JudgeDialog, self).__init__(parent)
        self.ui = Ui_JudgeDialog()
        self.ui.setupUi(self)
        self.num = num
        self.result = None

        self.show()

        #Connection
        self.ui.GuessButton.clicked.connect(self.guess)

    def guess(self):
        num_guess = self.ui.LineEditGuess.text()
        if num_guess == str(self.num):
            print('you win')
            self.result = True
            self.close()

        else:
            cur_chance_num = int(self.ui.LabelChanceNum.text())

            if cur_chance_num==1:
                print('you lose')
                self.result = False
                self.close()
            else:
                self.ui.LabelChanceNum.setText(str(cur_chance_num-1))

        self.ui.LineEditGuess.clear()

class Table(QDialog):
    def __init__(self,parent=None):
        super(Table, self).__init__(parent)
        self.ui = Ui_Table()
        self.ui.setupUi(self)
        self.directory = './scoreboard.csv'
        self.parent = parent
        self.nameList = self.loadData()

    def show_event(self):
        self.buildTable()
        self.show()

    def buildTable(self):
        self.nameList = self.loadData()
        name_sz = len(self.nameList[0])

        self.ui.TableHolder.clear()
        self.ui.TableHolder.setColumnCount(2)
        self.ui.TableHolder.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.ui.TableHolder.setHorizontalHeaderItem(1, QTableWidgetItem("time (s)"))
        self.ui.TableHolder.setColumnWidth(0, 50)
        self.ui.TableHolder.setColumnWidth(1, 120)
        self.ui.TableHolder.setRowCount(name_sz)

        if self.nameList != []:
            for key in range(name_sz):
                newitem = QTableWidgetItem(self.nameList[0][key])
                self.ui.TableHolder.setItem(key,0,newitem)
                self.ui.TableHolder.item(key,0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                newitem = QTableWidgetItem(self.nameList[1][key])
                self.ui.TableHolder.setItem(key,1,newitem)
                self.ui.TableHolder.item(key, 1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def loadData(self):
        nameList = []
        names = []
        scores = []

        if os.path.exists(self.directory):
            with open(self.directory) as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    print(row)
                    if row !=[]:
                        names.append(row[0])
                        scores.append(row[1])

                nameList.append(names)
                nameList.append(scores)
        else:
            nameList = []

        return nameList

    def record(self,mode,result,time=None):

        if mode=='mode1':
            self.nameList[0].append(self.parent.playerName)
            if result:
                self.nameList[1].append(str(time)+'(mode1)')
            else:
                self.nameList[1].append('mode1 fail('+str(time)+')')

        elif mode=='mode2':
            self.nameList[0].append(self.parent.playerName)
            if result:
                self.nameList[1].append(str(time) + '(mode2)')
            else:
                self.nameList[1].append('mode2 fail(' + str(time) + ')')
        else:
            print('record data error')

        with open(self.directory,'w') as f:
            f_csv = csv.writer(f)
            for key in range(len(self.nameList[0])):
                f_csv.writerow([self.nameList[0][key],self.nameList[1][key]])


