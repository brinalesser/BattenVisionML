import cv2 as cv
import numpy as np

'''

Trackbar Callback

'''
def tb_cb():
    img1 = np.copy(image)
    img2 = np.copy(image)
    batten_lines(img1)
    batten_bounds(img2)

'''

Trackbar Setup

'''
title_window = "Trackbar Test"

def tb_cb_mb(val):
    mb_ksize = val
    tb_cb()
mb_ksize = 5
mb_ksize_max = 20
mb_tb = "Median Blur - Kernal Size"
cv.createTrackbar(mb_tb, title_window, 5, mb_ksize_max, tb_cb_mb)

def tb_cb_bf_ds(val):
    bf_dsize = val
    tb_cb()
bf_dsize = 7
bf_dsize_max = 20
bf_ds_tb = "Bilateral Filter - Pixel Neighbourhood Diameter"
cv.createTrackbar(bf_ds_tb, title_window, 7, bf_dsize_max, tb_cb_bf_ds)

def tb_cb_bf_sc(val):
    bf_scolor = val
    tb_cb()
bf_scolor = 75
bf_scolor_max = 255
bf_sc_tb = "Bilateral Filter - Filter Sigma in Color Space"
cv.createTrackbar(bf_sc_tb, title_window, 75, bf_scolor_max, tb_cb_bf_sc)

def tb_cb_bf_ss(val):
    bf_sspace = val
    tb_cb()
bf_sspace = 75
bf_sspace_max = 255
bf_ss_tb = "Bilateral Filter - Filter Sigma in Coordinate Space"
cv.createTrackbar(bf_ss_tb, title_window, 75, bf_sspace_max, tb_cb_bf_ss)

def tb_cb_thresh1(val):
    thresh1 = val
    tb_cb()
thresh1 = 0
thresh1_max = 255
thresh1_tb = "Canny Edge Detection - First Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh1_tb, title_window, 0, thresh1_max, tb_cb_thresh1)

def tb_cb_thresh2(val):
    thresh2 = val
    tb_cb()
thresh2 = 200
thresh2_max = 255
thresh2_tb = "Canny Edge Detection - Second Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh2_tb, title_window, 200, thresh2_max, tb_cb_thresh2)

def tb_cb_rho(val):
    hl_rho = val
    tb_cb()
hl_rho = 1
hl_rho_max = 10
hl_rho_tb = "Hugh Lines - Resolution of \'r\' Parameter in Pixels"
cv.createTrackbar(hl_rho_tb, title_window, 1, hl_rho_max, tb_cb_rho)

def tb_cb_theta(val):
    hl_theta = np.pi / val
    tb_cb()
hl_theta = np.pi / 180
hl_theta_max = 360
hl_theta_tb = "Hugh Lines - Resolution of \'theta\' Parameter in Radians"
cv.createTrackbar(hl_theta_tb, title_window, 180, hl_theta_max, tb_cb_theta)

def tb_cb_thresh(val):
    hl_thresh = val
    tb_cb()
hl_thresh = 5
hl_thresh_max = 20
hl_thresh_tb = "Hugh Lines - Minimum Number of Intersections to Detect a Line"
cv.createTrackbar(hl_thresh_tb, title_window, 5, hl_thresh_max, tb_cb_thresh)

def tb_cb_mll(val):
    hl_minLineLen = val
    tb_cb()
hl_minLineLen = 100
hl_minLineLen_max = 1000
hl_minLineLen_tb = "Hugh Lines - Minimum Length of a Line in Pixels"
cv.createTrackbar(hl_minLineLen_tb, title_window, 100, hl_minLineLen_max, tb_cb_mll)

def tb_cb_mlg(val):
    hl_maxLineGap = val
    tb_cb()
hl_maxLineGap = 100
hl_maxLineGap_max = 1000
hl_maxLineGap_tb = "Hugh Lines - Maximum Gap of a Line in Pixels"
cv.createTrackbar(hl_maxLineGap_tb, title_window, 100, hl_maxLineGap_max, tb_cb_mlg)

def tb_cb_mode(val):
    contour_mode = val
    tb_cb()
contour_mode = 0
contour_mode_max = 1
contour_mode_tb = "Contour Mode - RETR_LIST or RETR_TREE"
cv.createTrackbar(contour_mode_tb, title_window, 0, contour_mode_max, tb_cb_mode)

def tb_cb_method(val):
    contour_method = val
    tb_cb()
contour_method = 0
contour_method_max = 1
contour_method_tb = "Contour Method - CHAIN_APPROX_NONE or CHAIN_APPROX_SIMPLE"
cv.createTrackbar(contour_method_tb, title_window, 0, contour_method_max, tb_cb_method)

def tb_cb_select(val):
    contour_select = val
    tb_cb()
contour_select = 0
contour_select_max = 1
contour_select_tb = "Contour Method - CHAIN_APPROX_NONE or CHAIN_APPROX_SIMPLE"
cv.createTrackbar(contour_select_tb, title_window, 0, contour_select_max, tb_cb_select)

'''

Edge Detection for Battens

'''
def batten_lines(im):
    
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, mb_ksize)
    blur2 = cv.bilateralFilter(blur, bf_dsize, bf_scolor, bf_sspace)
    edges = cv.Canny(blur2, thresh1, thresh2)
    
    lines = cv.HughLinesP(edges, hl_rho, hl_theta, hl_thresh, hl_minLineLen, hl_maxLineGap)
    if lines is not None:
        for line in lines:
            cv.line(im, (line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
        cv.imshow("Batten Lines", im)

'''

Edge Detection for Batten Stacks

'''
def batten_bounds(im):
    
    mode = cv.RETR_TREE
    if contour_mode == 0:
        mode = cv.RETR_LIST
        
    method = CHAIN_APPROX_SIMPLE
    if contour_method == 0:
        method = cv.CHAIN_APPROX_NONE
  
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY) 
    blur = cv.bilateralFilter(gray, bf_dsize, bf_scolor, bf_sspace)
    edges = cv.Canny(blur, thresh1, thresh2)
    contours, hierarchy = cv.findContours(edges, mode, method)
    
    if(contour_select == 0):
        cv.drawContours(im, contours, -1, (0,255,0),1)
        cv.imshow("Batten Bounds", im)
    elif len(contours) > 0:
        areas = [cv.contourArea(c) for c in contours]
        idx = np.argmax(areas)
        x,y,w,h = boundingRect(contours[idx])
        cv.rectangle(im, (x,y), (x+w,y+h), (0,255,0),1)
        cv.imshow("Batten Bounds", im)
        
    
'''

Main

'''
image = cv.imread("test_image2.jpg")
if image is None:
    print("Error reading image file")

cv.namedWindow(title_window)
cv.waitKey(0)
cv.destroyAllWindows()