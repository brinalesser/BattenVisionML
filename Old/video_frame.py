import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt

'''

detect battens and display bounding rectagles

'''
def find_objects(im):

	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	im_gs = cv.equalizeHist(im_gs)

	#find battens
	found = batten_data.detectMultiScale(im_gs, minSize=(20,20))
	amount_found = len(found)

	#draw rectangle around battens
	if(amount_found != 0):
		count = 0
		for(x, y, w, h) in found:
			im = cv.rectangle(im, (x,y), ((x+h), (y+w)), (0,255,0), 4)
			count += 1
			if count > 200:
				break
	
	return im

'''

detect edges and draw lines

'''
def find_edges(im):
	#convert to grey scale and blur
	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)

	#cv.imshow("Greyscale Blurred Image", im_gs_blur)
	#cv.waitKey(0)

	#edge detection
	im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)

	#cv.imshow("Edge Detection", im_edges)
	#cv.waitKey(0)

	#Hough Line Transform
	#cv.HoughLinesP(image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
	lines = cv.HoughLinesP(im_edges, 1, np.pi / 90, 10, None, 200, 20)

	im_line = np.copy(im) * 0  # blank
	if lines is not None:
		for line in lines:
    			for x1,y1,x2,y2 in line:
    				cv.line(im_line,(x1,y1),(x2,y2),(255,0,0),5)

		im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)

	return im_line

#cascade classifier
classifierFolder = "Images/cascade"
#video
vidname = "Videos for ML/vid0.mp4"
detectEdges = False
detectObjects = False

args = sys.argv[1:]
opts = "eov:c:"
longOpts = ["EdgeDetect", "ObjectDetect", "VideoName", "ClassifierFolder"]

try:
	arguments, values = getopt.getopt(args, opts, longOpts)
	for arg, val in arguments:
		if arg in ("-v", "--VideoName"):
			vidname = val
		elif arg in ("-c", "--Classifier"):
			classifierFolder = val
		elif arg in ("-e", "--EdgeDetect"):
			detectEdges = True
		elif arg in ("-o", "--ObjectDetect"):
			detectObjects = True
except getopt.error as err:
	print(str(err))

#cascade training data
batten_data = cv.CascadeClassifier(classifierFolder+"/cascade.xml")

#get VideoCapture Object
cap = cv.VideoCapture(vidname)
if(cap.isOpened() == False):
	print("Video failed to open")

while(cap.isOpened()):
	ret, frame = cap.read()
	if(ret==True):
		if(detectObjects):
			frame = find_objects(frame)
		if(detectEdges):
			frame = find_edges(frame)
		cv.imshow('Vid test', frame)
		if(cv.waitKey(1) & 0xFF == ord('q')):
			break
		if(cv.waitKey(1) & 0xFF == ord('p')):
			while(cv.waitKey(25) & 0xFF != ord('s')):
				pass
	else:
		print("Error reading frame")
		break

cap.release()
cv.destroyAllWindows()

