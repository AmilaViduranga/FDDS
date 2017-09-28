import cv2
import os

from src.imageQualityProcess import EyeDetector


def qualityAssessment():

    print("qualityAssessment method started ")
    imgDestination = 'E:\/4th year 2nd\/research\FDDS\Image\source.jpg'
    eyeDetected = EyeDetector.detectEye(cv2.imread(imgDestination))



    os.system('"E:/4th year 2nd/matalab-api/matalab-api/bin/Debug/matalab-api.exe"')
    resultFile = open("E:\/4th year 2nd\/research\FDDS\Support\QualityProcess\/result.txt", "r")
    vals = resultFile.readlines()
    brisqueVal = abs(vals[0])
    kurtosisVal = vals[1]

    print("eye detected : "+str(eyeDetected))
    print("brisque value : "+str(vals[0]))
    print("brisque value : " + str(vals[1]))

    if float(brisqueVal) < 15 or float(kurtosisVal) > 2.7 and eyeDetected:
        return True
    else:
        return False