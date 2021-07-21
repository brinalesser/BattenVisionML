import cv2 as cv
import numpy as np
import argparse

'''

detect wood by color

'''
def color_detect(im):

	lows = np.array([-50, 0, 100]) #H,S,V
	highs = np.array([50, 150, 255]) #H,S,V
	im_hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
	im_hsv = cv.inRange(im_hsv, lows, highs)
	return im_hsv

'''

draw lines to indicate where the battens are

'''
def edge_detect(im):
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
	lines = cv.HoughLinesP(im_edges, 1, np.pi / 180, 10, None, 100, 20)


	return lines


if __name__=='__main__':

	parser = argparse.ArgumentParser(description='Test to detect wood using color')
	parser.add_argument('-v', help='Video file', default="Videos for ML/vid0.mp4", type=str)
	args = parser.parse_args()

	cap = cv.VideoCapture(args.v)
	if(cap.isOpened() == False):
		print("Video failed to open")

	while(cap.isOpened()):
		ret, frame = cap.read()
		if(ret):
			frame_det = color_detect(frame)	
			frame_det = cv.cvtColor(frame_det, cv.COLOR_GRAY2BGR)
			lines = edge_detect(frame)
			if lines is not None:
				for line in lines:
    					for x1,y1,x2,y2 in line:
    						cv.line(frame_det,(x1,y1),(x2,y2),(255,0,0),5)

			cv.imshow("Original", frame)
			cv.imshow("Detected", frame_det)
			if(cv.waitKey(1) & 0xFF == ord('q')):
				break
			if(cv.waitKey(1) & 0xFF == ord('p')):
				while(cv.waitKey(1) & 0xFF != ord('s')):
					pass
		else:
			print("Error reading frame")
			break

	cap.release()
	cv.destroyAllWindows()