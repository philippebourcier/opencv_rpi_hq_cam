#!/usr/bin/python3

import time
import picamera
import picamera.array
import cv2
import numpy as np

def get_circles(img):
    # bitwise_not to be removed (I test on black circles over a white bg)
    image = cv2.medianBlur(cv2.resize(cv2.bitwise_not(img),(812,608)),5)
    ret,th = cv2.threshold(image,80,255,cv2.THRESH_TOZERO)
    gray = cv2.cvtColor(th,cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=50,param2=30,minRadius=48,maxRadius=80)
    bw = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    if circles is not None:
        print("Got at least one circle")
        circles = np.round(circles[0,:]).astype("int")
        for (x,y,r) in circles: cv2.circle(bw,(x,y),r,(0,0,255),4)
    else:
        print("Nothing found")
    cv2.imwrite("output.jpg",np.hstack([image,bw]))

with picamera.PiCamera(resolution="2028x1520",framerate=15,sensor_mode=2) as camera:
    time.sleep(0.2)
    with picamera.array.PiRGBArray(camera) as stream:
        while True:
            start = time.time()
            camera.capture(stream,format='bgr',use_video_port=True)
            get_circles(stream.array)
            stream.truncate()
            stream.seek(0)
            print(time.time()-start)

