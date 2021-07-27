'''
Program to tune values to see the effects on edge detection

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''

import cv2 as cv
import numpy as np

#image to test with
image = cv.imread("Images/test_image2.jpg")

#window to hold the trackbars
tb_window = 'Trackbars'
title_window = 'Frame'
cv.namedWindow(tb_window)

#global variables for values that change with the trackbars
mb_ksize = 5
bf_dsize = 7
bf_scolor = 75
bf_sspace = 75
thresh1 = 0
thresh2 = 200
hl_rho = 1
hl_theta = np.pi / 180
hl_thresh = 5
hl_minLineLen = 100
hl_maxLineGap = 50
contour_mode = 0
contour_method = 0
contour_select = 0
L2gradient = 0
aperture_size = 3

'''
Edge detection for battens using TB values

@param img a frame with battens
'''
def batten_lines(img):
    #TB input
    global mb_ksize, bf_dsize, bf_scolor, bf_sspace, thresh1, thresh2, hl_rho, hl_theta, hl_thresh, hl_minLineLen, hl_maxLineGap, aperture_size, L2gradient
    #convert to grayscale and blur
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur1 = cv.medianBlur(gray, mb_ksize)
    blur2 = cv.bilateralFilter(blur1, bf_dsize, bf_scolor, bf_sspace)
    #TB input
    gradient = True
    if L2gradient == 0:
        gradient = False
    #edge detection
    edges = cv.Canny(image=blur2, threshold1=thresh1, threshold2=thresh2, apertureSize=aperture_size, L2gradient=gradient)
    #draw lines
    lines = cv.HoughLinesP(edges, hl_rho, hl_theta, hl_thresh, hl_minLineLen, hl_maxLineGap)
    if lines is not None:
        for line in lines:
            cv.line(img,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),1)
    #show image
    cv.imshow("Batten Lines", img)

'''
Edge detection for batten stacks using TB values

@param img a frame with battens
'''
def batten_bounds(img):
    #TB input
    global contour_mode, contour_method, contour_select, bf_dsize, bf_scolor, bf_sspace, thresh1, thresh2, aperture_size, L2gradient
    mode = cv.RETR_TREE
    if contour_mode == 0:
        mode = cv.RETR_LIST
    method = cv.CHAIN_APPROX_SIMPLE
    if contour_method == 0:
        method = cv.CHAIN_APPROX_NONE
    #convert to grayscale and blur
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    blur = cv.bilateralFilter(gray, bf_dsize, bf_scolor, bf_sspace)
    gradient = True
    if L2gradient == 0:
        gradient = False
    #edge detection and contours
    edges = cv.Canny(image=blur, threshold1=thresh1, threshold2=thresh2, apertureSize=aperture_size, L2gradient=gradient)
    contours, hierarchy = cv.findContours(edges, mode, method)
    
    if(contour_select == 0):
        #draw all contours
        cv.drawContours(img, contours, -1, (0,255,0),1)
    elif len(contours) > 0:
        #draw largest contour bounding rect
        areas = [cv.contourArea(c) for c in contours]
        idx = np.argmax(areas)
        x,y,w,h = cv.boundingRect(contours[idx])
        cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0),1)
    cv.imshow("Batten Bounds", img)
    
'''

Trackbar Setup

