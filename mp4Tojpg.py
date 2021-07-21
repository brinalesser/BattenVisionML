import cv2 as cv
import os
import ntpath
import sys
import getopt

inputfile = './Videos for ML/vid1.mp4'
outputfolder = './Images/pos_img'

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

cap = cv.VideoCapture(inputfile)
ret, frame = cap.read()
count = 0

while ret:
	h, w, layers = frame.shape
	h = int(h / 2)
	w = int(w / 2)
	frame = cv.resize(frame, (w,h))
	cv.imshow("Frame", frame)
	if(cv.waitKey(25) & 0xFF == ord('q')):
		imagename = outputfolder + "/" + name + "_frame" + str(count) + ".jpg"
		print(imagename)
		cv.imwrite(imagename, frame)
	ret, frame = cap.read()
	count += 1

cap.release()
cv.destroyAllWindows()