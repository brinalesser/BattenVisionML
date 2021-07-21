import cv2 as cv
import numpy as np
from glob import glob
import os
import ntpath
import sys
import getopt
import matplotlib.pyplot as plt

#get all images
def get_all_images(pathToFiles):
	pathToFiles = pathToFiles + "/*.jpg"
	jpg_names = glob(pathToFiles)
	jpgs = []
	for file in jpg_names:
		im = cv.imread(file)
		jpgs.append(im)
		#cv.imshow("Original Image", im)
		#cv.waitKey(0)
	return jpgs, jpg_names

#plot edges
def find_edges(im):
	#convert to grey scale and blur
	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	im_gs_blur = cv.bilateralFilter(im_gs, 7, 75, 75)

	#cv.imshow("Greyscale Blurred Image", im_gs_blur)
	#cv.waitKey(0)

	#edge detection
	im_edges = cv.Canny(image=im_gs_blur, threshold1=100, threshold2=200)

	#cv.imshow("Edge Detection", im_edges)
	#cv.waitKey(0)

	#Hough Line Transform
	#cv.HoughLinesP(image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
	lines = cv.HoughLinesP(im_edges, 1, np.pi / 180, 10, None, 200, 30)

	im_line = np.copy(im) * 0  # blank
	if lines is not None:
		for line in lines:
    			for x1,y1,x2,y2 in line:
    				cv.line(im_line,(x1,y1),(x2,y2),(255,0,0),5)

		im_line = cv.addWeighted(im, 0.8, im_line, 1, 0)

	return im_line


if __name__=='__main__':
	
	#defaults
	inputfile = './Images/pos_img/img1.jpg'
	inputfolder = './Images/pos_img'
	outputfolder = './Images/pos_img'
	singleFile = False

	#get input from command line arguments
	args = sys.argv[1:]
	opts = "i:o:s:"
	longOpts = ["InputFolder", "OutputFolder", "SingleFile"]

	try:
		arguments, values = getopt.getopt(args, opts, longOpts)
		for arg, val in arguments:
			if arg in ("-s", "--SingleFile"):
				singleFile = True
			if arg in ("-i", "--InputFolder"):
				inputfolder = val
			if arg in ("-o", "--OutputFolder"):
				outputfolder = val
	except getopt.error as err:
		print(str(err))

	if(singleFile):
		#Do edge detection for a single file and display it
		im = cv.imread(inputfile)
		im_edges = find_edges(im)
		cv.imshow("Edge test", im_edges)

	else:
		#Do edge detection for every jpg file in input folder
		jpgs, jpg_names = get_all_images(inputfolder)

		edges = []
		for jpg in jpgs:
			edges.append(find_edges(jpg))

		#plot edges and save plots as pngs
		i = 0
		for img in edges:
			plt.imshow(img, cmap='gray')
			name = ntpath.basename(os.path.splitext(jpg_names[i])[0])
			filename = outputfolder + "/" + name +'.png'
			plt.savefig(filename)
			i = i + 1

	cv.waitKey(0)
	cv.destroyAllWindows()