
import cv2
import  matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageFilter,ImageEnhance
import os
from sklearn import neighbors,cross_validation
import pandas as pd
import glob

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
        in1 = cv2.imread("./Support/CharacterProcess/imgs/nu-Scand600 edit.jpg", 1)
        # in1 = cv2.imread("./Support/CharacterProcess/imgs/dup-scan600.jpg", 1)

        imgcpy1 = in1.copy()
        imgcpy2 = in1.copy()
        imgcpy3 = in1.copy()

        blured = cv2.medianBlur(in1,3)
        gray = cv2.cvtColor(blured,cv2.COLOR_BGR2GRAY)

        ret,imgThresh = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)

        cv2.imwrite("./Support/CharacterProcess/results/thresh.jpg",imgThresh)
        cv2.imshow("thresh", imgThresh)
        cv2.waitKey(1)

        imgContours,contours,npaHierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        contours.sort(key=lambda x:self.get_contour_precedence(x, imgThresh.shape[1]))

        cv2.drawContours(imgcpy1,contours,-1,(0,0,255), 0)
        cv2.imwrite("./Support/CharacterProcess/results/cont.jpg",imgcpy1)
        cv2.imshow("contour" , imgcpy1)
        cv2.waitKey(1)

        path ='./Support/CharacterProcess/results/characters/'

        num=0
        num1=0
        data=[]
        dt=[]
        for c in contours:
                cnt = contours[num]
                if cv2.contourArea(cnt) >area1:
                    x, y, w, h = cv2.boundingRect(cnt)
                    roi = imgcpy2[y:y + h, x:x + w]
                    # cv2.imwrite(path+str(num1) + '.jpg', roi)
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
                roi_a = imgcpy2[y:y + h, x:x + w]
                if (num2 == 1):
                    yofs = y
                    xofs = x
                numtwo=data[num2+1]
                x1, y1, w1, h1 = cv2.boundingRect(numtwo)
                roi = imgcpy1[y1:y1 + h1, x1:x1 + w1]
                # print("difference  " ,num2+1, "and ", num2, " = " ,x1,w1, x,w, (x1)-(x+w) )
                # print("difference  = " ,num2+1, "and ", num2, " = ", (x1)-(x+w)," ", (x1)/(x+w) )
                if (num2<9):
                    cv2.imwrite(path + str(num2) + '.jpg', roi_a)
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
        # cv2.imwrite("bottom.jpg", imgThresh)

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
        # Histogram Calculation
        img_h = cv2.imread("./Support/CharacterProcess/results/characters/1.jpg", 1)
        gray = cv2.cvtColor(img_h, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        plt.figure()
        plt.title("Grayscale Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()
        ar =[]
        value=0
        for img in glob.glob("Support/CharacterProcess/imgs/hist/*.jpg"):
            file_path = img
            file_name = os.path.basename(file_path)
            imga = cv2.imread(str(img), 1)
            gray2 = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
            hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
            a = cv2.compareHist(hist, hist2, cv2.HISTCMP_CORREL)
            print(os.path.splitext(file_name)[0], " ", a)
            round(a, 4)
            ar.append(a)
        print(sum(ar))
        print( "length is ",len(ar),sum(ar) / len(ar))
        histvalue = sum(ar) / len(ar)


        #profile checking
        ls =[1,2,3,4,5,6,7,8]
        prf=[]
        for ch in ls:
            rd = cv2.imread("./Support/CharacterProcess/results/characters/"+str(ch)+".jpg", 1)
            blured = cv2.medianBlur(rd, 3)
            gray = cv2.cvtColor(blured, cv2.COLOR_BGR2GRAY)
            ret, imgThresh = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY)
            cv2.imwrite("./Support/CharacterProcess/results/characters/profile/" + str(ch)+".jpg", imgThresh)
            rd2 = cv2.imread("./Support/CharacterProcess/results/characters/profile/" + str(ch)+".jpg", 0)

            r, c = rd2.shape
            bp = 0
            ar = np.array(rd2)
            for ca in range(0, r):
                for da in range(0, c):
                    if ((ar[ca][da]) < 200):
                        bp = bp + 1
            prf.append(bp)
            print(prf)

        dt = dt+prf
        return dt,histvalue


    def main(self):
        dt1,histval= self.process(1)
        print(1 ,dt1)
        print ("this is ",histval)
        # df=pd.read_csv('./Support/CharacterProcess/machine\one2.txt')
        df=pd.read_csv('./Support/CharacterProcess/machine\one2withbpfull.txt')
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