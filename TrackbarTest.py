import cv2 as cv
import numpy as np

'''

global variables

'''
image = cv.imread("Images/test_image2.jpg")
title_window = 'Trackbar Test'
cv.namedWindow(title_window)
mb_ksize = 5
bf_dsize = 7
bf_scolor = 75
bf_sspace = 75
thresh1 = 0
thresh2 = 200
hl_rho = 1
hl_theta = np.pi / 180
hl_thresh = 5
hl_minLineLen = 50
hl_maxLineGap = 10
contour_mode = 0
contour_method = 0
contour_select = 0

'''

Edge Detection for Battens

'''
def batten_lines(img):
    global mb_ksize, bf_dsize, bf_scolor, bf_sspace, thresh1, thresh2, hl_rho, hl_theta, hl_thresh, hl_minLineLen, hl_maxLineGap

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, mb_ksize)
    blur = cv.bilateralFilter(gray, bf_dsize, bf_scolor, bf_sspace)
    edges = cv.Canny(blur, thresh1, thresh2)
    lines = cv.HoughLinesP(edges, hl_rho, hl_theta, hl_thresh, hl_minLineLen, hl_maxLineGap)
    if lines is not None:
        for line in lines:
            cv.line(img,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
    cv.imshow("Batten Lines", img)

'''

Edge Detection for Batten Stacks

'''
def batten_bounds(img):
    global contour_mode, contour_method, contour_select, bf_dsize, bf_scolor, bf_sspace, thresh1, thresh2
    mode = cv.RETR_TREE
    if contour_mode == 0:
        mode = cv.RETR_LIST
        
    method = cv.CHAIN_APPROX_SIMPLE
    if contour_method == 0:
        method = cv.CHAIN_APPROX_NONE
  
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    blur = cv.bilateralFilter(gray, bf_dsize, bf_scolor, bf_sspace)
    edges = cv.Canny(blur, thresh1, thresh2)
    contours, hierarchy = cv.findContours(edges, mode, method)
    
    if(contour_select == 0):
        cv.drawContours(img, contours, -1, (0,255,0),1)
    elif len(contours) > 0:
        areas = [cv.contourArea(c) for c in contours]
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0),1)
    cv.imshow("Batten Bounds", img)
    
'''

Trackbar Setup

'''
def tb_cb():
    global image
    img1 = np.copy(image)
    img2 = np.copy(image)
    batten_lines(img1)
    batten_bounds(img2)

def tb_cb_mb(val):
    global mb_ksize
    mb_ksize = val
    tb_cb()
mb_ksize_max = 20
mb_tb = "Median Blur - Kernal Size"
cv.createTrackbar(mb_tb, title_window, mb_ksize, mb_ksize_max, tb_cb_mb)

def tb_cb_bf_ds(val):
    global bf_dsize
    bf_dsize = val
    tb_cb()
bf_dsize_max = 20
bf_ds_tb = "Bilateral Filter - Pixel Neighbourhood Diameter"
cv.createTrackbar(bf_ds_tb, title_window, bf_dsize, bf_dsize_max, tb_cb_bf_ds)

def tb_cb_bf_sc(val):
    global bf_scolor
    bf_scolor = val
    tb_cb()
bf_scolor_max = 255
bf_sc_tb = "Bilateral Filter - Filter Sigma in Color Space"
cv.createTrackbar(bf_sc_tb, title_window, bf_scolor, bf_scolor_max, tb_cb_bf_sc)

def tb_cb_bf_ss(val):
    global bf_sspace
    bf_sspace = val
    tb_cb()
bf_sspace_max = 255
bf_ss_tb = "Bilateral Filter - Filter Sigma in Coordinate Space"
cv.createTrackbar(bf_ss_tb, title_window, bf_sspace, bf_sspace_max, tb_cb_bf_ss)

def tb_cb_thresh1(val):
    global thresh1
    thresh1 = val
    tb_cb()
thresh1_max = 255
thresh1_tb = "Canny Edge Detection - First Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh1_tb, title_window, thresh1, thresh1_max, tb_cb_thresh1)

def tb_cb_thresh2(val):
    global thresh2
    thresh2 = val
    tb_cb()
thresh2_max = 255
thresh2_tb = "Canny Edge Detection - Second Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh2_tb, title_window, thresh2, thresh2_max, tb_cb_thresh2)

def tb_cb_rho(val):
    global hl_rho
    hl_rho = val
    tb_cb()
hl_rho_max = 10
hl_rho_tb = "Hugh Lines - Resolution of \'r\' Parameter in Pixels"
cv.createTrackbar(hl_rho_tb, title_window, hl_rho, hl_rho_max, tb_cb_rho)

def tb_cb_theta(val):
    global hl_theta
    hl_theta = np.pi / val
    tb_cb()
hl_theta_max = 360
hl_theta_tb = "Hugh Lines - Resolution of \'theta\' Parameter in Radians"
cv.createTrackbar(hl_theta_tb, title_window, 180, hl_theta_max, tb_cb_theta)

def tb_cb_thresh(val):
    global hl_thresh
    hl_thresh = val
    tb_cb()
hl_thresh_max = 20
hl_thresh_tb = "Hugh Lines - Minimum Number of Intersections to Detect a Line"
cv.createTrackbar(hl_thresh_tb, title_window, hl_thresh, hl_thresh_max, tb_cb_thresh)

def tb_cb_mll(val):
    global hl_minLineLen
    hl_minLineLen = val
    tb_cb()
hl_minLineLen_max = 1000
hl_minLineLen_tb = "Hugh Lines - Minimum Length of a Line in Pixels"
cv.createTrackbar(hl_minLineLen_tb, title_window, hl_minLineLen, hl_minLineLen_max, tb_cb_mll)

def tb_cb_mlg(val):
    global hl_maxLineGap
    hl_maxLineGap = val
    tb_cb()
hl_maxLineGap_max = 1000
hl_maxLineGap_tb = "Hugh Lines - Maximum Gap of a Line in Pixels"
cv.createTrackbar(hl_maxLineGap_tb, title_window, hl_maxLineGap, hl_maxLineGap_max, tb_cb_mlg)

def tb_cb_mode(val):
    global contour_mode
    contour_mode = val
    tb_cb()
contour_mode_max = 1
contour_mode_tb = "Contour Mode - RETR_LIST or RETR_TREE"
cv.createTrackbar(contour_mode_tb, title_window, contour_mode, contour_mode_max, tb_cb_mode)

def tb_cb_method(val):
    global contour_method
    contour_method = val
    tb_cb()
contour_method_max = 1
contour_method_tb = "Contour Method - CHAIN_APPROX_NONE or CHAIN_APPROX_SIMPLE"
cv.createTrackbar(contour_method_tb, title_window, contour_method, contour_method_max, tb_cb_method)

def tb_cb_select(val):
    global contour_select
    contour_select = val
    tb_cb()
contour_select_max = 1
contour_select_tb = "Contour Select - Draw all contours or bounding Rectangles"
cv.createTrackbar(contour_select_tb, title_window, contour_select, contour_select_max, tb_cb_select)


    
    
'''

Main

'''

if image is None:
    print("Error reading image file")
else:
    blank = np.copy(image) * 0
    cv.imshow(title_window, blank)
    tb_cb()
    cv.waitKey(0)
    cv.destroyAllWindows()
    
