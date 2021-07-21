import cv2 as cv
import numpy as np
import math

NUM_FRAMES = 8
PRECISION_M = 10
PRECISION = 10
PERCENT_OF_FRAMES = 0.25

ROBOT_X_OFFSET = 10
ROBOT_X_INCREMENT = 10
ROBOT_Y_OFFSET = 10
ROBOT_Y_INCREMENT = 10

def edge_detect_orig(im):
	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)
	im_gs_blur = cv.medianBlur(im_gs_blur, ksize=5)
	
	sigma = np.std(im_gs_blur)
	mean = np.mean(im_gs_blur)
	lower = int(max(0, (mean - sigma)))
	upper = int(min(255, (mean + sigma)))
		
	im_edges = cv.Canny(image=im_gs_blur, threshold1=lower, threshold2=upper)
	lines = cv.HoughLinesP(im_edges, 1, np.pi / 90, 10, None, 100, 25)

	im_line = np.copy(im) * 0  # blank
	if lines is not None:
		for line in lines:
    			for x1,y1,x2,y2 in line:
    				cv.line(im_line,(x1,y1),(x2,y2),(255,0,0),5)

		im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)

	return im_line
	
def detect_contours(im):
	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)

	im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)
	contours, hierarchy = cv.findContours(im_edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
	
	cv.drawContours(im, contours, -1, (0, 255, 0), 3)
	return im
	
def edge_detect(q):
	assert(len(q) == NUM_FRAMES), ("The size of the queue is "+str(q.qsize())+", but should be "+str(NUM_FRAMES))
	
	im = q[0]
	im_line = np.copy(im) * 0
	frame_height = q[0].shape[0]
	frame_width = q[0].shape[1]
	lines = []
	
	for frame in q:
		im_gs = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)
		im_gs_blur = cv.medianBlur(im_gs_blur, ksize=5)
		
		sigma = np.std(im_gs_blur)
		mean = np.mean(im_gs_blur)
		lower = int(max(0, (mean - sigma)))
		upper = int(min(255, (mean + sigma)))
		
		im_edges = cv.Canny(image=im_gs_blur, threshold1=lower, threshold2=upper)
		frame_lines = cv.HoughLinesP(im_edges, 10, np.pi / 90, 10, None, 100, 25)
		
		if frame_lines is not None:
			for frame_line in frame_lines:
				#y = mx + b
				x1_1 = frame_line[0][0]
				y1_1 = frame_line[0][1]
				x2_1 = frame_line[0][2]
				y2_1 = frame_line[0][3]
				m_1 = math.inf
				if((x2_1 - x1_1) != 0):
					m_1 = (y2_1 - y1_1) / (x2_1 - x1_1)
				b_1 = y1_1 - (m_1 * x1_1)
				
				merged = False
				for i in range(len(lines)):
					x1_2 = lines[i][0]
					y1_2 = lines[i][1]
					x2_2 = lines[i][2]
					y2_2 = lines[i][3]
					m_2 = lines[i][4]
					b_2 = lines[i][5]
					#combine lines when the lines are parallel and close together
					if(m_1 == math.inf and m_2 == math.inf and abs(x1_1 - x1_2) < PRECISION):
						lines[i][1] = min(y1_1, y1_2, y2_1, y2_2)
						lines[i][3] = max(y1_1, y1_2, y2_1, y2_2)
						lines[i][6] += 1
						merged = True
						break
					if(m_1 == 0 and m_2 == 0 and abs(y1_1 - y1_2) < PRECISION):
						lines[i][0] = min(x1_1, x1_2, x2_1, x2_2)
						lines[i][2] = max(x1_1, x1_2, x2_1, x2_2)
						lines[i][6] += 1
						merged = True
						break
					if(abs(m_1-m_2) < PRECISION_M and abs((y1_1+y2_1)/2-(y1_2 + y2_2)/2) < PRECISION and \
                       ((x1_2 < x1_1 and x1_1 < x2_2) or (x1_1 < x1_2 and x1_2 < x2_1) or \
                        (x1_2 < x2_1 and x2_1 < x2_2) or (x1_1 < x2_2 and x2_2 < x2_1)) ):
						if(x1_1 < x1_2):
							x1_2 = x1_1
							y1_2 = y1_1
						if(x2_1 > x2_2):
							x2_2 = x2_1
							y2_2 = y2_1
						m_2 = math.inf
						if((x2_2 - x1_2) != 0):
							m_2 = (y2_2 - y1_2) / (x2_2 - x1_2)
						b_2 = y1_2 - (m_2 * x1_2)
						lines[i][0] = x1_2
						lines[i][1] = y1_2
						lines[i][2] = x2_2
						lines[i][3] = y2_2
						lines[i][4] = m_2
						lines[i][5] = b_2
						lines[i][6] += 1
						merged = True
						break
				if not merged:
					lines.append([x1_1, y1_1, x2_1, y2_1, m_1, b_1, 1])
					
	ret_lines = []
	for line in lines:
		#print("("+str(line[0])+","+str(line[1])+"),("+str(line[2])+","+str(line[3])+")")
		if(line[6] >= NUM_FRAMES * PERCENT_OF_FRAMES):
			cv.line(im_line,(line[0],line[1]),(line[2],line[3]),(255,0,0),5)
			ret_lines.append([line[0],line[1],line[2],line[3]])
	im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)
	return im_line, ret_lines

def pixelToCoord(line):
	x1 = ROBOT_X_OFFSET + (line[0] / ROBOT_X_INCREMENT)
	y1 = ROBOT_Y_OFFSET + (line[1] / ROBOT_Y_INCREMENT)
	x2 = ROBOT_X_OFFSET + (line[2] / ROBOT_X_INCREMENT)
	y2 = ROBOT_Y_OFFSET + (line[3] / ROBOT_Y_INCREMENT)
	return [x1, y1, x2, y2]

if __name__=='__main__':
	


	cap = cv.VideoCapture("./vid1.mp4")
	if(cap.isOpened() == False):
		print("Video failed to open")

	q = []
	count = 0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if(cv.waitKey(1) & 0xFF == ord('q')):
			break
		if(cv.waitKey(1) & 0xFF == ord('p')):
			while(cv.waitKey(25) & 0xFF != ord('s')):
				pass
		if(ret): 
			#enqueue and dequeue frames
			q.append(frame)
			if(count >= NUM_FRAMES - 1):
				im, lines = edge_detect(q)
				im_orig = edge_detect_orig(q[0])
				#im_con = detect_contours(q[0])
				
				cv.imshow("New", im)
				cv.imshow("Original", im_orig)
				#cv.imshow("Contours", im_con)
				for line in lines:
					robo_coord = pixelToCoord(line)
					print(robo_coord)     
				q.pop(0)
			else:
				count += 1
		else:
			print("Failed to read frame")
			break