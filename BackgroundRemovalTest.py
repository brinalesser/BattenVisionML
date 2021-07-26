import cv2 as cv
import numpy as np
import copy

blur_value = 7
bin_thresh = 60
bg_thresh = 50
bg_captured = False

def remove_bg(im):
    mask = bg_model.apply(im, learningRate=0)
    blank = np.ones((3,3),np.uint8)
    mask = cv.erode(mask, blank, iterations=1)
    return cv.bitwise_and(im, im, mask=mask)

def detect_roi(im):
    ret = copy.deepcopy(im)
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    ret, thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY)
    cpy = copy.deepcopy(thresh)
    contours, hierarchy = cv.findContours(cpy, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        areas = [cv.contourArea(c) for c in contours]    
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        ret = im[y:y+h,x:x+w]
    return ret

if __name__=='__main__':

    cap = cv.VideoCapture(0)
    if(cap.isOpened() == False):   
        print("Video failed to open")
    
    pause = False
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if(ret):
            frame = cv.bilateralFilter(frame, 5, 50, 100)
            cv.imshow("Original", frame)
            if bg_captured:
                fg = remove_bg(frame)
                roi = detect_roi(fg)
                cv.imshow("ROI", roi)
        else:
            print("Failed to read frame")
            break
        
        key = cv.waitKey(10)
        if(key == 27 or key == 113): #esc or q
            cv.destroyAllWindows()
            break
        elif(key == 115): #s
            cv.imwrite("Screenshot.jpg", frame)
        elif(key == 112): #p
            pause = not pause
        elif(key == 98): #b
            bg_model = cv.createBackgroundSubtractorMOG2(0, bg_thresh)
            #bg_model = cv.createBackgroundSubtractorKNN()
            bg_captured = True
        elif(key == 114): #r
            bg_model = None
            bg_captured = False
            print("BG reset")