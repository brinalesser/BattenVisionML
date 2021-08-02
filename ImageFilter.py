
import cv2 as cv
import numpy as np
import cython

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

cap = cv.VideoCapture(0) #0 is for raspberry pi usb camera

if(cap.isOpened() == False):
    print("failed to open camera")

while(cap.isOpened()):
    ret, frame = cap.read()
    cv.imshow("Original", frame)
    if(ret):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("Original",frame)
        new_frame = process_image(frame)
        cv.imshow("New",new_frame)
    else:
        print("failed to read frame")
        break