'''
This program tests object detection and edge detection strategies
using a camera pointed at a sheet of paper with pencils on it

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''

import cv2 as cv
import numpy as np

#pencil color range
b_low = 85
b_high = 120
g_low = 160
g_high = 205
r_low = 200
r_high = 230

'''
Narrows the frame to the paper that the pencils are on

@param im the frame
@return only the part of the frame that contains the paper
'''
def detect_background(im):
    #blur the image and convert it to graysclae
    blur = cv.medianBlur(im, 5)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    #use a binary threshold to create a black and white image to isolate the white paper
    ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
    #find contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #find the largest contour which should be the paper
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    #return only the portion of the frame with the paper
    x,y,w,h = cv.boundingRect(contours[idx])
    return im[y+15:y+h-15,x+15:x+w-15]
'''
Detect a stack of pencils within the region of interest

@param im the frame only containing the paper
@return 
'''
def detect_stack(im):
    #convert to grayscale and blur the image
    ret = im.copy()
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur, 7, 75, 75)
    #edge detection
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    #find contours
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #find the area of each contour
    areas = [cv.contourArea(c) for c in contours]    
    
    flag = False
    x = 0
    y = 0
    w = 0
    h = 0
    #find the largest contour that is the right color
    while not flag and len(areas) > 0:
        #find the largest contour and create a region of interest
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        bounded = np.copy(im[y:y+h,x:x+w])

        #detect the colors in the ROI
        bgr_planes = cv.split(bounded)       
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)
        #find the dominant colors in the ROI
        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)
        #check the dominant colors against the color range of the pencils
        if( idx_b > b_low and idx_b < b_high and \
            idx_g > g_low and idx_g < g_high and \
            idx_r > r_low and idx_r < r_high ):
            flag = True
        else:
            #if the colors don't match, try the next largest contour
            areas.pop(idx)

    if flag:
        #pencils found
        return ret[y:y+h,x:x+w]
    else:
        #pencils not found
        return []
'''
Find the individual pencils in the stack

@param im the frame narrowed down to the stack of pencils
@return the frame with the lines of the pencil edges drawn
'''
def detect_pencils(im):
    #convert to grayscale and blue
    ret = im.copy()
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.bilateralFilter(gray, 7, 75, 75)
    #edge detection
    edges = cv.Canny(image=blur, threshold1=0, threshold2=150)
    #find and draw lines
    lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/90, threshold=2, minLineLength=100, maxLineGap=20)
    if lines is not None:
        for line in lines:
            cv.line(ret,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
    #return the frame with the lines drawn on it
    return ret
'''

Main

'''
if __name__=='__main__':
    #open video
    cap = cv.VideoCapture(0)
    if(cap.isOpened() == False):   
        print("Video failed to open")
    pause = False
    #process video frame by frame
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if(ret):
            #show original image
            cv.imshow("Frame",frame)
            #find the paper and show the ROI
            paper = detect_background(frame.copy())
            cv.imshow("Paper", paper)
            #find the stack and show the ROI
            stack = detect_stack(paper.copy())
            #if the stack was found
            if len(stack) > 0:
                #show the stack
                cv.imshow("Stack", stack)
                #enlarge the image
                width = int(stack.shape[1] * 2)
                height = int(stack.shape[0] * 2)
                dim = (width, height)
                resized = cv.resize(stack, dim, interpolation=cv.INTER_AREA)
                #detect the pencils and show the frame with the lines drawn
                pencils = detect_pencils(resized.copy())
                cv.imshow("Pencils", pencils)
        else:
            print("Failed to read frame")
            break
        #control keys
        key = cv.waitKey(1)
        if(key == 27 or key == 113): #esc or q
            break
        elif(key == 115): #s
            cv.imwrite("Screenshot.jpg", frame)
        elif(key == 112): #p
            pause = not pause
        elif(key != -1):
            print(key)
