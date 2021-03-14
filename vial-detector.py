#!/usr/bin/python3

import sys
import time
import picamera
from picamera import array
import numpy as np
import cv2
from random import shuffle
from daemonize import Daemonize
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

rez=picamera.PiResolution(round(2028/2.5),round(1520/2.5)).pad()
cx=int(str(rez).split("x")[0])//2
cy=int(str(rez).split("x")[1])//2
debug=False

def get_circles(img):
    image = cv2.medianBlur(img,5)
    ret,th = cv2.threshold(image,80,255,cv2.THRESH_TOZERO)
    gray = cv2.cvtColor(th,cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=50,param2=30,minRadius=48,maxRadius=80)
    bw = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    if circles is not None:
        if debug: print("Got at least one circle")
        shuffle(circles)
        circles = np.round(circles[0,:]).astype("int")
        for (x,y,r) in circles:
            cv2.circle(bw,(x,y),r,(0,0,255),4)
            offset_x=cx-x
            offset_y=cy-y
            if debug: cv2.circle(bw,(x+offset_x,y+offset_y),r,(255,255,0),2)
            else: return([offset_x,offset_y])
        if debug: cv2.circle(bw,(cx,cy),5,(0,255,255),2)
    else:
        if debug:
            print("Nothing found")
            cv2.imwrite("output.jpg",np.hstack([image,bw]))

def main():
    with picamera.PiCamera(resolution=rez,framerate=15,sensor_mode=2) as camera:
    	time.sleep(0.2)
    	with picamera.array.PiRGBArray(camera) as stream:
        	while True:
            		if debug: start = time.time()
            		camera.capture(stream,format='bgr',use_video_port=True)
            		off=get_circles(stream.array)
            		print(off)
            		stream.truncate()
            		stream.seek(0)
            		if debug: print(time.time()-start)

if len(sys.argv)==2 and sys.argv[1]=="-d":
    daemon=Daemonize(app="vial-detector",pid=pid,action=main)
    daemon.start()
else:
    main()

