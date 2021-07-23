import cv2 as cv
import numpy as np
import time

i = 0
def detect(frame):
    global i
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur1 = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur1, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    
    im_c = np.copy(frame)
    cv.drawContours(im_c, contours, -1, (0, 255, 0), 3)
    cv.imwrite("contours" + str(i) + ".jpg",im_c)
    
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    x,y,w,h = cv.boundingRect(contours[idx])
    cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
    cv.imwrite("bounding_rect" + str(i) + ".jpg",frame)
    
    i += 1
    time.sleep(5)
    
cap = cv.VideoCapture(0)
if(cap.isOpened() == False):
    print("Video failed to open")

paused = False
while(cap.isOpened()):
    if not paused:
        ret, frame = cap.read()
    if(ret):
        detect(frame.copy())
    else:
        print("error reading frame")
            
    key = cv.waitKey(1)
    if(key == 27 or key == 113): #esc or q
        break
    elif(key == 115): #s
        paused = False
    elif(key == 112): #p
        paused = True
    elif(key != -1):
        print(key)