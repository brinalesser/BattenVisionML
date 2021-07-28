
'''
This program is used to find the HSV colors in a video

*** Adapted from code found here ***
https://stackoverflow.com/questions/44480131/python-opencv-hsv-range-finder-creating-trackbars

@author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified 7/28/21
'''
	
import cv2
import numpy as np
import argparse

#Trackbar callback does nothing
def callback(x):
	pass

#command line arguments
parser = argparse.ArgumentParser(description='HSV Color tuning')
parser.add_argument('-v', help='Video file name. Default is Raspberry Pi USB camera.', default=0, type=str)
args = parser.parse_args()

#Open video
cap = cv.VideoCapture(args.v)

#Create separate window for trackbars
cv2.namedWindow('trackbars')

#Trackbar values
ilowH = 0
ihighH = 179
ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255

# create trackbars for color change
cv2.createTrackbar('lowH','trackbars',ilowH,179,callback)
cv2.createTrackbar('highH','trackbars',ihighH,179,callback)
cv2.createTrackbar('lowS','trackbars',ilowS,255,callback)
cv2.createTrackbar('highS','trackbars',ihighS,255,callback)
cv2.createTrackbar('lowV','trackbars',ilowV,255,callback)
cv2.createTrackbar('highV','trackbars',ihighV,255,callback)

pause = False
while True:
	# grab the frame
	if not pause:
		ret, frame = cap.read()
	# get trackbar positions
	ilowH = cv2.getTrackbarPos('lowH', 'trackbars')
	ihighH = cv2.getTrackbarPos('highH', 'trackbars')
	ilowS = cv2.getTrackbarPos('lowS', 'trackbars')
	ihighS = cv2.getTrackbarPos('highS', 'trackbars')
	ilowV = cv2.getTrackbarPos('lowV', 'trackbars')
	ihighV = cv2.getTrackbarPos('highV', 'trackbars')
	# filter out colors not in the range
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_hsv = np.array([ilowH, ilowS, ilowV])
	higher_hsv = np.array([ihighH, ihighS, ihighV])
	mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
	frame = cv2.bitwise_and(frame, frame, mask=mask)
	# show thresholded image
	cv2.imshow('image', frame)
	#control keys
	key = cv2.waitKey(1000)
	if(key == 27 or key == 113): #esc or q
		break
	elif(key == 115): #s
		cv2.imwrite("Frame"+str(count)+".jpg", frame)
		count += 1
	elif(key == 112): #p
		pause = not pause
	elif(key != -1):
		print(key)

 
cv2.destroyAllWindows()
