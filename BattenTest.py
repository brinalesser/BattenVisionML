'''
This program was an attempt to detect a stack of battens,
then identify individual battens within the stack.

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''
import cv2 as cv
import numpy as np

#bgr color range for battens
b_low = 130
b_high = 180
g_low = 130
g_high = 190
r_low = 150
r_high = 200

#hsv color range for battens
h_low = 0
h_high = 110
s_low = 0
s_high = 110
v_low = 110
v_high = 210

'''
Find the region of interest that the stack resides in
@param im a frame including a stack of battens
@return a frame including only the stack
'''
def detect_stack(im):
    ret = im.copy()
    
    #convert frame to hsv
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)

    #filter out colors outside the range
    lower_hsv = np.array([h_low, s_low, v_low])
    higher_hsv = np.array([h_high, s_high, v_high])
    mask = cv.inRange(hsv, lower_hsv, higher_hsv)
    hsv_filter = cv.bitwise_and(frame, frame, mask=mask)
    
    #blur the image and find the contours
    blur = cv.medianBlur(hsv_filter, 5)
    blur2 = cv.bilateralFilter(blur, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=100, threshold2=200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    #find the area of each contour
    areas = [cv.contourArea(c) for c in contours]    
    
    
    flag = False
    x = 0
    y = 0
    w = 0
    h = 0
    #find the largest contour that is the right color
    while not flag and len(areas) > 0:
        #get the bounding rectangle of the contour with the largest area
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        bounded = np.copy(im[y:y+h,x:x+w])

        #find the colors within the rectangle as a histogram
        bgr_planes = cv.split(bounded)       
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)

        #find the most common colors
        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)

        #if the dominant colors are within the range, then use that contour
        if( idx_b > b_low and idx_b < b_high and \
            idx_g > g_low and idx_g < g_high and \
            idx_r > r_low and idx_r < r_high ):
            flag = True
        #otherwise remove that contour and go to the next one
        else:
            areas.pop(idx)
    #return the ROI including the stack
    stack = np.copy(ret[y:y+h,x:x+w])
    cv.imshow("Ret",stack) 
    if flag:
        return ret[y:y+h,x:x+w]
    else:
        return []
    
'''
Find the locations of the battens within the frame
@param im a frame of a stack of battens
@return the lines that show the locations of the battens
'''    
def detect_battens(im):
    #convert to grayscale and blur the image
    ret = im.copy()
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.bilateralFilter(gray, 7, 75, 75)
    
    #edge detection
    edges = cv.Canny(image=blur, threshold1=0, threshold2=255)
    
    #find the straight lines for the edges and return them
    lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/90, threshold=2, minLineLength=200, maxLineGap=40)
    if lines is not None:
        for line in lines:
            cv.line(ret,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
    return ret
    
'''
Main
'''
if __name__=='__main__':
    #open the video
    count = 0
    cap = cv.VideoCapture("./Videos/test_vid.mp4")
    if(cap.isOpened() == False):   
        print("Video failed to open")
    pause = False
    #process video frame by frame
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if(ret):
            #Show original frame
            cv.imshow("Frame",frame)
            #Get stack ROI and show it
            stack = detect_stack(frame.copy())
            if len(stack) > 0:
                cv.imshow("Stack", stack)
                #Enlarge the frame, then get the batten lines and show them
                width = int(stack.shape[1] * 2)
                height = int(stack.shape[0] * 2)
                dim = (width, height)
                resized = cv.resize(stack, dim, interpolation=cv.INTER_AREA)
                battens = detect_battens(resized.copy())
                cv.imshow("Battens", battens)
        else:
            print("Failed to read frame")
            break
        #Control keys
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

