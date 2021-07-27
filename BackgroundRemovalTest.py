'''
This program can remove background for a stationary
camera with an unchanging background

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''

import cv2 as cv
import numpy as np
import copy

bg_captured = False

'''
Remove background from image using model
@param im the frame
@return the frame with the background black
'''
def remove_bg(im):
    #get the bit mask for the background
    mask = bg_model.apply(im, learningRate=0)
    #make a blank image
    blank = np.ones((3,3),np.uint8)
    #erode the mask (makes lines thinner like the opposite of dilation)
    mask = cv.erode(mask, blank, iterations=1)
    #return the backgroud mask && the image to black out
    #the background and leave only the foreground
    return cv.bitwise_and(im, im, mask=mask)
'''
Detect the region of interest (isolate the foreground)
@param im the frame with the background removed
@return the region of interest (the foreground)
'''
def detect_roi(im):
    #grayscale and blur
    ret = copy.deepcopy(im)
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    #binary threshold to make the image black and white
    #to differentiate between the background and foreground easier
    ret, thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY)
    #find the contours
    cpy = copy.deepcopy(thresh)
    contours, hierarchy = cv.findContours(cpy, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #if there are contours, find the largest
    if len(contours) > 0:
        #find the largest area of all the contours
        areas = [cv.contourArea(c) for c in contours]    
        idx = np.argmax(areas)
        #draw a bounding rectangle aroung the larges contour
        #and return only that part of the original image
        x,y,w,h = cv.boundingRect(contours[idx])
        ret = im[y:y+h,x:x+w]
    return ret

if __name__=='__main__':

    #open the video
    cap = cv.VideoCapture(0)
    if(cap.isOpened() == False):   
        print("Video failed to open")
    #play the video
    pause = False
    while(cap.isOpened()):
        if not pause:
            #get the next frame
            ret, frame = cap.read()
        if(ret):
            #filter the frame, remove the background, then get the region of interest only
            frame = cv.bilateralFilter(frame, 5, 50, 100)
            cv.imshow("Original", frame)
            if bg_captured:
                fg = remove_bg(frame)
                roi = detect_roi(fg)
                cv.imshow("ROI", roi)
        else:
            print("Failed to read frame")
            break
        
        #control keys
        key = cv.waitKey(10)
        if(key == 27 or key == 113): #esc or q
            cv.destroyAllWindows()
            break
        elif(key == 115): #s
            cv.imwrite("Screenshot.jpg", frame)
        elif(key == 112): #p
            pause = not pause
        elif(key == 98): #b
            #capture the background and create the model
            bg_model = cv.createBackgroundSubtractorMOG2(0, bg_thresh)
            #bg_model = cv.createBackgroundSubtractorKNN()
            bg_captured = True
        elif(key == 114): #r
            #reset the model for the background
            bg_model = None
            bg_captured = False