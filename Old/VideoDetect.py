import cv2 as cv
import numpy as np

def edge_detect(im):
	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	im_gs_blur = cv.bilateralFilter(im_gs, 3, 75, 75)

	im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)
	lines = cv.HoughLinesP(im_edges, 1, np.pi / 90, 10, None, 100, 20)

	im_line = np.copy(im) * 0  # blank
	if lines is not None:
		for line in lines:
    			for x1,y1,x2,y2 in line:
    				cv.line(im_line,(x1,y1),(x2,y2),(255,0,0),5)

		im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)

	return im_line

if __name__=='__main__':
    
	cap = cv.VideoCapture(0)
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
			im = edge_detect(frame)
			cv.imshow("Edge Detection", im)
		else:
			print("Failed to read frame")
			break