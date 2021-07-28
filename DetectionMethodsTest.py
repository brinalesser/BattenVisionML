'''
This program tests different ways to do feature and edge detection on images

Command Line (-m [N]) Options for different detection methods:
N =
0: Shows Hough Lines
1: Shows Harris Corner Detection
2: Shows contours
3: Shows goodFeaturesToTrack Feature Detection
4: Shows ORB (Oriented FAST and Rotated BRIEF) Feature Detection
5: Shows FAST Feature Detection

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''
import cv2 as cv
import numpy as np
from glob import glob
import os
import ntpath
import sys
import getopt
import matplotlib.pyplot as plt

'''
Gets all the .jpg files in a folder
@param the path to the files
@return an array of images, an array of the image filenames
'''
def get_all_images(pathToFiles):
    pathToFiles = pathToFiles + "/*.jpg"
    jpg_names = glob(pathToFiles)
    jpgs = []
    for file in jpg_names:
        im = cv.imread(file)
        jpgs.append(im)
    return jpgs, jpg_names
'''
Detection method 0: Using Canny Edge Detection and Hough Lines
@param im the image
@return the image with lines drawn at the edges
'''
detect0(im):
    #convert to grey scale and blur
    im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)
    #edge detection
    im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)
    #Hough Line Transform (image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
    lines = cv.HoughLinesP(im_edges, 1, np.pi / 180, 10, None, 200, 30)
    #blank image
    im_line = np.copy(im) * 0
    if lines is not None:
        for line in lines:
            cv.line(im_line,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(255,0,0),5)
        im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)
    return im_line
'''
Detection method 0: Using Harris Corner Detection
@param im the image
@return the image with circles indicating the corners
'''
def detect1(im):
    #convert to grayscale and float32s
    im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_gs = np.float32(im_gs)
    #find corners using Harris method, then dilate
    dst = cv.cornerHarris(im_gs, 2, 3, .04)
    dst = cv.dilate(dst, None)
    im[dst>0.01*dst.max()]=[0,0,255]
    return im
'''
Detection method 2: Using contours
@param im the image
@return the image with all contours drawn
'''
def detect2(im):
    #convert to grayscale and blur
    im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)
    #edge detection
    im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)
    #find contours and draw on returned image
    contours, hierarchy = cv.findContours(im_edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    cv.drawContours(im, contours, -1, (0, 255, 0), 3)
    return im
'''
Detection method 3: Using "good features to track" algorithm
@param im the image
@return the image with all contours drawn
'''
def detect3(im):
    #convert to grayscale
    im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    #find corners with good features to track
    corners = cv.goodFeaturesToTrack(im_gs, 25, 0.01, 10)
    corners = np.int0(corners)
    #draw circles at the corners and return
    for i in corners:
        x,y = i.ravel()
        cv.circle(im, (x,y),3,255,-1)
    return im
'''
Detection method 4: Match to training image with ORB and brute force matching
**Note** this could be done with SURF or SIFT instead of ORB, but those
are proprietary algorithms and have to be purchased somehow
@param im the image
@return the image and training image with matches drawn between the two
'''
def detect4(im):
    #convert both images to gray scale
    train = cv.imread('test.jpg')
    train_gs = cv.cvtColor(train, cv.COLOR_BGR2GRAY)
    query_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    #use ORB to find keypoints and descriptors for both images
    orb = cv.ORB_create()
    t_keypoints, t_descriptors = orb.detectAndCompute(train_gs, None)
    q_keypoints, q_descriptors = orb.detectAndCompute(query_gs, None)
    #Brute force matching
    matcher = cv.BFMatcher()
    matches = matcher.match(q_descriptors, t_descriptors)
    #draw matches between images on the returned image
    im = cv.drawMatches(frame, q_keypoints, train, t_keypoints, matches[:20], None)
    return im
'''
Detection method 5: Using fast feature detection
@param im the image
@return the image with keypoints drawn on it
'''
def detect5(im):
    #create a fast feature detector
    fast = cv.FastFeatureDetector_create()
    #find the keypoints in the image
    keypoints = fast.detect(im, None)
    #draw the keypoints on the returned image
    im = cv.drawKeypoints(im, keypoints, None, color=(255,0,0))
    return im

'''
Use different detection methods based on input
@param im the image
@param method which method to use
@return the image with the detection indicated on it
'''
def detect(im, method):
    if(method == 0):
        return detect0(im)
    elif(method == 1):
        return detect1(im)
    elif(method == 2):
        return detect2(im)
    elif(method == 3):
        return detect3(im)
    elif(method == 4):
        return detect4(im)
    elif(method == 5):
        return detect5(im)
    else:
        print("invalid detection method")
        return im
 
'''

Main

'''
if __name__=='__main__':

    #command line argument defaults
    inputfolder = './Images'
    outputfolder = './Images'
    singleFile = './Images/img1.jpg'
    method = 0

    #parse command line arguments
    args = sys.argv[1:]
    opts = "i:o:s:m:"
    longOpts = ["InputFolder", "OutputFolder", "SingleFile", "Method"]

    try:
        arguments, values = getopt.getopt(args, opts, longOpts)
        for arg, val in arguments:
            if arg in ("-s", "--SingleFile"):
                singleFile = val
            if arg in ("-i", "--InputFolder"):
                inputfolder = val
            if arg in ("-o", "--OutputFolder"):
                outputfolder = val
            if arg in ("-m", "--Method"):
    except getopt.error as err:
        print(str(err))

    if(singleFile):
        #Do detection method for a single file and display it
        im = cv.imread(singleFile)
        im_edges = detect(im, method)
        cv.imshow("Edge test", im_edges)

    else:
        #Do detection method for every jpg file in input folder
        jpgs, jpg_names = get_all_images(inputfolder)

        edges = []
        i = 0
        for jpg in jpgs:
            #find edges
            im_edges = detect(jpg, 0)
            #save as png
            name = ntpath.basename(os.path.splitext(jpg_names[i])[0])
            filename = outputfolder + "/" + name +'.png'
            cv.imwrite(filename, im_edges)
            i = i + 1            

    cv.waitKey(0)
    cv.destroyAllWindows()
