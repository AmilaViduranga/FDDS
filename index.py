import sys, os
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog, QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtGui import QPixmap
import cv2
#
#  -- import src packages --
#
from src.VideoController import VideoController
from src.CharacterController import CharacterController
from src.EmblemController import EmblemController
from src.LionPatternController import LionPatternController
from src.imageQualityProcess import QualityController
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
        self.width = 650
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
        self.resultDisplayer.insertPlainText("Results \n\n")
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
            #   -- capture image button --
            #
        self.captureImageButton = QPushButton('Capture Image', self)
        self.captureImageButton.setGeometry(0, 0, 120, 60)
        self.captureImageButton.move(455, 10)
        self.captureImageButton.clicked.connect(self.captureImage)
            #
            #   -- quality functionality --
            #
        self.qualityButton = QPushButton('Quality', self)
        self.qualityButton.setGeometry(0, 0, 120, 60)
        self.qualityButton.move(325,90)
        self.qualityButton.clicked.connect(self.qualityProcess)
            #
            # -- character functionality --
            #
        self.characterButton = QPushButton('Character', self)
        self.characterButton.setGeometry(0,0,120,60)
        self.characterButton.move(325, 170)
        self.characterButton.clicked.connect(self.loadCharacterFunction)
            #
            #  -- feature functionality --
            #
        self.featureButton = QPushButton('Features', self)
        self.featureButton.setGeometry(0,0,120,60)
        self.featureButton.move(325, 250)
        self.featureButton.clicked.connect(self.featureComparisionFunction)
            #
            #  -- video functionality --
            #
        self.videoButton = QPushButton('Video', self)
        self.videoButton.setGeometry(0, 0, 120, 60)
        self.videoButton.move(325, 410)
        self.videoButton.clicked.connect(self.loadVideoFunction)
            #
            # --pattern functionality --
            #
        self.patternButton = QPushButton('Pattern', self)
        self.patternButton.setGeometry(0, 0, 120, 60)
        self.patternButton.move(325, 330)
        self.patternButton.clicked.connect(self.patternComparisionFunction)

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

    #
    # pattern function load here
    #
    def patternComparisionFunction(self):
        self.PatternController = LionPatternController()
        patternResult = self.PatternController.MainCall()
        self.strResult = self.strResult + "\n \n --- Pattern Recognition --- \n"
        self.strResult = self.strResult + str(patternResult)
        self.resultDisplayer.setPlainText(self.strResult)
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

    #
    # capture image
    #
    def captureImage(self):
        ImageAacquisition.captureAllImages()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())