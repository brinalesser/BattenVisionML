'''
Object detection using color

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''

import cv2 as cv
import numpy as np
import argparse

'''
Detect wood by color, then filter out other colors

@param im the image
@return the image with a range of colors filtered out
'''
def color_detect(im):
    lows = np.array([-50, 0, 100]) #H,S,V
    highs = np.array([50, 150, 255]) #H,S,V
    im_hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    im_hsv = cv.inRange(im_hsv, lows, highs)
    return im_hsv

'''
Draw lines to indicate where the battens are

@param im the image
@return the lines that indicate edges in the image
'''
def edge_detect(im):
    #convert to grey scale and blur
    im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)
    #edge detection
    im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)
    #Hough Line Transform (image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
    lines = cv.HoughLinesP(im_edges, 1, np.pi / 180, 10, None, 100, 20)
    return lines

'''

Main

'''
if __name__=='__main__':
    
    #command line arguments
    parser = argparse.ArgumentParser(description='Test to detect wood using color')
    parser.add_argument('-v', help='Video file', default=0, type=str)
    parser.add_argument('-c', help='Camera', action='store_true')
    args = parser.parse_args()

    #open video
    if(args.c):
        vid = 0
    else:
        vid = args.v
    cap = cv.VideoCapture(vid)
    if(cap.isOpened() == False):
        print("Video failed to open")

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
            #filter out colors
            frame_det = color_detect(frame)
            #convert to bgr
            frame_det = cv.cvtColor(frame_det, cv.COLOR_GRAY2BGR)
            #find and draw lines
            lines = edge_detect(frame)
            if lines is not None:
                for line in lines:
                    for x1,y1,x2,y2 in line:
                        cv.line(frame_det,(x1,y1),(x2,y2),(255,0,0),5)

            #show original image vs processed image
            cv.imshow("Original", frame)
            cv.imshow("Detected", frame_det)
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