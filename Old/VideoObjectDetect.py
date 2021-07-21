import cv2 as cv
import numpy as np

def detect(frame):
	im_gs = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	im_gs = np.float32(im_gs)
	dst = cv.cornerHarris(im_gs, 2, 3, .04)
	dst = cv.dilate(dst, None)
	im = frame
	im[dst>0.01*dst.max()]=[0,0,255]
	return im

def detect2(frame):
	im_gs = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	corners = cv.goodFeaturesToTrack(im_gs, 25, 0.01, 10)
	corners = np.int0(corners)
	
	im = frame
	for i in corners:
		x,y = i.ravel()
		cv.circle(im, (x,y),3,255,-1)
	return im

def detect3(frame):
	
	train = cv.imread('test_image.png')
	train_gs = cv.cvtColor(train, cv.COLOR_BGR2GRAY)
	query_gs = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	
	orb = cv.ORB_create()
	
	t_keypoints, t_descriptors = orb.detectAndCompute(train_gs, None)
	q_keypoints, q_descriptors = orb.detectAndCompute(query_gs, None)
	
	matcher = cv.BFMatcher()
	matches = matcher.match(q_descriptors, t_descriptors)
	
	im = cv.drawMatches(frame, q_keypoints, train, t_keypoints, matches[:20], None)
	im = cv.resize(im, (1000, 500))
	return im

def detect4(frame):
	fast = cv.FastFeatureDetector_create()
	keypoints = fast.detect(frame, None)
	im = cv.drawKeypoints(frame, keypoints, None, color=(255,0,0))
	return im

def detect5(frame):
	im = frame
	image = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	image = cv.bilateralFilter(image, 7, 75, 75)
	#image = cv.equalizeHist(image)
	image = cv.medianBlur(image, ksize=5)
	ret, thresh = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
	conts, hier = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cv.drawContours(im, conts, -1, (0,255,0), 3)
	return im

if __name__=='__main__':
    
	cap = cv.VideoCapture("vid1.mp4")
	#cap = cv.VideoCapture(0)
	#cap = cv.VideoCapture('rtsp://service:Administrator1!@10.208.10.173/1')
	if(not cap.isOpened()):
		print("Could not access camera")
		exit()

	while(cap.isOpened()):
		ret, frame = cap.read()
		if(cv.waitKey(1) & 0xFF == ord('q')):
			break
		if(cv.waitKey(1) & 0xFF == ord('p')):
			while(cv.waitKey(25) & 0xFF != ord('s')):
				pass
		if(ret):
			#im = detect(frame)
			#cv.imshow("Detection", im)
			#im2 = detect2(frame)
			#cv.imshow("Detection2", im2)
			#im3 = detect3(frame)
			#im3 = cv.resize(im3, (1000, 500))
			#cv.imshow("Detection3", im3)
			#im4 = detect4(frame)
			#cv.imshow("Detection4", im4)
			im5 = detect5(frame)
			cv.imshow("Detection5", im5)
		else:
			print("Failed to read frame")
			break