'''
Object Detection Using Cascade Classifier

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt

'''
Detect battens and display bounding rectagles

@param im the image
@return the image with bounding rectangles drawn around the battens
'''
def find_objects(im):
    #convert to grayscale and equalize
    im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    im_gs = cv.equalizeHist(im_gs)

    #find battens using cascade classifier model
    found = batten_data.detectMultiScale(im_gs, minSize=(20,20))
    amount_found = len(found)

    #draw rectangle around battens
    if(amount_found != 0):
        for(x, y, w, h) in found:
            im = cv.rectangle(im, (x,y), ((x+h), (y+w)), (0,255,0), 4)
    return im

#command line option defaults

#folder containing cascade classifier model
classifierFolder = "Images/cascade"
#path to video to use
vidname = "Videos for ML/vid0.mp4"

args = sys.argv[1:]
opts = "v:c:r"
longOpts = ["VideoName", "ClassifierFolder", "RealTime"]

try:
    arguments, values = getopt.getopt(args, opts, longOpts)
    for arg, val in arguments:
        if arg in ("-v", "--VideoName"):
            vidname = val
        elif arg in ("-c", "--Classifier"):
            classifierFolder = val
        elif arg in ("-r", "--RealTime"):
            vidname = 0
except getopt.error as err:
    print(str(err))

#create model using cascade training data
batten_data = cv.CascadeClassifier(classifierFolder+"/cascade.xml")

#start video or camera
cap = cv.VideoCapture(vidname)
if(cap.isOpened() == False):
    print("Video failed to open")
    
count = 0
pause = False
#process frame by frame
while(cap.isOpened()):
    #get next frame if not paused
    if not pause:
        ret, frame = cap.read()
    if not ret:
        print("Error reading frame")
        break
    else:
        #object detect
        frame = find_objects(frame)
        cv.imshow('Object Detection', frame)
        #control keys
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


cap.release()
cv.destroyAllWindows()

