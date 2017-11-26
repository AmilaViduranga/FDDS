import numpy as np
import cv2
import glob
from PIL import Image



def detectEye(img):

  # Load the Cascade Classifier Xml file
  face_cascade = cv2.CascadeClassifier("E:\/4th_year_2nd\/research\FDDS\src\imageQualityProcess\cascade/mallick_haarcascade_frontalface_default.xml")

  # Specifying minimum and maximum size parameters
  MIN_FACE_SIZE = 100
  MAX_FACE_SIZE = 300

  resized_image = cv2.resize(img, (1000, 500))

  # Reading each frame
  frameBig = img

  # Fixing the scaling factor
  scale = 640.0 / frameBig.shape[0]

  # Resizing the image
  frame = cv2.resize(frameBig, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

  # Converting to grayscale
  frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Detect faces
  faces = face_cascade.detectMultiScale(frameGray, scaleFactor=1.1, minNeighbors=5, flags=0,
                                        minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE),
                                        maxSize=(MAX_FACE_SIZE, MAX_FACE_SIZE))

  detected = False

  # Loop over each detected face
  for i in range(0, len(faces)):

    # Dimension parameters for bounding rectangle for face
    x, y, width, height = faces[i];

    # Calculating the dimension parameters for eyes from the dimensions parameters of the face
    ex, ey, ewidth, eheight = int(x + 0.125 * width), int(y + 0.25 * height), int(0.75 * width), int(0.25 * height)

    # Drawing the bounding rectangle around the face
    cv2.rectangle(frame, (ex, ey), (ex + ewidth, ey + eheight), (128, 255, 0), 2)

    #cv2.imshow('Ninja Eye Detector', frame)
    #key = cv2.waitKey(1)

    detected = True


  return detected


