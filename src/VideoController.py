import os, os.path
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QPlainTextEdit
from PyQt5.QtCore import QBasicTimer
import numpy as np
import cv2
from multiprocessing import Pool

ESC = 27

class VideoController(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Hologram Comparision"
        self.left = 10
        self.top = 10
        self.height = 350
        self.width = 320
        self.progressBar = QProgressBar(self)
        self.timer = QBasicTimer()
        self.step = 0
        self.finalResult = QPlainTextEdit(self)
        self.finalResult.setGeometry(0,0,300,200)
        self.finalResult.setReadOnly(True)
        self.progressBar.setGeometry(30,40,300,25)
        self.buttonOriginal = QPushButton('Original', self)
        self.buttonGiven = QPushButton('Given', self)
        self.buttonComparision = QPushButton('Comparision', self)
        self.buttonOriginal.move(5,0)
        self.buttonGiven.move(105,0)
        self.buttonComparision.move(205, 0)
        self.finalResult.move(5,100)
        self.progressBar.move(5, 50)
        self.buttonOriginal.clicked.connect(self.getOriginalInfo)
        self.buttonGiven.clicked.connect(self.getGivenCardInfo)
        self.buttonComparision.clicked.connect(self.comparision)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def getOriginalInfo(self):
        self.captureImage('Support/VideoProcess/Original/', 'original')

    def getGivenCardInfo(self):
        self.captureImage('Support/VideoProcess/Given/', 'given')

    def captureImage(self, path, state):
        camera = cv2.VideoCapture(2)
        idx = 0
        if state == 'original':
            idx = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        while True:
            # os.system('"E:\/4th_year_2nd\/research\servoContrllers\VeidioCapturing\VeidioCapturing\/bin\Debug\VeidioCapturing.exe"')
            ret, imgCamColor = camera.read()
            imgCamColor, idx = self.cardUsingCanny(imgCamColor, idx, path)
            cv2.imshow('Camara', imgCamColor)
            key = cv2.waitKey(20)
            if key == ESC:
                break
        cv2.destroyAllWindows()
        camera.release()

    def cardUsingCanny(self, img, idx, path):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (1, 1), 1000)
        canny = cv2.Canny(blur, 50, 150, apertureSize=3)
        cv2.imshow('canny', canny)
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(canny, kernel, iterations=2)
        _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        preimeters = []
        for i in range(len(contours)):
            preimeters.append(cv2.arcLength(contours[i], True))

        for i in range(len(preimeters)):
            x, y, w, h = cv2.boundingRect(contours[i])
            peri = cv2.arcLength(contours[i], True)
            approx = cv2.approxPolyDP(contours[i], 0.06 * peri, True)
            if len(approx) == 4:
                if w > 120 and h > 130 and w < 200 and h < 200:
                    ratio = w / h
                    if ratio > 1 and ratio < 3:
                        try:
                            new_img = img[y:y + h, x:x + w]
                            idx = idx + 1
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                            cv2.imwrite(path + str(idx) + '.png', new_img)
                        except:
                            print('error')
        return img, idx

    def comparision(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            print('method called')
            dirOriginal = 'Support/VideoProcess/Original'
            dirGiven = 'Support/VideoProcess/Given'
            totalComparisions = 0
            countIngiven = len([name for name in os.listdir(dirGiven) if os.path.isfile(os.path.join(dirGiven, name))])
            countOriginal = len([name for name in os.listdir(dirOriginal) if os.path.isfile(os.path.join(dirOriginal, name))])
            self.progressBar.setRange(0, 2*countIngiven*countOriginal)
            self.timer.start(2*countIngiven*countOriginal, self)
            if self.step >= 2*countIngiven*countOriginal:
                self.timer.stop()
            self.progressBar.setValue(self.step)
            #
            # sift comparison application
            #
            for x in range (0, countIngiven):
                totalComparisions = totalComparisions + self.siftApplication(countOriginal, dirGiven + '/'+str(x+1)+'.png', (x+1))
            averageComparision = totalComparisions / countIngiven
            print("Average comparision amount for sift is "+str(averageComparision))
            strSift = "Average comparision amount for sift is "+str(averageComparision) + "\n"
            self.finalResult.setPlainText(strSift)
            #
            # orb comparison application
            #
            totalComparisions = 0
            for x in range (0, countIngiven):
                totalComparisions = totalComparisions + self.orbApplication(countOriginal, dirGiven + '/'+str(x+1)+'.png', (x+1))
            totalComparisions = totalComparisions / countIngiven
            print("Average compariasion for orb is "+ str(totalComparisions))
            strOrb = "Average compariasion for orb is "+ str(totalComparisions) + "\n"
            self.finalResult.setPlainText(strSift + strOrb)
            #
            # final comparison application
            #
            if averageComparision > 1 and totalComparisions > 1:
                print("Given card hologram is legal container")
                self.finalResult.setPlainText(strSift + strOrb + " \n According to above test result the given card is a legal card respect to hologram")
                return strSift + strOrb + " \n Given card is legal according to hologram"
            else:
                print("Given card hologram is not a legal container or inputs are not quality enough")
                self.finalResult.setPlainText(strSift + strOrb + "\n According to above test result the given card is a illegal card or not quality enough respect to hologram")
                return strSift + strOrb + "\n Given card is not legal according to hologram"

    def siftApplication(self, originalCount, givenImagePath, givenImageId):
        img2 = cv2.imread(givenImagePath, 0)
        match_count = 0
        for x in range (0, originalCount):
            comparision_count = 0
            img1 = cv2.imread('Support/VideoProcess/Original/'+str(x+1)+'.png', 0)  # queryImage
            sift = cv2.xfeatures2d.SIFT_create()
            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)

            # Fast Library for Approximate Nearest Neighbors
            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)

            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)
                    comparision_count = comparision_count + 1
                    match_count = match_count + 1
            self.step = self.step + 1
            self.progressBar.setValue(self.step)
            print('original image '+ str(x+1) + '.png VS given image '+ str(givenImageId) + ' = '+ str(comparision_count))
        return match_count/originalCount

    def orbApplication(self, originalCount, givenImagePath, givenImageId):
        img2 = cv2.imread(givenImagePath, 0)
        match_count = 0
        orb = cv2.ORB_create()
        for x in range(0, originalCount):
            comparision_count = 0
            img1 = cv2.imread('Support/VideoProcess/Original/' + str(x + 1) + '.png', 0)
            kp1, des1 = orb.detectAndCompute(img1, None)
            kp2, des2 = orb.detectAndCompute(img2, None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            comparision_count = comparision_count + len(matches)
            if comparision_count > 30:
             match_count = match_count + 1
            self.step = self.step + 1
            self.progressBar.setValue(self.step)
            print('original image ' + str(x + 1) + '.png VS given image ' + str(givenImageId) + ' = ' + str(comparision_count))
        return match_count