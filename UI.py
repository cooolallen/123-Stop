from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import cv2

import random_comp as rand


from ui_MainWindow import Ui_MainWindow
from ui_GuessWhatDialog import Ui_GuessWhatDialog
from ui_MessageDialog import Ui_MessageDialog

class MainWindow(QMainWindow):
    def __init__(self,mode1_fun,parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.guessDialog = None
        self.mode1_fun = mode1_fun
        self.show()

        # Connection
        self.ui.PlayButton.clicked.connect(self.showGuess)

    def showGuess(self):
        self.guessDialog = GuessWhatDialog(self)

    def mode1_trigger(self,mode1_fun):
        mode1_fun()


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
            self.timer_start(1500)

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
            # if(self.result=='win'):
            self.parent.mode1_trigger(self.parent.mode1_fun)

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
        elif(self.state=='fiar'):#Fair
            self.ui.PictureHolder.setPixmap(QPixmap("./figures/fair.png"))
        elif(self.state=='back'):
            self.ui.PictureHolder.setText("Back\nBack\nBack\nBack\nBack\n")
        elif(self.state=='start'):
            self.ui.PictureHolder.setText("Start\nStart\nStart\nStart\nStart\n")
        elif(self.state=='move'):
            self.ui.PictureHolder.setText("move\nmove\nmove\nmove\nmove\nmove\n")
        elif(self.state=='freeze'):
            self.ui.PictureHolder.setText("freeze\nfreeze\nfreeze\nfreeze\nfreeze\n")
