'''

This is a program to test interacting with a PLC using python

@author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified:7/28/21

'''
from pylogix import PLC
from struct import pack, unpack_from
import cv2 as cv
import argparse
import copy
import numpy as np
from matplotlib import pyplot as plt

#color range
b_low = 252
b_high = 256
g_low = 252
g_high = 256
r_low = 205
r_high = 220

h_low = 70
h_high = 90
s_low = 15
s_high = 60
v_low = 245
v_high = 255

'''
Narrows the frame to the paper that the pencils are on

@param im the frame
@return only the part of the frame that contains the paper
'''
def detect_background(im):
    #blur the image and convert it to graysclae
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    #use a binary threshold to create a black and white image to isolate the white paper
    ret, thresh = cv.threshold(blur, 230, 255, cv.THRESH_BINARY)
    #find edges and contours
    edges = cv.Canny(image=thresh, threshold1=0, threshold2=255)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #find the largest contour which should be the paper
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    #find the bounding rectangle, draw it, then return only the portion of the frame with the paper
    x,y,w,h = cv.boundingRect(contours[idx])
    im = cv.rectangle(im, (x,y), (x+w,y+h), (255,0,0), 3)
    return im[y:y+h,x:x+w] 

'''
Detect the objects within the region of interest

@param im the frame only containing the paper
@return a list of bounding rectangles around the objects
'''
def detect_obj(im):
    locations = [] #return value
    
    ##using HSV##
    #convert to hsv
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #filter out colors not in range
    lows = np.array([h_low, s_low, v_low])
    highs = np.array([h_high, s_high, v_high])
    mask = cv.inRange(hsv, lows, highs)
    im = cv.bitwise_and(im, im, mask=mask)
    #convert to grayscale and find contours
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    contours, hierarchy = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #if the area of the contour is large enough, find the bounding rectangle and add it to the return list
    for contour in contours:
        area = cv.contourArea(contour)
        if(area > 20): #this prevents small noise from being confused for the object
            locations.append(cv.boundingRect(contour))
    '''
    ##using dominant color##
    #convert to grayscale and blur the image
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    ret,thresh = cv.threshold(gray,250,255,cv.THRESH_BINARY_INV)    
    #find edges contours
    edges = cv.Canny(image=thresh, threshold1=0, threshold2=255)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #check which contours are around the desired object
    for contour in contours:
        x,y,w,h = cv.boundingRect(contour)
        center = (int((x+x+w)/2), int((y+y+h)/2))
        b,g,r = im[center[1],center[0]]
        bounded = im[y:y+h,x:x+w]
        bgr_planes = cv.split(bounded)       
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)
        #find the dominant colors
        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)
        #check the dominant colors against the color range of the pencils
        if( idx_b > b_low and idx_b < b_high and \
            idx_g > g_low and idx_g < g_high and \
            idx_r > r_low and idx_r < r_high):
            locations.append([x,y,w,h])
    '''
    return locations
'''

Main

'''
if __name__=='__main__':
    #command line arguments
    parser = argparse.ArgumentParser(description='Vision test with PLC communications')
    parser.add_argument('-v', help='Video file name. Default is usb camera.', default=0, type=str)
    parser.add_argument('-i', help='IP address of PLC', default='1.1.1.1', type=str)
    parser.add_argument('-s', help='Processor Slot of PLC', default=0, type=int)
    parser.add_argument('-r', help='Route to PLC', default=None, type=str)
    parser.add_argument('-c', help='Connection Size for PLC', default=4002, type=int)
    parser.add_argument('-p', help='Use PLC', action='store_true')
    args = parser.parse_args()

    #open video
    cap = cv.VideoCapture(args.v)
    if(cap.isOpened() == False):
        print("Video failed to open")
        
    if(args.p or args.i or args.s or args.r or args.c):
        #connect to PLC
        comm = PLC()
        comm.IPAddress = args.i
        comm.ProcessorSlot = args.s
        comm.Route = args.r
        comm.ConnectionSize = args.c
        use_plc = True
    else:
        use_plc = False
        
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
            #find the region of interest (the paper) and display it
            bounds = detect_background(frame)
            cv.imshow("Frame", frame)
            #get the shape of the ROI
            dim = bounds.shape
            #find the bounding rectangles for the objects
            rects = detect_obj(bounds)
            if(use_plc):
                leds = comm.Write('OUTPUT_LEDS',0)
                if(leds.Status is not 'Success'):
                    print('Failed to write to LED tag')
                    use_plc = False
            for rect in rects:
                x1 = rect[0]
                x2 = rect[0] + rect[2]
                y1 = rect[1]
                y2 = rect[1] + rect[3]
                center = (int((x1+x2)/2), int((y1+y2)/2))
                bounds = cv.rectangle(bounds, (x1,y1), (x2,y2), (0,255,0), 2)
                bounds = cv.circle(bounds, (center[0],center[1]), 2, (0,0,255), -1)
                if(use_plc):
                    if(center[0] < dim[1]*0.5):
                        if(center[1] < dim[0]*0.125):
                            grid_location = 0
                        elif(center[1] < dim[0]*0.25):
                            grid_location = 1
                        elif(center[1] < dim[0]*0.375):
                            grid_location = 2
                        elif(center[1] < dim[0]*0.5):
                            grid_location = 3
                        elif(center[1] < dim[0]*0.625):
                            grid_location = 4
                        elif(center[1] < dim[0]*0.75):
                            grid_location = 5
                        elif(center[1] < dim[0]*0.875):
                            grid_location = 6
                        else:
                            grid_location = 7
                    else:
                        if(center[1] < dim[0]*0.125):
                            grid_location = 8
                        elif(center[1] < dim[0]*0.25):
                            grid_location = 9
                        elif(center[1] < dim[0]*0.375):
                            grid_location = 10
                        elif(center[1] < dim[0]*0.5):
                            grid_location = 11
                        elif(center[1] < dim[0]*0.625):
                            grid_location = 12
                        elif(center[1] < dim[0]*0.75):
                            grid_location = 13
                        elif(center[1] < dim[0]*0.875):
                            grid_location = 14
                        else:
                            grid_location = 15
                    leds = comm.Write('OUTPUT_LEDS', (leds.Value[0] | (1 << grid_location)))
                    if(leds.Status is not 'Success'):
                        print('Failed to write to LED tag')
                        use_plc = False
            cv.imshow("Object", bounds)
            
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
    
    #From the API: If the PLC no longer sees a request,
    #it will eventually flush the connection, after about 90 seconds
    if(use_plc):
        comm.Close()
    

