'''
This program was an attempt to make the edge detection lines steadier.
It is extremely slow since multiple frames are processed to produce one image.

@author Sabrina Lesser
@date last modified 7/29/21
'''
import cv2 as cv
import numpy as np
import math

NUM_FRAMES = 8
PRECISION_M = 10
PRECISION = 10
PERCENT_OF_FRAMES = 0.25

'''
This program was an attempt to make the edge detection lines steadier

@param q a list of frames that acts like a queue
@return im_line an image with lines drawn on it
@return ret_lines the lines drawn on the image
'''
def edge_detect(q):
    assert(len(q) == NUM_FRAMES), ("The size of the queue is "+str(len(q))+", but should be "+str(NUM_FRAMES))

    #start with the first of the frames
    im = q[0]
    im_line = np.copy(im) * 0
    frame_height = q[0].shape[0]
    frame_width = q[0].shape[1]
    lines = []

    #go through each frame in the queue
    for frame in q:
        #convert to grayscale and blur
        im_gs = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)
        im_gs_blur = cv.medianBlur(im_gs_blur, ksize=5)
        
        sigma = np.std(im_gs_blur)
        mean = np.mean(im_gs_blur)
        lower = int(max(0, (mean - sigma)))
        upper = int(min(255, (mean + sigma)))

        #find edges and lines
        im_edges = cv.Canny(image=im_gs_blur, threshold1=lower, threshold2=upper)
        frame_lines = cv.HoughLinesP(im_edges, 10, np.pi / 90, 10, None, 100, 25)

        #go through the lines in the frame
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

                #compare the lines in the frame with the lines in other frames
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
        #add lines that appear in multiple frames
        if(line[6] >= NUM_FRAMES * PERCENT_OF_FRAMES):
            cv.line(im_line,(line[0],line[1]),(line[2],line[3]),(255,0,0),5)
            ret_lines.append([line[0],line[1],line[2],line[3]])
    im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)
    return im_line, ret_lines


if __name__=='__main__':
    cap = cv.VideoCapture("../Videos/vid1.mp4")
    if(cap.isOpened() == False):
            print("Video failed to open")
            
    count = 0
    q = []
    pause = False
    #process video frame by frame
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if not ret:
            print("failed to read frame")
            break
        
        if(len(q) < NUM_FRAMES - 1):
            q.append(frame)
        else:
            q.append(frame)
            im, lines = edge_detect(q)
            cv.imshow("Edges", im)
            q.pop(0)
            
        key = cv.waitKey(1)
        if(key == 27 or key == 113): #esc or q
            break
        elif(key == 115): #s
            cv.imwrite("Screenshot"+str(count)+".jpg", frame)
            count += 1
        elif(key == 112): #p
            pause = not pause
        elif(key != -1):
            print(key)

    cap.release()