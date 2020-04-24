
import pygame_visuals

import SpleeterFunctions
import os

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import multiprocessing

class ListViewRMB(QListView):

    def __init__(self,RMBFunction,*args, parent=None):
        QListView.__init__(self, parent)
        self.RMBFunction = RMBFunction
        self.RMBFunction_args = args

    def mousePressEvent(self, event):

        QListView.mousePressEvent(self, event)

        if event.button() == Qt.RightButton:

            self.RMBFunction(*self.RMBFunction_args)

class MainWindow(QMainWindow):

    def __init__(self):

        self.CreateDirectories()
        super().__init__()
        self.initUI()
        self.song_path = None
        self.song = None
        self.num_points = 100
        res = app.desktop().screenGeometry()
        self.screen_resolution = (res.width(),res.height())



    def initUI(self):

        self.setGeometry(500, 500, 300, 220)
        self.setWindowTitle('Soup Visualizer')
        self.setWindowIcon(QIcon('soupicon.png'))

        animation_points_action = QAction("Number of animation points",self)
        animation_points_action.setStatusTip("set the fidelity and file size of generated animations")
        animation_points_action.triggered.connect(self.setAnimationPoints)

        screen_resolution_action = QAction("Set Screen Resolution",self)
        screen_resolution_action.setStatusTip("Should probably match your screen")
        screen_resolution_action.triggered.connect(self.setScreenResolution)

        menu = self.menuBar()
        optionsbar = menu.addMenu('&Generation Options')
        optionsbar.addAction(animation_points_action)
        optionsbar.addAction(screen_resolution_action)

        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"SongCopies","16bit")

        self.list_title = QLabel("Processed Songs:")
        layout.addWidget(self.list_title)

        self.listview = ListViewRMB(self.right_click_list, )

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

        self.btn1.setToolTip('Plays the currently selected song with visuals')
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(self.on_click_run)

        self.btn2 = QPushButton('Select song to process', self)
        layout.addWidget(self.btn2)
        self.btn2.setToolTip('Enter a file browser to choose a wav song for processing')
        self.btn2.resize(self.btn1.sizeHint())
        self.btn2.clicked.connect(self.openFileNameDialog)
        self.show()

    # Creates the file structure for saving files
    def CreateDirectories(self):
        try:
            os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "SongCopies", "16bit"))
            os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "SpleeterOutputs_16-bit", "5stems"))
            os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "pickles"))
        except:
            pass

    def right_click_list(self):
        song_name = self.listview.selectedIndexes()[0].data()

        message = "Would you like to delete "+song_name+"'s stored data? This will only delete files created by Soup Visualizer and not the original wav file."
        reply = QMessageBox.question(self, '',
                                     message, QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            self.song = None
            self.currently_selected_song_textbox.setText("No song selected yet")

            print("deleting 16bit song copy")
            try:
                os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), "SongCopies", "16bit", song_name))
            except:
                pass

            print("deleting pickles")
            try:
                os.remove("pickles/" + song_name + "_beats.pickle")
            except:
                pass
            try:
                os.remove("pickles/" + song_name + "_ellipses.pickle")
            except:
                pass

            print("deleting split audio files")
            try:
                os.remove("SpleeterOutputs_16-bit" + "/" + "5stems" + "/" + song_name + "_" + "other" + "_16-bit.wav")
            except:
                print("failed to delete" + "SpleeterOutputs_16-bit" + "/" + song_name + "_" + "other" + "_16-bit.wav")

            try:
                os.remove("SpleeterOutputs_16-bit" + "/" + "5stems" + "/" + song_name + "_" + "bass" + "_16-bit.wav")
            except:
                print("failed to delete" + "SpleeterOutputs_16-bit" + "/" + song_name + "_" + "bass" + "_16-bit.wav")

            try:
                os.remove("SpleeterOutputs_16-bit" + "/" + "5stems" + "/" + song_name + "_" + "vocals" + "_16-bit.wav")
            except:
                print("failed to delete" + "SpleeterOutputs_16-bit" + "/" + song_name + "_" + "vocals" + "_16-bit.wav")

            try:
                os.remove("SpleeterOutputs_16-bit" + "/" + "5stems" + "/" + song_name + "_" + "drums" + "_16-bit.wav")
            except:
                print("failed to delete" + "SpleeterOutputs_16-bit" + "/" + song_name + "_" + "drums" + "_16-bit.wav")

        else:
            pass

    def setAnimationPoints(self):

        num_points, done = QInputDialog.getInt(self,'Animation Points','Larger numbers require more disk space',self.num_points, 10,2000,1)
        if done:
            self.num_points= num_points

    def setScreenResolution(self):

        item_strings = {'(640, 360)':(640,360), '(800, 600)':(800, 600), '(1024, 768)':(1024, 768),
                        '(1280, 720)':(1280, 720),'(1280, 800)':(1280, 800), '(1280, 1024)':(1280, 1024),
                        '(1360, 768)':(1360, 768),'(1366, 768)':(1366, 768),'(1440, 900)':(1440, 900),
                        '(1536, 864)':(1536, 864), '(1600, 900)':(1600, 900),'(1680, 1050)':(1680, 1050),
                        '(1920, 1080)':(1920, 1080), '(1920, 1200)':(1920, 1200),'(2048, 1152)':(2048, 1152),
                        '(2560, 1080)':(2560, 1080),'(2560, 1440)':(2560, 1440),'(3440, 1440)':(3440, 1440),
                        '(3840, 2160)':(3840, 2160)}

        items = item_strings.keys()

        chosen_resolution, reply = QInputDialog.getItem(self, "select screen resolution",
                                        "common resolutions", items, 0, False)

        if reply and chosen_resolution:

            self.screen_resolution = item_strings[chosen_resolution]

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

                    try:
                        child.close()
                    except:
                        pass
                else:
                    event.ignore()
                    quit = False
                    break
        if quit:
            event.accept()

    def preprocessed_song_options(self,item):

        item_data = self.listview.selectedIndexes()[0].data()
        self.song_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"SongCopies","16bit",item_data)
        self.song = os.path.basename(item_data)
        self.currently_selected_song_textbox.setText(self.song)

    def openFileNameDialog(self):
        # global song_path

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Wav file chooser", "",
                                                  "Wav Files(*.wav);;All Files (*)",
                                                  options=options)
        if fileName:

            self.song = os.path.basename(fileName)

            if fileName.endswith(".wav"):

                if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "SongCopies", "16bit",self.song)):

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

                    wav_16_output = os.path.join(os.path.dirname(os.path.realpath(__file__)), "SongCopies", "16bit",self.song)

                    split_wav_16_output = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                       "SpleeterOutputs_16-bit", "5stems")

                    P = multiprocessing.Process(name="spleeting_"+self.song,target=SpleeterFunctions.all_song_processing,args=(fileName,split_wav_16_output,wav_16_output,self.num_points,self.screen_resolution,))
                    P.start()
                    self.song_path = fileName
                    self.currently_selected_song_textbox.setText(self.song)

            else:
                QMessageBox.information(self, '',
                                        "File must be of type .wav"
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
                        QMessageBox.information(self, '',
                                                "Unable to play. Still processing song."
                                                )
                        acceptable_song = False

                if acceptable_song:
                    P = multiprocessing.Process(name="visualizer_window",target=pygame_visuals.run,args=(self.song_path,self.num_points,self.screen_resolution,))
                    P.start()

        else:
            QMessageBox.information(self, '',
                                    "Please choose a song from the list of processed songs."
                                    )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

