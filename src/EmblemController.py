import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10


class EmblemController():
    def mainCall(self):
        final_result = " - "
        print("Method has caleld")
       # Read image
        im = cv2.imread("./Image/source.jpg")

        resized_image = cv2.resize(im, (1000, 500))
        # Crop image
        imCrop = resized_image[int(30.0):int(30.0 + 108.0), int(850.0):int(850.0 + 120.0)]
        cv2.imwrite('./Support/Pattern/sample.jpg',imCrop)

        # img1 = cv2.imread('./Support/Pattern/sample.png',0)          # queryImage
        img1 = cv2.imread('./Support/Pattern/AA.jpg', 0)  # queryImage

        img2 = cv2.imread('./Support/Pattern/sample.jpg',0) # trainImage


        # Initiate SIFT detector
        surf =  cv2.xfeatures2d.SIFT_create(400)

        # find the keypoints and descriptors with SIFT
        kp1, des1 = surf.detectAndCompute(img1,None)
        kp2, des2 = surf.detectAndCompute(img2,None)

        # Fast Library for Approximate Nearest Neighbors
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1,des2,k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)

        print(good)
        # length compare with minimum matching count
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

            print("enough matches are found")
            final_result = final_result + "enough matches are found"
        else:
            print("enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            final_result = final_result + "enough matches are found"
            matchesMask = None


        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                           singlePointColor = None,
                           matchesMask = matchesMask, # draw only inliers
                           flags = 2)

        img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

        print("you are close to get result")

        plt.imshow(img3,),plt.show()
        return final_result
