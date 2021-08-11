'''
This program was an attempt to process frames pixel by pixel.
-> THIS IS TOO SLOW IF USING PYTHON so I attempted to use cython,
but it's easier and more efficient to just use C or C++

@author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 8/11/21
'''
import cv2 as cv
import numpy as np
import cython

'''
cython function to process a frame pixel by pixel

@param thresh the grayscale threshold
@param im a grayscale image
@return the filtered image 
'''
@cython.boundscheck(False)
cpdef unsigned char[:, :] process_image(int thresh, unsigned char [:, :] im):
    cdef int x, y, w, h
    h = im.shape[0]
    w = im.shape[1]
    
    for y in range(0,h):
        for x in range(0,w):
            im[y, x] = 255 if im[y, x] >= thresh else 0
            '''
            b, g, r = frame[y,x]
            if b < 75 or g > 15 or r < 130:
                m = (np.mean((b,g,r),dtype=np.uint8))
                im[y,x] = [m, m, m]
                '''
    return im

'''
main
'''
cap = cv.VideoCapture(0) #0 is for raspberry pi usb camera (replace with filename for video)

if(cap.isOpened() == False):
    print("failed to open camera")

while(cap.isOpened()):
    #get and show original frame
    ret, frame = cap.read()
    cv.imshow("Original", frame)
    if(ret):
        #convert frame to grayscale and display
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("Grayscale",frame)
        #process frame and display
        new_frame = process_image(frame)
        cv.imshow("Processed",new_frame)
    else:
        print("failed to read frame")
        break
