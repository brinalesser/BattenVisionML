import cv2 as cv
import numpy as np
import math

title_window = "Trackbar Test"
def tb_cb(val):
    pass

mb_ksize = 5
mb_ksize_max = 20
mb_tb = "Median Blur - Kernal Size"
cv.createTrackbar(mb_tb, title_window, mb_ksize, mb_ksize_max, tb_cb)

bf_dsize = 7
bf_dsize_max = 20
bf_ds_tb = "Bilateral Filter - Pixel Neighbourhood Diameter"
cv.createTrackbar(bf_ds_tb, title_window, bf_dsize, bf_dsize_max, tb_cb)

bf_scolor = 75
bf_scolor_max = 255
bf_sc_tb = "Bilateral Filter - Filter Sigma in Color Space"
cv.createTrackbar(bf_sc_tb, title_window, bf_scolor, bf_scolor_max, tb_cb)

bf_sspace = 75
bf_sspace_max = 255
bf_ss_tb = "Bilateral Filter - Filter Sigma in Coordinate Space"
cv.createTrackbar(bf_ss_tb, title_window, bf_sspace, bf_sspace_max, tb_cb)

thresh1 = 0
thresh1_max = 255
thresh1_tb = "Canny Edge Detection - First Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh1_tb, title_window, thresh1, thresh1_max, tb_cb)

thresh2 = 200
thresh2_max = 255
thresh2_tb = "Canny Edge Detection - Second Threshold for Hysteresis Procedure"
cv.createTrackbar(thresh2_tb, title_window, thresh2, thresh1_max, tb_cb)

def batten_lines(im):
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, mb_ksize)
    blur2 = cv.bilateralFilter(blur, bf_dsize, bf_scolor, bf_sspace)
    edges = cv.Canny(blur2, thresh1, thresh2)
    return cv.HughLinesP(edges, hl_rho, hl_theta, hl_thresh, hl_minLineLen, hl_maxLineGap)

image = cv.imread("test_image2.jpg")
if image is None:
    print("Error reading image file")

cv.namedWindow(title_window)
cv.waitKey(0)
cv.destroyAllWindows()
