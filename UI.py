from pygame_visuals import *

from PyQt5.QtGui import QIcon

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QMessageBox)
from PyQt5.QtGui import QFont

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QMainWindow
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Example(QMainWindow):

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

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        path = QDir.rootPath()

        print(path)

        self.listview = QListView()

        layout.addWidget(self.listview)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.listview.setModel(self.fileModel)
        self.listview.setRootIndex(self.fileModel.index(path))

        self.textbox = QLabel("No song selected yet")

        layout.addWidget(self.textbox)

        self.btn1 = QPushButton('Play Song', self)
        layout.addWidget(self.btn1)

        self.btn1.setToolTip('TODO')
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(self.on_click_run)

        self.btn2 = QPushButton('Select Song', self)
        layout.addWidget(self.btn2)
        self.btn2.setToolTip('TODO')
        self.btn2.resize(self.btn1.sizeHint())
        self.btn2.clicked.connect(self.openFileNameDialog)

        self.show()


    def openFileNameDialog(self):
        global song_path

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            song_path = fileName
            # print("chose ",song)
            song = os.path.basename(fileName)
            self.textbox.setText(song)


    def on_click_run(self):

        print("passing", song_path)
        if song_path is not None:

            run(song_path)
        else:
            print("TODO make \"please choose song\" dialogue box pop up")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
