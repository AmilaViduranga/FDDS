import os
import time
import cv2

def capture45():
    os.system('"E:\/4th_year_2nd\/research\servoContrllers\ServoMotorController45\ServoMotorController\/bin\Debug\ServoMotorController.exe"')
    droidCamCapture("45degrees")

def capture135():
    os.system('"E:\/4th_year_2nd\/research\servoContrllers\ServoMotorController135\ServoMotorController\/bin\Debug\ServoMotorController.exe"')
    droidCamCapture("source")

def capture90():
    os.system('"E:\/4th_year_2nd\/research\servoContrllers\ServoMotorController90\ServoMotorController\/bin\Debug\ServoMotorController.exe"')
    droidCamCapture("90degrees")



def droidCamCapture(name):
    # Camera 2 is the integrated web cam on my netbook
    camera_port = 2

    # Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30

    # Now we can initialize the camera capture object with the cv2.VideoCapture class.
    # All it needs is the index to a camera port.
    camera = cv2.VideoCapture(camera_port)


    # Captures a single image from the camera and returns it in PIL format
    def get_image():
        # read is the easiest way to get a full image out of a VideoCapture object.
        retval, im = camera.read()
        return im


    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    for i in range(ramp_frames):
        # Take the actual image we want to keep
        camera_capture = get_image()
        file = "E:\/4th_year_2nd\/research\FDDS\Image\/" + name + ".jpg"
        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!
        cv2.imwrite(file, camera_capture)

    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    del (camera)

def captureAllImages():
    capture45()
    time.sleep(3)

    capture90()
    print("over")

    capture135()
    time.sleep(3)



