import sys, os
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog, QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtGui import QPixmap
import cv2
import time
#
#  -- import src packages --
#
from PyQt5.uic.properties import QtCore

from src.VideoController import VideoController
from src.CharacterController import CharacterController
from src.EmblemController import EmblemController
from src.imageQualityProcess import QualityController
from src.LionPatternController import LionPatternController
from src.imageQualityProcess import  ImageAacquisition

ESC = 27
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.strResult = "--- Results --- \n"
        #
        # main panel orientation
        #
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 580
        self.title = "FDDS"

        #
        # image label
        #
        self.imageDisplayer = QLabel(self)
        self.imageDisplayer.setGeometry(0,0,400,450)
        self.imageDisplayer.setStyleSheet("border:1px solid rgb(0, 0, 255); ")
        self.imageDisplayer.move(5,10)

        #
        # result container
        #
        self.resultDisplayer = QPlainTextEdit(self)
        self.resultDisplayer.insertPlainText("Results \n\n")
        self.resultDisplayer.setGeometry(0,0,340,300)
        self.resultDisplayer.move(450, 10)
        self.resultDisplayer.setReadOnly(True)
        #
        # main button controllers
            #
            #   -- load image button --
            #
        self.loadImageButton = QPushButton('Load Image', self)
        self.loadImageButton.setGeometry(0,0,100,50)
        self.loadImageButton.move(120,480)
        self.loadImageButton.clicked.connect(self.loadImage)
            #
            # image capture
            #
        self.captureImageButton = QPushButton('Capture Image', self)
        self.captureImageButton.setGeometry(0, 0, 100, 50)
        self.captureImageButton.move(5, 480)
        self.captureImageButton.clicked.connect(self.captureImage)
            #
            #  -- video functionality --
            #
        self.videoButton = QPushButton('Video analyse', self)
        self.videoButton.setGeometry(0, 0, 100, 50)
        self.videoButton.move(570,330)
        self.videoButton.clicked.connect(self.loadVideoFunction)
            #
            # -- analysis image --
            #
        self.analyseButton = QPushButton('Image analyse', self)
        self.analyseButton.setGeometry(0, 0, 100, 50)
        self.analyseButton.move(690, 330)
        self.analyseButton.clicked.connect(self.anaysisProcess)
        #
        # load content prepared and render ui
        #
        self.setFixedSize(self.width, self.height)
        self.initUI()

    #
    # image analysis
    #
    def anaysisProcess(self):
        if(self.qualityProcess()):
            if(self.loadCharacterFunction()):
                if(self.patternComparisionFunction()):
                    self.featureComparisionFunction()
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
            givenImage = cv2.imread(fileName)
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
    # load character analysis and call character recognition method
    #
    def loadCharacterFunction(self):
        try:
            self.instance = CharacterController()
            self.result = CharacterController.main(self.instance)
            self.strResult = self.strResult + "\n \n --- Character Processing Result --- \n "
            if(self.result[0] == 1):
                print("this is original driving license")
                self.strResult = self.strResult + "After character recognition this driving license consider as original card \n"
                self.resultDisplayer.setPlainText(self.strResult)
            if(self.result[0] == 2):
                print("this is fake driving license")
                self.strResult = self.strResult + "After character recognition this driving license consider as fake card \n"
                self.resultDisplayer.setPlainText(self.strResult)
            return True
        except Exception as a:
            print(a)

    #
    # feature function load here
    #
    def featureComparisionFunction(self):
        self.EmblemController = EmblemController()
        featureResult = self.EmblemController.mainCall()
        self.strResult = self.strResult + "\n \n --- Feature Recognition --- \n"
        self.strResult = self.strResult + str(featureResult)
        self.resultDisplayer.setPlainText(self.strResult)
        return True

    #
    # pattern function load here
    #
    def patternComparisionFunction(self):
        self.PatternController = LionPatternController()
        patternResult = self.PatternController.MainCall()
        self.strResult = self.strResult + "\n \n --- Pattern Recognition --- \n"
        self.strResult = self.strResult + str(patternResult)
        self.resultDisplayer.setPlainText(self.strResult)
        return True

    #
    # quality process
    #
    def qualityProcess(self):
        # self.qualityController = QualityController()
        # self.qualityController.qualityAssessment()
        self.qualityResult = QualityController.qualityAssessment()
        self.strResult = self.strResult + "\n \n --- Quality Processing Result --- \n "
        self.strResult = self.strResult + str(self.qualityResult)
        print(self.strResult)
        self.resultDisplayer.setPlainText(self.strResult)
        return True

    #
    # capture image
    #
    def captureImage(self):
        ImageAacquisition.captureAllImages()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())