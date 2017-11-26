import cv2
import os

from src.imageQualityProcess import EyeDetector


def qualityAssessment():

    print("qualityAssessment method started ")
    imgDestination = 'E:\/4th_year_2nd\/research\FDDS\Image\source.jpg'
    eyeDetected = EyeDetector.detectEye(cv2.imread(imgDestination))



    os.system('"E:/4th_year_2nd/matalab-api/matalab-api/bin/Debug/matalab-api.exe"')
    resultFile = open("E:\/4th_year_2nd\/research\FDDS\Support\QualityProcess\/result.txt", "r")
    vals = resultFile.readlines()
    brisqueVal =  abs(float(vals[0]))
    kurtosisVal = vals[1]

    print("eye detected : "+str(eyeDetected))
    print("brisque value : "+str(vals[0]))
    print("brisque value : " + str(vals[1]))

    if float(brisqueVal) < 15 or (float(kurtosisVal) > 2.7 and eyeDetected):
        return "Given identification card is quality and ok to proceed"
    else:
        return "Warning! Given identification card is not quality and not ok to proceed"