'''
#this is called whenever a trackbar is changed
def tb_cb(): 
    global image
    img1 = np.copy(image)
    img2 = np.copy(image)
    batten_lines(img1)
    batten_bounds(img2)
#Canny L2Gradient trackbar setup
def tb_cb_l2(val):
    global L2gradient
    L2gradient = val
    tb_cb()
L2gradient_max = 1
L2gradient_tb = "Canny Edge Detection - L2Gradient used or not"
cv.createTrackbar(L2gradient_tb, title_window, L2gradient, L2gradient_max, tb_cb_l2)    
#Canny aperture size trackbar setup
def tb_cb_as(val):
    global aperture_size
    if val % 2 != 1:
        val += 1
    if val < 3:
        val = 3
    aperture_size = val
    tb_cb()
aperture_size_max = 7
aperture_size_tb = "Canny Edge Detection - Aperture Size"
cv.createTrackbar(aperture_size_tb, title_window, aperture_size, aperture_size_max, tb_cb_as)    
#Median blur kernal size trackbar setup
def tb_cb_mb(val):
    global mb_ksize
    if val % 2 != 1:
        val += 1
    mb_ksize = val
    tb_cb()
mb_ksize_max = 20
mb_tb = "Median Blur - Kernal Size"
cv.createTrackbar(mb_tb, title_window, mb_ksize, mb_ksize_max, tb_cb_mb)
#bilateral filter diameter trackbar setup
def tb_cb_bf_ds(val):
    global bf_dsize
    bf_dsize = val
    tb_cb()
bf_dsize_max = 20
bf_ds_tb = "Bilateral Filter - Pixel Neighbourhood Diameter"
cv.createTrackbar(bf_ds_tb, title_window, bf_dsize, bf_dsize_max, tb_cb_bf_ds)
#bilateral filter color sigma value trackbar setup
def tb_cb_bf_sc(val):
    global bf_scolor
    bf_scolor = val
    tb_cb()
bf_scolor_max = 255
bf_sc_tb = "Bilateral Filter - Filter Sigma in Color Space"
cv.createTrackbar(bf_sc_tb, title_window, bf_scolor, bf_scolor_max, tb_cb_bf_sc)
#bilateral filter coordinate sigma value trackbar setup
def tb_cb_bf_ss(val):
    global bf_sspace
    bf_sspace = val
    tb_cb()
bf_sspace_max = 255
bf_ss_tb = "Bilateral Filter - Filter Sigma in Coordinate Space"
cv.createTrackbar(bf_ss_tb, title_window, bf_sspace, bf_sspace_max, tb_cb_bf_ss)
#Canny threshold 1 trackbar setup
def tb_cb_thresh1(val):
    global thresh1
    thresh1 = val
    tb_cb()
thresh1_max = 255
thresh1_tb = "Canny Edge Detection - First Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh1_tb, title_window, thresh1, thresh1_max, tb_cb_thresh1)
#Canny threshold 2 trackbar setup
def tb_cb_thresh2(val):
    global thresh2
    thresh2 = val
    tb_cb()
thresh2_max = 255
thresh2_tb = "Canny Edge Detection - Second Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh2_tb, title_window, thresh2, thresh2_max, tb_cb_thresh2)
#Hough Lines rho trackbar setup
def tb_cb_rho(val):
    global hl_rho
    hl_rho = val
    tb_cb()
hl_rho_max = 10
hl_rho_tb = "Hugh Lines - Resolution of \'r\' Parameter in Pixels"
cv.createTrackbar(hl_rho_tb, title_window, hl_rho, hl_rho_max, tb_cb_rho)
#Hough Lines theta trackbar setup
def tb_cb_theta(val):
    global hl_theta
    hl_theta = np.pi / val
    tb_cb()
hl_theta_max = 360
hl_theta_tb = "Hugh Lines - Divides Pi to Get Resolution of \'theta\' Parameter in Radians"
cv.createTrackbar(hl_theta_tb, title_window, 180, hl_theta_max, tb_cb_theta)
#Hough Lines threshold trackbar setup
def tb_cb_thresh(val):
    global hl_thresh
    hl_thresh = val
    tb_cb()
hl_thresh_max = 20
hl_thresh_tb = "Hugh Lines - Minimum Number of Intersections to Detect a Line"
cv.createTrackbar(hl_thresh_tb, title_window, hl_thresh, hl_thresh_max, tb_cb_thresh)
#Hough Lines minimum line length trackbar setup
def tb_cb_mll(val):
    global hl_minLineLen
    hl_minLineLen = val
    tb_cb()
hl_minLineLen_max = 1000
hl_minLineLen_tb = "Hugh Lines - Minimum Length of a Line in Pixels"
cv.createTrackbar(hl_minLineLen_tb, title_window, hl_minLineLen, hl_minLineLen_max, tb_cb_mll)
#Hough Lines maximum line gap trackbar setup
def tb_cb_mlg(val):
    global hl_maxLineGap
    hl_maxLineGap = val
    tb_cb()
hl_maxLineGap_max = 1000
hl_maxLineGap_tb = "Hugh Lines - Maximum Gap of a Line in Pixels"
cv.createTrackbar(hl_maxLineGap_tb, title_window, hl_maxLineGap, hl_maxLineGap_max, tb_cb_mlg)
#Contour mode trackbar setup
def tb_cb_mode(val):
    global contour_mode
    contour_mode = val
    tb_cb()
contour_mode_max = 1
contour_mode_tb = "Contour Mode - RETR_LIST or RETR_TREE"
cv.createTrackbar(contour_mode_tb, title_window, contour_mode, contour_mode_max, tb_cb_mode)
#Contour method trackbar setup
def tb_cb_method(val):
    global contour_method
    contour_method = val
    tb_cb()
contour_method_max = 1
contour_method_tb = "Contour Method - CHAIN_APPROX_NONE or CHAIN_APPROX_SIMPLE"
cv.createTrackbar(contour_method_tb, title_window, contour_method, contour_method_max, tb_cb_method)
#All contour vs bounding rectangle of largest contour trackbar setup
def tb_cb_select(val):
    global contour_select
    contour_select = val
    tb_cb()
contour_select_max = 1
contour_select_tb = "Contour Select - Draw All Contours or Bounding Rectangle of Largest Contour"
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
    
