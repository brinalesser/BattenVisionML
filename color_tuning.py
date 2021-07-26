#Adapted from code found here:
#https://stackoverflow.com/questions/44480131/python-opencv-hsv-range-finder-creating-trackbars
	
import cv2
import numpy as np

def callback(x):
	pass

cap = cv2.VideoCapture('./Videos/test_vid.mp4')
cv2.namedWindow('image')

ilowH = 0
ihighH = 179

ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255

# create trackbars for color change
cv2.createTrackbar('lowH','image',ilowH,179,callback)
cv2.createTrackbar('highH','image',ihighH,179,callback)

cv2.createTrackbar('lowS','image',ilowS,255,callback)
cv2.createTrackbar('highS','image',ihighS,255,callback)

cv2.createTrackbar('lowV','image',ilowV,255,callback)
cv2.createTrackbar('highV','image',ihighV,255,callback)

pause = False
while True:
    # grab the frame
	if not pause:
		ret, frame = cap.read()
    # get trackbar positions
	ilowH = cv2.getTrackbarPos('lowH', 'image')
	ihighH = cv2.getTrackbarPos('highH', 'image')
	ilowS = cv2.getTrackbarPos('lowS', 'image')
	ihighS = cv2.getTrackbarPos('highS', 'image')
	ilowV = cv2.getTrackbarPos('lowV', 'image')
	ihighV = cv2.getTrackbarPos('highV', 'image')

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_hsv = np.array([ilowH, ilowS, ilowV])
	higher_hsv = np.array([ihighH, ihighS, ihighV])
	mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

	frame = cv2.bitwise_and(frame, frame, mask=mask)

    # show thresholded image
	cv2.imshow('image', frame)
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
