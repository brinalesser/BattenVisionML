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

PIXEL_WIDTH_PER_PAGE = 200
PIXEL_HEIGHT_PER_PAGE = 275
PAGE_WIDTH = 11
PAGE_HEIGHT = 17
ROBOT_X_OFFSET = 0
ROBOT_X_INCREMENT = PIXEL_WIDTH_PER_PAGE / PAGE_WIDTH
ROBOT_Y_OFFSET = 0
ROBOT_Y_INCREMENT = PIXEL_HEIGHT_PER_PAGE / PAGE_HEIGHT

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
    return ((x,y), im[y:y+h,x:x+w])

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
Gets the grid location on a 2x8 grid and the location on a 11x17 sheet of paper
given the center point of the object and the height and width of the frame
@param point the center point of the object
@param height the height of the frame
@param width the width of the frame
@return the grid location on a 2x8 grid, the x and y position on a sheet of paper in inches
'''
def get_grid_location(point, height, width):
    x = ROBOT_X_OFFSET + (point[0] / ROBOT_X_INCREMENT)
    y = ROBOT_Y_OFFSET + (point[1] / ROBOT_Y_INCREMENT)
    if(point[0] < width*0.5):
        if(point[1] < height*0.125):
            return (0, (x,y))
        elif(point[1] < height*0.25):
            return (1, (x,y))
        elif(point[1] < height*0.375):
            return (2, (x,y))
        elif(point[1] < height*0.5):
            return (3, (x,y))
        elif(point[1] < height*0.625):
            return (4, (x,y))
        elif(point[1] < height*0.75):
            return (5, (x,y))
        elif(point[1] < height*0.875):
            return (6, (x,y))
        else:
            return (7, (x,y))
    else:
        if(center[1] < height*0.125):
            return (8, (x,y))
        elif(center[1] < height*0.25):
            return (9, (x,y))
        elif(center[1] < height*0.375):
            return (10, (x,y))
        elif(center[1] < height*0.5):
            return (11, (x,y))
        elif(center[1] < height*0.625):
            return (12, (x,y))
        elif(center[1] < height*0.75):
            return (13, (x,y))
        elif(center[1] < height*0.875):
            return (14, (x,y))
        else:
            return (15, (x,y))

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
            ((x_offset, y_offset), bounds) = detect_background(frame)
            #get the shape of the ROI
            dim = bounds.shape
            #find the bounding rectangles for the objects
            rects = detect_obj(bounds)
            #draw grid
            frame = cv.line(frame, (x_offset+int(dim[1]*0.5),y_offset), (x_offset+int(dim[1]*0.5),y_offset+dim[0]), (255,0,0), 1)
            for i in range(8):
                frame = cv.line(frame, (x_offset,y_offset+int(dim[0]*i*0.125)), (x_offset+dim[1],y_offset+int(dim[0]*i*0.125)), (255,0,0), 1)
            #process locations of objects
            write_val = 0
            for rect in rects:
                x1 = rect[0]
                x2 = rect[0]+rect[2]
                y1 = rect[1]
                y2 = rect[1]+rect[3]
                center = (int((x1+x2)/2), int((y1+y2)/2))
                #get location on grid
                (grid, (x,y)) = get_grid_location(center, dim[0], dim[1])
                #draw on frame
                frame = cv.rectangle(frame, (x_offset+x1,y_offset+y1), (x_offset+x2,y_offset+y2), (0,255,0), 2) #bounding rectangle for object
                frame = cv.circle(frame, (x_offset+center[0],y_offset+center[1]), 2, (0,0,255), -1) #center point of object
                frame = cv.putText(frame, (" ("+str(round(x, 2))+","+str(round(y, 2))+")"), (x_offset+center[0], y_offset+center[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1) #location of object
                write_val = write_val | (1 << grid) #update value to write to PLC
            #write new value to PLC
            if(use_plc):
                leds = comm.Write('OUTPUT_LEDS', write_val)
                if(leds.Status is not 'Success'):
                    print('Failed to write to LED tag')
                    use_plc = False
            cv.imshow("Image", frame)
            
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