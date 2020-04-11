# from pygame_visuals import *
import pygame_visuals
from SpleeterFunctions import *

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
from multiprocessing import Process

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(500, 500, 300, 220)
        self.setWindowTitle('Soup Visualizer')
        self.setWindowIcon(QIcon('soupicon.png'))

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"TestSongs","16bit")

        self.listview = QListView()

        layout.addWidget(self.listview)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.listview.setModel(self.fileModel)
        self.listview.setRootIndex(self.fileModel.index(path))
        self.listview.setRootIndex(self.fileModel.setRootPath(path))

        self.listview.clicked.connect(self.preprocessed_song_options)

        self.textbox = QLabel("No song selected yet")

        layout.addWidget(self.textbox)

        self.btn1 = QPushButton('Play Song', self)
        layout.addWidget(self.btn1)

        self.btn1.setToolTip('TODO')
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(self.on_click_run)

        self.btn2 = QPushButton('Select song to process', self)
        layout.addWidget(self.btn2)
        self.btn2.setToolTip('TODO')
        self.btn2.resize(self.btn1.sizeHint())
        self.btn2.clicked.connect(self.openFileNameDialog)

        self.show()

    def preprocessed_song_options(self,item):
        global song_path

        item_data = self.listview.selectedIndexes()[0].data()
        song_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"TestSongs","16bit",item_data)
        song = os.path.basename(item_data)
        self.textbox.setText(song)

    def openFileNameDialog(self):
        global song_path

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:

            song = os.path.basename(fileName)

            if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "TestSongs", "16bit",song)):

                reply = QMessageBox.question(self, '',
                                             "Song file has already been pre-processed. Would you like to process again"
                                             " and overwrite?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)

            else:
                reply = QMessageBox.question(self, '',
                                             "Song file needs to be preprocessed before visualization. This can take a while. "
                                             "Would you like to process it now?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:

                wav_16_output = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TestSongs", "16bit",song)

                split_wav_16_output = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                   "SpleeterOutputs_16-bit", "5stems")

                spleet_wav(fileName, split_wav_16_output, 5)
                pygame_visuals.create_16_bit_wav(fileName, wav_16_output)
                pygame_visuals.create_instrument_charactaristics(fileName)

                song_path = fileName
                self.textbox.setText(song)

    def on_click_run(self):

        if song_path is not None:

            P = Process(name="visualizer_window",target=pygame_visuals.run,args=(song_path,))
            P.start()

        else:
            print("TODO make \"please choose song\" dialogue box pop up")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
