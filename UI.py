from pygame_visuals import *

from PyQt5.QtGui import QIcon

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QMessageBox)
from PyQt5.QtGui import QFont

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class Example(QWidget):

    song = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def closeEvent(self, event):

        #TODO make it end the pygame animation

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def initUI(self):
        self.setGeometry(500, 500, 300, 220)
        self.setWindowTitle('Soup Visualizer')
        self.setWindowIcon(QIcon('soupicon.png'))
        #
        # QToolTip.setFont(QFont('SansSerif', 10))

        self.btn1 = QPushButton('Play Song', self)
        self.btn1.setToolTip('TODO')
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.move(50, 50)
        self.btn1.clicked.connect(self.on_click_run)

        self.btn2 = QPushButton('Select Song', self)
        self.btn2.setToolTip('TODO')
        self.btn2.resize(self.btn1.sizeHint())
        self.btn2.move(100, 100)
        self.btn2.clicked.connect(self.openFileNameDialog)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')

        self.show()


    def openFileNameDialog(self):
        global song

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            song = fileName
            # print("chose ",song)

    def on_click_run(self):

        print("passing", song)
        if song is not None:

            run(song)
        else:
            print("TODO make \"please choose song\" dialogue box pop up")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
