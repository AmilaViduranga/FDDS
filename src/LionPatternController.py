import os
import cv2

class LionPatternController():
    def MainCall(self):
        final_result = "Given driving license is "
        # change project path according to yours
        # path = 'D:\\FDDS'
        path = 'E:\\4th_year_2nd\\research\\FDDS'

        im = cv2.imread(""+path+"\\Image\\source.jpg")

        resized_image = cv2.resize(im, (1000, 500))
        # Crop image
        imCrop = resized_image[int(136.0):int(136.0 + 80.0), int(708.0):int(708.0 + 244.0)]
        cv2.imwrite(path+'\\Support\\Pattern\\1.png', imCrop)

        with open(""+path+"\\Support\\Pattern\\Values.txt") as f:
            with open(""+path+"\\\Support\\Pattern\\sampleValues.txt", "w") as f1:
                for line in f:
                    f1.write(line)

        F = open(""+path+"\\Support\\Pattern\\sampleValues.txt", "a")
        image = cv2.imread(path+'\\Support\\Pattern\\1.png',0)
        img2 = cv2.resize(image,(64,128))

        img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2RGB)
        hog = cv2.HOGDescriptor((64, 128),(16, 16),(8, 8),(8, 8), 9, 0, -1, 0, 0.2, 0)

        winStride = (8,8)
        padding = (0,0)
        locations = []
        hist = hog.compute(img2,winStride,padding,locations)

        F.write("\n")
        F.write("-1 ")

        for i in range(len(hist)):
            F.write(str(i+1))
            F.write(":%s" % round(float(hist[i]),6))
            F.write(" ")

        F.close()

        os.system(""+path+"\\Support\\Pattern\\libsvm-3.18\\windows\\svm-scale -l -1 -u 1 -s range "+path+"\\Support\\Pattern\\sampleValues.txt > "+path+"\\Support\\Pattern\\hogvaluesscale.scale")
        os.system(""+path+"\\Support\\Pattern\\libsvm-3.18\\windows\\svm-predict -b 0 "+path+"\\Support\\Pattern\\hogvaluesscale.scale "+path+"\\Support\\Pattern\\model.model "+path+"\\Support\\Pattern\\final.txt");


        data = []
        F1 = open(""+path+"\\Support\\Pattern\\final.txt", "r")
        data = F1.readlines()
        var1 = data[-1]

        if int(var1) == -1:
            final_result = final_result + "fake driving license"
            print(var1+'fake driving license')
        else:
            final_result = final_result + "legal driving license"
            print(var1+'original driving license')


        f.close()
        f1.close()
        F.close()
        F1.close()

        os.remove(path+'\\Support\\Pattern\\sampleValues.txt')
        os.remove(path+'\\Support\\Pattern\\hogvaluesscale.scale')
        os.remove(path+'\\Support\\Pattern\\final.txt')

        return final_result






