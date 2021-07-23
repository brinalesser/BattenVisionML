import cv2 as cv
import numpy as np
import time

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

def detect(im):
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=150)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    areas = [cv.contourArea(c) for c in contours]
    
    
    for contour in contours:
        img = np.copy(im)
        x,y,w,h = cv.boundingRect(contour)
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
        cv.imshow("Img",img)
        
        bounded = im[y:y+h,x:x+w]
        bgr_planes = cv.split(bounded)     
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)

        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)
        
        print("Blue Max Idx: "+ str(idx_b) + ", Blue Max: " + str(b_hist[idx_b]))
        print("Green Max Idx: "+ str(idx_g) + ", Green Max: " + str(g_hist[idx_g]))
        print("Red Max Idx: "+ str(idx_r) + ", Red Max: " + str(r_hist[idx_r]))
        
        while cv.waitKey(0) == -1:
            pass
    
    '''
    found = False
    count = 0
    while not found:
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        
        img = np.copy(im)
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
        cv.imshow("Img",img)
        
        bounded = im[y:y+h,x:x+w]
        bgr_planes = cv.split(bounded)     
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)

        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)

        if(idx_b > b_low and idx_b < b_high and idx_g > g_low and idx_g < g_high and idx_r > r_low and idx_r < r_high):
            found = True
            print("Blue Max Idx: "+ str(idx_b) + ", Blue Max: " + str(b_hist[idx_b]))
            print("Green Max Idx: "+ str(idx_g) + ", Green Max: " + str(g_hist[idx_g]))
            print("Red Max Idx: "+ str(idx_r) + ", Red Max: " + str(r_hist[idx_r]))
        elif(len(areas) > 2):
            areas.pop(idx)
        else:
            print("Not found")
            break
'''
    
cap = cv.VideoCapture(0)
if(cap.isOpened() == False):
    print("Video failed to open")

paused = False
while(cap.isOpened()):
    if not paused:
        ret, frame = cap.read()
    if(ret):
        bounded_frame = detect_frame(frame.copy())
        detect(bounded_frame)
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