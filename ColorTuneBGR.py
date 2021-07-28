'''
This program can be used to find the dominant color of certain objects. 
It displays the colors in a region of interest of a frame as a histogram.
The peaks indicate in the histogram represent the dominant colors (for BGR).

@author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified 7/28/21
'''
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

'''

@param im the frame
'''
def tune(im):
    
    ## Find paper to use as ROI ##
    
    cv.imshow("Original", im)
    #convert to grayscale and blur
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    #use binary threshold - converts everything that is not white like the paper to black
    ret,thresh = cv.threshold(gray,230,255,cv.THRESH_BINARY_INV)
    #find the contours
    edges = cv.Canny(image=thresh, threshold1=0, threshold2=255)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #locate the contour with the largest area (should be the paper)
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    #find bounding rectangle for contour
    x,y,w,h = cv.boundingRect(contours[idx])
    #region of interest is the paper
    roi = im[y:y+h,x:x+w]
    roi_blur = blur[y:y+h,x:x+w]
    cv.imshow("ROI", roi)

    ## Visualize the colors of the largest object on the paper ##
    
    #find contours within roi
    edges = cv.Canny(image=roi_blur, threshold1=0, threshold2=255)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #find largest contour
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    #find bounding rectangle for contour
    x,y,w,h = cv.boundingRect(contours[idx])
    #make new region of interest that only includes the object
    color_roi = roi[y:y+h,x:x+w]
    cv.imshow("Color ROI", color_roi)
    #find the dominant color in the new region of interest
    color = ('b','g','r')
    for i,col in enumerate(color):
        #makes a histogram of the different colors where each line represents
        #the values for a single color found in the ROI
        histr = cv.calcHist([color_roi],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.show()


cap = cv.VideoCapture(0)
count = 0
pause = False
#process video frame by frame
while(cap.isOpened()):
    if not pause:
        ret, frame = cap.read()
    if not ret:
        print("failed to read frame")
        break
    else:
        #call function to visualize the colours of the frame in histogram
        tune(frame)
    #control keys
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
cv.destroyAllWindows()
