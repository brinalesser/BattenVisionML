'''
This program was an attempt to isolate the dominant colors in a stack of battens.

@author Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified  4/2021
'''

import cv2 as cv
import numpy as np

'''
#Data dump:

Blue Max Idx: 156, Blue Max: [711.]
Blue Max Idx: 162, Blue Max: [1404.]
Blue Max Idx: 161, Blue Max: [1623.]
Blue Max Idx: 144, Blue Max: [1202.]
Blue Max Idx: 140, Blue Max: [1873.]
Blue Max Idx: 145, Blue Max: [5494.]
Blue Max Idx: 158, Blue Max: [2575.]
Blue Max Idx: 130, Blue Max: [1428.]
Blue Max Idx: 130, Blue Max: [742.]
Blue Max Idx: 169, Blue Max: [529.]
Blue Max Idx: 175, Blue Max: [984.]

Green Max Idx: 185, Green Max: [778.]
Green Max Idx: 170, Green Max: [1424.]
Green Max Idx: 174, Green Max: [1650.]
Green Max Idx: 150, Green Max: [1235.]
Green Max Idx: 153, Green Max: [1806.]
Green Max Idx: 158, Green Max: [6499.]
Green Max Idx: 255, Green Max: [2855.]
Green Max Idx: 138, Green Max: [1891.]
Green Max Idx: 146, Green Max: [780.]
Green Max Idx: 184, Green Max: [627.]
Green Max Idx: 166, Green Max: [1469.]

Red Max Idx: 192, Red Max: [1225.]
Red Max Idx: 196, Red Max: [1613.]
Red Max Idx: 195, Red Max: [2193.]
Red Max Idx: 157, Red Max: [1930.]
Red Max Idx: 168, Red Max: [1323.]
Red Max Idx: 163, Red Max: [6467.]
Red Max Idx: 255, Red Max: [28286.]
Red Max Idx: 160, Red Max: [1776.]
Red Max Idx: 152, Red Max: [639.]
Red Max Idx: 195, Red Max: [786.]
Red Max Idx: 185, Red Max: [1341.]

'''

'''
#Trackbars to tune in real time

title_window = 'Trackbars'
cv.namedWindow(title_window)
b_low = 95
b_high = 110
g_low = 170
g_high = 195
r_low = 210
r_high = 220
bgr_max = 255


def tb_cb_bl(val):#blue low
    global b_low
    if val < b_high:
        b_low = val
    else:
        b_low = b_high
def tb_cb_gl(val):#green low
    global g_low
    if val < g_high:
        g_low = val
    else:
        g_low = g_high
def tb_cb_rl(val):#red low
    global r_low
    if val < r_high:
        r_low = val
    else:
        r_low = r_high
def tb_cb_bh(val):#blue high
    global b_high
    if val > b_low:
        b_high = val
    else:
        b_high = b_low
def tb_cb_gh(val):#green high
    global g_high
    if val > g_low:
        g_high = val
    else:
        g_high = g_low
def tb_cb_rh(val):#red high
    global r_high
    if val > r_low:
        rhigh = val
    else:
        r_high = r_low

cv.createTrackbar("Blue Low Threshold", title_window, b_low, bgr_max, tb_cb_bl)
cv.createTrackbar("Blue High Threshold", title_window, b_high, bgr_max, tb_cb_bh) 
cv.createTrackbar("Green Low Threshold", title_window, g_low, bgr_max, tb_cb_gl)
cv.createTrackbar("Green High Threshold", title_window, g_high, bgr_max, tb_cb_gh)
cv.createTrackbar("Red Low Threshold", title_window, r_low, bgr_max, tb_cb_rl)
cv.createTrackbar("Red High Threshold", title_window, r_high, bgr_max, tb_cb_rh)

'''

'''
Detect region of interest
@param frame the current frame
@return the frame cropped to the region of interest
'''
def detect_frame(frame):
    #blur and convert to grayscale
    img = cv.medianBlur(frame, 5)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #binary threshold to isolate white background
    ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
    #find contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #get largest contour
    areas = [cv.contourArea(c) for c in contours]
    idx = np.argmax(areas)
    #draw rectangle around largest contour
    x,y,w,h = cv.boundingRect(contours[idx])
    cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
    cv.imshow("Frame", frame)
    #return the region inside the largest contour
    return frame[y+15:y+h-15,x+15:x+w-15]

'''
Detect the dominant colors in an image and display as a histogram
@param im the image
'''
def detect(im):
    #convert to grayscale and blur
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur, 7, 75, 75)
    #get edges
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    #get contours
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #get area of each contour
    areas = [cv.contourArea(c) for c in contours]
    #iterate through the contours
    for contour in contours:
        #get the bounding rectangle for the contour, then show it
        img = np.copy(im)
        x,y,w,h = cv.boundingRect(contour)
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
        cv.imshow("Img",img)
        
        #only look at the region inside the bounding rectangle
        bounded = im[y:y+h,x:x+w]
        #make a histogram of the blue, green, and red values present in the region
        bgr_planes = cv.split(bounded)     
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)

        #find the location of the highest peaks in the histograms (most dominant color)
        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)
        
        #print the dominant colors
        print("Blue Max Idx: "+ str(idx_b) + ", Blue Max: " + str(b_hist[idx_b]))
        print("Green Max Idx: "+ str(idx_g) + ", Green Max: " + str(g_hist[idx_g]))
        print("Red Max Idx: "+ str(idx_r) + ", Red Max: " + str(r_hist[idx_r]))
        
        #go to next contour after key is pressed
        while cv.waitKey(0) == -1:
            pass
    
#open the video
cap = cv.VideoCapture("./Videos/vid1.mp4")
if(cap.isOpened() == False):
    print("Video failed to open")

#process the video
paused = False
while(cap.isOpened()):
    if not paused:
        #get the next frame
        ret, frame = cap.read()
    if(ret):
        #bounded_frame = detect_frame(frame.copy())
        #detect(bounded_frame)
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
