import cv2 as cv
import numpy as np
import math

def detect_frame(frame):
	img = cv.medianBlur(frame, 5)
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
	contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	
	areas = [cv.contourArea(c) for c in contours]
	idx = np.argmax(areas)
	
	x,y,w,h = cv.boundingRect(contours[idx])
	cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
	cv.imshow("Frame", frame)
	return frame[y+15:y+h-15,x+15:x+w-15]
	
def batten_lines(frame):
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	gray = cv.medianBlur(gray, 5)
	blur = cv.bilateralFilter(gray, 7, 75, 75)
	edges = cv.Canny(image=blur, threshold1=0, threshold2=200)
	return cv.HoughLinesP(image=edges, rho=1, theta=np.pi/90, threshold=2, minLineLength=50, maxLineGap=10)

def batten_bounds(im):
	gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	blur = cv.bilateralFilter(gray, 7, 75, 75)
	
	edges = cv.Canny(image=blur, threshold1=0, threshold2=150)
	contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
	
	if len(contours) > 0:
		cv.drawContours(im.copy(), contours, -1, (0, 255, 0), 3)
		areas = [cv.contourArea(c) for c in contours]
		idx = np.argmax(areas)
		return cv.boundingRect(contours[idx])
	else:
		return [0, 0, 0, 0]
	
def batten_bounds_hsv(im):
	
	#color bounds for pencils and battens, respectively
	lows = np.array([15, 25, 50]) #H,S,V
	highs = np.array([50, 255, 255]) #H,S,V
	#lows = np.array([0, 0, 150]) #H,S,V
	#highs = np.array([179, 100, 222]) #H,S,V
	hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
	hsv = cv.inRange(hsv, lows, highs)
	
	blur = cv.medianBlur(hsv, 5)
	edges = cv.Canny(image=blur, threshold1=0, threshold2=150)
	contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
	
	if len(contours) > 0:
		cv.drawContours(im.copy(), contours, -1, (0, 255, 0), 3)
		areas = [cv.contourArea(c) for c in contours]
		idx = np.argmax(areas)
		return cv.boundingRect(contours[idx])
	else:
		return [0, 0, 0, 0]
	
if __name__=='__main__':
	cap = cv.VideoCapture(0)
	if(cap.isOpened() == False):
		print("Video failed to open")
	while(cap.isOpened()):
		ret, frame = cap.read()
		if(ret):
			#Region of Interest
			roi = detect_frame(frame)
			cv.imshow("Region of interest", roi)
			
			#Hugh Lines
			img = np.copy(roi)
			lines = batten_lines(roi)
			if lines is not None:
				for line in lines:
					cv.line(img,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
			cv.imshow("Hugh Lines", img)
			
			#Bounding Rectangles
			img2 = np.copy(roi)
			x,y,w,h = batten_bounds(img2)
			cv.rectangle(img2, (x,y), (x+w,y+h), (0,255,0),2)
			cv.imshow("Bounding Rectangle", img2)
			
			img3 = np.copy(roi)
			x,y,w,h = batten_bounds_hsv(img3)
			cv.rectangle(img3, (x,y), (x+w,y+h), (0,255,0),2)
			cv.imshow("Bounding Rectangle Using HSV", img3)
		else:
			print("Failed to read frame")
			break
		
		if(cv.waitKey(1) & 0xFF == ord('q')):
			break
		if(cv.waitKey(1) & 0xFF == ord('p')):
			while(cv.waitKey(25) & 0xFF != ord('s')):
				pass