'''
Program to save screenshots from video as jpgs

@author: Sabrina Lesser (Sabrina.Lesser@rfpco.com)
@date last modified: 7/27/21
'''
import cv2 as cv
import os
import ntpath
import sys
import getopt

#get filenames from command line or use defaults
inputfile = './Videos/test_vid.mp4'
outputfolder = './Images'

args = sys.argv[1:]
opts = "i:o:"
longOpts = ["InputFile", "OutputFolder"]

try:
    arguments, values = getopt.getopt(args, opts, longOpts)
    for arg, val in arguments:
        if arg in ("-i", "--InputFile"):
            inputfile = val
        elif arg in ("-o", "--OutputFolder"):
            outputfolder = val
except getopt.error as err:
    print(str(err))

name = os.path.splitext(inputfile)[0]
name = ntpath.basename(name)

#open video
cap = cv.VideoCapture(inputfile)
ret, frame = cap.read()
count = 0
#play video
while ret:
    h, w, layers = frame.shape
    h = int(h / 2)
    w = int(w / 2)
    frame = cv.resize(frame, (w,h))
    cv.imshow("Frame", frame)
    
    #control keys
    key = cv.waitKey(1)
    if(key == 27 or key == 113): #esc or q
        break
    elif(key == 115): #s
        #save screenshot
        imagename = outputfolder + "/" + name + "_frame" + str(count) + ".jpg"
        print(imagename)
        cv.imwrite(imagename, frame)
    elif(key == 112): #p
        pause = not pause
    elif(key != -1):
        print(key)
    ret, frame = cap.read()
    count += 1

cap.release()
cv.destroyAllWindows()