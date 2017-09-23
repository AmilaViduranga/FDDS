import sys, os
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog, QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtGui import QPixmap
import cv2
import time
#
#  -- import src packages --
#
from src.VideoController import VideoController
from src.EmblemController import EmblemController

ESC = 27
class App(QWidget):
    def __init__(self):
        super().__init__()
        #
        # main panel orientation
        #
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 570
        self.title = "FDDS"

        #
        # image label
        #
        self.imageDisplayer = QLabel(self)
        self.imageDisplayer.setGeometry(0,0,200,230)
        self.imageDisplayer.setStyleSheet("border:1px solid rgb(0, 0, 255); ")
        self.imageDisplayer.move(5,10)

        #
        # result container
        #
        self.resultDisplayer = QPlainTextEdit(self)
        self.resultDisplayer.insertPlainText("Results are display here \n\n")
        self.resultDisplayer.setGeometry(0,0,300,300)
        self.resultDisplayer.move(5, 250)
        self.resultDisplayer.setReadOnly(True)
        #
        # main button controllers
            #
            #   -- load image button --
            #
        self.loadImageButton = QPushButton('Load Image', self)
        self.loadImageButton.setGeometry(0,0,120,60)
        self.loadImageButton.move(325,10)
        self.loadImageButton.clicked.connect(self.loadImage)
            #
            #   -- quality functionality --
            #
        self.qualityButton = QPushButton('Quality', self)
        self.qualityButton.setGeometry(0, 0, 120, 60)
        self.qualityButton.move(325,90)
            #
            # -- character functionality --
            #
        self.characterButton = QPushButton('Character', self)
        self.characterButton.setGeometry(0,0,120,60)
        self.characterButton.move(325, 170)
            #
            #  -- pattern functionality --
            #
        self.patternButton = QPushButton('Pattern', self)
        self.patternButton.setGeometry(0,0,120,60)
        self.patternButton.move(325, 250)
        self.patternButton.clicked.connect(self.patternComparisionFunction)
            #
            #  -- video functionality --
            #
        self.videoButton = QPushButton('Video', self)
        self.videoButton.setGeometry(0, 0, 120, 60)
        self.videoButton.move(325, 330)
        self.videoButton.clicked.connect(self.loadVideoFunction)

        #
        # load content prepared and render ui
        #
        self.setFixedSize(self.width, self.height)
        self.initUI()

    #
    # load the predefined contents at main method
    #
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    #
    #  load the image
    #
    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            pixmap = QPixmap(fileName)
            givenImage = cv2.imread(fileName,0)
            cv2.imwrite("Image/source.jpg", givenImage)
            self.imageDisplayer.setPixmap(pixmap)
            self.show()
    #
    #  load video function using cmd method
    #
    def loadVideoFunction(self):
        try:
            self.videoLoacator = VideoController()
            self.videoLoacator.show()
        except Exception as e:
            print(str(e))

    #
    # pattern function load here
    #
    def patternComparisionFunction(self):
        self.EmblemController = EmblemController()
        self.EmblemController.mainCall()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())