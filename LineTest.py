import cv2 as cv
import numpy as np
import copy
import math
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

MAX_DIST = 50

def get_lines(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blur1 = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur1, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=255, apertureSize=3, L2gradient=False)
        
    return cv.HoughLinesP(edges, 1, np.pi/180, 1, MAX_DIST, 1)
    
def merge_lines(lines):
    midpoints = []
    if lines is not None:
        for line in lines:
            mid = [(line[0][0] + line[0][2])/2, (line[0][1] + line[0][3])/2]
            midpoints.append(mid)
      
    points = []
    groups = []
    for p1 in midpoints:
        x1 = p1[0]
        y1 = p1[1]
        #check which groups in the sorted points have points that are close to the point
        for i in range(len(points)):
            for j in range(len(points[i][0])):
                x2 = points[i][0][j]
                y2 = points[i][1][j]
                if math.sqrt(pow(x1-x2,2)+pow(y1-y2,2)) < MAX_DIST: #distance formula
                    groups.append(i)
                    break
                
        #point is not added to any group - make a new group
        if len(groups) < 1:
            points.append([[x1],[y1]])
        
        #point is added to group(s)
        else:
            idx = groups[0] #first group
            points[idx][0].append(x1)
            points[idx][1].append(y1)
            groups.pop(0)
            #merge all groups that have a point close to the new point into the first group
            while(len(groups) > 0):
                points[idx][0] += points[groups[0]][0]
                points[idx][1] += points[groups[0]][1]
                points.pop(groups[0])
                groups.pop(0)
        
    #draw lines
    lines = []
    for p in points: #p is a group of points that makes up one line
        x = p[0]
        y = p[1]
        plt.scatter(x, y)
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        #plt.plot(x,p(x),"r--")
        #plt.show()
        lines.append([x, p(x)])
    for line in lines:
        plt.plot(line[0],line[1],"r--")
    plt.show()
        
    '''
        n = len(x)
        xy_sum = 0
        xx_sum = 0
        for i in range(n):
            xy_sum += x[i] * y[i]
            xx_sum += x[i] ** 2
            
        a = (((n*xy_sum) - (sum(x)*sum(y))) / ((n*xx_sum) - pow(sum(x),2)))
        b = ((sum(y) - a*sum(x)) / n)
        lines.append((a, b)) #y = ax + b
        '''
    return lines

def get_rect(img):
    ret = copy.deepcopy(img)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    lower_hsv = np.array([0, 0, 110])
    higher_hsv = np.array([180, 110, 210])
    mask = cv.inRange(hsv, lower_hsv, higher_hsv)
    
    blur1 = cv.medianBlur(mask, 5)
    blur2 = cv.bilateralFilter(blur1, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=0, threshold2=45, apertureSize=3, L2gradient=False)

    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    areas = [cv.contourArea(c) for c in contours]   
    idx = np.argmax(areas)
    return cv.boundingRect(contours[idx])

if __name__=='__main__':

    count = 0
    cap = cv.VideoCapture("./Videos/test_vid.mp4")
    if(cap.isOpened() == False):   
        print("Video failed to open")
    pause = False
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if(ret):
            im_lines = copy.deepcopy(frame)
            lines = get_lines(im_lines)
            merged_lines = merge_lines(lines)
            
            #if merged_lines is not None:
                #for line in merged_lines:
                    #cv.line(im_lines,(0,0),(x, p(x),(255,0,0),1))
            '''
            cv.imshow("Lines", im_lines)
            im_rect = copy.deepcopy(frame)
            x,y,w,h = get_rect(im_rect)
            cv.rectangle(im_rect, (x, y),(x+w, y+h), (0,0,255), 3)
            cv.imshow("Image",im_rect)
            '''
        else:
            print("Failed to read frame")
            break
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
    
    cv.destroyAllWindows()
    