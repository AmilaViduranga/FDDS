
import cv2
import  matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageFilter,ImageEnhance
import os
from sklearn import neighbors,cross_validation
import pandas as pd

area1 =400
area2=90

class CharacterController():
    def get_contour_precedence(self,contour, cols):
        tolerance_factor =150
        origin = cv2.boundingRect(contour)
        return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


    def get_contour_precedence2(self, contour, cols):
        tolerance_factor =30
        origin = cv2.boundingRect(contour)
        return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


    # re2 = cv2.imread("./4n img/original/original c4.jpg",1)
    # re2 = cv2.imread("./4n img/duplicate/Scan7h.jpg",1)
    # re2 = cv2.imread("./4n img/duplicate/duplicate 3.jpg",1)
    # re2 = cv2.imread("./4n img/original/original n2.jpg",1)
    # re2 = cv2.imread("./4n img/duplicate/apple/1.jpg",1)

    # re2 = cv2.imread("./scan/nu-Scand600 edit.jpg",1)
    # re2 = cv2.imread("./scan/dup-scan600 edit.jpg",1)
    # re2 = cv2.imread("./scan/dupA-scan600.jpg",1)


    def process(self, innum):
        # re2 = cv2.imread(in1)
        # in1 = cv2.imread("C:/Users/sami/Desktop/research integreation/FDDS/Support/CharacterProcess/imgs/nu-Scand600 edit.jpg", 1)
        in1 = cv2.imread("C:/Users/sami/Desktop/research integreation/FDDS/Support/CharacterProcess/imgs/dup-f.jpg", 1)
        imgcpy1 = in1.copy()
        imgcpy2 = in1.copy()
        imgcpy3 = in1.copy()

        blured = cv2.medianBlur(in1,3)
        gray = cv2.cvtColor(blured,cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("./papper/gray.jpg",gray)
        ret,imgThresh = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)
    # ret,imgThresh = cv2.threshold(gray,95,255,cv2.THRESH_OTSU)

        # cv2.imwrite("./papper/thresh.jpg",imgThresh)

        # cv2.imshow("thresh",imgThresh)
        cv2.imwrite("../Support/CharacterProcess/results/thresh.jpg",imgThresh)
        cv2.waitKey(1)

        imgContours,contours,npaHierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        contours.sort(key=lambda x:self.get_contour_precedence(x, imgThresh.shape[1]))

        cv2.drawContours(imgcpy1,contours,-1,(0,0,255), 0)
        cv2.imwrite("cont.jpg",imgcpy1)
        # cv2.imshow("contour" , imgcpy1)
        cv2.waitKey(1)

        path ='C:/Users/sami/Desktop/research integration/FDDS/Support/result/'+str(innum)+'/'

        num=0
        num1=0
        data=[]
        dt=[]
        for c in contours:
                cnt = contours[num]
                if cv2.contourArea(cnt) >area1:
                    x, y, w, h = cv2.boundingRect(cnt)
                    roi = imgcpy2[y:y + h, x:x + w]
                    cv2.imwrite(path+str(num1) + '.jpg', roi)
                    #print in terminal
                    # print(num1, cv2.contourArea(cnt))
                    # print(num1,"height = ",h ,"width =", w)
                    # print(num1, "x point = ", x, "y point =", y)
                    data.append(cnt)
                    num1 += 1
                num=num+1
        print(" ")
        num2=1
        yofs = 0
        xofs = 0
        try:
            for p in data:

                cnt = data[num2]
                x, y, w, h = cv2.boundingRect(cnt)
                # print(num2, cv2.contourArea(cnt))
                # print(num2,"height = ",h ,"width =", w)
                # print(num2, "x point = ", x, "y point =", y)
                # print(" ")
                numone=data[num2]
                x, y, w, h = cv2.boundingRect(numone)
                roi = imgcpy1[y:y + h, x:x + w]
                if (num2 == 1):
                    yofs = y
                    xofs = x
                numtwo=data[num2+1]
                x1, y1, w1, h1 = cv2.boundingRect(numtwo)
                roi = imgcpy1[y1:y1 + h1, x1:x1 + w1]
                # print("difference  " ,num2+1, "and ", num2, " = " ,x1,w1, x,w, (x1)-(x+w) )
                # print("difference  = " ,num2+1, "and ", num2, " = ", (x1)-(x+w)," ", (x1)/(x+w) )
                if (num2<9):
                    dt.append(w)
                    dt.append((x1)-(x+w))

                num2 +=1
        except:IndexError

        path2 = path+str(innum)+'/'

        bottom = imgcpy2[1070 + yofs:1070 + yofs + 80, xofs - 50:400]

        gray = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)
        ret, imgThresh = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY)
        # cv2.imshow("ro1", imgThresh)
        cv2.waitKey(1)
        cv2.imwrite("bottom.jpg", imgThresh)

        imgContours, contours, npaHierarchy = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours.sort(key=lambda x: self.get_contour_precedence2(x, imgThresh.shape[1]))

        cv2.drawContours(imgcpy1, contours, -1, (0, 0, 255), 1)

        num = 0
        num1 = 0
        data = []
        for c in contours:
            cnt = contours[num]
            if cv2.contourArea(cnt) > area2:
                x, y, w, h = cv2.boundingRect(cnt)
                roi = bottom[y:y + h, x:x + w]
                cv2.imwrite(path2 + str(num1) + '.jpg', roi)
                # print in terminal
                # print(num1, cv2.contourArea(cnt))
                # print(num1, "height = ", h, "width =", w)
                # print(num1, "x point = ", x, "y point =", y)
                data.append(cnt)
                num1 += 1
            num = num + 1


        num2 = 1
        try:
            for p in data:
                cnt = data[num2]
                x, y, w, h = cv2.boundingRect(cnt)
                roi = bottom[y:y + h, x:x + w]
                # print(num2, cv2.contourArea(cnt))
                # print(num2, "height = ", h, "width =", w)
                # print(num2, "x point = ", x, "y point =", y)
                # print(" ")
                numone = data[num2]
                x, y, w, h = cv2.boundingRect(numone)
                roi = bottom[y:y + h, x:x + w]

                numtwo = data[num2 + 1]
                x1, y1, w1, h1 = cv2.boundingRect(numtwo)
                roi = bottom[y1:y1 + h1, x1:x1 + w1]
                # print("difference  " ,num2+1, "and ", num2, " = " ,x1,w1, x,w, (x1)-(x+w) )
                # print("difference  = ", num2 + 1, "and ", num2, " = ", (x1) - (x + w), " ", (x1) / (x + w))
                # if (num2<6):
                #     dt.append(w)
                #     dt.append((x1)-(x+w))
                num2 += 1
        except:
            IndexError

        return dt

    def main(self):
        dt1= self.process(1)
        print(1 ,dt1)

        df=pd.read_csv('C:/Users/sami/Desktop/research integreation/FDDS/Support/CharacterProcess/machine\one.txt')
        df.replace('?',-99999,inplace=True)
        df.drop(['id'],1,inplace=True)

        #
        x= np.array(df.drop(['class'],1))
        y=np.array(df['class'])

        x_train, x_test, y_train,y_test = cross_validation.train_test_split(x,y,test_size=0.2)

        clf = neighbors.KNeighborsClassifier()
        clf.fit(x_train,y_train)
        accuracy = clf.score(x_test,y_test)
        print(accuracy)

        a = np.array(dt1)
        ex = a.reshape(1,-1)
        prediction = clf.predict(ex)
        print(prediction)
        return prediction

    # def callTest(self):
    #     return "test info"