import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def tune(im):
    cv.imshow("Original", im)
    #convert to grayscale and blur
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    #use binary threshold to locate white paper
    ret,thresh = cv.threshold(gray,230,255,cv.THRESH_BINARY_INV)
    edges = cv.Canny(image=thresh, threshold1=0, threshold2=255)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas) #white paper should be largest contour
    x,y,w,h = cv.boundingRect(contours[idx])
    #make paper roi
    roi = im[y:y+h,x:x+w]
    roi_blur = blur[y:y+h,x:x+w]
    cv.imshow("ROI", roi)

    #locate contours on top of paper
    ret,thresh = cv.threshold(roi_blur,250,255,cv.THRESH_BINARY_INV)
    edges = cv.Canny(image=thresh, threshold1=0, threshold2=255)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #find largest contour on the paper
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    #draw rectangle around largest contour on the paper and show it
    x,y,w,h = cv.boundingRect(contours[idx])
    color_roi = roi[y:y+h,x:x+w]
    cv.imshow("Color ROI", color_roi)
    
    #find the dominant color in the largest contour on the paper
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv.calcHist([color_roi],[i],None,[257],[0,257])
        plt.plot(histr,color = col)
        plt.xlim([0,257])
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
        tune(frame)
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