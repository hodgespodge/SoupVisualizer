
import pygame_visuals

import SpleeterFunctions
import os

import sys

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import multiprocessing

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.song_path = None
        self.song = None

    def initUI(self):

        self.setGeometry(500, 500, 300, 220)
        self.setWindowTitle('Soup Visualizer')
        self.setWindowIcon(QIcon('soupicon.png'))

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"TestSongs","16bit")

        self.list_title = QLabel("Processed Songs:")
        layout.addWidget(self.list_title)

        self.listview = QListView()

        layout.addWidget(self.listview)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.listview.setModel(self.fileModel)
        self.listview.setRootIndex(self.fileModel.index(path))
        self.listview.setRootIndex(self.fileModel.setRootPath(path))

        self.listview.clicked.connect(self.preprocessed_song_options)

        self.currently_selected_song_textbox = QLabel("No song selected yet")

        layout.addWidget(self.currently_selected_song_textbox)

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

    def closeEvent(self, event):

        children_processes = multiprocessing.active_children()

        quit = True

        for child in children_processes:
            if child.name != "visualizer_window":

                message = child.name[10:] + " is still being processed. Would you like to end the process and quit?"
                reply = QMessageBox.question(self, '',
                                         message, QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    child.close()
                else:
                    event.ignore()
                    quit = False
                    break
        if quit:
            event.accept()

    def preprocessed_song_options(self,item):

        item_data = self.listview.selectedIndexes()[0].data()
        self.song_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"TestSongs","16bit",item_data)
        self.song = os.path.basename(item_data)
        self.currently_selected_song_textbox.setText(self.song)

    def openFileNameDialog(self):
        # global song_path

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:

            self.song = os.path.basename(fileName)

            if fileName.endswith(".wav"):

                if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "TestSongs", "16bit",self.song)):

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

                    wav_16_output = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TestSongs", "16bit",self.song)

                    split_wav_16_output = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                       "SpleeterOutputs_16-bit", "5stems")

                    P = multiprocessing.Process(name="spleeting_"+self.song,target=SpleeterFunctions.all_song_processing,args=(fileName,split_wav_16_output,wav_16_output,))
                    P.start()
                    self.song_path = fileName
                    self.currently_selected_song_textbox.setText(self.song)

            else:
                QMessageBox.information(self, '',
                                        "File must be of type .wav!"
                                        )


    def on_click_run(self):

        if self.song_path is not None:

            acceptable_song = True
            children_processes = multiprocessing.active_children()

            if not self.song_path.endswith(".wav"):
                QMessageBox.information(self,'',
                                        "File must be of type .wav!"
                                        )
            else:
                for child in children_processes:
                    if child.name == "spleeting_" + self.song:
                        print("Unable to visualize ",self.song)
                        acceptable_song = False

                if acceptable_song:
                    P = multiprocessing.Process(name="visualizer_window",target=pygame_visuals.run,args=(self.song_path,))
                    P.start()

        else:
            QMessageBox.information(self, '',
                                    "Please choose a song from the list of processed songs."
                                    )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
