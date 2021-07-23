import cv2 as cv
import numpy as np

b_low = 130
b_high = 180
g_low = 130
g_high = 190
r_low = 150
r_high = 200

def detect_stack(im):
    #TODO
    #NEED TO FIND A WAY TO REMOVE BACKGROUND AND ONLY LOOK AT BATTENS
    #MAYBE USE HSV OR OTHER COLOR FILTER WITH BITMASK
    ret = im.copy()
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    blur2 = cv.bilateralFilter(blur, 7, 75, 75)
    edges = cv.Canny(image=blur2, threshold1=100, threshold2=200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    areas = [cv.contourArea(c) for c in contours]    
    
    flag = False
    x = 0
    y = 0
    w = 0
    h = 0
    while not flag and len(areas) > 0:
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        bounded = np.copy(im[y:y+h,x:x+w])

        bgr_planes = cv.split(bounded)       
        b_hist = cv.calcHist(bgr_planes, [0], None, [256], (0, 256), accumulate=False)
        g_hist = cv.calcHist(bgr_planes, [1], None, [256], (0, 256), accumulate=False)
        r_hist = cv.calcHist(bgr_planes, [2], None, [256], (0, 256), accumulate=False)

        idx_b = np.argmax(b_hist)
        idx_g = np.argmax(g_hist)
        idx_r = np.argmax(r_hist)

        if( idx_b > b_low and idx_b < b_high and \
            idx_g > g_low and idx_g < g_high and \
            idx_r > r_low and idx_r < r_high ):
            flag = True
        else:
            areas.pop(idx)

    if flag:
        return ret[y:y+h,x:x+w]
    else:
        return []
    
def detect_battens(im):
    ret = im.copy()
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.bilateralFilter(gray, 7, 75, 75)
    edges = cv.Canny(image=blur, threshold1=0, threshold2=150)
    lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/90, threshold=2, minLineLength=100, maxLineGap=20)
    if lines is not None:
        for line in lines:
            cv.line(ret,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
    return ret
    
if __name__=='__main__':
    count = 0
    cap = cv.VideoCapture("./Videos/vid1.mp4")
    if(cap.isOpened() == False):   
        print("Video failed to open")
    pause = False
    while(cap.isOpened()):
        if not pause:
            ret, frame = cap.read()
        if(ret):
            cv.imshow("Frame",frame)
            stack = detect_stack(frame.copy())
            if len(stack) > 0:
                cv.imshow("Stack", stack)
                width = int(stack.shape[1] * 2)
                height = int(stack.shape[0] * 2)
                dim = (width, height)
                resized = cv.resize(stack, dim, interpolation=cv.INTER_AREA)
                battens = detect_battens(resized.copy())
                cv.imshow("Battens", battens)
        else:
            print("Failed to read frame")
            break
        key = cv.waitKey(1)
        if(key == 27 or key == 113): #esc or q
            break
        elif(key == 115): #s
            cv.imwrite("Battens"+str(count)+".jpg", battens)
            count += 1
        elif(key == 112): #p
            pause = not pause
        elif(key != -1):
            print(key)

