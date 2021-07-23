import cv2 as cv
import numpy as np
import math
import argparse
from statistics import mean
from matplotlib import pyplot as plt
import time

b_low = 95
b_high = 110
g_low = 170
g_high = 195
r_low = 210
r_high = 220

def detect_frame(frame):
    img = cv.medianBlur(frame, 5)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    
    x,y,w,h = cv.boundingRect(contours[idx])
    cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
    cv.imshow("Frame", frame)
    return frame[y+15:y+h-15,x+15:x+w-15]

def pencil_lines(im):
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 3)
    blur2 = cv.bilateralFilter(blur, 5, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    areas = [cv.contourArea(c) for c in contours]    
    
    flag = False
    x = 0
    y = 0
    w = 0
    h = 0
    while not flag:
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        bounded = np.copy(im[y:y+h,x:x+w])

        bgr_planes = cv.split(bounded)       
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)

        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)

        if( idx_b > b_low and idx_b < b_high and \
            idx_g > g_low and idx_g < g_high and \
            idx_r > r_low and idx_r < r_high ):
            flag = True
        else:
            if(len(areas) > 2):
                areas.pop(idx)
            else:
                break
    
    if flag:
        cv.rectangle(im, (x,y), (x+w,y+h), (0,255,0),2)
    
    width = int(im.shape[1] * 2)
    height = int(im.shape[0] * 2)
    dim = (width, height)
    resized = cv.resize(im, dim, interpolation=cv.INTER_AREA)
    cv.imshow("Pencils",resized)
    
def batten_lines(img, pencil):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur1 = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur1, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/90, threshold=5, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            cv.line(img,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
    cv.imshow("Lines", img)
    
mb = 5
bf = 7
def batten_bounds(im, drawBounds, drawConts, useHSV, pencilSettings):
    global mb, bf
    if useHSV:
        if pencilSettings:
            lows = np.array([15, 25, 50]) #H,S,V
            highs = np.array([50, 255, 255]) #H,S,V
        else:
            lows = np.array([0, 0, 150]) #H,S,V
            highs = np.array([179, 100, 222]) #H,S,V
        hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
        img = cv.inRange(hsv, lows, highs)#BW
    else:
        img = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur1 = cv.medianBlur(img, mb)
    blur2 = cv.bilateralFilter(blur1, bf, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    
    timeout = 5
    while(len(contours) > 5 or len(contours) < 1):
        if len(contours) > 5:
            mb += 2
            bf += 1
        elif(len(contours) < 1):
            mb -= 2
            bf -= 1
        blur1 = cv.medianBlur(img, mb)
        blur2 = cv.bilateralFilter(blur1, bf, 75, 75)
        edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
        contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        timeout -= 1
        if timeout == 0:
            break
    im_c = np.copy(im)
    cv.drawContours(im_c, contours, -1, (0, 255, 0), 3)
    if drawConts:
        cv.imshow("Contours",im_c)
    if drawBounds:
        areas = [cv.contourArea(c) for c in contours]
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        cv.rectangle(im, (x,y), (x+w,y+h), (0,255,0),2)
        cv.imshow("Bounding Rectangle", im)

if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-l', '--lines', help='show Hough Lines', action="store_true")
    parser.add_argument('-c', '--contours', help='show Contour lines', action="store_true")
    parser.add_argument('-b', '--boundRect', help='show bounding rectangle for largest contour', action="store_true")
    parser.add_argument('-s', '--hsv', help='use hsv image to create contours', action="store_true")
    parser.add_argument('-p', '--pencil', help='pencil settings', action="store_true")
    args = parser.parse_args()

    vidName="Videos/test_vid.mp4"
    if args.pencil:
        vidName = 0
    cap = cv.VideoCapture(vidName)
    if(cap.isOpened() == False):   
        print("Video failed to open")
    pause = False
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if(ret):
            #Region of Interest
            if args.pencil:
                roi = detect_frame(frame)
                #cv.imshow("Region of interest", roi)
            else:
                roi = np.copy(frame)
            #Hugh Lines
            if args.lines:
                img = np.copy(roi)
                if args.pencil:
                    pencil_lines(img)
                else:
                    batten_lines(img)
            #Bounding Rectangles and Contours
            if args.boundRect or args.contours or args.hsv:
                img2 = np.copy(roi)
                batten_bounds(img2, args.boundRect, args.contours, args.hsv, args.pencil)
            #Show something
            elif not args.lines and not args.pencil:
                cv.imshow("Region of Interest", roi)
        else:
            print("Failed to read frame")
            break
        key = cv.waitKey(1)
        if(key == 27 or key == 113): #esc or q
            break
        elif(key == 115): #s
            cv.imwrite("Screenshot.jpg", frame)
        elif(key == 112): #p
            pause = not pause
        elif(key != -1):
            print(key)
